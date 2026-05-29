#include "ds18b20.hpp"

#define DS18B20_CMD_SKIP_ROM        (0xCCU)
#define DS18B20_CMD_CONVERT_T       (0x44U)
#define DS18B20_CMD_READ_SCRATCHPAD (0xBEU)
#define DS18B20_CONVERSION_MS       (750U)

static void DS18B20_EnableClock(void)
{
    __HAL_RCC_GPIOA_CLK_ENABLE();
}

static void DS18B20_DelayInit(void)
{
    CoreDebug->DEMCR |= CoreDebug_DEMCR_TRCENA_Msk;
    DWT->CYCCNT = 0U;
    DWT->CTRL |= DWT_CTRL_CYCCNTENA_Msk;
}

static void DS18B20_DelayUs(uint32_t us)
{
    const uint32_t ticks = (SystemCoreClock / 1000000U) * us;
    const uint32_t start = DWT->CYCCNT;

    while ((DWT->CYCCNT - start) < ticks)
    {
    }
}

static void DS18B20_IO_IN(void)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};

    GPIO_InitStruct.Pin = DS18B20_DQ_Pin;
    GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
    GPIO_InitStruct.Pull = GPIO_PULLUP;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
    HAL_GPIO_Init(DS18B20_DQ_GPIO_Port, &GPIO_InitStruct);
}

static void DS18B20_IO_OUT(void)
{
    GPIO_InitTypeDef GPIO_InitStruct = {0};

    GPIO_InitStruct.Pin = DS18B20_DQ_Pin;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_OD;
    GPIO_InitStruct.Pull = GPIO_PULLUP;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
    HAL_GPIO_Init(DS18B20_DQ_GPIO_Port, &GPIO_InitStruct);
}

static uint8_t DS18B20_DQ_Read(void)
{
    return (HAL_GPIO_ReadPin(DS18B20_DQ_GPIO_Port, DS18B20_DQ_Pin) == GPIO_PIN_SET) ? 1U : 0U;
}

static void DS18B20_DQ_Write(uint8_t state)
{
    HAL_GPIO_WritePin(DS18B20_DQ_GPIO_Port,
                      DS18B20_DQ_Pin,
                      state ? GPIO_PIN_SET : GPIO_PIN_RESET);
}

static uint8_t DS18B20_Crc8(const uint8_t *data, uint8_t len)
{
    uint8_t crc = 0U;

    for (uint8_t i = 0U; i < len; i++)
    {
        uint8_t inByte = data[i];
        for (uint8_t bit = 0U; bit < 8U; bit++)
        {
            const uint8_t mix = (crc ^ inByte) & 0x01U;
            crc >>= 1U;
            if (mix != 0U)
            {
                crc ^= 0x8CU;
            }
            inByte >>= 1U;
        }
    }

    return crc;
}

uint8_t DS18B20_Init(void)
{
    DS18B20_EnableClock();
    DS18B20_DelayInit();
    DS18B20_IO_OUT();
    DS18B20_DQ_Write(1U);
    DS18B20_Rst();
    return DS18B20_Check();
}

void DS18B20_Rst(void)
{
    DS18B20_IO_OUT();
    DS18B20_DQ_Write(0U);
    DS18B20_DelayUs(750U);
    DS18B20_DQ_Write(1U);
    DS18B20_DelayUs(15U);
}

uint8_t DS18B20_Check(void)
{
    uint16_t retry = 0U;

    DS18B20_IO_IN();

    while ((DS18B20_DQ_Read() != 0U) && (retry < 200U))
    {
        retry++;
        DS18B20_DelayUs(1U);
    }

    if (retry >= 200U)
    {
        return DS18B20_ERROR;
    }

    retry = 0U;
    while ((DS18B20_DQ_Read() == 0U) && (retry < 240U))
    {
        retry++;
        DS18B20_DelayUs(1U);
    }

    return (retry >= 240U) ? DS18B20_ERROR : DS18B20_OK;
}

uint8_t DS18B20_Read_Bit(void)
{
    uint8_t data = 0U;

    DS18B20_IO_OUT();
    DS18B20_DQ_Write(0U);
    DS18B20_DelayUs(2U);
    DS18B20_DQ_Write(1U);
    DS18B20_IO_IN();
    DS18B20_DelayUs(12U);
    data = DS18B20_DQ_Read();
    DS18B20_DelayUs(50U);

    return data;
}

uint8_t DS18B20_Read_Byte(void)
{
    uint8_t dat = 0U;

    for (uint8_t i = 0U; i < 8U; i++)
    {
        dat >>= 1U;
        if (DS18B20_Read_Bit() != 0U)
        {
            dat |= 0x80U;
        }
    }

    return dat;
}

void DS18B20_Write_Byte(uint8_t dat)
{
    DS18B20_IO_OUT();

    for (uint8_t i = 0U; i < 8U; i++)
    {
        if ((dat & 0x01U) != 0U)
        {
            DS18B20_DQ_Write(0U);
            DS18B20_DelayUs(2U);
            DS18B20_DQ_Write(1U);
            DS18B20_DelayUs(60U);
        }
        else
        {
            DS18B20_DQ_Write(0U);
            DS18B20_DelayUs(60U);
            DS18B20_DQ_Write(1U);
            DS18B20_DelayUs(2U);
        }

        dat >>= 1U;
    }
}

void DS18B20_Start(void)
{
    DS18B20_Rst();
    if (DS18B20_Check() == DS18B20_OK)
    {
        DS18B20_Write_Byte(DS18B20_CMD_SKIP_ROM);
        DS18B20_Write_Byte(DS18B20_CMD_CONVERT_T);
    }
}

uint8_t DS18B20_ReadScratchpad(uint8_t scratchpad[9])
{
    if (scratchpad == nullptr)
    {
        return DS18B20_ERROR;
    }

    DS18B20_Rst();
    if (DS18B20_Check() != DS18B20_OK)
    {
        return DS18B20_ERROR;
    }

    DS18B20_Write_Byte(DS18B20_CMD_SKIP_ROM);
    DS18B20_Write_Byte(DS18B20_CMD_READ_SCRATCHPAD);

    for (uint8_t i = 0U; i < 9U; i++)
    {
        scratchpad[i] = DS18B20_Read_Byte();
    }

    return (DS18B20_Crc8(scratchpad, 8U) == scratchpad[8]) ? DS18B20_OK : DS18B20_ERROR;
}

uint8_t DS18B20_GetTempDeciC(int16_t *temperature)
{
    uint8_t scratchpad[9] = {0};

    if (temperature == nullptr)
    {
        return DS18B20_ERROR;
    }

    *temperature = DS18B20_TEMP_INVALID;
    DS18B20_Start();
    HAL_Delay(DS18B20_CONVERSION_MS);

    if (DS18B20_ReadScratchpad(scratchpad) != DS18B20_OK)
    {
        return DS18B20_ERROR;
    }

    const int16_t raw = (int16_t)((uint16_t)scratchpad[0] | ((uint16_t)scratchpad[1] << 8U));
    int32_t deciC = (int32_t)raw * 10L;

    if (deciC >= 0L)
    {
        deciC = (deciC + 8L) / 16L;
    }
    else
    {
        deciC = (deciC - 8L) / 16L;
    }

    *temperature = (int16_t)deciC;
    return DS18B20_OK;
}

int16_t DS18B20_Get_Temp(void)
{
    int16_t temperature = DS18B20_TEMP_INVALID;

    if (DS18B20_GetTempDeciC(&temperature) != DS18B20_OK)
    {
        return DS18B20_TEMP_INVALID;
    }

    return temperature;
}

float DS18B20_GetTempC(void)
{
    int16_t temperature = DS18B20_TEMP_INVALID;

    if (DS18B20_GetTempDeciC(&temperature) != DS18B20_OK)
    {
        return -1000.0f;
    }

    return ((float)temperature) / 10.0f;
}
