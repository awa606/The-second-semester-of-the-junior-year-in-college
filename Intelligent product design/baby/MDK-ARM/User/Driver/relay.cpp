#include "relay.hpp"

/**
  ******************************************************************************
  * @file    relay.cpp
  * @brief   继电器控制实现，通过高低电平控制水泵1/2和加热棒
  ******************************************************************************
  */

#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief 水泵引脚映射表
 */
typedef struct
{
    GPIO_TypeDef *port;  /*!< GPIO 端口 */
    uint16_t      pin;   /*!< GPIO 引脚 */
} RelayPumpMap_t;

static const RelayPumpMap_t s_pumpMap[RELAY_PUMP_NUM] =
{
    { Pump1_GPIO_Port, Pump1_Pin }, /* RELAY_PUMP_1 */
    { Pump2_GPIO_Port, Pump2_Pin }, /* RELAY_PUMP_2 */
    { HeatingRod_GPIO_Port, HeatingRod_Pin }, /* RELAY_HEATING_ROD */
};

/**
 * @brief 激活水泵的有效电平控制
 */
static inline void relayActive(GPIO_TypeDef *port, uint16_t pin)
{
#if (RELAY_ACTIVE_HIGH == 1U)
    bspGpioHigh(port, pin);
#else
    bspGpioLow(port, pin);
#endif
}

/**
 * @brief 关闭水泵的有效电平控制
 */
static inline void relayInactive(GPIO_TypeDef *port, uint16_t pin)
{
#if (RELAY_ACTIVE_HIGH == 1U)
    bspGpioLow(port, pin);
#else
    bspGpioHigh(port, pin);
#endif
}

/**
 * @brief 继电器控制初始化，统一处于关闭状态
 */
void relayInit(void)
{
    for (uint8_t i = 0; i < (uint8_t)RELAY_PUMP_NUM; i++)
    {
        relayInactive(s_pumpMap[i].port, s_pumpMap[i].pin);
    }
}

/**
 * @brief 打开指定水泵
 */
void relayPumpOn(RelayPump_t pump)
{
    if (pump >= RELAY_PUMP_NUM) return;
    relayActive(s_pumpMap[pump].port, s_pumpMap[pump].pin);
}

/**
 * @brief 关闭指定水泵
 */
void relayPumpOff(RelayPump_t pump)
{
    if (pump >= RELAY_PUMP_NUM) return;
    relayInactive(s_pumpMap[pump].port, s_pumpMap[pump].pin);
}

/**
 * @brief 翻转指定水泵状态
 */
void relayPumpToggle(RelayPump_t pump)
{
    if (pump >= RELAY_PUMP_NUM) return;
    bspGpioToggle(s_pumpMap[pump].port, s_pumpMap[pump].pin);
}

/**
 * @brief 设置指定水泵状态
 */
void relayPumpSet(RelayPump_t pump, RelayState_t state)
{
    if (state == RELAY_STATE_ON)
    {
        relayPumpOn(pump);
    }
    else
    {
        relayPumpOff(pump);
    }
}

/**
 * @brief 获取指定水泵当前状态
 */
RelayState_t relayPumpGet(RelayPump_t pump)
{
    if (pump >= RELAY_PUMP_NUM) return RELAY_STATE_OFF;

#if (RELAY_ACTIVE_HIGH == 1U)
    return bspGpioIsHigh(s_pumpMap[pump].port, s_pumpMap[pump].pin) ?
           RELAY_STATE_ON : RELAY_STATE_OFF;
#else
    return bspGpioIsLow(s_pumpMap[pump].port, s_pumpMap[pump].pin) ?
           RELAY_STATE_ON : RELAY_STATE_OFF;
#endif
}

/**
 * @brief 打开所有水泵
 */
void relayPumpAllOn(void)
{
    for (uint8_t i = 0; i < (uint8_t)RELAY_PUMP_NUM; i++)
    {
        relayActive(s_pumpMap[i].port, s_pumpMap[i].pin);
    }
}

/**
 * @brief 关闭所有水泵
 */
void relayPumpAllOff(void)
{
    for (uint8_t i = 0; i < (uint8_t)RELAY_PUMP_NUM; i++)
    {
        relayInactive(s_pumpMap[i].port, s_pumpMap[i].pin);
    }
}

/**
 * @brief   打开加热棒
 * @retval  无  
 */
void relayHeatingRodOn(void)
{
    relayActive(s_pumpMap[RELAY_HEATING_ROD].port, s_pumpMap[RELAY_HEATING_ROD].pin);
}

/**
 * @brief   关闭加热棒
 * @retval  无
 */
void relayHeatingRodOff(void)
{
    relayInactive(s_pumpMap[RELAY_HEATING_ROD].port, s_pumpMap[RELAY_HEATING_ROD].pin);
}

/**
 * @brief   设置加热棒状态
 * @param   state 目标状态 @ref RelayState_t
 * @retval  无
 */
void relayHeatingRodSet(RelayState_t state)
{
    if (state == RELAY_STATE_ON) {
        relayHeatingRodOn();
    } else {
        relayHeatingRodOff();
    }
}

#ifdef __cplusplus
} 
#endif
