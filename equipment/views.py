from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from rest_framework.generics import GenericAPIView, ListAPIView
from .models import Dataset
from .serializers import CSVUploadSerializer, DatasetSerializer
import io
import ast
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import json


class DatasetList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get user's last 5 datasets with summary."""
        datasets = Dataset.objects.filter(user=request.user).order_by('-uploaded_at')[:5]

        data = []
        for d in datasets:
            data.append({
                "id": d.id,
                "filename": d.filename,
                "uploaded_at": d.uploaded_at,
                "total_equipment": d.total_equipment,
                "average_flowrate": d.average_flowrate,
                "average_pressure": d.average_pressure,
                "average_temperature": d.average_temperature,
                "type_distribution": d.type_distribution
            })

        return Response(data)


class DataSummary(APIView):
    """Return aggregated data summary for all user datasets."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get aggregated summary of all datasets."""
        datasets = Dataset.objects.filter(user=request.user)
        
        if not datasets.exists():
            return Response({
                "total_count": 0,
                "total_equipment": 0,
                "average_flowrate": 0,
                "average_pressure": 0,
                "average_temperature": 0,
                "type_distribution": {},
                "datasets_count": 0
            })
        
        total_equipment = sum(d.total_equipment for d in datasets)
        avg_flowrate = sum(d.average_flowrate * d.total_equipment for d in datasets) / total_equipment if total_equipment > 0 else 0
        avg_pressure = sum(d.average_pressure * d.total_equipment for d in datasets) / total_equipment if total_equipment > 0 else 0
        avg_temperature = sum(d.average_temperature * d.total_equipment for d in datasets) / total_equipment if total_equipment > 0 else 0
        
        # Aggregate type distribution
        type_dist = {}
        for dataset in datasets:
            for eq_type, count in dataset.type_distribution.items():
                type_dist[eq_type] = type_dist.get(eq_type, 0) + count
        
        return Response({
            "total_count": datasets.count(),
            "total_equipment": total_equipment,
            "average_flowrate": round(avg_flowrate, 2),
            "average_pressure": round(avg_pressure, 2),
            "average_temperature": round(avg_temperature, 2),
            "type_distribution": type_dist,
            "datasets_count": datasets.count()
        })


class UploadCSV(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CSVUploadSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = serializer.validated_data["file"]
        try:
            df = pd.read_csv(file)
            
            # Validate required columns
            required_columns = {"Type", "Flowrate", "Pressure", "Temperature"}
            if not required_columns.issubset(df.columns):
                return Response(
                    {"error": f"CSV must contain columns: {', '.join(required_columns)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            summary = {
                "total_equipment": len(df),
                "average_flowrate": round(df["Flowrate"].mean(), 2),
                "average_pressure": round(df["Pressure"].mean(), 2),
                "average_temperature": round(df["Temperature"].mean(), 2),
                "type_distribution": df["Type"].value_counts().to_dict(),
            }

            Dataset.objects.create(
                user=request.user,
                filename=file.name,
                total_equipment=summary["total_equipment"],
                average_flowrate=summary["average_flowrate"],
                average_pressure=summary["average_pressure"],
                average_temperature=summary["average_temperature"],
                type_distribution=summary["type_distribution"],
            )

            # Keep only last 5 uploads per user
            datasets = Dataset.objects.filter(user=request.user).order_by("-uploaded_at")
            if datasets.count() > 5:
                for old in datasets[5:]:
                    old.delete()

            return Response(summary, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": f"Failed to process CSV: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )


class ExportPDF(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, dataset_id):
        try:
            dataset = Dataset.objects.get(id=dataset_id, user=request.user)
        except Dataset.DoesNotExist:
            return Response(
                {"error": "Dataset not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Create PDF
        buffer = io.BytesIO()
        pdf = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        # Title
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=30,
        )
        elements.append(Paragraph(f"Dataset Analysis Report: {dataset.filename}", title_style))
        elements.append(Spacer(1, 0.3*inch))

        # Summary table
        summary_data = [
            ['Metric', 'Value'],
            ['Total Equipment', str(dataset.total_equipment)],
            ['Average Flowrate', f"{dataset.average_flowrate} L/min"],
            ['Average Pressure', f"{dataset.average_pressure} bar"],
            ['Average Temperature', f"{dataset.average_temperature} °C"],
            ['Uploaded Date', dataset.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')],
        ]

        summary_table = Table(summary_data, colWidths=[2.5*inch, 2.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(summary_table)
        elements.append(Spacer(1, 0.3*inch))

        # Type distribution
        elements.append(Paragraph("Equipment Type Distribution", styles['Heading2']))
        elements.append(Spacer(1, 0.2*inch))

        type_dist = dataset.type_distribution
        type_data = [['Type', 'Count']]
        for eq_type, count in type_dist.items():
            type_data.append([str(eq_type), str(count)])

        type_table = Table(type_data, colWidths=[2.5*inch, 2.5*inch])
        type_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(type_table)

        # Build PDF
        pdf.build(elements)
        buffer.seek(0)

        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{dataset.filename}.pdf"'
        return response


class DatasetDetail(APIView):
    """Get or delete a specific dataset."""
    permission_classes = [IsAuthenticated]

    def get(self, request, dataset_id):
        """Get dataset details."""
        try:
            dataset = Dataset.objects.get(id=dataset_id, user=request.user)
            return Response({
                "id": dataset.id,
                "filename": dataset.filename,
                "uploaded_at": dataset.uploaded_at,
                "total_equipment": dataset.total_equipment,
                "average_flowrate": dataset.average_flowrate,
                "average_pressure": dataset.average_pressure,
                "average_temperature": dataset.average_temperature,
                "type_distribution": dataset.type_distribution
            })
        except Dataset.DoesNotExist:
            return Response(
                {"error": "Dataset not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, dataset_id):
        """Delete a dataset."""
        try:
            dataset = Dataset.objects.get(id=dataset_id, user=request.user)
            dataset.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Dataset.DoesNotExist:
            return Response(
                {"error": "Dataset not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class DatasetListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DatasetSerializer

    def get_queryset(self):
        return Dataset.objects.filter(user=self.request.user).order_by('-uploaded_at')[:5]