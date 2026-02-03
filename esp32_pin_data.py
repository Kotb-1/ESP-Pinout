"""ESP32 pin definitions and categorization."""
from typing import Dict
from pin import Pin


class ESP32PinData:
    """Manages ESP32 pin definitions and categorization."""
    
    def __init__(self):
        self.pins: Dict[str, Pin] = self._initialize_pins()
        self.i2c_pins = ['GPIO21', 'GPIO22']
        self.adc_pins = ['GPIO32', 'GPIO33', 'GPIO34', 'GPIO35', 'GPIO36', 'GPIO39', 'GPIO25', 'GPIO26', 'GPIO27', 'GPIO12', 'GPIO13', 'GPIO14', 'GPIO15']
        self.spi_pins = ['GPIO18', 'GPIO19', 'GPIO23', 'GPIO5', 'GPIO12', 'GPIO13', 'GPIO14', 'GPIO15']
        self.pwm_pins = ['GPIO0', 'GPIO1', 'GPIO2', 'GPIO3', 'GPIO4', 'GPIO5', 'GPIO12', 'GPIO13', 'GPIO14', 'GPIO15', 'GPIO16', 'GPIO17', 'GPIO18', 'GPIO19', 'GPIO21', 'GPIO22', 'GPIO23', 'GPIO25', 'GPIO26', 'GPIO27', 'GPIO32', 'GPIO33']
        self.power_pins = ['3V3', 'VIN', 'GND1', 'GND2', 'GND3']
        self.input_only_pins = [pin_id for pin_id, pin in self.pins.items() if pin.pin_type == 'Input only']
        self.in_out_pins = [pin_id for pin_id, pin in self.pins.items() if pin.pin_type == 'Input/Output']
    
    def _initialize_pins(self) -> Dict[str, Pin]:
        """Initialize all pin definitions."""
        return {
            'GPIO0': Pin('GPIO0', ['Boot button', 'ADC2 –CH1–', 'PWM'], 'Input/Output', 
                        'Pull-down during boot to flash'),
            'GPIO1': Pin('GPIO1 (TX0)', ['UART0 TX', 'PWM'], 'Input/Output', 
                        'Used for UART logging'),
            'GPIO2': Pin('GPIO2', ['ADC2 –CH2–', 'PWM'], 'Input/Output', 
                        'Must be low to enter boot mode'),
            'GPIO3': Pin('GPIO3 (RX0)', ['UART0 RX', 'PWM'], 'Input/Output', 
                        'Used for UART logging'),
            'GPIO4': Pin('GPIO4', ['ADC2 –CH0–', 'PWM'], 'Input/Output'),
            'GPIO5': Pin('GPIO5', ['VSPI –SS–', 'PWM'], 'Input/Output', 
                        'Must be high during boot'),
            'GPIO6': Pin('GPIO6', ['Integrated SPI Flash SCK'], 'Internal (do not use)', 
                        'Connected to SPI flash; using will cause boot failure'),
            'GPIO7': Pin('GPIO7', ['Integrated SPI Flash SD0'], 'Internal (do not use)', 
                        'Connected to SPI flash; using will cause boot failure'),
            'GPIO8': Pin('GPIO8', ['Integrated SPI Flash SD1'], 'Internal (do not use)', 
                        'Connected to SPI flash; using will cause boot failure'),
            'GPIO9': Pin('GPIO9', ['Integrated SPI Flash SD2'], 'Internal (do not use)', 
                        'Connected to SPI flash; using will cause boot failure'),
            'GPIO10': Pin('GPIO10', ['Integrated SPI Flash SD3'], 'Internal (do not use)', 
                         'Connected to SPI flash; using will cause boot failure'),
            'GPIO11': Pin('GPIO11', ['Integrated SPI Flash CMD'], 'Internal (do not use)', 
                         'Connected to SPI flash; using will cause boot failure'),
            'GPIO12': Pin('GPIO12', ['ADC2 –CH5–', 'HSPI –MISO–', 'PWM'], 'Input only', 
                         'Must be low during boot &  , Only Digital if WiFi is used'),
            'GPIO13': Pin('GPIO13', ['ADC2 –CH4–', 'HSPI –MOSI–', 'PWM'], 'Input/Output', 'Only Digital if WiFi is used'),
            'GPIO14': Pin('GPIO14', ['ADC2 –CH6–', 'HSPI –CLK–', 'PWM'], 'Input/Output', 'Only Digital if WiFi is used'),
            'GPIO15': Pin('GPIO15', ['ADC2 –CH3–', 'HSPI –SS–', 'PWM'], 'Input/Output', 
                         'Must be low during boot &  , Only Digital if WiFi is used'),
            'GPIO16': Pin('GPIO16'     , ['UART2 –RX–', 'PWM']          , 'Input/Output'),
            'GPIO17': Pin('GPIO17'     , ['UART2 –TX–', 'PWM']          , 'Input/Output'),
            'GPIO18': Pin('GPIO18'     , ['VSPI –CLK–', 'PWM']   , 'Input/Output'),
            'GPIO19': Pin('GPIO19'     , ['VSPI –MISO–', 'PWM']         , 'Input/Output'),
            'GPIO21': Pin('GPIO21'     , ['I2C –SDA–', 'PWM']    , 'Input/Output'),
            'GPIO22': Pin('GPIO22'     , ['I2C –SCL–', 'PWM']    , 'Input/Output'),
            'GPIO23': Pin('GPIO23'     , ['VSPI –MOSI–', 'PWM']  , 'Input/Output'),
            'GPIO25': Pin('GPIO25'     , ['DAC1', 'ADC2 –CH8–', 'PWM'], 'Input/Output' , 'Only Digital if WiFi is used'),
            'GPIO26': Pin('GPIO26'     , ['DAC2', 'ADC2 –CH9–', 'PWM'], 'Input/Output' , 'Only Digital if WiFi is used'),
            'GPIO27': Pin('GPIO27'     , ['ADC2 –CH7–', 'PWM']        , 'Input/Output' , 'Only Digital if WiFi is used'),
            'GPIO32': Pin('GPIO32'     , ['ADC1 –CH4–', 'PWM']        , 'Input/Output'),
            'GPIO33': Pin('GPIO33'     , ['ADC1 –CH5–', 'PWM']        , 'Input/Output'),
            'GPIO34': Pin('GPIO34'     , ['ADC1 –CH6–']        , 'Input only')  ,
            'GPIO35': Pin('GPIO35'     , ['ADC1 –CH7–']        , 'Input only')  ,
            'GPIO36': Pin('GPIO36 (VP)', ['ADC1 –CH0–']        , 'Input only')  ,
            'GPIO39': Pin('GPIO39 (VN)', ['ADC1 –CH3–']        , 'Input only')  ,
            'EN': Pin('EN (Enable)'    , ['Reset']             , 'Input'        , 'Active high to enable chip'),
            'VIN': Pin('VIN'           , ['Power']             , 'Power'        , 'Typically 5V input'),
            '3V3': Pin('3.3V'          , ['Power']             , 'Power'        , '3.3V output/input'),
            'GND2': Pin('GND'          , ['Ground']            , 'Power')       ,
            'GND3': Pin('GND'          , ['Ground']            , 'Power')       ,
            'GND1': Pin('GND'          , ['Ground']            , 'Power')       ,
        }
    
    def get_pin_category(self, pin_id: str) -> str:
        """Determine the category of a pin for styling."""
        if pin_id in self.i2c_pins:
            return 'i2c'
        elif pin_id in self.adc_pins:
            return 'adc'
        elif pin_id in self.spi_pins:
            return 'spi'
        elif pin_id in self.pwm_pins:
            return 'pwm'
        elif pin_id in self.power_pins:
            return 'power'
        return 'default'
