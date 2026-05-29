/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file    ds18b20.h
  * @brief   DS18B20 one-wire temperature sensor driver for STM32F407 HAL.
  ******************************************************************************
  */
/* USER CODE END Header */

#ifndef __DS18B20_H
#define __DS18B20_H

#ifdef __cplusplus
extern "C" {
#endif

#include "main.h"
#include <stdint.h>

#define DS18B20_OK             0U
#define DS18B20_ERROR          1U
#define DS18B20_TEMP_ERROR     ((int16_t)-10000)

void DS18B20_DelayInit(void);
uint8_t DS18B20_Init(void);
int16_t DS18B20_ReadTemperatureX10(void);
void test_ds18b20(void);

#ifdef __cplusplus
}
#endif

#endif /* __DS18B20_H */
