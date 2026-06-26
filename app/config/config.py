"""
Application configuration and settings.
"""

from pathlib import Path


class AppConfig:
    """Configuration class for application-wide settings."""
    
    # Application metadata
    APP_NAME = "Conways Multiverse"
    APP_VERSION = "1.0.0"
    
    # Window settings
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    WINDOW_MIN_WIDTH = 800
    WINDOW_MIN_HEIGHT = 600
    
    # Paths
    BASE_DIR = Path(__file__).parent.parent.parent
    RESOURCES_DIR = BASE_DIR / "app" / "resources"
    STYLES_DIR = RESOURCES_DIR / "styles"
    ASSETS_DIR = RESOURCES_DIR / "assets"
    
    # Debug mode
    DEBUG = True
    
    @classmethod
    def get_style_path(cls, filename: str) -> Path:
        """Get the full path to a style file."""
        return cls.STYLES_DIR / filename
    
    @classmethod
    def get_asset_path(cls, filename: str) -> Path:
        """Get the full path to an asset file."""
        return cls.ASSETS_DIR / filename
