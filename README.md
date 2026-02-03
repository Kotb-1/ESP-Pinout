# ESP32 Pinout GUI - Know Your Pins

An interactive GUI application for exploring and understanding ESP32 microcontroller pinout configurations. This tool provides a visual, user-friendly interface to learn about pin functions, capabilities, and boot restrictions.

## Features

- **Interactive Pin Map**: Click on any pin to view detailed information
- **Visual Color-Coded Legend**: Easy identification of pin types (I2C, SPI, ADC, PWM, Power, Input/Output)
- **Comprehensive Pin Details**: 
  - Pin functions and alternate modes
  - Input/Output capabilities
  - Boot-time restrictions and warnings
- **Pin Categorization**: Quick filtering by function type:
  - I2C pins (GPIO21, GPIO22)
  - SPI pins (HSPI, VSPI)
  - ADC-capable pins
  - PWM-capable pins
  - Power pins (3V3, VIN, GND)
  - Input-only vs Input/Output pins
- **Navigation History**: Back/Forward buttons to track your pin exploration
- **SVG-Based Visualization**: Crisp, scalable ESP32 board diagram

## Screenshots

The application displays an ESP32 board diagram with clickable pins. Hovering over pins highlights them, and clicking reveals detailed information about each pin's capabilities and restrictions.

## Requirements

- Python 3.7+
- PyQt5

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd "ESP Pinout"
```

2. Install required dependencies:
```bash
pip install PyQt5
```

## Usage

### Running from Source

```bash
python Pinout_GUI.py
```

### Building Executable

The project includes PyInstaller spec files for creating standalone executables:

```bash
pyinstaller Pinout_GUI.spec
```

The executable will be created in the `dist/` folder.

## Project Structure

```
ESP Pinout/
├── Pinout_GUI.py          # Main application entry point
├── esp32_pin_data.py      # ESP32 pin definitions and data
├── pin.py                 # Pin data model
├── pin_button.py          # Custom pin button widget
├── layout_config.py       # Layout and positioning configuration
├── oval_tag_label.py      # Custom oval label widget for categories
├── create_icon.py         # Icon generation utility
├── styles.qss             # Qt stylesheet for UI theming
├── esp32_38_pinout.svg    # ESP32 board diagram (SVG)
├── Pinout_GUI.spec        # PyInstaller build configuration
└── README.md              # This file
```

## Key Components

### PinoutApp (Pinout_GUI.py)
Main application window managing the GUI layout, pin interactions, and information display.

### ESP32PinData (esp32_pin_data.py)
Central repository of all ESP32 pin definitions, including:
- Pin functions (UART, I2C, SPI, ADC, PWM)
- Pin types (Input/Output, Input-only, Internal)
- Boot restrictions and warnings
- Pin categorization for easy filtering

### PinButton (pin_button.py)
Custom clickable button widget for each pin with:
- Category-based color coding
- Hover effects
- Click handlers for information display

### Pin (pin.py)
Data model representing individual pin properties and capabilities.

## Pin Categories

- **I2C**: GPIO21 (SDA), GPIO22 (SCL)
- **SPI**: VSPI and HSPI pins (MISO, MOSI, SCK, SS)
- **ADC**: Analog-to-Digital Converter capable pins (ADC1 and ADC2 channels)
- **PWM**: Pulse Width Modulation capable pins
- **Power**: Power supply pins (3V3, VIN, GND)
- **Input Only**: Pins that can only read signals (GPIO34-39)
- **Input/Output**: Bidirectional GPIO pins
- **Internal**: Flash-connected pins (DO NOT USE)

## Important Notes

⚠️ **Boot Restrictions**:
- GPIO0: Must be HIGH during boot (unless flashing)
- GPIO2: Must be LOW to enter boot mode
- GPIO5: Must be HIGH during boot
- GPIO12: Must be LOW during boot
- GPIO15: Must be LOW during boot

⚠️ **Internal Pins**: GPIO6-11 are connected to integrated SPI flash and should NEVER be used - doing so will cause boot failure.

⚠️ **WiFi Limitations**: When WiFi is active, ADC2 pins (GPIO12-15, GPIO25-27) cannot be used for analog reading.

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## License

This project is provided as-is for educational and development purposes.

## Author

Created for ESP32 developers and hobbyists who want to understand their microcontroller's pin capabilities at a glance.

## Acknowledgments

- ESP32 technical documentation and pinout specifications
- PyQt5 framework for the GUI implementation
