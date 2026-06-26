"""Main application window and layout composition for the PySide UI."""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QMenuBar, QMenu, QPushButton, QStatusBar, QLabel
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QAction

from app.config.config import AppConfig
from app.ui.widgets.grid import GameGrid
from app.utils.helpers import load_stylesheet

from Game.GameInstance import GameInstance


class MainWindow(QMainWindow):
    """Top-level application window with a square-resize constraint.

    The central layout contains a playable grid in the middle and placeholder
    side panels for future controls and status content.
    """
    
    def __init__(self):
        """Initialize window metadata, layout, and standard UI elements."""
        super().__init__()
        self.setWindowTitle(AppConfig.APP_NAME)
        self.setGeometry(100, 100, AppConfig.WINDOW_WIDTH, AppConfig.WINDOW_HEIGHT)
        self.setMinimumSize(AppConfig.WINDOW_MIN_WIDTH, AppConfig.WINDOW_MIN_HEIGHT)
        
        # Ensure window is always square
        self.resize(800, 800)
        
        self.setup_ui()
        self.create_menu_bar()
        self.create_status_bar()
        self.apply_styles()

    def resizeEvent(self, event):
        """Enforce a square window aspect ratio during user resize.

        Args:
            event: Qt resize event containing the proposed dimensions.
        """
        super().resizeEvent(event)
        # Get the new size
        new_size = event.size()
        # Make it square: use the minimum of width and height
        size = min(new_size.width(), new_size.height())
        # Resize to square
        self.resize(size, size)
    
    def setup_ui(self):
        """Create the full central layout and wire widget interactions."""
        # Create the root central widget and top-level vertical layout.
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(5)
        
        # Top toolbar row for immediate actions.
        button_layout = QHBoxLayout()
        
        btn_action = QPushButton("Action Button")
        button_layout.addWidget(btn_action)
        
        btn_exit = QPushButton("Exit")
        btn_exit.clicked.connect(self.close)
        button_layout.addWidget(btn_exit)
        
        main_layout.addLayout(button_layout, 0)
        
        # Middle section combines placeholder regions around the game grid.
        middle_layout = QVBoxLayout()
        middle_layout.setContentsMargins(0, 0, 0, 0)
        middle_layout.setSpacing(5)
        
        # Top placeholder
        top_placeholder = self.create_placeholder("Top Panel")
        middle_layout.addWidget(top_placeholder, 1)
        
        # Center row: left panel, grid, right panel.
        center_layout = QHBoxLayout()
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(5)
        
        # Left placeholder
        left_placeholder = self.create_placeholder("Left Panel")
        center_layout.addWidget(left_placeholder, 1)
        
        # Grid receives a larger stretch factor than side placeholders.
        game_grid = GameGrid()
        center_layout.addWidget(game_grid, 3)
        
        # Right placeholder
        right_placeholder = self.create_placeholder("Right Panel")
        center_layout.addWidget(right_placeholder, 1)
        
        middle_layout.addLayout(center_layout, 3)
        
        # Bottom placeholder
        bottom_placeholder = self.create_placeholder("Bottom Panel")
        middle_layout.addWidget(bottom_placeholder, 1)

        # Wire the action button to step the simulation by one generation.
        btn_action.clicked.connect(game_grid.step_game)

        main_layout.addLayout(middle_layout, 1)
    
    def create_placeholder(self, title: str) -> QWidget:
        """
        Create a placeholder widget with centered text.
        
        Args:
            title: The text to display in the placeholder.
        
        Returns:
            QWidget: A placeholder widget with the given title.
        """
        placeholder = QWidget()
        placeholder.setStyleSheet("background-color: #e8e8e8; border: 1px solid #999;")
        layout = QVBoxLayout(placeholder)
        label = QLabel(title)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        return placeholder
    
    def create_menu_bar(self):
        """Create and populate the application menu bar."""
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
        """Create the status bar and set an initial ready message."""
        status_bar = self.statusBar()
        status_bar.showMessage("Ready")
    
    def apply_styles(self):
        """Apply the shared application stylesheet when available."""
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
