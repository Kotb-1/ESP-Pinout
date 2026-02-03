"""Layout configuration for the pinout GUI."""
from typing import Tuple


class LayoutConfig:
    """Configuration for window and component layout."""
    
    WINDOW_WIDTH = 1500
    WINDOW_HEIGHT = 800
    IMAGE_ASPECT_RATIO = 214 / 105
    IMAGE_WIDTH = 300
    
    # Pin positioning constants
    PIN_BUTTON_WIDTH = 36
    PIN_BUTTON_HEIGHT = 20
    PIN_VERTICAL_STEP = 27
    
    # Info box dimensions
    INFO_BOX_WIDTH = 280
    INFO_BOX_HEIGHT = 450
    INFO_BOX_MARGIN = 50
    
    # Title configuration
    TITLE_HEIGHT = 60
    TITLE_MARGIN = 20
    
    # Legend configuration
    LEGEND_WIDTH = 200
    LEGEND_HEIGHT = 350
    LEGEND_MARGIN = 50
    
    @classmethod
    def get_image_dimensions(cls) -> Tuple[int, int]:
        """Calculate image dimensions based on aspect ratio."""
        width = cls.IMAGE_WIDTH
        height = int(width * cls.IMAGE_ASPECT_RATIO)
        return width, height
    
    @classmethod
    def get_image_position(cls) -> Tuple[int, int, int, int]:
        """Calculate centered image position (start_x, end_x, top_y, bottom_y)."""
        width, height = cls.get_image_dimensions()
        start_x = int((cls.WINDOW_WIDTH - width) / 2)
        end_x = int((cls.WINDOW_WIDTH + width) / 2)
        top_y = int((cls.WINDOW_HEIGHT - height) / 2)
        bottom_y = int((cls.WINDOW_HEIGHT + height) / 2)
        return start_x, end_x, top_y, bottom_y
