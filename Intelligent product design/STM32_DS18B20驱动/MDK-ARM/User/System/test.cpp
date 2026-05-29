#include "variables.hpp"
#include "test.hpp"

volatile int16_t g_ds18b20TemperatureDeciC = DS18B20_TEMP_INVALID;
volatile uint8_t g_ds18b20Online = 0U;

void test_ws2812()
{
    WS2812_SetAllColorBrightness(255, 140, 20, 10);
}

void test_moter()
{
//    motor.turnaround(0.5f);
    motor.yaonai();
}

void test_ds18b20()
{
    static uint32_t lastTick = 0U;
    const uint32_t now = HAL_GetTick();

    if ((lastTick != 0U) && ((now - lastTick) < 1000U))
    {
        return;
    }

    lastTick = now;

    int16_t temperature = DS18B20_TEMP_INVALID;
    if (DS18B20_GetTempDeciC(&temperature) == DS18B20_OK)
    {
        g_ds18b20TemperatureDeciC = temperature;
        g_ds18b20Online = 1U;
    }
    else
    {
        g_ds18b20Online = 0U;
    }
}
