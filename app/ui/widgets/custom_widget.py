"""
Example custom widget implementation.
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt


class CustomWidget(QWidget):
    """A template custom widget."""
    
    def __init__(self, parent=None):
        """Initialize the custom widget."""
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the UI components."""
        layout = QVBoxLayout(self)
        label = QLabel("Custom Widget Content")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
