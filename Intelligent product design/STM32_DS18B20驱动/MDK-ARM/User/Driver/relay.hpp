#pragma once

/**
  ******************************************************************************
  * @file    relay.hpp
  * @brief   继电器控制模块，支持水泵1/2通断
  * @note    通过 BSP GPIO 接口控制继电器开关的高低电平来控制水泵的开关
  ******************************************************************************
  */

#include "main.h"
#include "bsp_gpio.hpp"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief 继电器控制电平定义
 * @note  1 = 高电平有效，0 = 低电平有效
 *        根据实际继电器模块触发方式修改
 */
#define RELAY_ACTIVE_HIGH   (1U)

/**
 * @brief 水泵编号定义
 */
typedef enum
{
    RELAY_PUMP_1 = 0,   /*!< 水泵1-PE0 */
    RELAY_PUMP_2 = 1,   /*!< 水泵2-PB9 */
    RELAY_HEATING_ROD = 2, /*!< 加热棒 */
    RELAY_PUMP_NUM
} RelayPump_t;

/**
 * @brief 水泵状态
 */
typedef enum
{
    RELAY_STATE_OFF = 0, /*!< 关闭 */
    RELAY_STATE_ON  = 1  /*!< 开启 */
} RelayState_t;

/**
 * @brief  继电器控制初始化，统一处于关闭状态
 * @retval 无
 */
void relayInit(void);

/**
 * @brief  打开指定水泵
 * @param  pump 水泵编号 @ref RelayPump_t
 * @retval 无
 */
void relayPumpOn(RelayPump_t pump);

/**
 * @brief  关闭指定水泵
 * @param  pump 水泵编号 @ref RelayPump_t
 * @retval 无
 */
void relayPumpOff(RelayPump_t pump);


/**
 * @brief  设置指定水泵状态
 * @param  pump  水泵编号
 * @param  state 目标状态 @ref RelayState_t
 * @retval 无
 */
void relayPumpSet(RelayPump_t pump, RelayState_t state);


/**
 * @brief  打开所有水泵
 */
void relayPumpAllOn(void);

/**
 * @brief  关闭所有水泵
 */
void relayPumpAllOff(void);

/**
 * @brief  打开加热棒
 * @retval 无
 */
void relayHeatingRodOn(void);

/**
 * @brief  关闭加热棒
 * @retval 无
 */
void relayHeatingRodOff(void);

/**
 * @brief  设置加热棒状态
 * @param  state 目标状态 @ref RelayState_t
 * @retval 无
 */
void relayHeatingRodSet(RelayState_t state);

#ifdef __cplusplus
}
#endif
