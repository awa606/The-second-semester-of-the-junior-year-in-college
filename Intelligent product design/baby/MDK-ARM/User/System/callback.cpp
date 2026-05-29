#include "callback.hpp"
#include "variables.hpp"

/**
 * @brief PWM DMA 发送完成回调
 *
 * 这个函数不用你手动调用，HAL 会在 DMA 发送完成后自动调用。
 */
void HAL_TIM_PWM_PulseFinishedCallback(TIM_HandleTypeDef *htim)
{
    if (htim->Instance == TIM3)
    {
        HAL_TIM_PWM_Stop_DMA(&htim3, TIM_CHANNEL_1);
        ws2812_busy = 0;
    }
}

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
    if (huart->Instance == USART1)
    {
        
    }
}
