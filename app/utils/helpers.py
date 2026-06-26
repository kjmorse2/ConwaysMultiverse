"""
Helper functions and utilities for the application.
"""

from pathlib import Path
from PySide6.QtGui import QIcon


def load_icon(icon_path: str) -> QIcon:
    """
    Load an icon from the assets directory.
    
    Args:
        icon_path: Relative path to the icon file.
    
    Returns:
        QIcon: The loaded icon.
    """
    from app.config.config import AppConfig
    full_path = AppConfig.get_asset_path(icon_path)
    return QIcon(str(full_path))


def load_stylesheet(style_filename: str) -> str:
    """
    Load a stylesheet from the styles directory.
    
    Args:
        style_filename: Name of the .qss file to load.
    
    Returns:
        str: The stylesheet content.
    """
    from app.config.config import AppConfig
    style_path = AppConfig.get_style_path(style_filename)
    if style_path.exists():
        return style_path.read_text()
    return ""
