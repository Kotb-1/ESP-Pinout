"""ESP32 Pinout GUI Application - Main Entry Point"""
import sys
import os
from typing import Dict, Tuple, List
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QDesktopWidget, QLabel, QVBoxLayout, QFrame, QScrollArea, QPushButton
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QPainter, QPainterPath, QColor, QIcon, QPixmap
from PyQt5.QtSvg import QSvgWidget, QSvgRenderer

from pin_button import PinButton
from esp32_pin_data import ESP32PinData
from layout_config import LayoutConfig
from oval_tag_label import OvalTagLabel


class PinoutApp(QWidget):
    """Main application window for ESP32 pinout visualization."""
    
    def __init__(self):
        super().__init__()
        self.pin_data = ESP32PinData()
        self.config = LayoutConfig()
        self.pin_buttons = {}  # Store pin buttons for highlighting
        self.highlighted_buttons = []  # Track highlighted buttons
        self.arrow_labels = []  # Track arrow indicators
        self.pin_history = []  # History of viewed pins
        self.history_index = -1  # Current position in history
        
        self._load_stylesheet()
        self._init_window()
        self._create_scroll_area()
        self._create_title()
        self._create_svg_widget()
        self._create_navigation_buttons()
        self._create_info_box()
        self._create_legend()
        self._create_pin_buttons()
    
    def _load_stylesheet(self):
        """Load the external stylesheet."""
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        stylesheet_path = os.path.join(base_path, 'styles.qss')
        
        try:
            with open(stylesheet_path, 'r') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Warning: Could not find stylesheet at {stylesheet_path}")
    
    def _create_scroll_area(self):
        """Create the main scroll area for the content."""
        # Create main layout for the window
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Create content widget
        self.content_widget = QWidget()
        self.content_widget.setMinimumSize(self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT)
        
        # Set the content widget to the scroll area
        self.scroll_area.setWidget(self.content_widget)
        main_layout.addWidget(self.scroll_area)
        
    def _init_window(self):
        """Initialize window properties and center it on screen."""
        self.setWindowTitle('Know Your Pins')
        
        # Create a custom microchip icon
        icon_pixmap = self._create_chip_icon()
        self.setWindowIcon(QIcon(icon_pixmap))
        
        self.resize(self.config.WINDOW_WIDTH, self.config.WINDOW_HEIGHT)
        self._center_window()
    
    def _create_chip_icon(self) -> QPixmap:
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
    
    def _center_window(self):
        """Center the window on the screen."""
        frame_geometry = self.frameGeometry()
        screen_center = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())
    
    def _get_svg_path(self) -> str:
        """Get the path to the SVG file, compatible with PyInstaller."""
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, 'esp32_38_pinout.svg')
    
    def _create_svg_widget(self):
        """Create and position the SVG pinout diagram."""
        svg_path = self._get_svg_path()
        self.svg_widget = QSvgWidget(svg_path, self.content_widget)
        
        img_start, _, img_top, _ = self.config.get_image_position()
        img_width, img_height = self.config.get_image_dimensions()
        
        self.svg_widget.setGeometry(img_start, img_top, img_width, img_height)
    
    def _create_navigation_buttons(self):
        """Create back and forward navigation buttons."""
        y_position = self.config.TITLE_HEIGHT + self.config.TITLE_MARGIN + self.config.INFO_BOX_MARGIN - 45
        
        # Back button
        self.back_button = QPushButton('◄ Back', self.content_widget)
        self.back_button.setGeometry(
            self.config.INFO_BOX_MARGIN,
            y_position,
            80,
            35
        )
        self.back_button.setCursor(Qt.PointingHandCursor)
        self.back_button.clicked.connect(self._navigate_back)
        self.back_button.setEnabled(False)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: 2px solid #2980b9;
                border-radius: 6px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 10pt;
                font-weight: bold;
                padding: 5px;
            }
            QPushButton:hover:enabled {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                border-color: #95a5a6;
                color: #7f8c8d;
            }
        """)
        
        # Forward button
        self.forward_button = QPushButton('Forward ►', self.content_widget)
        self.forward_button.setGeometry(
            self.config.INFO_BOX_MARGIN + 90,
            y_position,
            90,
            35
        )
        self.forward_button.setCursor(Qt.PointingHandCursor)
        self.forward_button.clicked.connect(self._navigate_forward)
        self.forward_button.setEnabled(False)
        self.forward_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: 2px solid #2980b9;
                border-radius: 6px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 10pt;
                font-weight: bold;
                padding: 5px;
            }
            QPushButton:hover:enabled {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
                border-color: #95a5a6;
                color: #7f8c8d;
            }
        """)
    
    def _create_info_box(self):
        """Create the information display area."""
        y_position = self.config.TITLE_HEIGHT + self.config.TITLE_MARGIN + self.config.INFO_BOX_MARGIN
        
        # Create scroll area
        self.info_scroll = QScrollArea(self.content_widget)
        self.info_scroll.setObjectName('info_scroll')
        self.info_scroll.setGeometry(
            self.config.INFO_BOX_MARGIN,
            y_position,
            self.config.INFO_BOX_WIDTH,
            self.config.INFO_BOX_HEIGHT
        )
        self.info_scroll.setWidgetResizable(True)
        
        # Create content widget
        self.info_widget = QWidget()
        self.info_layout = QVBoxLayout(self.info_widget)
        self.info_layout.setAlignment(Qt.AlignTop)
        self.info_layout.setContentsMargins(15, 15, 15, 15)
        self.info_layout.setSpacing(10)
        
        # Placeholder label
        self.placeholder_label = QLabel("Click on a pin to view information...")
        self.placeholder_label.setObjectName('placeholder_label')
        self.info_layout.addWidget(self.placeholder_label)
        
        self.info_scroll.setWidget(self.info_widget)

    def _create_title(self):
        """Create the application title."""
        title = QLabel('ESP32 DevKit V1 - 38 Pin Pinout Reference', self.content_widget)
        title.setObjectName('title')
        title.setGeometry(
            0,
            self.config.TITLE_MARGIN,
            self.config.WINDOW_WIDTH,
            self.config.TITLE_HEIGHT
        )
        title.setAlignment(Qt.AlignCenter)
    
    def _create_legend(self):
        """Create a color legend for pin categories."""
        legend_frame = QFrame(self.content_widget)
        legend_frame.setObjectName('legend_frame')
        
        x_position = self.config.WINDOW_WIDTH - self.config.LEGEND_WIDTH - self.config.LEGEND_MARGIN
        y_position = self.config.TITLE_HEIGHT + self.config.TITLE_MARGIN + self.config.LEGEND_MARGIN
        
        legend_frame.setGeometry(
            x_position,
            y_position,
            self.config.LEGEND_WIDTH,
            self.config.LEGEND_HEIGHT
        )
        
        # Create legend title
        legend_title = QLabel('Pin Categories', legend_frame)
        legend_title.setObjectName('legend_title')
        legend_title.setGeometry(5, 5, self.config.LEGEND_WIDTH - 10, 55)
        legend_title.setAlignment(Qt.AlignCenter)
        
        # Legend items with colors
        self.categories_data = [
            ('I2C Pins', '#0080FF', 'i2c'),
            ('ADC Pins', '#00C800', 'adc'),
            ('SPI Pins', "#C0C0C0", 'spi'),
            ('PWM Pins', '#FFA500', 'pwm'),
            ('Power Pins', "#9662FE", 'power'),
            ('Input Only Pins', "#F700FF", 'Input only'),
            ('In/Out Pins', "#00C3FF", 'Input/Output'),
            ('Other GPIO', '#FF0000', 'default')
        ]
        
        y_offset = 55
        for category_name, color, category_key in self.categories_data:
            # Clickable category button
            category_btn = QPushButton('', legend_frame)
            category_btn.setProperty('class', 'category_btn')
            category_btn.setGeometry(10, y_offset+10, self.config.LEGEND_WIDTH - 20, 30)
            category_btn.setCursor(Qt.PointingHandCursor)
            category_btn.clicked.connect(lambda checked, key=category_key, name=category_name: self.show_category_pins(key, name))
            
            # Color box inside button
            color_box = QLabel('', category_btn)
            color_box.setGeometry(5, 3, 25, 25)
            color_box.setStyleSheet(f"""
                QLabel {{
                    background-color: {color};
                    border: 2px solid #2c3e50;
                    border-radius: 4px;
                }}
            """)
            
            # Category label inside button
            label = QLabel(category_name, category_btn)
            label.setProperty('class', 'category_label')
            label.setGeometry(38, -6, self.config.LEGEND_WIDTH - 60, 40)
            label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            
            y_offset += 35
    
    def _get_pin_positions(self) -> Dict[str, Tuple[int, int, int, int]]:
        """Calculate pin button positions based on image layout."""
        img_start, img_end, _, img_bottom = self.config.get_image_position()
        
        pin_right = img_end - 35
        pin_left = img_start
        step = self.config.PIN_VERTICAL_STEP
        gpio0_y = img_bottom - 182
        w = self.config.PIN_BUTTON_WIDTH
        h = self.config.PIN_BUTTON_HEIGHT
        
        return {
            'GPIO0': (pin_right, gpio0_y, w, h),
            'GPIO1': (pin_right, gpio0_y - step * 10 - 4, w, h),
            'GPIO2': (pin_right, gpio0_y + step + 1, w, h),
            'GPIO3': (pin_right, gpio0_y - step * 9 - 3, w, h),
            'GPIO4': (pin_right, gpio0_y - step, w, h),
            'GPIO5': (pin_right, gpio0_y - step * 4 - 1, w, h),
            'GPIO6': (pin_right, gpio0_y + step * 5 + 2, w, h),
            'GPIO7': (pin_right, gpio0_y + step * 4 + 2, w, h),
            'GPIO8': (pin_right, gpio0_y + step * 3 + 2, w, h),
            'GPIO9': (pin_left, gpio0_y + step * 2 + 1, w, h),
            'GPIO10': (pin_left, gpio0_y + step * 3 + 2, w, h),
            'GPIO11': (pin_left, gpio0_y + step * 4 + 2, w, h),
            'GPIO12': (pin_left, gpio0_y - step, w, h),
            'GPIO13': (pin_left, gpio0_y + step + 1, w, h),
            'GPIO14': (pin_left, gpio0_y - step * 2, w, h),
            'GPIO15': (pin_right, gpio0_y + step * 2 + 1, w, h),
            'GPIO16': (pin_right, gpio0_y - step * 2, w, h),
            'GPIO17': (pin_right, gpio0_y - step * 3 - 1, w, h),
            'GPIO18': (pin_right, gpio0_y - step * 5 - 2, w, h),
            'GPIO19': (pin_right, gpio0_y - step * 6 - 2, w, h),
            'GPIO21': (pin_right, gpio0_y - step * 8 - 3, w, h),
            'GPIO22': (pin_right, gpio0_y - step * 11 - 4, w, h),
            'GPIO23': (pin_right, gpio0_y - step * 12 - 4, w, h),
            'GPIO25': (pin_left, gpio0_y - step * 5 - 2, w, h),
            'GPIO26': (pin_left, gpio0_y - step * 4 - 1, w, h),
            'GPIO27': (pin_left, gpio0_y - step * 3 - 1, w, h),
            'GPIO32': (pin_left, gpio0_y - step * 7 - 2, w, h),
            'GPIO33': (pin_left, gpio0_y - step * 6 - 2, w, h),
            'GPIO34': (pin_left, gpio0_y - step * 9 - 3, w, h),
            'GPIO35': (pin_left, gpio0_y - step * 8 - 3, w, h),
            'GPIO36': (pin_left, gpio0_y - step * 11 - 4, w, h),
            'GPIO39': (pin_left, gpio0_y - step * 10 - 4, w, h),
            'EN': (pin_left, gpio0_y - step * 12 - 4, w, h),
            'VIN': (pin_left, gpio0_y + step * 5 + 2, w, h),
            'GND1': (pin_right, gpio0_y - step * 7 - 2, w, h),
            'GND2': (pin_right, gpio0_y - step * 13 - 5, w, h),
            'GND3': (pin_left, gpio0_y, w, h),
            '3V3': (pin_left, gpio0_y - step * 13 - 5, w, h),
        }
    
    def _create_pin_buttons(self):
        """Create interactive buttons for all pins."""
        pin_positions = self._get_pin_positions()
        
        for pin_id, (x, y, w, h) in pin_positions.items():
            category = self.pin_data.get_pin_category(pin_id)
            btn = PinButton(pin_id, x, y, w, h, category, self.content_widget)
            btn.clicked.connect(lambda checked, p=pin_id: self.show_pin_info(p))
            self.pin_buttons[pin_id] = btn  # Store for later access
    
    def show_pin_info(self, pin_id: str, from_navigation: bool = False):
        """Display information about the selected pin using Qt widgets."""
        # Clear any category highlights first
        self._clear_highlights()
        
        # Add to history if not navigating
        if not from_navigation:
            # Remove any forward history if we're not at the end
            if self.history_index < len(self.pin_history) - 1:
                self.pin_history = self.pin_history[:self.history_index + 1]
            
            # Add new pin to history (type, data)
            self.pin_history.append(('pin', pin_id))
            self.history_index = len(self.pin_history) - 1
            
            # Update button states
            self._update_navigation_buttons()
        
        pin = self.pin_data.pins.get(pin_id)
        if pin:
            # Clear existing widgets
            while self.info_layout.count():
                child = self.info_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
            
            # Pin name header
            name_label = QLabel(pin.name)
            name_label.setProperty('class', 'pin_name')
            self.info_layout.addWidget(name_label)
            
            # Type header
            type_header = QLabel("Type:")
            type_header.setProperty('class', 'section_header')
            self.info_layout.addWidget(type_header)
            
            # Type tag
            type_tag = OvalTagLabel(pin.pin_type, '#16a085')
            self.info_layout.addWidget(type_tag)
            
            # Functions header
            func_header = QLabel("Functions:")
            func_header.setProperty('class', 'section_header')
            self.info_layout.addWidget(func_header)
            
            # Function tags with proper oval shapes
            colors = ['#3498db', '#9b59b6', '#e74c3c', '#f39c12', '#1abc9c', '#34495e']
            for i, func in enumerate(pin.functions):
                tag = OvalTagLabel(func, colors[i % len(colors)])
                self.info_layout.addWidget(tag)
            
            # Note if exists
            if pin.note:
                note_label = QLabel(f"⚠ Note: {pin.note}")
                note_label.setWordWrap(True)
                note_label.setProperty('class', 'note_label')
                self.info_layout.addWidget(note_label)
            
            self.info_layout.addStretch()
    
    def show_category_pins(self, category_key: str, category_name: str, from_navigation: bool = False):
        """Display all pins in a category and highlight them."""
        # Clear previous highlights
        self._clear_highlights()
        
        # Add to history if not navigating
        if not from_navigation:
            # Remove any forward history if we're not at the end
            if self.history_index < len(self.pin_history) - 1:
                self.pin_history = self.pin_history[:self.history_index + 1]
            
            # Add new category to history (type, data)
            self.pin_history.append(('category', (category_key, category_name)))
            self.history_index = len(self.pin_history) - 1
            
            # Update button states
            self._update_navigation_buttons()
        
        # Get pins for this category
        if category_key == 'i2c':
            pins = self.pin_data.i2c_pins
        elif category_key == 'adc':
            pins = self.pin_data.adc_pins
        elif category_key == 'spi':
            pins = self.pin_data.spi_pins
        elif category_key == 'pwm':
            pins = self.pin_data.pwm_pins
        elif category_key == 'power':
            pins = self.pin_data.power_pins
        elif category_key == 'Input only':
            pins = self.pin_data.input_only_pins
        elif category_key == 'Input/Output':
            pins = self.pin_data.in_out_pins
        else:  # default - all other GPIO
            all_categorized = set(self.pin_data.i2c_pins + self.pin_data.adc_pins + 
                                 self.pin_data.spi_pins + self.pin_data.pwm_pins + self.pin_data.power_pins + 
                                 self.pin_data.input_only_pins + self.pin_data.in_out_pins)
            pins = [pin_id for pin_id in self.pin_buttons.keys() 
                   if pin_id not in all_categorized and pin_id.startswith('GPIO')]
        
        # Highlight pins on diagram
        for pin_id in pins:
            if pin_id in self.pin_buttons:
                btn = self.pin_buttons[pin_id]
                self._highlight_button(btn)
                self.highlighted_buttons.append(btn)
        
        # Display in info box
        self._display_category_info(category_name, pins)
    
    def _highlight_button(self, button):
        """Apply highlight effect to a pin button."""
        # Store original stylesheet if not already stored
        if not hasattr(button, 'original_style'):
            button.original_style = button.styleSheet()
        
        # Apply highlight
        category = self.pin_data.get_pin_category(button.pin_id)
        from pin_button import PinButton
        hover_color = PinButton.HOVER_COLORS.get(category, PinButton.HOVER_COLORS['default'])
        
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {hover_color};
                border: 3px solid #2c3e50;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
                border: 3px solid #e74c3c;
                border-radius: 6px;
            }}
        """)
        
        # Add arrow indicator
        arrow = QLabel('►' if button.x() < self.content_widget.width() / 2 else '◄', self.content_widget)
        arrow.setProperty('class', 'arrow')
        arrow_x = button.x() - (int(button.width()/2) + 5) if button.x() < self.content_widget.width() / 2 else button.x() + button.width() + 5
        arrow.setGeometry(arrow_x, button.y() + 2, 25, button.height() - 4)
        
        # Extract RGB from hover_color (rgba format)
        # Parse rgba(R, G, B, A) to get RGB values
        rgb_values = hover_color.replace('rgba(', '').replace(')', '').split(',')
        arrow_color = f"rgb({rgb_values[0].strip()}, {rgb_values[1].strip()}, {rgb_values[2].strip()})"
        
        arrow.setStyleSheet(f"QLabel.arrow {{ color: {arrow_color}; }}")
        arrow.show()
        self.arrow_labels.append(arrow)
    
    def _clear_highlights(self):
        """Remove highlights from all previously highlighted buttons."""
        for btn in self.highlighted_buttons:
            if hasattr(btn, 'original_style'):
                btn.setStyleSheet(btn.original_style)
        self.highlighted_buttons.clear()
        
        # Remove arrow labels
        for arrow in self.arrow_labels:
            arrow.deleteLater()
        self.arrow_labels.clear()
    
    def _display_category_info(self, category_name: str, pins: List[str]):
        """Display category information in the info box."""
        # Clear existing widgets
        while self.info_layout.count():
            child = self.info_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Category header
        header = QLabel(f"{category_name} ({len(pins)} pins)")
        header.setProperty('class', 'category_header')
        self.info_layout.addWidget(header)
        
        # Pins list header
        pins_header = QLabel("Pins in this category:")
        pins_header.setProperty('class', 'section_header')
        self.info_layout.addWidget(pins_header)
        
        # Display each pin as a clickable tag
        colors = ['#3498db', '#9b59b6', '#e74c3c', '#f39c12', '#1abc9c', '#34495e']
        for i, pin_id in enumerate(sorted(pins)):
            pin_info = self.pin_data.pins.get(pin_id)
            if pin_info:
                # Create clickable pin tag
                pin_widget = QWidget()
                pin_layout = QVBoxLayout(pin_widget)
                pin_layout.setContentsMargins(0, 0, 0, 0)
                
                pin_btn = QPushButton(pin_info.name)
                pin_btn.setCursor(Qt.PointingHandCursor)
                pin_btn.clicked.connect(lambda checked, p=pin_id: self.show_pin_info(p))
                
                color = colors[i % len(colors)]
                pin_btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {color};
                        color: white;
                        font-family: 'Segoe UI', Arial, sans-serif;
                        font-size: 11pt;
                        font-weight: 600;
                        border: 2px solid {color};
                        border-radius: 20px;
                        padding: 10px 20px;
                        text-align: center;
                        min-height: 20px;
                    }}
                    QPushButton:hover {{
                        background-color: {color};
                        border: 2px solid #2c3e50;
                    }}
                """)
                
                pin_layout.addWidget(pin_btn)
                self.info_layout.addWidget(pin_widget)
        
        self.info_layout.addStretch()
    
    def _navigate_back(self):
        """Navigate to the previous pin in history."""
        if self.history_index > 0:
            self.history_index -= 1
            view_type, data = self.pin_history[self.history_index]
            
            if view_type == 'pin':
                self.show_pin_info(data, from_navigation=True)
            elif view_type == 'category':
                category_key, category_name = data
                self.show_category_pins(category_key, category_name, from_navigation=True)
            
            self._update_navigation_buttons()
    
    def _navigate_forward(self):
        """Navigate to the next pin in history."""
        if self.history_index < len(self.pin_history) - 1:
            self.history_index += 1
            view_type, data = self.pin_history[self.history_index]
            
            if view_type == 'pin':
                self.show_pin_info(data, from_navigation=True)
            elif view_type == 'category':
                category_key, category_name = data
                self.show_category_pins(category_key, category_name, from_navigation=True)
            
            self._update_navigation_buttons()
    
    def _update_navigation_buttons(self):
        """Update the enabled state of navigation buttons."""
        self.back_button.setEnabled(self.history_index > 0)
        self.forward_button.setEnabled(self.history_index < len(self.pin_history) - 1)
    
    def keyPressEvent(self, event):
        """Handle keyboard shortcuts for navigation."""
        # Ctrl+Shift+Z for forward navigation
        if event.modifiers() == (Qt.ControlModifier | Qt.ShiftModifier) and event.key() == Qt.Key_Z:
            self._navigate_forward()
        # Ctrl+Z for back navigation
        elif event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_Z:
            self._navigate_back()
        else:
            super().keyPressEvent(event)
    
    def mousePressEvent(self, event):
        """Clear highlights when clicking anywhere on the window."""
        # Only clear if there are highlights active
        if self.highlighted_buttons:
            self._clear_highlights()
        super().mousePressEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PinoutApp()
    window.show()
    sys.exit(app.exec_())
    app = QApplication(sys.argv)
    window = PinoutApp()
    window.show()
    sys.exit(app.exec_())
