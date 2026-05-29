#include "bsp_gpio.hpp"

#ifdef __cplusplus
extern "C" {
#endif

/**
  ******************************************************************************
  * @file    bsp_gpio.cpp
  * @brief   BSP 层 GPIO 驱动实现
  ******************************************************************************
  */

/**
 * @brief  将指定 GPIO 引脚置为高电平
 */
void bspGpioHigh(GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin)
{
    HAL_GPIO_WritePin(GPIOx, GPIO_Pin, GPIO_PIN_SET);
}

/**
 * @brief  将指定 GPIO 引脚置为低电平
 */
void bspGpioLow(GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin)
{
    HAL_GPIO_WritePin(GPIOx, GPIO_Pin, GPIO_PIN_RESET);
}

/**
 * @brief  翻转指定 GPIO 引脚电平
 */
void bspGpioToggle(GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin)
{
    HAL_GPIO_TogglePin(GPIOx, GPIO_Pin);
}

/**
 * @brief  写入指定 GPIO 引脚电平
 */
void bspGpioWrite(GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin, GPIO_PinState PinState)
{
    HAL_GPIO_WritePin(GPIOx, GPIO_Pin, PinState);
}

/**
 * @brief  读取指定 GPIO 引脚输入电平
 */
GPIO_PinState bspGpioRead(GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin)
{
    return HAL_GPIO_ReadPin(GPIOx, GPIO_Pin);
}

/**
 * @brief  判断指定 GPIO 引脚是否为高电平
 */
uint8_t bspGpioIsHigh(GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin)
{
    return (HAL_GPIO_ReadPin(GPIOx, GPIO_Pin) == GPIO_PIN_SET) ? 1U : 0U;
}

/**
 * @brief  判断指定 GPIO 引脚是否为低电平
 */
uint8_t bspGpioIsLow(GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin)
{
    return (HAL_GPIO_ReadPin(GPIOx, GPIO_Pin) == GPIO_PIN_RESET) ? 1U : 0U;
}

/**
 * @brief  锁定指定 GPIO 引脚配置
 */
HAL_StatusTypeDef bspGpioLock(GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin)
{
    return HAL_GPIO_LockPin(GPIOx, GPIO_Pin);
}

#ifdef __cplusplus
}
#endif


