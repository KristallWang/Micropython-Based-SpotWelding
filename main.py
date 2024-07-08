import network
import time
import machine
import ssd1306
from wifi import wifi_connect

from machine import Pin, I2C, ADC
from ssd1306 import SSD1306_I2C
#Toggle reset
OledRST = Pin(21, Pin.OUT)
OledRST.off()
OledRST.on()
# OledRST.off()
WeldPin = Pin(45, Pin.OUT) #光耦，低电位时激活
Button = ADC(Pin(7)) #, Pin.IN, Pin.PULLUP)) #按钮输入，30k上拉无触发，18.65k时按钮-，13.6k时按钮+，7.8k时按钮切换
Button.atten(ADC.ATTN_11DB)  #设置11db衰减
pin_buttonup     = Pin(1, Pin.IN, Pin.PULL_UP)
pin_buttondown   = Pin(2, Pin.IN, Pin.PULL_UP)
pin_buttonswitch = Pin(40, Pin.IN, Pin.PULL_UP)
pin_buttontrigger= Pin(5, Pin.IN, Pin.PULL_UP)
pin_button_reserved = Pin(35, Pin.IN, Pin.PULL_UP)
i2c = I2C(1,scl=Pin(18), sda=Pin(17))
oled = SSD1306_I2C(128, 64, i2c)
oled.fill(0)

WeldPin.value(0)   


OnePulseWidth = 20
gap = 10
TwoPulseWidth = 20
#current_value = 0

current_variable = 0  # 当前选择的变量

# 初始化触发引脚和焊接引脚


def display_numbers(OnePulseWidth, gap, TwoPulseWidth, current_variable):
    oled.fill(0)  # 清空屏幕
    if current_variable == 0:
        oled.text(">1Pulse:" + str(OnePulseWidth) + "ms", 0, 0)  # 高亮显示第一行
        print(f">FirstPulse:" + str(OnePulseWidth) + "ms")
    else:
        oled.text(" 1Pulse:" + str(OnePulseWidth) + "ms", 0, 0)
        print(f"FirstPulse:" + str(OnePulseWidth) + "ms")
    
    if current_variable == 1:
        oled.text(">Gap:" + str(gap) + "ms", 0, 10)  # 高亮显示第二行
        print(f">Gap:" + str(gap) + "ms")
    else:
        oled.text(" Gap:" + str(gap) + "ms", 0, 10)
        print(f"Gap:" + str(gap) + "ms")
    
    if current_variable == 2:
        oled.text(">2Pulse:" + str(TwoPulseWidth) + "ms", 0, 20)  # 高亮显示第三行
        print(f">SecondPulse:" + str(TwoPulseWidth) + "ms")
    else:
        oled.text(" 2Pulse:" + str(TwoPulseWidth) + "ms", 0, 20)
        print(f"SecondPulse:" + str(TwoPulseWidth) + "ms")
    
    oled.show()

def weld_sequence(Pulse1, gap0, Pulse2):
    WeldPin.value(1)
    time.sleep_ms(Pulse1)
    WeldPin.value(0)
    time.sleep_ms(gap0)
    WeldPin.value(1)
    time.sleep_ms(Pulse2)
    WeldPin.value(0)
    time.sleep_ms(500)

# 显示初始数字
display_numbers(OnePulseWidth, gap, TwoPulseWidth, current_variable)

while True:
    if not pin_buttonup.value():    # 检查增加按钮是否被按下
        if current_variable == 0:
            OnePulseWidth += 1
        elif current_variable == 1:
            gap += 1
        elif current_variable == 2:
            TwoPulseWidth += 1
        display_numbers(OnePulseWidth, gap, TwoPulseWidth, current_variable)
        time.sleep(0.05)  # 防止按键抖动

    if not pin_buttondown.value():  # 检查减少按钮是否被按下
        if current_variable == 0:
            OnePulseWidth -= 1
        elif current_variable == 1:
            gap -= 1
        elif current_variable == 2:
            TwoPulseWidth -= 1
        display_numbers(OnePulseWidth, gap, TwoPulseWidth, current_variable)
        time.sleep(0.05)  # 防止按键抖动

    if pin_buttonswitch.value()==0:  # 检查切换按钮是否被按下
        current_variable = (current_variable + 1) % 3
        display_numbers(OnePulseWidth, gap, TwoPulseWidth, current_variable)
        time.sleep(0.2)  # 防止按键抖动

    if pin_buttontrigger.value()==0:  # 检查自定义按钮是否被按下
        weld_sequence(OnePulseWidth, gap, TwoPulseWidth)
        print("triggered")
        time.sleep(0.5)  # 防止按键抖动

    if not pin_button_reserved.value():  # 检查保留按钮是否被按下
        # 刷新屏幕
        print("Reserved button pressed")
        #OledRST.off()
        #OledRST.on()
        #OledRST.off()
        oled.fill(0)
        time.sleep(0.2)  # 防止按键抖动






