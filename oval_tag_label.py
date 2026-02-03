"""Custom oval-shaped tag label widget."""
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainter, QPainterPath, QColor, QPen


class OvalTagLabel(QLabel):
    """Custom label with oval/pill shape background."""
    
    def __init__(self, text: str, color: str, parent=None):
        super().__init__(text, parent)
        self.bg_color = QColor(color)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedHeight(40)
        self.setMinimumWidth(100)
        self.setMaximumWidth(250)
        self.setStyleSheet(f"""
            QLabel {{
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 11pt;
                font-weight: 600;
                color: white;
                background-color: transparent;
                padding: 8px 20px;
            }}
        """)
    
    def paintEvent(self, event):
        """Custom paint to draw oval background."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw oval background
        path = QPainterPath()
        rect = QRectF(self.rect()).adjusted(2, 2, -2, -2)
        radius = rect.height() / 2
        path.addRoundedRect(rect, radius, radius)
        
        # Fill with color
        painter.fillPath(path, self.bg_color)
        
        # Draw border
        pen = QPen(self.bg_color.darker(110), 2)
        painter.setPen(pen)
        painter.drawPath(path)
        
        # Draw text
        painter.setPen(QColor("white"))
        painter.setFont(self.font())
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())
