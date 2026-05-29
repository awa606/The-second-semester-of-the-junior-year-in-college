#pragma once
#include "variables.hpp"

#define WS2812_LED_NUM          40       // 改成你的灯珠数量
#define WS2812_0                30
#define WS2812_1                60
#define WS2812_RESET_SLOTS      250
#define WS2812_BUF_LEN          (WS2812_LED_NUM * 24 + WS2812_RESET_SLOTS)

extern volatile uint8_t ws2812_busy;

uint8_t WS2812_SetAllColorBrightness(uint8_t r, uint8_t g, uint8_t b, uint8_t brightness);

