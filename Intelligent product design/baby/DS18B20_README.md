# baby DS18B20 temperature sensing

## Wiring

- DS18B20 VCC/red wire -> 3.3V
- DS18B20 GND/black wire -> GND
- DS18B20 DQ/yellow wire -> PA0
- Add a 4.7k or 10k pull-up resistor between DQ and 3.3V.

## Runtime Flow

1. Initialize GPIO, including PA0 as open-drain output with pull-up.
2. Initialize the DS18B20 delay timer and sensor.
3. Read temperature once per second.
4. Print `Temp: xx.x C` or `DS18B20 Error` on USART1 at 115200 baud.
5. Later, the temperature value can be used for HeatingRod control, for example heating below 40.0 C and stopping above 45.0 C. Closed-loop heating is intentionally not enabled yet to avoid unintended heater action during serial verification.
