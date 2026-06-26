"""
Main application window implementation.
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QMenuBar, QMenu, QPushButton, QStatusBar
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

from app.config.config import AppConfig
from app.ui.widgets.custom_widget import CustomWidget
from app.utils.helpers import load_stylesheet


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        self.setWindowTitle(AppConfig.APP_NAME)
        self.setGeometry(100, 100, AppConfig.WINDOW_WIDTH, AppConfig.WINDOW_HEIGHT)
        self.setMinimumSize(AppConfig.WINDOW_MIN_WIDTH, AppConfig.WINDOW_MIN_HEIGHT)
        
        self.setup_ui()
        self.create_menu_bar()
        self.create_status_bar()
        self.apply_styles()
    
    def setup_ui(self):
        """Set up the main UI layout."""
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Add custom widget
        custom_widget = CustomWidget()
        main_layout.addWidget(custom_widget)
        
        # Add button layout
        button_layout = QHBoxLayout()
        
        btn_action = QPushButton("Action Button")
        btn_action.clicked.connect(self.on_action_button_clicked)
        button_layout.addWidget(btn_action)
        
        btn_exit = QPushButton("Exit")
        btn_exit.clicked.connect(self.close)
        button_layout.addWidget(btn_exit)
        
        main_layout.addLayout(button_layout)
    
    def create_menu_bar(self):
        """Create the application menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        exit_action = QAction("E&xit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("&Edit")
        
        undo_action = QAction("&Undo", self)
        undo_action.triggered.connect(self.on_undo)
        edit_menu.addAction(undo_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.on_about)
        help_menu.addAction(about_action)
    
    def create_status_bar(self):
        """Create the status bar."""
        status_bar = self.statusBar()
        status_bar.showMessage("Ready")
    
    def apply_styles(self):
        """Apply stylesheets to the application."""
        stylesheet = load_stylesheet("style.qss")
        if stylesheet:
            self.setStyleSheet(stylesheet)
    
    def on_action_button_clicked(self):
        """Handle action button click."""
        self.statusBar().showMessage("Action button clicked")
    
    def on_undo(self):
        """Handle undo action."""
        self.statusBar().showMessage("Undo action triggered")
    
    def on_about(self):
        """Handle about action."""
        self.statusBar().showMessage(
            f"{AppConfig.APP_NAME} v{AppConfig.APP_VERSION}"
        )
