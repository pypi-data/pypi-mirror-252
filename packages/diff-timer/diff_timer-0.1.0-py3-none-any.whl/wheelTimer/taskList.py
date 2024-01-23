'''
:@Author: tangchengqin
:@Date: 2023/12/29 10:46:20
:@LastEditors: tangchengqin
:@LastEditTime: 2023/12/29 10:46:20
:Description: 
:Copyright: Copyright (©)}) 2023 Clairfy. All rights reserved.
'''

class TaskList:

    def __init__(self):
        self.m_curId = 1
        self.m_headNode = TaskNode(0, None, None, "headNode")     # 头结点id为0，尾结点id为-1
        self.m_tailNode = TaskNode(-1, None, None, "tailNode")
        self.m_headNode.setNext(self.m_tailNode)
        self.m_tailNode.setPrev(self.m_headNode)

    def getHeadNode(self):
        return self.m_headNode
    
    def getTailNode(self):
        return self.m_tailNode

    def addTask(self, func, timeout, name):
        tail = self.getTailNode()
        prev = tail.prev()
        node = TaskNode(self.m_curId, func, timeout, name)
        prev.setNext(node)
        node.setNext(tail)
        node.setPrev(prev)
        tail.setPrev(node)
        self.m_curId += 1

    def removeTask(self, taskId):
        node = self.getHeadNode()
        while True:
            if node.m_id == -1:
                raise ValueError(f"no such task id {taskId}")
            if node.m_id == taskId:
                prevNode = node.prev()
                nextNode = node.next()
                prevNode.setNext(nextNode)
                nextNode.setPrev(prevNode)
                del node
                break

    def getTask(self, taskFlag):
        node = self.getHeadNode()
        while True:
            if node.m_id == -1:
                raise ValueError(f"no such task id/name {taskFlag}")
            if node.m_id == taskFlag:
                return node
            if node.m_name == taskFlag:
                return node


class TaskNode:

    def __init__(self, taskId, func, timeout, name):
        self.m_func = func
        self.m_timeout = timeout
        self.m_name = name
        self.m_id = taskId
        self.m_prev = None
        self.m_next = None

    def setPrev(self, prev):
        self.m_prev = prev

    def setNext(self, next):
        self.m_next = next

    def prev(self):
        return self.m_prev
    
    def next(self):
        return self.m_next

    def removeSelf(self):   # 从任务链表中分离自身
        prev = self.prev()
        next = self.next()
        if prev:
            prev.setNext(next)
        if next:
            next.setPrev(prev)

    async def execute(self):
        self.removeSelf()   # 先从任务链表中移除节点
        if not self.m_func:
            return
        self.m_func()
