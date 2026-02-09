from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QPainter, QBrush, QPainterPath
import os

class LoginView(QWidget):
    login_success = pyqtSignal(dict)

    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.is_login_mode = True
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Left panel - Purple gradient
        left_panel = QFrame()
        left_panel.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
            }
            QLabel {
                color: white;
            }
        """)
        left_panel.setMinimumWidth(450)
        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignCenter)
        left_layout.setContentsMargins(50, 50, 50, 50)
        
        # Logo - circular image
        logo_label = QLabel()
        logo_label.setFixedSize(140, 140)
        logo_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'logo.png')
        
        if os.path.exists(logo_path):
            # Load and make circular
            pixmap = QPixmap(logo_path)
            pixmap = pixmap.scaled(140, 140, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            
            # Create circular mask
            circular = QPixmap(140, 140)
            circular.fill(Qt.transparent)
            
            painter = QPainter(circular)
            painter.setRenderHint(QPainter.Antialiasing)
            path = QPainterPath()
            path.addEllipse(0, 0, 140, 140)
            painter.setClipPath(path)
            painter.drawPixmap(0, 0, pixmap)
            painter.end()
            
            logo_label.setPixmap(circular)
        else:
            # Fallback
            logo_label.setStyleSheet("""
                QLabel {
                    background-color: rgba(255, 255, 255, 0.2);
                    border-radius: 70px;
                    color: white;
                    font-size: 48px;
                    font-weight: bold;
                }
            """)
            logo_label.setText("CEV")
            logo_label.setAlignment(Qt.AlignCenter)
        
        left_layout.addWidget(logo_label, 0, Qt.AlignCenter)
        
        # Title
        brand_title = QLabel("POTASH")
        brand_title.setFont(QFont("Segoe UI", 32, QFont.Bold))
        brand_title.setAlignment(Qt.AlignCenter)
        brand_title.setWordWrap(True)
        left_layout.addWidget(brand_title)
        
        # Subtitle
        brand_subtitle = QLabel("Chemical Equipment Data\nAnalysis & Visualization")
        brand_subtitle.setFont(QFont("Segoe UI", 13))
        brand_subtitle.setAlignment(Qt.AlignCenter)
        brand_subtitle.setWordWrap(True)
        left_layout.addWidget(brand_subtitle)
        
        left_layout.addStretch()
        
        # Features
        features = QLabel("✓ AI-Powered Insights\n✓ Real-time Analysis\n✓ 3D Visualizations\n✓ Secure Exports")
        features.setFont(QFont("Segoe UI", 13))
        features.setAlignment(Qt.AlignLeft)
        left_layout.addWidget(features)
        
        left_panel.setLayout(left_layout)
        
        # Right panel - White form
        right_panel = QFrame()
        right_panel.setStyleSheet("QFrame { background-color: white; }")
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignCenter)
        right_layout.setContentsMargins(80, 80, 80, 80)
        
        form_container = QFrame()
        form_container.setMaximumWidth(400)
        form_layout = QVBoxLayout()
        form_layout.setSpacing(25)
        
        # Welcome
        self.welcome_label = QLabel("Welcome Back")
        self.welcome_label.setFont(QFont("Segoe UI", 28, QFont.Bold))
        self.welcome_label.setStyleSheet("color: #1e293b;")
        form_layout.addWidget(self.welcome_label)
        
        # Subtitle
        self.mode_subtitle = QLabel("Sign in to continue")
        self.mode_subtitle.setFont(QFont("Segoe UI", 13))
        self.mode_subtitle.setStyleSheet("color: #64748b;")
        form_layout.addWidget(self.mode_subtitle)
        
        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setMinimumHeight(55)
        self.username_input.setFont(QFont("Segoe UI", 12))
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                padding: 12px 16px;
                color: #1e293b;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
                background-color: white;
            }
        """)
        form_layout.addWidget(self.username_input)
        
        # Email (hidden initially)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email address")
        self.email_input.setMinimumHeight(55)
        self.email_input.setFont(QFont("Segoe UI", 12))
        self.email_input.setStyleSheet("""
            QLineEdit {
                background-color: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                padding: 12px 16px;
                color: #1e293b;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
                background-color: white;
            }
        """)
        self.email_input.setVisible(False)
        form_layout.addWidget(self.email_input)
        
        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(55)
        self.password_input.setFont(QFont("Segoe UI", 12))
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                padding: 12px 16px;
                color: #1e293b;
            }
            QLineEdit:focus {
                border: 2px solid #667eea;
                background-color: white;
            }
        """)
        form_layout.addWidget(self.password_input)
        
        # Sign In button
        self.action_btn = QPushButton("Sign In")
        self.action_btn.setMinimumHeight(55)
        self.action_btn.setFont(QFont("Segoe UI", 13, QFont.Bold))
        self.action_btn.setCursor(Qt.PointingHandCursor)
        self.action_btn.setStyleSheet("""
            QPushButton {
                background-color: #667eea;
                color: white;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #5568d3;
            }
            QPushButton:pressed {
                background-color: #4c5fc7;
            }
            QPushButton:disabled {
                background-color: #cbd5e1;
                color: #94a3b8;
            }
        """)
        self.action_btn.clicked.connect(self.handle_action)
        form_layout.addWidget(self.action_btn)
        
        # Toggle
        toggle_layout = QHBoxLayout()
        toggle_layout.setAlignment(Qt.AlignCenter)
        
        self.toggle_text = QLabel("Don't have an account?")
        self.toggle_text.setFont(QFont("Segoe UI", 11))
        self.toggle_text.setStyleSheet("color: #64748b;")
        toggle_layout.addWidget(self.toggle_text)
        
        self.toggle_btn = QPushButton("Sign Up")
        self.toggle_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.toggle_btn.setCursor(Qt.PointingHandCursor)
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #667eea;
                border: none;
                padding: 5px;
            }
            QPushButton:hover {
                color: #5568d3;
            }
        """)
        self.toggle_btn.clicked.connect(self.toggle_mode)
        toggle_layout.addWidget(self.toggle_btn)
        
        form_layout.addLayout(toggle_layout)
        
        form_container.setLayout(form_layout)
        right_layout.addWidget(form_container)
        right_panel.setLayout(right_layout)
        
        main_layout.addWidget(left_panel, 2)
        main_layout.addWidget(right_panel, 3)
        
        self.password_input.returnPressed.connect(self.handle_action)
        self.setLayout(main_layout)
    
    def toggle_mode(self):
        self.is_login_mode = not self.is_login_mode
        
        if self.is_login_mode:
            self.welcome_label.setText("Welcome Back")
            self.mode_subtitle.setText("Sign in to continue")
            self.action_btn.setText("Sign In")
            self.toggle_text.setText("Don't have an account?")
            self.toggle_btn.setText("Sign Up")
            self.email_input.setVisible(False)
        else:
            self.welcome_label.setText("Create Account")
            self.mode_subtitle.setText("Sign up to get started")
            self.action_btn.setText("Create Account")
            self.toggle_text.setText("Already have an account?")
            self.toggle_btn.setText("Sign In")
            self.email_input.setVisible(True)
    
    def handle_action(self):
        if self.is_login_mode:
            self.handle_login()
        else:
            self.handle_signup()
    
    def handle_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return

        try:
            self.action_btn.setEnabled(False)
            self.action_btn.setText("Signing in...")
            
            result = self.api_client.login(username, password)
            
            if self.api_client.access_token:
                self.login_success.emit(result)
            else:
                error_msg = result.get('detail', 'Invalid credentials')
                QMessageBox.critical(self, "Login Failed", error_msg)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Connection error: {str(e)}")
        finally:
            self.action_btn.setEnabled(True)
            self.action_btn.setText("Sign In")
    
    def handle_signup(self):
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text()

        if not username or not email or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return

        try:
            self.action_btn.setEnabled(False)
            self.action_btn.setText("Creating account...")
            
            result = self.api_client.signup(username, email, password)
            
            if self.api_client.access_token:
                self.login_success.emit(result)
            else:
                error_msg = result.get('username', result.get('email', ['Registration failed']))[0]
                QMessageBox.critical(self, "Signup Failed", error_msg)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Connection error: {str(e)}")
        finally:
            self.action_btn.setEnabled(True)
            self.action_btn.setText("Create Account")
