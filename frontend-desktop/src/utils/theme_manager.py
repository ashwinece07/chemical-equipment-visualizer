from PyQt5.QtCore import QSettings

class ThemeManager:
    LIGHT_THEME = """
        QMainWindow, QWidget {
            background-color: #f8fafc;
            color: #1e293b;
        }
        QPushButton {
            background-color: #2563eb;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #1d4ed8;
        }
        QPushButton:pressed {
            background-color: #1e40af;
        }
        QPushButton:disabled {
            background-color: #cbd5e1;
            color: #94a3b8;
        }
        QLineEdit, QTextEdit {
            background-color: white;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            padding: 8px;
            color: #1e293b;
            font-size: 14px;
        }
        QLineEdit:focus, QTextEdit:focus {
            border-color: #2563eb;
        }
        QLabel {
            color: #1e293b;
            font-size: 14px;
        }
        QTableWidget {
            background-color: white;
            alternate-background-color: #f8fafc;
            border: 1px solid #e2e8f0;
            gridline-color: #e2e8f0;
            border-radius: 8px;
        }
        QTableWidget::item {
            padding: 8px;
            color: #1e293b;
        }
        QHeaderView::section {
            background-color: #2563eb;
            color: white;
            padding: 12px;
            border: none;
            font-weight: bold;
            font-size: 13px;
        }
        QTabWidget::pane {
            border: 1px solid #e2e8f0;
            background-color: white;
            border-radius: 8px;
        }
        QTabBar::tab {
            background-color: #f1f5f9;
            color: #64748b;
            padding: 14px 28px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            margin-right: 2px;
            font-weight: 600;
            font-size: 14px;
            min-width: 100px;
        }
        QTabBar::tab:selected {
            background-color: #2563eb;
            color: white;
        }
        QTabBar::tab:hover {
            background-color: #e0e7ff;
        }
        QScrollBar:vertical {
            background-color: #f1f5f9;
            width: 12px;
            border-radius: 6px;
        }
        QScrollBar::handle:vertical {
            background-color: #cbd5e1;
            border-radius: 6px;
        }
        QScrollBar::handle:vertical:hover {
            background-color: #2563eb;
        }
        QComboBox {
            background-color: white;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            padding: 8px;
            color: #1e293b;
        }
        QComboBox:focus {
            border-color: #2563eb;
        }
        QProgressBar {
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            text-align: center;
            background-color: #f8fafc;
            color: #1e293b;
            font-weight: bold;
        }
        QProgressBar::chunk {
            background-color: #2563eb;
            border-radius: 6px;
        }
        QListWidget {
            background-color: white;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            padding: 4px;
        }
        QListWidget::item {
            padding: 10px;
            border-radius: 6px;
            margin: 2px;
            color: #1e293b;
        }
        QListWidget::item:selected {
            background-color: #2563eb;
            color: white;
        }
        QListWidget::item:hover {
            background-color: #e0e7ff;
        }
    """

    DARK_THEME = """
        QMainWindow, QWidget {
            background-color: #0f172a;
            color: #e2e8f0;
        }
        QPushButton {
            background-color: #2563eb;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #1d4ed8;
        }
        QPushButton:pressed {
            background-color: #1e40af;
        }
        QPushButton:disabled {
            background-color: #334155;
            color: #64748b;
        }
        QLineEdit, QTextEdit {
            background-color: #1e293b;
            border: 2px solid #334155;
            border-radius: 8px;
            padding: 8px;
            color: #e2e8f0;
            font-size: 14px;
        }
        QLineEdit:focus, QTextEdit:focus {
            border-color: #2563eb;
        }
        QLabel {
            color: #e2e8f0;
            font-size: 14px;
        }
        QTableWidget {
            background-color: #1e293b;
            alternate-background-color: #0f172a;
            border: 1px solid #334155;
            gridline-color: #334155;
            color: #e2e8f0;
            border-radius: 8px;
        }
        QTableWidget::item {
            padding: 8px;
            color: #e2e8f0;
        }
        QHeaderView::section {
            background-color: #2563eb;
            color: white;
            padding: 12px;
            border: none;
            font-weight: bold;
            font-size: 13px;
        }
        QTabWidget::pane {
            border: 1px solid #334155;
            background-color: #1e293b;
            border-radius: 8px;
        }
        QTabBar::tab {
            background-color: #334155;
            color: #94a3b8;
            padding: 14px 28px;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
            margin-right: 2px;
            font-weight: 600;
            font-size: 14px;
            min-width: 100px;
        }
        QTabBar::tab:selected {
            background-color: #2563eb;
            color: white;
        }
        QTabBar::tab:hover {
            background-color: #475569;
        }
        QScrollBar:vertical {
            background-color: #1e293b;
            width: 12px;
            border-radius: 6px;
        }
        QScrollBar::handle:vertical {
            background-color: #475569;
            border-radius: 6px;
        }
        QScrollBar::handle:vertical:hover {
            background-color: #2563eb;
        }
        QComboBox {
            background-color: #1e293b;
            border: 2px solid #334155;
            border-radius: 8px;
            padding: 8px;
            color: #e2e8f0;
        }
        QComboBox:focus {
            border-color: #2563eb;
        }
        QComboBox QAbstractItemView {
            background-color: #1e293b;
            color: #e2e8f0;
            selection-background-color: #2563eb;
        }
        QProgressBar {
            border: 2px solid #334155;
            border-radius: 8px;
            text-align: center;
            background-color: #1e293b;
            color: #e2e8f0;
            font-weight: bold;
        }
        QProgressBar::chunk {
            background-color: #2563eb;
            border-radius: 6px;
        }
        QListWidget {
            background-color: #1e293b;
            border: 2px solid #334155;
            border-radius: 8px;
            padding: 4px;
        }
        QListWidget::item {
            padding: 10px;
            border-radius: 6px;
            margin: 2px;
            color: #e2e8f0;
        }
        QListWidget::item:selected {
            background-color: #2563eb;
            color: white;
        }
        QListWidget::item:hover {
            background-color: #334155;
        }
    """

    def __init__(self):
        self.settings = QSettings("ChemicalVisualizer", "Desktop")
        self.is_dark = self.settings.value("dark_mode", True, type=bool)  # Default to dark

    def get_theme(self) -> str:
        return self.DARK_THEME if self.is_dark else self.LIGHT_THEME

    def toggle_theme(self) -> str:
        self.is_dark = not self.is_dark
        self.settings.setValue("dark_mode", self.is_dark)
        return self.get_theme()

    def is_dark_mode(self) -> bool:
        return self.is_dark
