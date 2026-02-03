"""Create icon file for the application"""
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap, QPainter, QColor

def create_chip_icon():
    """Create a microchip-style icon programmatically."""
    pixmap = QPixmap(QSize(64, 64))
    pixmap.fill(Qt.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    
    # Draw chip body
    chip_rect = pixmap.rect().adjusted(12, 12, -12, -12)
    painter.setBrush(QColor('#2c3e50'))
    painter.setPen(QColor('#34495e'))
    painter.drawRoundedRect(chip_rect, 4, 4)
    
    # Draw chip notch (top-left corner indicator)
    painter.setBrush(QColor('#ecf0f1'))
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(15, 15, 8, 8)
    
    # Draw pins on left and right sides
    pin_color = QColor('#95a5a6')
    painter.setBrush(pin_color)
    
    # Left side pins
    for i in range(6):
        y = 16 + i * 7
        painter.drawRect(8, y, 4, 5)
    
    # Right side pins
    for i in range(6):
        y = 16 + i * 7
        painter.drawRect(52, y, 4, 5)
    
    # Draw circuit traces (decorative lines on chip)
    painter.setPen(QColor('#3498db'))
    painter.drawLine(20, 25, 44, 25)
    painter.drawLine(20, 32, 44, 32)
    painter.drawLine(20, 39, 44, 39)
    
    painter.end()
    return pixmap

if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    icon = create_chip_icon()
    icon.save('app_icon.ico', 'ICO')
    print("Icon created: app_icon.ico")
