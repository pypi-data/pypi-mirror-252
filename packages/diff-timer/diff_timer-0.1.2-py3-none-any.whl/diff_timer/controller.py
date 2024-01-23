'''
:@Author: tangchengqin
:@Date: 2023/11/6 10:29:52
:@LastEditors: tangchengqin
:@LastEditTime: 2024/1/22 15:36:47
:Description: 
:Copyright: Copyright (©)}) 2023 Clairfy. All rights reserved.
'''

"""
Timer Controller
"""

from timer import initTimer
from wheelTimer import initWheelTimer
from heapTimer import initHeapTimer

class Controller:

    __isinstance = None
    
    def __init__(self):
        if hasattr(self, "m_isInit"):
            return
        self.m_timerCol = None
        self.m_tickPerSecond = 0
        self.m_time = None
        self.m_isInit = False

    def __new__(cls, *args, **kwargs):
        if cls.__isinstance:
            return cls.__isinstance
        cls.__isinstance = object.__new__(cls)
        return cls.__isinstance

    def init(self, tps):
        self.m_tickPerSecond = tps
        self.m_time = Time(tps)
        self.m_isInit = True

    def initTimer(self, timerType, interval, tps, size=300):
        TIMER_MAP = {
            "NORMAL": initTimer,
            "HEAP": initHeapTimer,
            "WHEEL": initWheelTimer,
        }
        if timerType not in TIMER_MAP:
            raise KeyError(f"error with timer type {timerType}")
        if not self.m_isInit:
            self.init(tps)
        initFunc = TIMER_MAP[timerType]
        if timerType != "WHEEL":
            self.m_timerCol = initFunc(interval, tps)
            return
        self.m_timerCol = initFunc(interval, tps, size)

    def tick(self, curTick):
        if not self.m_time:
            raise PermissionError("time is not initial")
        self.m_time.tick(curTick)
        self.m_timerCol.tick(curTick)

    def setTimeOut(self, func, timeout, name):
        if not self.m_isInit:
            raise PermissionError("controller is not initial")
        self.m_timerCol.setTimeOut(func, timeout, name)

    def removeTimeOut(self, name):
        if not self.m_isInit:
            raise PermissionError("controller is not initial")
        self.m_timerCol.removeTimeOut(name)

    def getTimeOut(self, name):
        if not self.m_isInit:
            raise PermissionError("controller is not initial")
        return self.m_timerCol.getTimeOut(name)


class Time:

    def __init__(self, tps):
        self.m_close = 0
        self.m_tickPerSecond = tps
        self.m_tick = 0
        self.m_dayTick = 86400 * tps
        self.m_hourTick = 3600 * tps
        self.m_minuteTick = 60 * tps

    def tick(self, newTick=None):
        if not newTick:
            self.m_tick += 1
            return
        self.m_tick = newTick

    def getTick(self):
        return self.m_tick

    def getNowTime(self):
        if not self.m_tick:
            return
        day = self.m_tick // self.m_dayTick
        hour = (self.m_tick % self.m_dayTick) // self.m_hourTick
        minute = (self.m_tick % self.m_hourTick) // self.m_minuteTick
        second = (self.m_tick % self.m_minuteTick) // self.m_secondTick
        return {"day": day, "hour": hour, "minute": minute, "second": second}


def setTimeOut(func, timeOut, name):
    Controller().setTimeOut(func, timeOut, name)

def removeTimeOut(name):
    Controller().removeTimeOut(name)

def getTimeOut(name):
    Controller().getTimeOut(name)
