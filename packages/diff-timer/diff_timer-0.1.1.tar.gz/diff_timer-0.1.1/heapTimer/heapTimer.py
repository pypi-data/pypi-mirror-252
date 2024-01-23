'''
:@Author: tangchengqin
:@Date: 2024/1/16 20:31:15
:@LastEditors: tangchengqin
:@LastEditTime: 2024/1/22 15:37:01
:Description: 
:Copyright: Copyright (©)}) 2024 Clairfy. All rights reserved.
'''

"""
基于堆排序的Timer
"""

import heapq
import asyncio


class HeapTimerManager:

    __isinstance = None

    def __init__(self, interval, tps):
        self.m_tickPerSecond = tps
        self.m_interval = interval
        self.m_taskQueue = []
        heapq.heapify(self.m_taskQueue)
        self.m_nameList = []
        self.m_ignoreTimer = []
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
        if name in self.m_nameList:
            raise NameError(f"timer name repeated: {name}")
        timeout = self.time2Tick(timeout) + self.m_curTick
        if not timeout:
            raise ValueError(f"timer timeout error: {name}")
        timer = HeapTimer(func, timeout, name)
        heapq.heappush(self.m_taskQueue, timer)
        self.m_nameList.append(name)
        return True
    
    def removeTimeOut(self, name):
        if name not in self.m_nameList:
            return
        self.m_nameList.remove(name)
        self.m_ignoreTimer.append(name)

    def CheckTimer(self, curTick):
        while True:
            try:
                timer = heapq.heappop(self.m_taskQueue)
            except IndexError:
                break
            if timer.getTimeOut() < curTick:
                func = timer.execute()
                asyncio.run(func)
                continue
            heapq.heappush(self.m_taskQueue, timer)
            break
            
    def time2Tick(self, time):
        if type(time) != int:
            return
        return time * self.m_tickPerSecond


class HeapTimer:

    def __init__(self, func, timeout, name):
        self.m_func = func
        self.m_timeout = timeout
        self.m_name = name

    def __str__(self):
        return f"timer {self.m_name} timeout {self.m_timeout}"
    
    def __lt__(self, other):    # 实现对象可堆化
        return self.m_timeout < other.m_timeout

    def __gt__(self, other):
        return self.m_timeout > other.m_timeout

    def __eq__(self, other):
        return self.m_timeout == other.m_timeout

    def getTimeOut(self):
        return self.m_timeout

    async def execute(self):
        timerMgr = getHeapTimerMgr()
        timerMgr.removeTimeOut(self.m_name)
        self.m_func()

def initHeapTimer(interval, tps):
    if "g_HeapTimerMgr" in globals():
        return
    global g_HeapTimerMgr
    g_HeapTimerMgr = HeapTimerManager(interval, tps)
    return g_HeapTimerMgr

def getHeapTimerMgr():
    if "g_HeapTimerMgr" not in globals():
        raise PermissionError("heap timer manager is not exist")
    return g_HeapTimerMgr
