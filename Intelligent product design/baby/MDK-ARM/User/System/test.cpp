#include "variables.hpp"
#include "test.hpp"

void test_ws2812()
{
    WS2812_SetAllColorBrightness(255, 140, 20, 10);
}

void test_moter()
{
//    motor.turnaround(0.5f);
    motor.yaonai();
}
