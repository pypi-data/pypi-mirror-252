'''
:@Author: tangchengqin
:@Date: 2023/11/6 10:29:57
:@LastEditors: tangchengqin
:@LastEditTime: 2024/1/22 15:36:56
:Description: 
:Copyright: Copyright (©)}) 2023 Clairfy. All rights reserved.
'''

"""
定时器
基于游戏中的tick, 一秒钟有30tick
定时器管理器每5个tick检查一次是否有到时间的tick, 因此会存在一定时间误差
每个子进程都会部署一个该子进程的timer
"""

import asyncio


class TimerManager:

    __isinstance = None

    def __init__(self, interval, tps):
        self.m_taskQueue = {}
        self.m_tickPerSecond = tps
        self.m_interval = interval
        self.m_curTick = 0
        self.m_tick5 = 0

    def __new__(cls, *args, **kwargs):
        if cls.__isinstance:
            return cls.__isinstance
        cls.__isinstance = object.__new__(cls)
        return cls.__isinstance

    def tick(self, curTick):
        self.m_curTick = curTick
        self.m_tick5 += 1
        if self.m_tick5 != self.m_interval:
            return
        self.m_tick5 = 0
        self.CheckTimer(self.m_curTick)

    def setTimeOut(self, func, timeout, name):
        if name in self.m_taskQueue:
            raise NameError(f"timer name repeated: {name}")
        timeout = self.time2Tick(timeout) + self.m_curTick
        if not timeout:
            raise ValueError(f"timer timeout error: {name}")
        timer = Timer(func, timeout, name)
        self.m_taskQueue[name] = timer
        return True

    def getTimeOut(self, name):
        if name not in self.m_taskQueue:
            return
        return self.m_taskQueue[name]
    
    def removeTimeOut(self, name):
        if name not in self.m_taskQueue:
            return
        del self.m_taskQueue[name]

    def CheckTimer(self, curTick):
        for timer in list(self.m_taskQueue.values()):
            if timer.getTimeOut() < curTick:
                func = timer.execute()
                asyncio.run(func)
            
    def time2Tick(self, time):
        if type(time) != int:
            return
        return time * self.m_tickPerSecond


class Timer:

    def __init__(self, func, timeout, name):
        self.m_func = func
        self.m_timeout = timeout
        self.m_name = name

    def __str__(self):
        return f"timer {self.m_name} timeout {self.m_timeout}"

    def getTimeOut(self):
        return self.m_timeout

    async def execute(self):
        timerMgr = getTimerMgr()
        timerMgr.removeTimeOut(self.m_name)
        self.m_func()


def initTimer(interval, tps):
    if "g_TimerMgr" in globals():
        return
    global g_TimerMgr
    g_TimerMgr = TimerManager(interval, tps)
    return g_TimerMgr

def getTimerMgr():
    if "g_TimerMgr" not in globals():
        raise PermissionError("timer manager is not exist")
    return g_TimerMgr
