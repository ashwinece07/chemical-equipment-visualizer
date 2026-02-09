import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtCore import Qt
from api_client import APIClient
from utils.theme_manager import ThemeManager
from views.login_view import LoginView
from views.dashboard_view import DashboardView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api_client = APIClient()
        self.theme_manager = ThemeManager()
        
        self.setWindowTitle("POTASH - Desktop Application")
        self.setGeometry(100, 100, 1400, 900)
        
        # Stack widget for switching views
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)
        
        # Create views
        self.login_view = LoginView(self.api_client)
        self.login_view.login_success.connect(self.show_dashboard)
        
        self.stack.addWidget(self.login_view)
        
        # Apply theme
        self.setStyleSheet(self.theme_manager.get_theme())
        
        self.show()

    def show_dashboard(self, user_data):
        # Remove old dashboard if exists
        if self.stack.count() > 1:
            old_dashboard = self.stack.widget(1)
            self.stack.removeWidget(old_dashboard)
            old_dashboard.deleteLater()
        
        # Create new dashboard
        self.dashboard_view = DashboardView(self.api_client, self.theme_manager)
        self.stack.addWidget(self.dashboard_view)
        self.stack.setCurrentIndex(1)

    def show_login(self):
        self.stack.setCurrentIndex(0)
        # Clear login fields
        self.login_view.username_input.clear()
        self.login_view.password_input.clear()

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Chemical Equipment Visualizer")
    app.setOrganizationName("ChemicalVisualizer")
    
    window = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
