#include "motor.hpp"
#include <stdlib.h>
#include "usart.h"
/**
  ******************************************************************************
  * @file    motor.cpp
  * @brief   电机驱动实现
  ******************************************************************************
  */
uint8_t rxBuffer[20];

extern UART_HandleTypeDef huart1;

void Motor_ZDT::setSpeed(int16_t speed)
{
    targetSpeed = speed;
}

void Motor_ZDT::updateSpeed()
{
    uint8_t cmd[8];
    if (currentSpeed == targetSpeed) {
        return; // 无需更新
    }
    cmd[0] = 0x01;	/* 地址 */
    cmd[1] = 0xF6;	/* 命令 */ 
    if(targetSpeed > 0) {
        cmd[2] = 0x01;	/* 旋转方向：顺时针 */
    } else {
        cmd[2] = 0x00;	/* 旋转方向：逆时针 */
    }
    cmd[3] = (targetSpeed >> 8) & 0xFF;    /* 速度高8位 */
    cmd[4] = targetSpeed & 0xFF;	/* 速度低8位 */
    cmd[5] = 0x08;			//acc
    cmd[6] = 0x00;    /* 是否多机协同 */
    cmd[7] = 0x6B;	/* 校验 */

    for(uint8_t i=0; i < 8; i++) {
        HAL_UART_Transmit(&huart1, cmd+i, 1,100);
    }
		
}

void Motor_ZDT::stop()
{
    uint8_t cmd[4];
    if (currentSpeed == targetSpeed) {
        return; // 无需更新
    }
    cmd[0] = 0x01;	/* 地址 */
    cmd[1] = 0xF6;	/* 命令 */ 
    cmd[2] = 0xFE;    /* 是否多机协同 */
    cmd[3] = 0x6B;	/* 校验 */

    for(uint8_t i=0; i < 4; i++) {
        HAL_UART_Transmit(&huart1, cmd+i, 1,100);
    }
}

uint8_t Motor_ZDT::error(uint8_t* data, uint16_t len)
{
    return 0; // 无错误
}

void Motor_ZDT::yaonai()
{
    setSpeed(222);
	updateSpeed();
	HAL_Delay(10000);
    
	setSpeed(0);
	updateSpeed();
	HAL_Delay(3000);
    
	setSpeed(-222);
	updateSpeed();
	HAL_Delay(10000);
}

void Motor_ZDT::askpos()
{
    uint8_t cmd[3];
    cmd[0] = 0x01;	/* 地址 */
    cmd[1] = 0x36;	/* 命令 */ 
    cmd[2] = 0x6B;	/* 校验 */

    for(uint8_t i=0; i < 3; i++) {
        HAL_UART_Transmit(&huart1, cmd+i, 1,100);
    }
}

void Motor_ZDT::update_pos()
{
	HAL_UART_Receive_IT(&huart1, pos_data, 8);
    if(pos_data[0] == 0x01 && pos_data[7] == 0x36 && pos_data[1] == 0x36) {
        if(pos_data[2] == 0x01) {
            pos = (pos_data[3] << 24) | (pos_data[4] << 16) | (pos_data[5] << 8) | pos_data[6];
        } else {
            pos = -((pos_data[3] << 24) | (pos_data[4] << 16) | (pos_data[5] << 8) | pos_data[6]);
        }
    }
    pos = (pos*360)/65536; // 转换为角度
}

void Motor_ZDT::turnaround(float data)
{
    uint8_t cmd[13];
    cmd[0] = 0x01;    /* 地址 */
    cmd[1] = 0xFD;    /* 命令：位置模式 */

    // 方向：01 = CCW, 00 = CW
    cmd[2] = (data > 0) ? 0x01 : 0x00;

    // 速度（默认500 RPM = 0x05DC）
    uint16_t speed = 500;
    cmd[3] = (speed >> 8) & 0xFF;
    cmd[4] = speed & 0xFF;

    // 加速度档
    cmd[5] = 0xC;

    // 脉冲数 = |data| * 3200 (16细分下：3200脉冲/圈)
    uint32_t pulses = (uint32_t)(((data > 0) ? data : -data) * 3200);
    // 按示例使用大端序填充4字节
    cmd[6] = (pulses >> 24) & 0xFF;
    cmd[7] = (pulses >> 16) & 0xFF;
    cmd[8] = (pulses >> 8) & 0xFF;
    cmd[9] = pulses & 0xFF;

    // 相对/绝对模式：0x00 = 相对模式
    cmd[10] = 0x00;
    // 多机同步标志：0x00 = 不启用
    cmd[11] = 0x00;

    // 校验（设备协议中常用固定值0x6B）
    cmd[12] = 0x6B;

    for (uint8_t i = 0; i < 13; i++) {
        HAL_UART_Transmit(&huart1, cmd + i, 1, 100);
    }
}

void Motor_ZDT::turnaround_angle(int16_t data)
{
    float c = (float)(data/360.0f); // 直接使用输入的角度值
    turnaround(c);
}

void Motor_ZDT::chufen()
{
    turnaround(3.0f);
}
