from controller import Controller, setTimeOut
import time

counting = 1

def test():
    global counting
    print(f"test count {counting} done")
    counting += 1
    setTimeOut(test, 2, f"test_{counting}")

def main():
    curTick = 1
    flag = 0
    tps = 50
    interval = 5
    controller = Controller()
    controller.initTimer("WHEEL", interval, tps)
    while True:
        time.sleep(0.02)
        controller.tick(curTick)
        if not flag:
            flag = 1
            setTimeOut(test, 2, f"test_{counting}")
        curTick += 1

if __name__ == "__main__":
    main()