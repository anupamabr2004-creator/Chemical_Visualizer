import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title } from 'chart.js';
import { Doughnut, Bar } from 'react-chartjs-2';
import jsPDF from 'jspdf';
import 'jspdf-autotable';
import html2canvas from 'html2canvas';
import './Dashboard.css';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, Title);

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

function Dashboard({ authToken, username, onLogout, message, messageType, showMessage }) {
  const [datasets, setDatasets] = useState([]);
  const [selectedDataset, setSelectedDataset] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [loading, setLoading] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  const [showTable, setShowTable] = useState(false);
  const [tableData, setTableData] = useState(null);
  const chartRef = useRef(null);
  const exportRef = useRef(null);

  useEffect(() => {
    loadDatasets();
  }, []);

  const loadDatasets = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE}/equipment/datasets/`, {
        headers: { Authorization: `Bearer ${authToken}` }
      });
      setDatasets(response.data);
    } catch (error) {
      showMessage('Error loading datasets: ' + error.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    const fileInput = e.target.querySelector('input[type="file"]');
    const file = fileInput.files[0];

    if (!file) {
      showMessage('Please select a file', 'error');
      return;
    }

    if (!file.name.endsWith('.csv')) {
      showMessage('Please upload a CSV file', 'error');
      return;
    }

    setUploading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      await axios.post(`${API_BASE}/equipment/upload/`, formData, {
        headers: { Authorization: `Bearer ${authToken}` }
      });
      showMessage('File uploaded successfully!', 'success');
      fileInput.value = '';
      loadDatasets();
    } catch (error) {
      showMessage(error.response?.data?.detail || 'Upload failed: ' + error.message, 'error');
    } finally {
      setUploading(false);
    }
  };

  const handleAnalyze = async (datasetId) => {
    try {
      const response = await axios.get(`${API_BASE}/equipment/datasets/`, {
        headers: { Authorization: `Bearer ${authToken}` }
      });
      const dataset = response.data.find(d => d.id === datasetId);
      setSelectedDataset(datasetId);
      setAnalysis(dataset);
      setShowTable(false);
    } catch (error) {
      showMessage('Error loading analysis: ' + error.message, 'error');
    }
  };

  const handleViewTable = async (datasetId) => {
    try {
      const response = await axios.get(`${API_BASE}/equipment/datasets/`, {
        headers: { Authorization: `Bearer ${authToken}` }
      });
      const dataset = response.data.find(d => d.id === datasetId);
      setTableData(dataset);
      setShowTable(true);
      setSelectedDataset(datasetId);
      setAnalysis(null);
    } catch (error) {
      showMessage('Error loading table data: ' + error.message, 'error');
    }
  };

  const handleExportPDF = async (datasetId) => {
    try {
      showMessage('Generating PDF...', 'info');
      
      // Create PDF document
      const pdf = new jsPDF('p', 'mm', 'a4');
      const pageWidth = pdf.internal.pageSize.getWidth();
      const pageHeight = pdf.internal.pageSize.getHeight();
      let yPosition = 10;

      // Add title
      pdf.setFontSize(16);
      pdf.text('Chemical Visualizer Report', pageWidth / 2, yPosition, { align: 'center' });
      yPosition += 10;

      // Add dataset info
      pdf.setFontSize(11);
      const dataset = datasets.find(d => d.id === datasetId);
      pdf.text(`Dataset: ${dataset.filename}`, 10, yPosition);
      yPosition += 7;
      pdf.text(`Date: ${new Date(dataset.uploaded_at).toLocaleDateString()}`, 10, yPosition);
      yPosition += 7;
      pdf.text(`User: ${username}`, 10, yPosition);
      yPosition += 12;

      // Add statistics section
      pdf.setFontSize(12);
      pdf.text('Summary Statistics', 10, yPosition);
      yPosition += 8;

      pdf.setFontSize(10);
      const stats = [
        ['Metric', 'Value'],
        ['Total Equipment', dataset.total_equipment.toString()],
        ['Avg Flowrate (L/min)', dataset.average_flowrate.toString()],
        ['Avg Pressure (bar)', dataset.average_pressure.toString()],
        ['Avg Temperature (°C)', dataset.average_temperature.toString()],
      ];

      pdf.autoTable({
        startY: yPosition,
        head: [stats[0]],
        body: stats.slice(1),
        theme: 'grid',
        margin: { left: 10, right: 10 },
        styles: { fontSize: 9 },
        headStyles: { fillColor: [66, 139, 202], textColor: 255 },
      });

      yPosition = pdf.lastAutoTable.finalY + 12;

      // Add type distribution
      if (dataset.type_distribution && Object.keys(dataset.type_distribution).length > 0) {
        pdf.setFontSize(12);
        pdf.text('Equipment Type Distribution', 10, yPosition);
        yPosition += 8;

        const typeData = Object.entries(dataset.type_distribution).map(([type, count]) => [type, count.toString()]);
        pdf.autoTable({
          startY: yPosition,
          head: [['Type', 'Count']],
          body: typeData,
          theme: 'grid',
          margin: { left: 10, right: 10 },
          styles: { fontSize: 9 },
          headStyles: { fillColor: [66, 139, 202], textColor: 255 },
        });

        yPosition = pdf.lastAutoTable.finalY + 12;
      }

      // Add chart sections if analysis is available
      if (analysis && analysis.id === datasetId) {
        // Capture the charts container (both charts) as a single image
        if (exportRef.current) {
          try {
            // increase scale for better resolution
            const canvas = await html2canvas(exportRef.current, { backgroundColor: '#fff', scale: 2 });
            const imgData = canvas.toDataURL('image/png');
            const imgWidth = pageWidth - 20;
            const imgHeight = (canvas.height * imgWidth) / canvas.width;

            if (yPosition + imgHeight > pageHeight - 10) {
              pdf.addPage();
              yPosition = 10;
            }

            pdf.text('Charts', 10, yPosition);
            yPosition += 8;
            pdf.addImage(imgData, 'PNG', 10, yPosition, imgWidth, imgHeight);
            yPosition += imgHeight + 12;
          } catch (chartError) {
            console.error('Chart export error:', chartError);
          }
        }
      }

      // Add footer
      pdf.setFontSize(8);
      pdf.text('Generated by Chemical Visualizer', pageWidth / 2, pageHeight - 5, { align: 'center' });

      // Save PDF
      pdf.save(`dataset-${datasetId}-report.pdf`);
      showMessage('PDF exported successfully!', 'success');
    } catch (error) {
      showMessage('Error exporting PDF: ' + error.message, 'error');
    }
  };

  const getChartData = () => {
    if (!analysis || !analysis.type_distribution) return null;

    const types = Object.keys(analysis.type_distribution);
    const counts = Object.values(analysis.type_distribution);
    const colors = [
      '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
      '#FF9F40', '#FF6384', '#C9CBCF', '#FF5A5F', '#5A9FD4'
    ];

    return {
      labels: types,
      datasets: [{
        label: 'Count',
        data: counts,
        backgroundColor: colors.slice(0, types.length),
        borderColor: '#fff',
        borderWidth: 2,
      }],
    };
  };

  const getBarChartData = () => {
    if (!analysis) return null;

    return {
      labels: ['Flowrate', 'Pressure', 'Temperature'],
      datasets: [{
        label: 'Average Values',
        data: [
          analysis.average_flowrate,
          analysis.average_pressure,
          analysis.average_temperature,
        ],
        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
        borderColor: ['#FF6384', '#36A2EB', '#FFCE56'],
        borderWidth: 1,
      }],
    };
  };

  return (
    <div className="dashboard-container">
      <div className="card">
        <div className="dashboard-header">
          <h2> Dashboard</h2>
          <div className="header-right">
            <span className="username">Welcome, {username}!</span>
            <button className="logout-btn" onClick={onLogout}>
              Logout
            </button>
          </div>
        </div>

        {message && (
          <div className={`message ${messageType}`}>
            {message}
          </div>
        )}

        <div className="section">
          <h3> Upload CSV</h3>
          <form onSubmit={handleUpload} className="upload-form">
            <input type="file" accept=".csv" required disabled={uploading} />
            <button type="submit" disabled={uploading}>
              {uploading ? 'Uploading...' : 'Upload'}
            </button>
          </form>
          <p className="help-text">Upload a CSV file with columns: Equipment, Type, Flowrate, Pressure, Temperature</p>
        </div>

        <div className="section">
          <div className="section-header">
            <h3>My Datasets</h3>
            <div className="history-dropdown">
              <button className="history-btn" onClick={() => setShowHistory(!showHistory)}>
                 History ({datasets.length})
              </button>
              {showHistory && (
                <div className="history-menu">
                  <p className="history-title">Last {Math.min(5, datasets.length)} Uploads</p>
                  {datasets.length === 0 ? (
                    <p className="empty-text">No datasets yet</p>
                  ) : (
                    datasets.map((dataset, idx) => (
                      <div key={dataset.id} className="history-item">
                        <span className="history-num">{idx + 1}.</span>
                        <span className="history-name">{dataset.filename}</span>
                        <span className="history-date">{new Date(dataset.uploaded_at).toLocaleDateString()}</span>
                      </div>
                    ))
                  )}
                </div>
              )}
            </div>
          </div>

          {loading ? (
            <p className="loading">Loading datasets...</p>
          ) : datasets.length === 0 ? (
            <p className="empty-text">No datasets uploaded yet</p>
          ) : (
            <div className="datasets-list">
              {datasets.map(dataset => (
                <div key={dataset.id} className="dataset-item">
                  <div className="dataset-info">
                    <h4>{dataset.filename}</h4>
                    <p> Uploaded: {new Date(dataset.uploaded_at).toLocaleDateString()}</p>
                    <p>Equipment: {dataset.total_equipment} items</p>
                  </div>
                  <div className="dataset-actions">
                    <button
                      className="btn-small btn-analyze"
                      onClick={() => handleAnalyze(dataset.id)}
                      title="View analysis and charts"
                    >
                       Analyze
                    </button>
                    <button
                      className="btn-small btn-table"
                      onClick={() => handleViewTable(dataset.id)}
                      title="View data table"
                    >
                      Table
                    </button>
                    <button
                      className="btn-small btn-export"
                      onClick={() => handleExportPDF(dataset.id)}
                      title="Export as PDF with charts"
                    >
                       PDF
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {showTable && tableData && (
          <div className="section table-section">
            <h3>Data Table: {tableData.filename}</h3>
            <button className="close-btn" onClick={() => setShowTable(false)}>✕ Close</button>
            
            <div className="table-wrapper">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Metric</th>
                    <th>Value</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>Total Equipment</td>
                    <td>{tableData.total_equipment}</td>
                  </tr>
                  <tr>
                    <td>Average Flowrate (L/min)</td>
                    <td>{tableData.average_flowrate}</td>
                  </tr>
                  <tr>
                    <td>Average Pressure (bar)</td>
                    <td>{tableData.average_pressure}</td>
                  </tr>
                  <tr>
                    <td>Average Temperature (°C)</td>
                    <td>{tableData.average_temperature}</td>
                  </tr>
                </tbody>
              </table>

              {tableData.type_distribution && Object.keys(tableData.type_distribution).length > 0 && (
                <>
                  <h4>Equipment Type Breakdown</h4>
                  <table className="data-table">
                    <thead>
                      <tr>
                        <th>Equipment Type</th>
                        <th>Count</th>
                      </tr>
                    </thead>
                    <tbody>
                      {Object.entries(tableData.type_distribution).map(([type, count]) => (
                        <tr key={type}>
                          <td>{type}</td>
                          <td>{count}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </>
              )}
            </div>
          </div>
        )}

        {analysis && (
          <div className="section analysis-section">
            <h3>Analysis Results: {analysis.filename}</h3>
            
            <div className="stat-grid">
              <div className="stat-card">
                <div className="stat-label">📦 Total Equipment</div>
                <div className="stat-value">{analysis.total_equipment}</div>
              </div>
              <div className="stat-card">
                <div className="stat-label">💧 Avg Flowrate</div>
                <div className="stat-value">{analysis.average_flowrate} <span className="unit">L/min</span></div>
              </div>
              <div className="stat-card">
                <div className="stat-label">🔧 Avg Pressure</div>
                <div className="stat-value">{analysis.average_pressure} <span className="unit">bar</span></div>
              </div>
              <div className="stat-card">
                <div className="stat-label">🌡️ Avg Temperature</div>
                <div className="stat-value">{analysis.average_temperature} <span className="unit">°C</span></div>
              </div>
            </div>

            <div className="charts-grid" ref={exportRef}>
              {Object.entries(analysis.type_distribution || {}).length > 0 && (
                <div className="chart-container">
                  <h4>Equipment Distribution</h4>
                  <div className="chart-wrapper" ref={chartRef}>
                    <Doughnut data={getChartData()} options={{
                      responsive: true,
                      plugins: {
                        legend: { position: 'bottom' },
                      },
                    }} />
                  </div>
                </div>
              )}

              <div className="chart-container">
                <h4>Average Parameters</h4>
                <div className="chart-wrapper">
                  <Bar data={getBarChartData()} options={{
                    responsive: true,
                    plugins: {
                      legend: { position: 'top' },
                      title: { display: false },
                    },
                    scales: {
                      y: {
                        beginAtZero: true,
                      },
                    },
                  }} />
                </div>
              </div>
            </div>

            <div className="type-distribution">
              <h4>Equipment Type Details</h4>
              {Object.entries(analysis.type_distribution || {}).length === 0 ? (
                <p className="empty-text">No equipment data</p>
              ) : (
                <div className="type-items-grid">
                  {Object.entries(analysis.type_distribution || {}).map(([type, count]) => (
                    <div key={type} className="type-item">
                      <span className="type-name">{type}</span>
                      <span className="type-count">{count}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="action-buttons">
              <button
                className="btn-export-large"
                onClick={() => handleExportPDF(selectedDataset)}
              >
                Export as PDF (with Charts)
              </button>
              <button
                className="btn-close"
                onClick={() => {
                  setAnalysis(null);
                  setSelectedDataset(null);
                }}
              >
                ✕ Close Analysis
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
