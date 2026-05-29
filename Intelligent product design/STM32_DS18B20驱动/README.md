# STM32_DS18B20 driver

This project is based on the `baby` STM32F407VETx CubeMX/MDK-ARM project and ports the DS18B20 timing from the DS18B20 v3.0 STM32 example to the STM32F4 HAL style used here.

## Wiring

- DS18B20 VDD: 3.3 V
- DS18B20 GND: GND
- DS18B20 DQ: PA0 (`DS18B20_DQ_Pin`)
- Add a 4.7 kOhm pull-up resistor between DQ and 3.3 V.

## Added files

- `MDK-ARM/User/Driver/ds18b20.hpp`
- `MDK-ARM/User/Driver/ds18b20.cpp`
- `Core/Inc/main.h`: PA0 pin macro
- `Core/Src/gpio.c`: PA0 open-drain output with pull-up
- `MDK-ARM/User/System/test.cpp`: `test_ds18b20()` reads once per second

## Use

Open `MDK-ARM/STM32_DS18B20.uvprojx` in Keil. The main loop calls `test_ds18b20()`, which updates:

- `g_ds18b20Online`: `1` when the sensor read succeeds
- `g_ds18b20TemperatureDeciC`: temperature in 0.1 Celsius units, for example `253` means `25.3 C`

The driver also exposes `DS18B20_GetTempDeciC()` and `DS18B20_GetTempC()` for direct reads.
