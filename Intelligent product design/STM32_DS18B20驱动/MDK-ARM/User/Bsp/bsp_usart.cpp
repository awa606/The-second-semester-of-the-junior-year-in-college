
#include "bsp_usart.hpp"
#include "bsp_gpio.hpp"
#include "variables.hpp"
#include "stdarg.h"
#include "stdio.h"

#ifdef __cplusplus
extern "C" {
#endif

volatile uint32_t log_cnt = 0;


void bspUsart1Init(uint32_t baudrate)
{
}


void bspUsart2Init(uint32_t baudrate)
{

}

/**
 * @description: 串口1发送单字节数据
 * @param {uint8_t} data 待发送数据
 * @return {*}
 */
void Uart1_Send(uint8_t data)
{
    while((USART1->SR & 0x80) == RESET);
    USART1->DR = data;
}

/**
 * @description: 串口2发送单字节数据
 * @param {uint8_t} data 待发送数据
 * @return {*}
 */
void Uart2_Send(uint8_t data)
{
    while((USART2->SR & 0x80) == RESET);
    USART2->DR = data;
}

/**
  * @brief  串口1 printf格式化打印
  * @param  { uint8_t* } 字符串
  * @retval None
  */
void Uart1_print(uint8_t* str)
{
    while(*str != '\0')
        Uart1_Send(*str++);
}

/**
  * @brief  串口2 printf格式化打印
  * @param  { uint8_t* } 字符串
  * @retval None
  */
void Uart2_print(uint8_t* str)
{
    while(*str != '\0')
        Uart2_Send(*str++);
}

/**
  * @brief  串口printf格式化打印
  * @param  { char* } format 格式化字符串
  * @retval None
  */
void uart1_log_format(char* format, ...)
{
    uint8_t str[256];
      va_list aptr;
      va_start(aptr, format);
      vsprintf((char *)str, format, aptr);
      va_end(aptr);
    Uart1_print(str);
}

/**
 * @description: 接收串口单字节数据
 * @param {UART_HandleTypeDef} *huartx  串口句柄
 * @return {*}                          串口接收到的数据
 */
uint8_t USARTx_ReceiveData(USART_TypeDef *huartx)
{
    return (uint8_t) (huartx->DR &0xFF);
}


/**
  * @brief  Retargets the C library printf function to the USART.
  * @param  None
  * @retval None
  */
//PUTCHAR_PROTOTYPE
//{
//    uint32_t Timeout = 0;
//    FlagStatus Status;

//    USART_SendData(USART1, (uint8_t) ch);

//    do
//    {
//        Status = USART_GetFlagStatus(USART1, USART_FLAG_TXE);
//        Timeout++;
//    } while ((Status == RESET) && (Timeout != 0xFFFF));

//    return (ch);
//}





#ifdef __cplusplus
}
#endif
