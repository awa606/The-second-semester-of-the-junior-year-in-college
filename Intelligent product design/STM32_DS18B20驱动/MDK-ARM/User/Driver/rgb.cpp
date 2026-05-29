#include "rgb.hpp"
#include "main.h"

static uint16_t ws2812_pwm_buf[WS2812_BUF_LEN];
volatile uint8_t ws2812_busy = 0;

static uint8_t WS2812_ApplyBrightness(uint8_t value, uint8_t brightness)
{
    return (uint8_t)(((uint16_t)value * brightness) / 255);
}


/**
 * @brief 设置整条 WS2812 灯带的颜色和亮度
 *
 * @param r 红色分量，0~255
 * @param g 绿色分量，0~255
 * @param b 蓝色分量，0~255
 * @param brightness 总亮度，0~255
 *
 * @return 1：发送成功；0：上一次 DMA 还没发完
 */
uint8_t WS2812_SetAllColorBrightness(uint8_t r, uint8_t g, uint8_t b, uint8_t brightness)
{
    if (ws2812_busy)
    {
        return 0;
    }

    uint8_t r_out = WS2812_ApplyBrightness(r, brightness);
    uint8_t g_out = WS2812_ApplyBrightness(g, brightness);
    uint8_t b_out = WS2812_ApplyBrightness(b, brightness);

    uint32_t index = 0;

    for (uint16_t led = 0; led < WS2812_LED_NUM; led++)
    {
        /*
         * WS2812 数据顺序是 GRB，不是 RGB
         */
        uint8_t color[3] = {g_out, r_out, b_out};

        for (uint8_t c = 0; c < 3; c++)
        {
            for (int8_t bit = 7; bit >= 0; bit--)
            {
                if (color[c] & (1 << bit))
                {
                    ws2812_pwm_buf[index++] = WS2812_1;
                }
                else
                {
                    ws2812_pwm_buf[index++] = WS2812_0;
                }
            }
        }
    }

    /*
     * Reset / Latch 低电平
     */
    for (uint16_t i = 0; i < WS2812_RESET_SLOTS; i++)
    {
        ws2812_pwm_buf[index++] = 0;
    }

    ws2812_busy = 1;

    HAL_TIM_PWM_Start_DMA(
        &htim3,
        TIM_CHANNEL_1,
        (uint32_t *)ws2812_pwm_buf,
        WS2812_BUF_LEN
    );

    return 1;
}

/**
 * @brief 关闭整条灯带
 */
void WS2812_Off(void)
{
    WS2812_SetAllColorBrightness(0, 0, 0, 0);
}

