#pragma once

/**
  ******************************************************************************
  * @file    bsp_gpio.hpp
  * @brief   BSP 层 GPIO 驱动接口封装
  * @note    对 HAL_GPIO 相关操作进行统一封装，便于上层业务调用
  ******************************************************************************
  */

#include "main.h"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief  将指定 GPIO 引脚置为高电平
 * @param  GPIOx     GPIO 端口 (GPIOA ~ GPIOK)
 * @param  GPIO_Pin  GPIO 引脚 (GPIO_PIN_0 ~ GPIO_PIN_15)
 * @retval 无
 */
void bspGpioHigh(GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin);

/**
 * @brief  将指定 GPIO 引脚置为低电平
 * @param  GPIOx     GPIO 端口
 * @param  GPIO_Pin  GPIO 引脚
 * @retval 无
 */
void bspGpioLow(GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin);

/**
 * @brief  翻转指定 GPIO 引脚电平
 * @param  GPIOx     GPIO 端口
 * @param  GPIO_Pin  GPIO 引脚
 * @retval 无
 */
void bspGpioToggle(GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin);

/**
 * @brief  写入指定 GPIO 引脚电平
 * @param  GPIOx      GPIO 端口
 * @param  GPIO_Pin   GPIO 引脚
 * @param  PinState   电平状态 (GPIO_PIN_RESET / GPIO_PIN_SET)
 * @retval 无
 */
void bspGpioWrite(GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin, GPIO_PinState PinState);

/**
 * @brief  读取指定 GPIO 引脚输入电平
 * @param  GPIOx     GPIO 端口
 * @param  GPIO_Pin  GPIO 引脚
 * @retval GPIO_PIN_RESET 低电平 / GPIO_PIN_SET 高电平
 */
GPIO_PinState bspGpioRead(GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin);

/**
 * @brief  读取指定 GPIO 引脚是否为高电平
 * @param  GPIOx     GPIO 端口
 * @param  GPIO_Pin  GPIO 引脚
 * @retval 1 高电平 / 0 低电平
 */
uint8_t bspGpioIsHigh(GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin);

/**
 * @brief  读取指定 GPIO 引脚是否为低电平
 * @param  GPIOx     GPIO 端口
 * @param  GPIO_Pin  GPIO 引脚
 * @retval 1 低电平 / 0 高电平
 */
uint8_t bspGpioIsLow(GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin);

/**
 * @brief  锁定指定 GPIO 引脚配置，直到下次复位
 * @param  GPIOx     GPIO 端口
 * @param  GPIO_Pin  GPIO 引脚
 * @retval HAL_OK / HAL_ERROR
 */
HAL_StatusTypeDef bspGpioLock(GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin);

#ifdef __cplusplus
}
#endif


