"""Dashboard window with dataset management, analysis, and visualization."""
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox, QScrollArea,
    QComboBox, QTabWidget, QSpinBox
)
from PyQt5.QtCore import Qt, QSize, QTimer, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import json
from api_client import APIClient
from datetime import datetime
import os


class ChartWidget(QWidget):
    """Widget for displaying charts using matplotlib."""
    
    def __init__(self):
        super().__init__()
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
    
    def plot_type_distribution(self, type_dist: dict):
        """Plot equipment type distribution as pie chart."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        types = list(type_dist.keys())
        counts = list(type_dist.values())
        colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4', '#ec4899']
        
        if len(types) > 0:
            ax.pie(counts, labels=types, autopct='%1.1f%%', colors=colors[:len(types)], startangle=90)
            ax.set_title('Equipment Type Distribution', fontsize=14, fontweight='bold')
        self.canvas.draw()
    
    def plot_average_metrics(self, data: dict):
        """Plot average metrics as bar chart."""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        
        metrics = ['Flowrate\n(L/min)', 'Pressure\n(bar)', 'Temperature\n(°C)']
        values = [
            data.get('average_flowrate', 0),
            data.get('average_pressure', 0),
            data.get('average_temperature', 0)
        ]
        colors = ['#3b82f6', '#10b981', '#f59e0b']
        
        bars = ax.bar(metrics, values, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
        ax.set_ylabel('Value', fontsize=12, fontweight='bold')
        ax.set_title('Average Equipment Metrics', fontsize=14, fontweight='bold')
        ax.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.2f}',
                   ha='center', va='bottom', fontweight='bold')
        
        self.canvas.draw()


class DashboardWindow(QMainWindow):
    """Main dashboard window."""
    
    def __init__(self, api_client: APIClient, username: str):
        super().__init__()
        self.api_client = api_client
        self.username = username
        self.datasets = []
        self.current_dataset = None
        self.selected_file = None
        
        self.setWindowTitle(f"Chemical Visualizer - Dashboard ({username})")
        self.setGeometry(50, 50, 1400, 900)
        
        self._create_ui()
        self._apply_styles()
        self._load_datasets()
    
    def _create_ui(self):
        """Create main UI."""
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)
        
        # Header with logo/title and user info
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        title = QLabel("Chemical Equipment Dashboard")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: black;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        welcome = QLabel(f"Welcome, {self.username}!")
        welcome.setStyleSheet("color: black; font-weight: 600; font-size: 13px;")
        header_layout.addWidget(welcome)
        
        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self._logout)
        logout_btn.setMaximumWidth(100)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """)
        header_layout.addWidget(logout_btn)
        
        main_layout.addLayout(header_layout)
        
        # Upload section card
        upload_card = QWidget()
        upload_card.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #e6eef6;
                border-radius: 8px;
                color:black;
            }
        """)
        upload_card.setMaximumHeight(120)
        upload_layout = QVBoxLayout()
        upload_layout.setContentsMargins(20, 16, 20, 16)
        upload_layout.setSpacing(12)
        
        upload_title = QLabel("Upload CSV File")
        upload_title.setStyleSheet("color: black; font-weight: 700; font-size: 14px;")
        upload_layout.addWidget(upload_title)
        
        help_text = QLabel("CSV format required: Equipment, Type, Flowrate, Pressure, Temperature")
        help_text.setStyleSheet("color: black; font-size: 11px; font-weight: 500; margin-bottom: 8px;")
        upload_layout.addWidget(help_text)
        
        file_layout = QHBoxLayout()
        file_layout.setSpacing(12)
        
        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("color: black; font-size: 12px; padding: 10px;")
        file_layout.addWidget(self.file_label, 1)
        
        self.file_input = QPushButton("Select File")
        self.file_input.clicked.connect(self._select_file)
        self.file_input.setMaximumWidth(120)
        self.file_input.setMinimumHeight(40)
        self.file_input.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: 2px solid #1e40af;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
            QPushButton:pressed {
                background-color: #1e40af;
            }
        """)
        file_layout.addWidget(self.file_input)
        
        upload_btn = QPushButton("Upload")
        upload_btn.clicked.connect(self._upload_file)
        upload_btn.setMaximumWidth(120)
        upload_btn.setMinimumHeight(40)
        upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                border: 2px solid #059669;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
            QPushButton:pressed {
                background-color: #047857;
            }
        """)
        file_layout.addWidget(upload_btn)
        
        upload_layout.addLayout(file_layout)
        upload_card.setLayout(upload_layout)
        main_layout.addWidget(upload_card)
        
        # Datasets section
        datasets_title = QLabel("My Datasets (Last 5)")
        datasets_title.setStyleSheet("color: #0b1220; font-weight: 700; font-size: 14px;")
        main_layout.addWidget(datasets_title)
        
        self.datasets_table = QTableWidget()
        self.datasets_table.setColumnCount(5)
        self.datasets_table.setHorizontalHeaderLabels(["Filename", "Uploaded", "Equipment", "Actions", ""])
        self.datasets_table.horizontalHeader().setStretchLastSection(False)
        self.datasets_table.setColumnWidth(0, 260)  # Filename
        self.datasets_table.setColumnWidth(1, 130)  # Uploaded
        self.datasets_table.setColumnWidth(2, 100)  # Equipment
        self.datasets_table.setColumnWidth(3, 280)  # Actions

        self.datasets_table.verticalHeader().setDefaultSectionSize(56)
        self.datasets_table.verticalHeader().setMinimumSectionSize(56)
        self.datasets_table.setIconSize(QSize(24, 24))
        self.datasets_table.setMaximumHeight(300)
        self.datasets_table.setAlternatingRowColors(True)
        self.datasets_table.setStyleSheet("""
            QTableWidget {
                alternate-background-color: #f8fafc;
                background-color: #ffffff;
            }
        """)
        self.datasets_table.itemSelectionChanged.connect(self._on_dataset_selected)
        main_layout.addWidget(self.datasets_table)
        
        # Analysis tabs
        self.tabs = QTabWidget()
        self.analysis_tab = QWidget()
        self.analysis_tab.setStyleSheet("background-color: #ffffff;")
        self.table_tab = self._create_table_tab()
        self.summary_tab = self._create_summary_tab()
        
        self.tabs.addTab(self.analysis_tab, "Dataset Analysis")
        self.tabs.addTab(self.table_tab, "Data Table")
        self.tabs.addTab(self.summary_tab, "Overall Summary")
        main_layout.addWidget(self.tabs)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
    
    def _create_table_tab(self) -> QWidget:
        """Create table view tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(2)
        self.data_table.setHorizontalHeaderLabels(["Metric", "Value"])
        
        layout.addWidget(self.data_table)
        widget.setLayout(layout)
        return widget
    
    def _create_summary_tab(self) -> QWidget:
        """Create overall summary tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Summary info
        self.summary_label = QLabel("Load a dataset to view summary")
        self.summary_label.setStyleSheet("color: black; font-size: 12px; padding: 16px;")
        layout.addWidget(self.summary_label)
        
        self.summary_table = QTableWidget()
        self.summary_table.setColumnCount(2)
        self.summary_table.setHorizontalHeaderLabels(["Metric", "Aggregated Value"])
        
        layout.addWidget(self.summary_table)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh Summary")
        refresh_btn.clicked.connect(self._load_summary)
        refresh_btn.setMaximumWidth(150)
        layout.addWidget(refresh_btn)
        
        widget.setLayout(layout)
        return widget
    
    def _select_file(self):
        """Open file dialog to select CSV."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv);;All Files (*)"
        )
        if file_path:
            self.selected_file = file_path
            filename = os.path.basename(file_path)
            self.file_label.setText(f"Selected: {filename}")
    
    def _upload_file(self):
        """Upload selected file."""
        if not self.selected_file:
            QMessageBox.warning(self, "Error", "Please select a file first")
            return
        
        if not os.path.exists(self.selected_file):
            QMessageBox.warning(self, "Error", f"File not found: {self.selected_file}")
            self.selected_file = None
            self.file_label.setText("No file selected")
            return
        
        success, message = self.api_client.upload_file(self.selected_file)
        if success:
            QMessageBox.information(self, "Success", message)
            self.file_label.setText("No file selected")
            self.selected_file = None
            self._load_datasets()
        else:
            QMessageBox.critical(self, "Upload Error", message)
    
    def _load_datasets(self):
        """Load datasets from API."""
        success, message, datasets = self.api_client.get_datasets()
        if success:
            self.datasets = datasets
            self._populate_datasets_table()
        else:
            QMessageBox.critical(self, "Error", f"Failed to load datasets: {message}")
    
    def _load_summary(self):
        """Load and display overall summary."""
        success, message, data = self.api_client.get_data_summary()
        if success:
            self._populate_summary_table(data)
        else:
            QMessageBox.critical(self, "Error", f"Failed to load summary: {message}")
    
    def _populate_summary_table(self, data: dict):
        """Populate summary table."""
        self.summary_table.setRowCount(0)
        
        summary_data = [
            ("Total Datasets", str(data.get('datasets_count', 0))),
            ("Total Equipment", str(data.get('total_equipment', 0))),
            ("Average Flowrate (L/min)", f"{data.get('average_flowrate', 0):.2f}"),
            ("Average Pressure (bar)", f"{data.get('average_pressure', 0):.2f}"),
            ("Average Temperature (°C)", f"{data.get('average_temperature', 0):.2f}"),
        ]
        
        for row, (metric, value) in enumerate(summary_data):
            self.summary_table.insertRow(row)
            self.summary_table.setItem(row, 0, QTableWidgetItem(metric))
            self.summary_table.setItem(row, 1, QTableWidgetItem(value))
        
        # Add type distribution
        if data.get('type_distribution'):
            row = self.summary_table.rowCount()
            self.summary_table.insertRow(row)
            header = QTableWidgetItem("Equipment Type Distribution")
            header_font = QFont("Arial", 11, QFont.Bold)
            header.setFont(header_font)
            self.summary_table.setItem(row, 0, header)
            row += 1
            
            for eq_type, count in data['type_distribution'].items():
                self.summary_table.insertRow(row)
                self.summary_table.setItem(row, 0, QTableWidgetItem(f"  {eq_type}"))
                self.summary_table.setItem(row, 1, QTableWidgetItem(str(count)))
                row += 1
        
        self.summary_table.resizeColumnsToContents()
        self.summary_label.setText("Summary of all your uploaded datasets")
    
    def _populate_datasets_table(self):
        """Populate datasets table."""
        self.datasets_table.setRowCount(len(self.datasets))
        
        for row, dataset in enumerate(self.datasets):
            # Filename
            self.datasets_table.setItem(row, 0, QTableWidgetItem(dataset['filename']))
            
            # Uploaded date
            try:
                uploaded = datetime.fromisoformat(dataset['uploaded_at']).strftime("%Y-%m-%d %H:%M")
            except:
                uploaded = dataset['uploaded_at'][:10]
            self.datasets_table.setItem(row, 1, QTableWidgetItem(uploaded))
            
            # Total equipment
            self.datasets_table.setItem(row, 2, QTableWidgetItem(str(dataset['total_equipment'])))
            
            # Action buttons
            btn_layout = QHBoxLayout()
            btn_layout.setContentsMargins(6, 4, 6, 4)
            btn_layout.setSpacing(10)
            btn_layout.setAlignment(Qt.AlignCenter)
            
            analyze_btn = QPushButton("Analyze")
            analyze_btn.clicked.connect(lambda checked, did=dataset['id']: self._analyze_dataset(did))
            analyze_btn.setMinimumWidth(80)
            analyze_btn.setFixedHeight(32)

            analyze_btn.setStyleSheet("""
            QPushButton {
              background-color: #3b82f6;
              color: white;
              border: none;
              border-radius: 6px;
              font-size: 13px;
              font-weight: 500;
              padding: 6px 10px;
            }
            QPushButton:hover {
              background-color: #2563eb;
            }
""")

            
            table_btn = QPushButton("Table")
            table_btn.clicked.connect(lambda checked, did=dataset['id']: self._view_table(did))
            table_btn.setMinimumWidth(70)
            table_btn.setFixedHeight(32)
            table_btn.setStyleSheet("""
            QPushButton {
              background-color: #8b5cf6;
              color: white;
              border-radius: 6px;
              font-size: 13px;
              font-weight: 500;
              padding: 6px 10px;
           }
            QPushButton:hover {
              background-color: #7c3aed;
            }
""")

            
            pdf_btn = QPushButton("PDF")
            pdf_btn.clicked.connect(lambda checked, did=dataset['id']: self._export_pdf(did))
            pdf_btn.setMinimumWidth(60)
            pdf_btn.setFixedHeight(32)
            pdf_btn.setStyleSheet("""
            QPushButton {
              background-color: #f59e0b;
              color: white;
              border-radius: 6px;
              font-size: 13px;
              font-weight: 500;
              padding: 6px 10px;
           }
            QPushButton:hover {
              background-color: #d97706;
           }
""")

            
            del_btn = QPushButton("Delete")
            del_btn.clicked.connect(lambda checked, did=dataset['id']: self._delete_dataset(did))
            del_btn.setMinimumWidth(70)
            del_btn.setFixedHeight(32)
            del_btn.setStyleSheet("""
            QPushButton {
              background-color: #ef4444;
              color: white;
              border-radius: 6px;
              font-size: 13px;
              font-weight: 500;
              padding: 6px 10px;
           }
            QPushButton:hover {
              background-color: #dc2626;
           }
""")

            btn_layout.addWidget(analyze_btn)
            btn_layout.addWidget(table_btn)
            btn_layout.addWidget(pdf_btn)
            btn_layout.addWidget(del_btn)
            
            btn_container = QWidget()
            btn_container.setLayout(btn_layout)
            
            self.datasets_table.setCellWidget(row, 3, btn_container)
    
    def _on_dataset_selected(self):
        """Handle dataset selection."""
        selected = self.datasets_table.selectedIndexes()
        if selected:
            row = selected[0].row()
            if row < len(self.datasets):
                self.current_dataset = self.datasets[row]
    
    def _analyze_dataset(self, dataset_id: int):
        """Analyze dataset and show charts."""
        success, message, data = self.api_client.get_dataset_detail(dataset_id)
        
        if not success:
            QMessageBox.critical(self, "Error", f"Failed to load dataset: {message}")
            return
        
        # Clear previous layout
        layout = self.analysis_tab.layout()
        if layout:
            while layout.count():
                w = layout.takeAt(0).widget()
                if w:
                    w.deleteLater()
        else:
            layout = QVBoxLayout()
            self.analysis_tab.setLayout(layout)
        
        # Statistics header
        stats_widget = QWidget()
        stats_widget.setStyleSheet("""
            QWidget {
                background-color: #f0f9ff;
                border-radius: 6px;
                padding: 12px;
            }
        """)
        stats_layout = QHBoxLayout()
        stats_layout.setContentsMargins(12, 12, 12, 12)
        stats_layout.setSpacing(30)
        
        stats_items = [
            ("Total Equipment", str(data['total_equipment']), "📊"),
            ("Avg Flowrate", f"{data['average_flowrate']:.2f} L/min", "💧"),
            ("Avg Pressure", f"{data['average_pressure']:.2f} bar", "⚙"),
            ("Avg Temp", f"{data['average_temperature']:.2f} °C", "🌡"),
        ]
        
        for label, value, icon in stats_items:
            stat_box = QVBoxLayout()
            icon_label = QLabel(icon)
            icon_label.setStyleSheet("font-size: 20px;")
            stat_box.addWidget(icon_label)
            label_widget = QLabel(label)
            label_widget.setStyleSheet("color: #64748b; font-size: 11px; font-weight: 600;")
            stat_box.addWidget(label_widget)
            value_widget = QLabel(value)
            value_widget.setStyleSheet("color: #1e40af; font-size: 13px; font-weight: bold;")
            stat_box.addWidget(value_widget)
            stats_layout.addLayout(stat_box)
        
        stats_layout.addStretch()
        stats_widget.setLayout(stats_layout)
        layout.addWidget(stats_widget)
        
        # Charts
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(12)
        
        if data.get('type_distribution'):
            chart1 = ChartWidget()
            chart1.plot_type_distribution(data['type_distribution'])
            charts_layout.addWidget(chart1, 1)
        
        chart2 = ChartWidget()
        chart2.plot_average_metrics(data)
        charts_layout.addWidget(chart2, 1)
        
        layout.addLayout(charts_layout)
        
        self.tabs.setCurrentIndex(0)
    
    def _view_table(self, dataset_id: int):
        """View dataset as table."""
        success, message, data = self.api_client.get_dataset_detail(dataset_id)
        
        if not success:
            QMessageBox.critical(self, "Error", f"Failed to load dataset: {message}")
            return
        
        # Clear previous rows
        self.data_table.setRowCount(0)
        
        # Add statistics rows
        row = 0
        stats = [
            ("Total Equipment", str(data['total_equipment'])),
            ("Average Flowrate (L/min)", f"{data['average_flowrate']:.2f}"),
            ("Average Pressure (bar)", f"{data['average_pressure']:.2f}"),
            ("Average Temperature (°C)", f"{data['average_temperature']:.2f}"),
        ]
        
        for metric, value in stats:
            self.data_table.insertRow(row)
            self.data_table.setItem(row, 0, QTableWidgetItem(metric))
            self.data_table.setItem(row, 1, QTableWidgetItem(value))
            row += 1
        
        # Add type distribution
        if data.get('type_distribution'):
            self.data_table.insertRow(row)
            header = QTableWidgetItem("Equipment Type Distribution")
            header.setFont(QFont("Arial", 11, QFont.Bold))
            self.data_table.setItem(row, 0, header)
            row += 1
            
            for eq_type, count in data['type_distribution'].items():
                self.data_table.insertRow(row)
                self.data_table.setItem(row, 0, QTableWidgetItem(f"  {str(eq_type)}"))
                self.data_table.setItem(row, 1, QTableWidgetItem(str(count)))
                row += 1
        
        self.data_table.resizeColumnsToContents()
        self.tabs.setCurrentIndex(1)
    
    def _export_pdf(self, dataset_id: int):
        """Export analysis as PDF."""
        try:
            success, message, pdf_content = self.api_client.export_pdf(dataset_id)
            
            if not success:
                QMessageBox.critical(self, "Error", f"Failed to export PDF: {message}")
                return
            
            file_path, _ = QFileDialog.getSaveFileName(
                self, "Save PDF", f"dataset_{dataset_id}_report.pdf", "PDF Files (*.pdf)"
            )
            
            if not file_path:
                return
            
            with open(file_path, 'wb') as f:
                f.write(pdf_content)
            
            QMessageBox.information(self, "Success", f"PDF exported to:\n{file_path}")
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export PDF: {str(e)}")
    
    def _delete_dataset(self, dataset_id: int):
        """Delete a dataset."""
        reply = QMessageBox.question(
            self, "Confirm Delete",
            "Are you sure you want to delete this dataset?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            success, message = self.api_client.delete_dataset(dataset_id)
            if success:
                QMessageBox.information(self, "Success", message)
                self._load_datasets()
            else:
                QMessageBox.critical(self, "Error", message)
    
    def _logout(self):
        """Logout and close dashboard."""
        self.api_client.token = None
        self.api_client.username = None
        self.close()
    
    def _apply_styles(self):
        """Apply light theme styles matching web frontend."""
        self.setStyleSheet("""
            QMainWindow {
                background: linear-gradient(180deg, #f8fafc 0%, #eef2f7 50%, #ffffff 100%);
            }
            QLabel {
                color: #0b1220;
                font-weight: 500;
            }
            QLineEdit {
                border: 1px solid #e6eef6;
                border-radius: 8px;
                padding: 10px 14px;
                background-color: #ffffff;
                color: black;
                font-weight: 500;
                selection-background-color: #dbeafe;
            }
            QLineEdit:focus {
                border: 2px solid #3b82f6;
                padding: 9px 13px;
                background-color: #ffffff;
            }
            QPushButton {
                background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 20px;
            }
            QPushButton:hover {
                background: linear-gradient(135deg, #1D4ED8 0%, #1E3A8A 100%);
            }
            QPushButton:pressed {
                background: linear-gradient(135deg, #1E40AF 0%, #1E3A8A 100%);
            }
            QTableWidget {
                border: 1px solid #e6eef6;
                gridline-color: black;
                background-color: #ffffff;
                border-radius: 8px;
            }
            QHeaderView::section {
                background: linear-gradient(135deg, #2563EB 0%, #1E40AF 100%);
                color: black;
                padding: 8px;
                border: none;
                font-weight: bold;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f1f5f9;
            }
            QTableWidget::item:selected {
                background-color: #dbeafe;
                color: black;
            }
            QTabBar::tab {
                background-color: #f1f5f9;
                color: black;
                padding: 8px 20px;
                border: none;
                border-bottom: 2px solid transparent;
                font-weight: 600;
                font-size: 12px;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                border-bottom: 2px solid #2563eb;
                color: #2563eb;
            }
            QTabWidget::pane {
                border: 1px solid #e6eef6;
                background-color: #ffffff;
            }
            QmessageBox {
                background-color: #ffffff;
                color: black;
            }
        """)
