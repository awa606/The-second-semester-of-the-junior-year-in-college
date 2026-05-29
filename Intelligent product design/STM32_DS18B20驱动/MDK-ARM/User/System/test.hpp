#pragma once
#include "variables.hpp"

void test_ws2812();
void test_moter();
void test_ds18b20();

extern volatile int16_t g_ds18b20TemperatureDeciC;
extern volatile uint8_t g_ds18b20Online;

