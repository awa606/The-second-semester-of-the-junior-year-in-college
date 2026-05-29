/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file    ds18b20.c
  * @brief   DS18B20 one-wire temperature sensor driver for STM32F407 HAL.
  ******************************************************************************
  */
/* USER CODE END Header */

#include "ds18b20.h"
#include "usart.h"

#include <stdio.h>
#include <string.h>

static void DS18B20_DelayUs(uint32_t us);
static void DS18B20_DQ_Output(void);
static void DS18B20_DQ_Input(void);
static uint8_t DS18B20_ResetAndCheck(void);
static void DS18B20_WriteByte(uint8_t data);
static uint8_t DS18B20_ReadByte(void);
static uint8_t DS18B20_ReadBit(void);
static uint8_t DS18B20_Crc8(const uint8_t *data, uint8_t length);

void DS18B20_DelayInit(void)
{
  CoreDebug->DEMCR |= CoreDebug_DEMCR_TRCENA_Msk;
  DWT->CYCCNT = 0U;
  DWT->CTRL |= DWT_CTRL_CYCCNTENA_Msk;
}

static void DS18B20_DelayUs(uint32_t us)
{
  uint32_t ticks;
  uint32_t start;

  if ((DWT->CTRL & DWT_CTRL_CYCCNTENA_Msk) == 0U)
  {
    DS18B20_DelayInit();
  }

  ticks = (SystemCoreClock / 1000000U) * us;
  start = DWT->CYCCNT;
  while ((DWT->CYCCNT - start) < ticks)
  {
  }
}

static void DS18B20_DQ_Output(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};

  GPIO_InitStruct.Pin = DS18B20_DQ_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_OD;
  GPIO_InitStruct.Pull = GPIO_PULLUP;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
  HAL_GPIO_Init(DS18B20_DQ_GPIO_Port, &GPIO_InitStruct);
}

static void DS18B20_DQ_Input(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};

  GPIO_InitStruct.Pin = DS18B20_DQ_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_PULLUP;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
  HAL_GPIO_Init(DS18B20_DQ_GPIO_Port, &GPIO_InitStruct);
}

static uint8_t DS18B20_ResetAndCheck(void)
{
  uint16_t timeout;

  DS18B20_DQ_Output();
  HAL_GPIO_WritePin(DS18B20_DQ_GPIO_Port, DS18B20_DQ_Pin, GPIO_PIN_RESET);
  DS18B20_DelayUs(480U);
  HAL_GPIO_WritePin(DS18B20_DQ_GPIO_Port, DS18B20_DQ_Pin, GPIO_PIN_SET);
  DS18B20_DQ_Input();
  DS18B20_DelayUs(70U);

  if (HAL_GPIO_ReadPin(DS18B20_DQ_GPIO_Port, DS18B20_DQ_Pin) == GPIO_PIN_SET)
  {
    DS18B20_DQ_Output();
    HAL_GPIO_WritePin(DS18B20_DQ_GPIO_Port, DS18B20_DQ_Pin, GPIO_PIN_SET);
    return DS18B20_ERROR;
  }

  timeout = 0U;
  while (HAL_GPIO_ReadPin(DS18B20_DQ_GPIO_Port, DS18B20_DQ_Pin) == GPIO_PIN_RESET)
  {
    DS18B20_DelayUs(1U);
    if (++timeout > 240U)
    {
      DS18B20_DQ_Output();
      HAL_GPIO_WritePin(DS18B20_DQ_GPIO_Port, DS18B20_DQ_Pin, GPIO_PIN_SET);
      return DS18B20_ERROR;
    }
  }

  DS18B20_DQ_Output();
  HAL_GPIO_WritePin(DS18B20_DQ_GPIO_Port, DS18B20_DQ_Pin, GPIO_PIN_SET);
  DS18B20_DelayUs(10U);
  return DS18B20_OK;
}

uint8_t DS18B20_Init(void)
{
  __HAL_RCC_GPIOA_CLK_ENABLE();
  DS18B20_DelayInit();
  DS18B20_DQ_Output();
  HAL_GPIO_WritePin(DS18B20_DQ_GPIO_Port, DS18B20_DQ_Pin, GPIO_PIN_SET);
  return DS18B20_ResetAndCheck();
}

static void DS18B20_WriteByte(uint8_t data)
{
  uint8_t i;

  DS18B20_DQ_Output();
  for (i = 0U; i < 8U; i++)
  {
    HAL_GPIO_WritePin(DS18B20_DQ_GPIO_Port, DS18B20_DQ_Pin, GPIO_PIN_RESET);
    if ((data & 0x01U) != 0U)
    {
      DS18B20_DelayUs(6U);
      HAL_GPIO_WritePin(DS18B20_DQ_GPIO_Port, DS18B20_DQ_Pin, GPIO_PIN_SET);
      DS18B20_DelayUs(64U);
    }
    else
    {
      DS18B20_DelayUs(60U);
      HAL_GPIO_WritePin(DS18B20_DQ_GPIO_Port, DS18B20_DQ_Pin, GPIO_PIN_SET);
      DS18B20_DelayUs(10U);
    }
    data >>= 1;
  }
}

static uint8_t DS18B20_ReadBit(void)
{
  uint8_t bit;

  DS18B20_DQ_Output();
  HAL_GPIO_WritePin(DS18B20_DQ_GPIO_Port, DS18B20_DQ_Pin, GPIO_PIN_RESET);
  DS18B20_DelayUs(3U);
  HAL_GPIO_WritePin(DS18B20_DQ_GPIO_Port, DS18B20_DQ_Pin, GPIO_PIN_SET);
  DS18B20_DQ_Input();
  DS18B20_DelayUs(10U);
  bit = (HAL_GPIO_ReadPin(DS18B20_DQ_GPIO_Port, DS18B20_DQ_Pin) == GPIO_PIN_SET) ? 1U : 0U;
  DS18B20_DelayUs(53U);
  DS18B20_DQ_Output();
  HAL_GPIO_WritePin(DS18B20_DQ_GPIO_Port, DS18B20_DQ_Pin, GPIO_PIN_SET);
  return bit;
}

static uint8_t DS18B20_ReadByte(void)
{
  uint8_t i;
  uint8_t data = 0U;

  for (i = 0U; i < 8U; i++)
  {
    data >>= 1;
    if (DS18B20_ReadBit() != 0U)
    {
      data |= 0x80U;
    }
  }

  return data;
}

static uint8_t DS18B20_Crc8(const uint8_t *data, uint8_t length)
{
  uint8_t crc = 0U;
  uint8_t i;

  while (length-- != 0U)
  {
    crc ^= *data++;
    for (i = 0U; i < 8U; i++)
    {
      if ((crc & 0x01U) != 0U)
      {
        crc = (crc >> 1) ^ 0x8CU;
      }
      else
      {
        crc >>= 1;
      }
    }
  }

  return crc;
}

int16_t DS18B20_ReadTemperatureX10(void)
{
  uint8_t scratchpad[9];
  uint8_t i;
  int16_t raw_temperature;
  int32_t temperature_x10;

  if (DS18B20_ResetAndCheck() != DS18B20_OK)
  {
    return DS18B20_TEMP_ERROR;
  }

  DS18B20_WriteByte(0xCCU);
  DS18B20_WriteByte(0x44U);
  HAL_Delay(750U);

  if (DS18B20_ResetAndCheck() != DS18B20_OK)
  {
    return DS18B20_TEMP_ERROR;
  }

  DS18B20_WriteByte(0xCCU);
  DS18B20_WriteByte(0xBEU);
  for (i = 0U; i < 9U; i++)
  {
    scratchpad[i] = DS18B20_ReadByte();
  }

  if (DS18B20_Crc8(scratchpad, 8U) != scratchpad[8])
  {
    return DS18B20_TEMP_ERROR;
  }

  raw_temperature = (int16_t)(((uint16_t)scratchpad[1] << 8) | scratchpad[0]);
  temperature_x10 = (int32_t)raw_temperature * 10;
  if (temperature_x10 >= 0)
  {
    temperature_x10 = (temperature_x10 + 8) / 16;
  }
  else
  {
    temperature_x10 = (temperature_x10 - 8) / 16;
  }

  if ((temperature_x10 > 32767) || (temperature_x10 < -32768))
  {
    return DS18B20_TEMP_ERROR;
  }

  return (int16_t)temperature_x10;
}

void test_ds18b20(void)
{
  static uint32_t last_tick = 0U;
  uint32_t now = HAL_GetTick();
  int16_t temperature_x10;
  int16_t abs_temperature;
  char tx_buffer[48];

  if ((now - last_tick) < 1000U)
  {
    return;
  }
  last_tick = now;

  temperature_x10 = DS18B20_ReadTemperatureX10();
  if (temperature_x10 == DS18B20_TEMP_ERROR)
  {
    static const char error_msg[] = "DS18B20 Error\r\n";
    HAL_UART_Transmit(&huart1, (uint8_t *)error_msg, (uint16_t)(sizeof(error_msg) - 1U), 100U);
    return;
  }

  abs_temperature = (temperature_x10 < 0) ? (int16_t)(-temperature_x10) : temperature_x10;
  (void)snprintf(tx_buffer, sizeof(tx_buffer), "Temp: %s%d.%d C\r\n",
                 (temperature_x10 < 0) ? "-" : "",
                 abs_temperature / 10,
                 abs_temperature % 10);
  HAL_UART_Transmit(&huart1, (uint8_t *)tx_buffer, (uint16_t)strlen(tx_buffer), 100U);

  /*
   * Future heating control hook:
   * temperature_x10 can drive HeatingRod, for example on below 40.0 C
   * and off above 45.0 C. It stays disabled now to avoid unintended heat.
   */
}
