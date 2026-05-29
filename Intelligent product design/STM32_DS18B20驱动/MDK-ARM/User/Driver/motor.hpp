#pragma once
#ifndef __MOTOR_HPP
#define __MOTOR_HPP

#ifdef __cplusplus
extern "C" {
#endif

#include "main.h"

extern uint8_t rxBuffer[20];

#ifdef __cplusplus
}
#endif
/**
  ******************************************************************************
  * @file    motor.hpp
  * @brief   电机驱动头文件
  ******************************************************************************
  */
class Motor_ZDT
{
public:
    Motor_ZDT(){};
    int16_t targetSpeed;
    void setSpeed(int16_t speed);
    void askpos();
    void update_pos();
    uint8_t pos_data[8];
    int16_t pos;
    void stop();
    void updateSpeed();
    uint8_t error(uint8_t* data, uint16_t len);
    uint8_t errorFalg;
    void turnaround(float data);
    void turnaround_angle(int16_t data);

    void yaonai();
    void chufen();
private:
    int16_t currentSpeed;
};


#endif /* __MOTOR_HPP */