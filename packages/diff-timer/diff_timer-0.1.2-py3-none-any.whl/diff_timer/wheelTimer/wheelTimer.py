'''
:@Author: tangchengqin
:@Date: 2023/12/29 10:30:06
:@LastEditors: tangchengqin
:@LastEditTime: 2024/1/22 15:36:37
:Description: 
:Copyright: Copyright (©)}) 2023 Clairfy. All rights reserved.
'''

"""
Timer base on timing wheel
"""

from .taskList import TaskList
from .defines import *
import asyncio

class WheelTimerManager:

    __isinstance = None

    def __init__(self, interval, tps, size=300):
        self.m_tickPerSecond = tps
        self.m_interval = interval
        self.m_wheelSize = size
        self.m_curTick = 0
        self.m_tick5 = 0
        self.m_nameList = {}
        self.m_wheelTimerLow = WheelTimerLow(interval, size)
        self.m_wheelTimerMid = WheelTimerMid(interval, size)
        self.m_wheelTimerTop = WheelTimerTop(interval, size)
        self.init()

    def __new__(cls, *args, **kwargs):
        if cls.__isinstance:
            return cls.__isinstance
        cls.__isinstance = object.__new__(cls)
        return cls.__isinstance

    def init(self):
        self.m_wheelTimerLow.setUpperTimer(self.m_wheelTimerMid)
        self.m_wheelTimerMid.setUpperTimer(self.m_wheelTimerTop)
        self.m_wheelTimerTop.setLowerTimer(self.m_wheelTimerMid)
        self.m_wheelTimerMid.setLowerTimer(self.m_wheelTimerLow)

    def tick(self, curTick):
        self.m_curTick = curTick
        self.m_tick5 += 1
        if self.m_tick5 != self.m_interval:
            return
        self.m_tick5 = 0
        self.m_wheelTimerLow.tick(curTick)
        if not self.m_wheelTimerLow.isCompleteRound():
            self.m_wheelTimerMid.downgradeTask()
            return
        self.m_wheelTimerMid.tick(curTick)
        if not self.m_wheelTimerMid.isCompleteRound():
            self.m_wheelTimerMid.downgradeTask()
            return
        self.m_wheelTimerTop.tick(curTick)

    def setTimeOut(self, func, timeout, name):
        if name in self.m_nameList:
            raise NameError(f"timer name repeat {name}")
        tick = self.time2Tick(timeout)
        if tick == None:
            raise ValueError(f"error with timeout {timeout}")
        ret = self.m_wheelTimerLow.addTask(func, tick, name)
        if not ret:
            return
        self.m_nameList[name] = [self.m_curTick, tick]

    def removeTimeOut(self, name):
        if name not in self.m_nameList:
            raise NameError(f"no such timer {name}")
        ret = self.m_wheelTimerLow.removeTask(name)
        if not ret:
            return
        del self.m_nameList[name]

    def getTimeOut(self, name):
        if name not in self.m_nameList:
            raise NameError(f"no such timer {name}")
        return self.m_wheelTimerLow.getTask(name)

    def time2Tick(self, timeStamp):
        if type(timeStamp) != int:
            return
        return timeStamp * self.m_tickPerSecond


class WheelTimerBase:

    def __init__(self, interval, size):
        self.m_curTick = 0
        self.m_upperTimer = None
        self.m_lowerTimer = None
        self.m_interval = interval
        self.m_type = None
        self.m_size = size
        self.m_wheel = [TaskList() for _ in range(self.m_size)]
        self.m_pointer = 0
        self.m_timerNames = []
        self.m_ignoreTimer = []     # 不执行的timer
        self.m_startFlag = 0    # 开始标记

    def isCompleteRound(self):  # 时间轮指针走完一圈
        if self.m_startFlag:
            return True
        if not self.m_pointer:
            return True
        return False

    def setUpperTimer(self, timer):
        self.m_upperTimer = timer

    def setLowerTimer(self, timer):
        self.m_lowerTimer = timer

    def getUpperTimer(self):
        return self.m_upperTimer
    
    def getLowerTimer(self):
        return self.m_lowerTimer

    def tick(self, curTick):
        self.m_curTick = curTick
        self.m_pointer += 1
        if self.m_type == WHEEL_SECOND:
            self.execute()
        if self.m_pointer >= self.m_size - 1:
            self.m_pointer = 0
            if not self.m_startFlag:
                self.m_startFlag += 1

    def execute(self):
        raise SystemError(f"error timer execute {self}")

    def addTask(self, func, tick, name):
        if tick > self.m_interval * self.m_size:
            self.upgradeTask(func, tick, name)
            return
        idx = tick // self.m_interval + self.m_pointer
        if self.m_type != WHEEL_SECOND:
            idx -= 1                    # 减去下层时间轮的时间
        taskList = self.m_wheel[idx]
        if name in self.m_timerNames:
            raise NameError(f"timer name {name} repeated")
        taskList.addTask(func, tick, name)
        self.m_timerNames.append(name)

    def removeTask(self, name):
        self.m_ignoreTimer.append(name)

    def getTask(self, name):      # 只获取最低层时间轮上的任务，因此若任务不存在，不代表没有该定时器
        if name not in self.m_timerNames:
            return
        if name in self.m_ignoreTimer:
            return
        for taskList in self.m_wheel:
            task = taskList.getTask(name)
            if task:
                return task

    def upgradeTask(self, func, tick, name):  # 任务升级
        upperTimer = self.getUpperTimer()
        if not upperTimer:
            raise TypeError("wheelTimer", f"no upper timer {self.m_type}")
        upperTimer.addTask(func, tick, name)

    def downgradeTask(self):      # 任务降级
        lowerTimer = self.getLowerTimer()
        if not lowerTimer:
            raise TypeError(f"no lower timer {self.m_type}")
        taskList = self.m_wheel[self.m_pointer-1]
        curNode = taskList.getHeadNode()
        curNode = curNode.next()
        while True:
            if curNode.m_id == TASK_LIST_TAIL_ID:
                break
            if curNode.m_name in self.m_ignoreTimer:
                continue
            func = curNode.m_func
            if not func:
                curNode.removeSelf()
                return
            newTick = curNode.m_timeout - self.m_interval * self.m_pointer
            if newTick < 0 or newTick > self.m_interval:
                break
            next = curNode.next()
            curNode.removeSelf()
            name = curNode.m_name
            lowerTimer.addTask(func, newTick, name)
            curNode = next
            self.m_timerNames.remove(name)


class WheelTimerLow(WheelTimerBase):

    def __init__(self, interval, size):
        WheelTimerBase.__init__(self, interval, size)
        self.m_interval = interval
        self.m_type = WHEEL_SECOND

    def execute(self):
        taskList = self.m_wheel[self.m_pointer-1]
        curNode = taskList.getHeadNode()
        curNode = curNode.next()
        while True:
            if curNode.m_id == TASK_LIST_TAIL_ID:
                return
            if curNode.m_name in self.m_ignoreTimer:
                curNode = curNode.next()
                continue
            if not curNode.m_func:
                curNode = curNode.next()
                continue
            next = curNode.next()
            func = curNode.execute()
            name = curNode.m_name
            self.m_timerNames.remove(name)
            asyncio.run(func)
            curNode = next


class WheelTimerMid(WheelTimerBase):

    def __init__(self, interval, size):
        WheelTimerBase.__init__(self, interval, size)
        self.m_interval = size * interval
        self.m_type = WHEEL_MINUTE


class WheelTimerTop(WheelTimerBase):

    def __init__(self, interval, size):
        WheelTimerBase.__init__(self, interval, size)
        self.m_interval = size * interval * interval
        self.m_type = WHEEL_HOUR


def initWheelTimer(interval, tps, size):
    if "g_WheelTimerMgr" in globals():
        return
    global g_WheelTimerMgr
    g_WheelTimerMgr = WheelTimerManager(interval, tps, size)
    return g_WheelTimerMgr

def getTimerMgr():
    if "g_WheelTimerMgr" not in globals():
        raise PermissionError("wheel timer manager is not exist")
    return g_WheelTimerMgr
