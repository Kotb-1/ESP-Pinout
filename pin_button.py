"""Custom button widget for pin interaction."""
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QRect, Qt


class PinButton(QPushButton):
    """Custom button for pin interaction with hover effects."""
    
    HOVER_COLORS = {
        'i2c': 'rgba(0, 128, 255, 80)',           # blue - #0080FF
        'adc': 'rgba(0, 200, 0, 80)',             # green - #00C800
        'spi': 'rgba(192, 192, 192, 80)',         # silver - #C0C0C0
        'pwm': 'rgba(255, 165, 0, 80)',           # orange - #FFA500
        'power': 'rgba(150, 98, 254, 80)',        # purple - #9662FE
        'input_only': 'rgba(247, 0, 255, 80)',    # magenta - #F700FF
        'in_out': 'rgba(0, 195, 255, 80)',        # cyan - #00C3FF
        'default': 'rgba(255, 0, 0, 80)'          # red - #FF0000
    }
    
    def __init__(self, pin_id: str, x: int, y: int, w: int, h: int, 
                 pin_category: str, parent=None):
        super().__init__('', parent)
        self.pin_id = pin_id
        self.setGeometry(QRect(x, y, w, h))
        self._apply_style(pin_category)
    
    def _apply_style(self, category: str):
        """Apply styling based on pin category."""
        hover_color = self.HOVER_COLORS.get(category, self.HOVER_COLORS['default'])
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(0, 0, 0, 0);
                border: none;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
                border: 2px solid rgba(44, 62, 80, 180);
                border-radius: 6px;
            }}
            QPushButton:pressed {{
                background-color: rgba(52, 152, 219, 120);
                border: 2px solid rgba(44, 62, 80, 255);
            }}
        """)
        self.setCursor(Qt.PointingHandCursor)
