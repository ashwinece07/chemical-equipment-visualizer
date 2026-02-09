from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                             QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem,
                             QTabWidget, QTextEdit, QProgressBar, QListWidget, QInputDialog,
                             QSplitter, QScrollArea, QGridLayout, QLineEdit)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

class UploadThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)

    def __init__(self, api_client, file_path):
        super().__init__()
        self.api_client = api_client
        self.file_path = file_path

    def run(self):
        try:
            self.progress.emit(30)
            result = self.api_client.upload_file(self.file_path)
            self.progress.emit(100)
            if result.get('status') == 'success':
                self.finished.emit(result)
            else:
                self.error.emit(result.get('error', 'Upload failed'))
        except Exception as e:
            self.error.emit(str(e))

class DashboardView(QWidget):
    def __init__(self, api_client, theme_manager):
        super().__init__()
        self.api_client = api_client
        self.theme_manager = theme_manager
        self.current_analysis = None
        self.current_file_id = None
        self.init_ui()
        self.load_history()

    def init_ui(self):
        main_layout = QHBoxLayout()
        
        # Sidebar
        sidebar = QWidget()
        sidebar.setMaximumWidth(250)
        sidebar_layout = QVBoxLayout()
        
        user_label = QLabel(f"{self.api_client.user_data.get('username', 'User')}")
        user_label.setFont(QFont("Arial", 12, QFont.Bold))
        sidebar_layout.addWidget(user_label)
        
        self.upload_btn = QPushButton("Upload CSV (Ctrl+U)")
        self.upload_btn.clicked.connect(self.upload_file)
        sidebar_layout.addWidget(self.upload_btn)
        
        self.theme_btn = QPushButton("Toggle Theme")
        self.theme_btn.clicked.connect(self.toggle_theme)
        sidebar_layout.addWidget(self.theme_btn)
        
        sidebar_layout.addWidget(QLabel("Recent Uploads:"))
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.load_analysis_from_history)
        sidebar_layout.addWidget(self.history_list)
        
        # Delete button
        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.clicked.connect(self.delete_file)
        sidebar_layout.addWidget(self.delete_btn)
        
        self.compare_btn = QPushButton("Compare Selected")
        self.compare_btn.clicked.connect(self.compare_datasets)
        self.compare_btn.setEnabled(False)
        sidebar_layout.addWidget(self.compare_btn)
        
        self.profile_btn = QPushButton("Profile")
        self.profile_btn.clicked.connect(self.show_profile)
        sidebar_layout.addWidget(self.profile_btn)
        
        self.logout_btn = QPushButton("Logout")
        self.logout_btn.clicked.connect(self.logout)
        sidebar_layout.addWidget(self.logout_btn)
        
        sidebar_layout.addStretch()
        sidebar.setLayout(sidebar_layout)
        
        # Main content
        content = QWidget()
        content_layout = QVBoxLayout()
        
        # Header
        header = QLabel("Chemical Equipment Analysis Dashboard")
        header.setFont(QFont("Arial", 18, QFont.Bold))
        content_layout.addWidget(header)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        content_layout.addWidget(self.progress_bar)
        
        # Tabs
        self.tabs = QTabWidget()
        
        # Overview Tab
        overview_tab = QWidget()
        overview_layout = QVBoxLayout()
        
        stats_grid = QGridLayout()
        self.stat_total = QLabel("Total: 0")
        self.stat_health = QLabel("Health: 0%")
        self.stat_outliers = QLabel("Outliers: 0")
        self.stat_avg_pressure = QLabel("Avg Pressure: 0")
        self.stat_avg_temp = QLabel("Avg Temp: 0")
        self.stat_avg_flow = QLabel("Avg Flow: 0")
        
        for i, stat in enumerate([self.stat_total, self.stat_health, self.stat_outliers,
                                  self.stat_avg_pressure, self.stat_avg_temp, self.stat_avg_flow]):
            stat.setFont(QFont("Arial", 12, QFont.Bold))
            stat.setStyleSheet("padding: 15px; border: 2px solid #3b82f6; border-radius: 8px;")
            stats_grid.addWidget(stat, i // 3, i % 3)
        
        overview_layout.addLayout(stats_grid)
        
        self.ai_insights = QTextEdit()
        self.ai_insights.setReadOnly(True)
        self.ai_insights.setPlaceholderText("AI insights will appear here after uploading data...")
        overview_layout.addWidget(QLabel("AI-Powered Insights:"))
        overview_layout.addWidget(self.ai_insights)
        
        overview_tab.setLayout(overview_layout)
        self.tabs.addTab(overview_tab, "Overview")
        
        # Data Tab
        data_tab = QWidget()
        data_layout = QVBoxLayout()
        self.data_table = QTableWidget()
        data_layout.addWidget(self.data_table)
        data_tab.setLayout(data_layout)
        self.tabs.addTab(data_tab, "Data Table")
        
        # Charts Tab
        charts_tab = QWidget()
        charts_layout = QVBoxLayout()
        
        self.chart_canvas = FigureCanvas(Figure(figsize=(10, 8)))
        charts_layout.addWidget(self.chart_canvas)
        
        chart_buttons = QHBoxLayout()
        self.btn_bar = QPushButton("Bar Chart")
        self.btn_scatter = QPushButton("Scatter Plot")
        self.btn_pie = QPushButton("Pie Chart")
        self.btn_3d = QPushButton("3D Plot")
        self.btn_heatmap = QPushButton("Heatmap")
        self.btn_box = QPushButton("Box Plot")
        self.btn_histogram = QPushButton("Histogram")
        
        self.btn_bar.clicked.connect(lambda: self.plot_chart('bar'))
        self.btn_scatter.clicked.connect(lambda: self.plot_chart('scatter'))
        self.btn_pie.clicked.connect(lambda: self.plot_chart('pie'))
        self.btn_3d.clicked.connect(lambda: self.plot_chart('3d'))
        self.btn_heatmap.clicked.connect(lambda: self.plot_chart('heatmap'))
        self.btn_box.clicked.connect(lambda: self.plot_chart('box'))
        self.btn_histogram.clicked.connect(lambda: self.plot_chart('histogram'))
        
        for btn in [self.btn_bar, self.btn_scatter, self.btn_pie, self.btn_3d, 
                    self.btn_heatmap, self.btn_box, self.btn_histogram]:
            chart_buttons.addWidget(btn)
        
        charts_layout.addLayout(chart_buttons)
        charts_tab.setLayout(charts_layout)
        self.tabs.addTab(charts_tab, "Visualizations")
        
        # Export Tab
        export_tab = QWidget()
        export_layout = QVBoxLayout()
        export_layout.setAlignment(Qt.AlignCenter)
        
        export_label = QLabel("Export Analysis Reports")
        export_label.setFont(QFont("Arial", 16, QFont.Bold))
        export_layout.addWidget(export_label)
        
        self.export_pdf_btn = QPushButton("Export PDF Report")
        self.export_pdf_btn.setMinimumHeight(50)
        self.export_pdf_btn.clicked.connect(self.export_pdf)
        export_layout.addWidget(self.export_pdf_btn)
        
        self.export_excel_btn = QPushButton("Export Excel Report")
        self.export_excel_btn.setMinimumHeight(50)
        self.export_excel_btn.clicked.connect(self.export_excel)
        export_layout.addWidget(self.export_excel_btn)
        
        export_layout.addStretch()
        export_tab.setLayout(export_layout)
        self.tabs.addTab(export_tab, "Export")
        
        content_layout.addWidget(self.tabs)
        content.setLayout(content_layout)
        
        # Add to main layout
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(sidebar)
        splitter.addWidget(content)
        splitter.setStretchFactor(1, 1)
        
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "", "CSV Files (*.csv)")
        if file_path:
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            
            self.upload_thread = UploadThread(self.api_client, file_path)
            self.upload_thread.progress.connect(self.progress_bar.setValue)
            self.upload_thread.finished.connect(self.handle_upload_success)
            self.upload_thread.error.connect(self.handle_upload_error)
            self.upload_thread.start()

    def handle_upload_success(self, result):
        self.progress_bar.setVisible(False)
        self.current_analysis = result.get('data')
        self.current_file_id = result.get('file_id')
        self.display_analysis(self.current_analysis)
        self.load_history()
        QMessageBox.information(self, "Success", "File uploaded and analyzed successfully!")

    def handle_upload_error(self, error):
        self.progress_bar.setVisible(False)
        QMessageBox.critical(self, "Upload Error", error)

    def display_analysis(self, data):
        if not data:
            return
        
        # Update stats
        self.stat_total.setText(f"Total: {data.get('total_count', 0)}")
        self.stat_health.setText(f"Health: {data.get('health_score_avg', 0):.1f}%")
        self.stat_outliers.setText(f"Outliers: {data.get('outliers_count', 0)}")
        
        avgs = data.get('averages', {})
        self.stat_avg_pressure.setText(f"Avg Pressure: {avgs.get('Pressure', 0):.2f}")
        self.stat_avg_temp.setText(f"Avg Temp: {avgs.get('Temperature', 0):.2f}")
        self.stat_avg_flow.setText(f"Avg Flow: {avgs.get('Flowrate', 0):.2f}")
        
        # AI insights
        self.ai_insights.setPlainText(data.get('ai_insights', 'No insights available'))
        
        # Data table
        raw_data = data.get('raw_data', [])
        if raw_data:
            self.data_table.setRowCount(len(raw_data))
            self.data_table.setColumnCount(len(raw_data[0]))
            self.data_table.setHorizontalHeaderLabels(list(raw_data[0].keys()))
            
            for i, row in enumerate(raw_data):
                for j, (key, value) in enumerate(row.items()):
                    self.data_table.setItem(i, j, QTableWidgetItem(str(value)))
        
        # Plot default chart
        self.plot_chart('bar')

    def plot_chart(self, chart_type):
        if not self.current_analysis:
            QMessageBox.warning(self, "No Data", "Please upload a file first")
            return
        
        self.chart_canvas.figure.clear()
        
        try:
            if chart_type == 'bar':
                ax = self.chart_canvas.figure.add_subplot(111)
                type_dist = self.current_analysis.get('type_distribution', {})
                if type_dist:
                    ax.bar(type_dist.keys(), type_dist.values(), color='#3b82f6', edgecolor='white', linewidth=1.5)
                    ax.set_title('Equipment Type Distribution', fontsize=16, fontweight='bold', pad=20)
                    ax.set_xlabel('Equipment Type', fontsize=12, fontweight='bold')
                    ax.set_ylabel('Count', fontsize=12, fontweight='bold')
                    ax.tick_params(axis='x', rotation=45)
                    ax.grid(axis='y', alpha=0.3)
            
            elif chart_type == 'scatter':
                ax = self.chart_canvas.figure.add_subplot(111)
                raw_data = self.current_analysis.get('raw_data', [])
                
                if raw_data and len(raw_data) > 0:
                    # Get numeric columns
                    first_row = raw_data[0]
                    numeric_cols = []
                    for key, value in first_row.items():
                        try:
                            float(str(value))
                            numeric_cols.append(key)
                        except:
                            pass
                    
                    if len(numeric_cols) >= 2:
                        # Use first two numeric columns
                        x_col = numeric_cols[0]
                        y_col = numeric_cols[1]
                        
                        x_data = []
                        y_data = []
                        for row in raw_data:
                            try:
                                x_data.append(float(row.get(x_col, 0)))
                                y_data.append(float(row.get(y_col, 0)))
                            except:
                                pass
                        
                        if x_data and y_data:
                            ax.scatter(x_data, y_data, alpha=0.6, s=100, color='#06b6d4', edgecolors='white', linewidth=1)
                            ax.set_title(f'{x_col} vs {y_col}', fontsize=16, fontweight='bold', pad=20)
                            ax.set_xlabel(x_col, fontsize=12, fontweight='bold')
                            ax.set_ylabel(y_col, fontsize=12, fontweight='bold')
                            ax.grid(True, alpha=0.3)
                        else:
                            ax.text(0.5, 0.5, 'No valid data for scatter plot', 
                                   ha='center', va='center', fontsize=14)
                    else:
                        ax.text(0.5, 0.5, 'Need at least 2 numeric columns', 
                               ha='center', va='center', fontsize=14)
                else:
                    ax.text(0.5, 0.5, 'No data available', ha='center', va='center', fontsize=14)
            
            elif chart_type == 'pie':
                ax = self.chart_canvas.figure.add_subplot(111)
                health_dist = self.current_analysis.get('health_score_distribution', {})
                if health_dist:
                    labels = ['Excellent\n(90-100%)', 'Good\n(70-89%)', 'Fair\n(50-69%)', 'Poor\n(<50%)']
                    sizes = [health_dist.get('excellent', 0), health_dist.get('good', 0),
                            health_dist.get('fair', 0), health_dist.get('poor', 0)]
                    colors = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444']
                    explode = (0.05, 0, 0, 0.05)
                    
                    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', 
                          startangle=90, explode=explode, shadow=True,
                          textprops={'fontsize': 11, 'fontweight': 'bold'})
                    ax.set_title('Health Score Distribution', fontsize=16, fontweight='bold', pad=20)
            
            elif chart_type == '3d':
                ax = self.chart_canvas.figure.add_subplot(111, projection='3d')
                raw_data = self.current_analysis.get('raw_data', [])
                
                if raw_data and len(raw_data) > 0:
                    # Get numeric columns
                    first_row = raw_data[0]
                    numeric_cols = []
                    for key, value in first_row.items():
                        try:
                            float(str(value))
                            numeric_cols.append(key)
                        except:
                            pass
                    
                    if len(numeric_cols) >= 3:
                        x_col, y_col, z_col = numeric_cols[:3]
                        
                        x_data, y_data, z_data = [], [], []
                        for row in raw_data:
                            try:
                                x_data.append(float(row.get(x_col, 0)))
                                y_data.append(float(row.get(y_col, 0)))
                                z_data.append(float(row.get(z_col, 0)))
                            except:
                                pass
                        
                        if x_data and y_data and z_data:
                            scatter = ax.scatter(x_data, y_data, z_data, c=z_data, 
                                               cmap='viridis', marker='o', s=50, alpha=0.7)
                            ax.set_xlabel(x_col, fontsize=10, fontweight='bold')
                            ax.set_ylabel(y_col, fontsize=10, fontweight='bold')
                            ax.set_zlabel(z_col, fontsize=10, fontweight='bold')
                            ax.set_title('3D Parameter Visualization', fontsize=14, fontweight='bold', pad=20)
                            self.chart_canvas.figure.colorbar(scatter, ax=ax, shrink=0.5)
                        else:
                            ax.text(0.5, 0.5, 0.5, 'No valid data', ha='center', va='center')
                    else:
                        ax.text(0.5, 0.5, 0.5, 'Need at least 3 numeric columns', 
                               ha='center', va='center')
                else:
                    ax.text(0.5, 0.5, 0.5, 'No data available', ha='center', va='center')
            
            elif chart_type == 'heatmap':
                ax = self.chart_canvas.figure.add_subplot(111)
                correlation = self.current_analysis.get('correlation', {})
                
                if correlation:
                    # Extract correlation matrix
                    params = set()
                    for key in correlation.keys():
                        p1, p2 = key.split(' vs ')
                        params.add(p1)
                        params.add(p2)
                    
                    params = sorted(list(params))
                    n = len(params)
                    corr_matrix = np.ones((n, n))
                    
                    for i, p1 in enumerate(params):
                        for j, p2 in enumerate(params):
                            if i != j:
                                key1 = f"{p1} vs {p2}"
                                key2 = f"{p2} vs {p1}"
                                if key1 in correlation:
                                    corr_matrix[i][j] = correlation[key1]
                                elif key2 in correlation:
                                    corr_matrix[i][j] = correlation[key2]
                    
                    im = ax.imshow(corr_matrix, cmap='RdYlGn', aspect='auto', vmin=-1, vmax=1)
                    ax.set_xticks(np.arange(n))
                    ax.set_yticks(np.arange(n))
                    ax.set_xticklabels(params, rotation=45, ha='right')
                    ax.set_yticklabels(params)
                    
                    # Add correlation values
                    for i in range(n):
                        for j in range(n):
                            text = ax.text(j, i, f'{corr_matrix[i, j]:.2f}',
                                         ha="center", va="center", color="black", fontsize=9)
                    
                    ax.set_title('Correlation Heatmap', fontsize=16, fontweight='bold', pad=20)
                    self.chart_canvas.figure.colorbar(im, ax=ax, label='Correlation')
                else:
                    ax.text(0.5, 0.5, 'No correlation data', ha='center', va='center', fontsize=14)
            
            elif chart_type == 'box':
                ax = self.chart_canvas.figure.add_subplot(111)
                raw_data = self.current_analysis.get('raw_data', [])
                
                if raw_data:
                    numeric_cols = []
                    for key, value in raw_data[0].items():
                        try:
                            float(str(value))
                            numeric_cols.append(key)
                        except:
                            pass
                    
                    if numeric_cols:
                        data_arrays = []
                        labels = []
                        for col in numeric_cols[:5]:  # Max 5 parameters
                            values = []
                            for row in raw_data:
                                try:
                                    values.append(float(row.get(col, 0)))
                                except:
                                    pass
                            if values:
                                data_arrays.append(values)
                                labels.append(col)
                        
                        if data_arrays:
                            bp = ax.boxplot(data_arrays, labels=labels, patch_artist=True,
                                          notch=True, showmeans=True)
                            
                            # Color boxes
                            colors_list = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
                            for patch, color in zip(bp['boxes'], colors_list):
                                patch.set_facecolor(color)
                                patch.set_alpha(0.7)
                            
                            ax.set_title('Box Plot - Parameter Distribution', fontsize=16, fontweight='bold', pad=20)
                            ax.set_ylabel('Value', fontsize=12, fontweight='bold')
                            ax.grid(axis='y', alpha=0.3)
                            ax.tick_params(axis='x', rotation=45)
                    else:
                        ax.text(0.5, 0.5, 'No numeric data', ha='center', va='center', fontsize=14)
                else:
                    ax.text(0.5, 0.5, 'No data available', ha='center', va='center', fontsize=14)
            
            elif chart_type == 'histogram':
                raw_data = self.current_analysis.get('raw_data', [])
                
                if raw_data:
                    numeric_cols = []
                    for key, value in raw_data[0].items():
                        try:
                            float(str(value))
                            numeric_cols.append(key)
                        except:
                            pass
                    
                    if numeric_cols:
                        n_cols = min(len(numeric_cols), 3)
                        for idx, col in enumerate(numeric_cols[:n_cols]):
                            ax = self.chart_canvas.figure.add_subplot(1, n_cols, idx + 1)
                            
                            values = []
                            for row in raw_data:
                                try:
                                    values.append(float(row.get(col, 0)))
                                except:
                                    pass
                            
                            if values:
                                ax.hist(values, bins=20, color='#2563eb', alpha=0.7, edgecolor='white')
                                ax.set_title(col, fontsize=12, fontweight='bold')
                                ax.set_xlabel('Value', fontsize=10)
                                ax.set_ylabel('Frequency', fontsize=10)
                                ax.grid(axis='y', alpha=0.3)
                    else:
                        ax = self.chart_canvas.figure.add_subplot(111)
                        ax.text(0.5, 0.5, 'No numeric data', ha='center', va='center', fontsize=14)
                else:
                    ax = self.chart_canvas.figure.add_subplot(111)
                    ax.text(0.5, 0.5, 'No data available', ha='center', va='center', fontsize=14)
            
            self.chart_canvas.figure.tight_layout()
            self.chart_canvas.draw()
            
        except Exception as e:
            QMessageBox.critical(self, "Chart Error", f"Failed to generate chart: {str(e)}")

    def load_history(self):
        try:
            history = self.api_client.get_history()
            self.history_list.clear()
            for item in history:
                self.history_list.addItem(f"{item['filename']} ({item['row_count']} rows)")
                self.history_list.item(self.history_list.count() - 1).setData(Qt.UserRole, item['id'])
            
            self.compare_btn.setEnabled(self.history_list.count() >= 2)
        except Exception as e:
            print(f"History load error: {e}")

    def load_analysis_from_history(self, item):
        file_id = item.data(Qt.UserRole)
        try:
            result = self.api_client.get_analysis(file_id)
            if result.get('status') == 'success':
                self.current_analysis = result.get('data')
                self.current_file_id = file_id
                self.display_analysis(self.current_analysis)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load analysis: {str(e)}")

    def delete_file(self):
        selected = self.history_list.selectedItems()
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select a file to delete")
            return
        
        file_id = selected[0].data(Qt.UserRole)
        reply = QMessageBox.question(self, "Confirm Delete", 
                                     "Are you sure you want to delete this file?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                if self.api_client.delete_file(file_id):
                    QMessageBox.information(self, "Success", "File deleted successfully!")
                    self.load_history()
                    if self.current_file_id == file_id:
                        self.current_file_id = None
                        self.current_analysis = None
                else:
                    QMessageBox.critical(self, "Error", "Failed to delete file")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Delete error: {str(e)}")

    def compare_datasets(self):
        selected = self.history_list.selectedItems()
        if len(selected) != 2:
            QMessageBox.warning(self, "Selection Error", "Please select exactly 2 datasets")
            return
        
        file_id_1 = selected[0].data(Qt.UserRole)
        file_id_2 = selected[1].data(Qt.UserRole)
        
        try:
            result = self.api_client.compare_datasets(file_id_1, file_id_2)
            msg = f"Dataset 1: {result['dataset1']['name']}\n"
            msg += f"Health: {result['dataset1']['stats']['health_score_avg']:.1f}%\n\n"
            msg += f"Dataset 2: {result['dataset2']['name']}\n"
            msg += f"Health: {result['dataset2']['stats']['health_score_avg']:.1f}%"
            QMessageBox.information(self, "Comparison Results", msg)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def export_pdf(self):
        if not self.current_file_id:
            QMessageBox.warning(self, "No Data", "Please upload a file first")
            return
        
        password, ok = QInputDialog.getText(self, "Password", "Enter password for PDF:", QLineEdit.Password)
        if ok and password:
            try:
                self.export_pdf_btn.setEnabled(False)
                self.export_pdf_btn.setText("Generating PDF...")
                
                pdf_data = self.api_client.export_pdf(self.current_file_id, password)
                
                file_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", "report.pdf", "PDF Files (*.pdf)")
                if file_path:
                    with open(file_path, 'wb') as f:
                        f.write(pdf_data)
                    QMessageBox.information(self, "Success", f"PDF saved to:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Export failed: {str(e)}")
            finally:
                self.export_pdf_btn.setEnabled(True)
                self.export_pdf_btn.setText("Export PDF Report")

    def export_excel(self):
        if not self.current_file_id:
            QMessageBox.warning(self, "No Data", "Please upload a file first")
            return
        
        password, ok = QInputDialog.getText(self, "Password", "Enter password for Excel:", QLineEdit.Password)
        if ok and password:
            try:
                self.export_excel_btn.setEnabled(False)
                self.export_excel_btn.setText("Generating Excel...")
                
                excel_data = self.api_client.export_excel(self.current_file_id, password)
                
                file_path, _ = QFileDialog.getSaveFileName(self, "Save Excel", "report.xlsx", "Excel Files (*.xlsx)")
                if file_path:
                    with open(file_path, 'wb') as f:
                        f.write(excel_data)
                    QMessageBox.information(self, "Success", f"Excel saved to:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Export failed: {str(e)}")
            finally:
                self.export_excel_btn.setEnabled(True)
                self.export_excel_btn.setText("Export Excel Report")

    def show_profile(self):
        try:
            profile = self.api_client.get_profile()
            msg = f"Username: {profile.get('username')}\n"
            msg += f"Email: {profile.get('email')}\n"
            msg += f"Uploads: {profile.get('upload_count', 0)}\n"
            msg += f"Storage: {profile.get('storage_mb', 0):.2f} MB"
            QMessageBox.information(self, "Profile", msg)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def toggle_theme(self):
        new_theme = self.theme_manager.toggle_theme()
        self.window().setStyleSheet(new_theme)

    def logout(self):
        reply = QMessageBox.question(self, "Logout", "Are you sure you want to logout?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.api_client.logout()
            self.window().show_login()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_U and event.modifiers() == Qt.ControlModifier:
            self.upload_file()
