#pragma once
#ifndef __DS18B20_HPP
#define __DS18B20_HPP

#include "main.h"

#ifdef __cplusplus
extern "C" {
#endif

#define DS18B20_OK            (0U)
#define DS18B20_ERROR         (1U)
#define DS18B20_TEMP_INVALID  ((int16_t)0x7FFF)

uint8_t DS18B20_Init(void);
void DS18B20_Rst(void);
uint8_t DS18B20_Check(void);
uint8_t DS18B20_Read_Bit(void);
uint8_t DS18B20_Read_Byte(void);
void DS18B20_Write_Byte(uint8_t dat);
void DS18B20_Start(void);
uint8_t DS18B20_ReadScratchpad(uint8_t scratchpad[9]);
uint8_t DS18B20_GetTempDeciC(int16_t *temperature);
int16_t DS18B20_Get_Temp(void);
float DS18B20_GetTempC(void);

#ifdef __cplusplus
}
#endif

#endif
