import time

from framework.handler.looper import Looper
from framework.live_data.live_data import LiveData
from framework.runtime.core.kizuna.waifu import Waifu
from framework.runtime.drive.kizuna.kizuna_impl import KizunaImpl
from framework.runtime.drive.looper.looper_impl_qt import QtLooper

if __name__ == '__main__':
    # 伪造 main looper
    Looper("main", manualStart=True).start()

    QtLooper().start()
    kizuna = KizunaImpl()

    print(Looper.loopers())

    Waifu.link()
    wf = Waifu.create("kasumi", "kasumi的性格描述", "你好呀")
    lwf = LiveData(wf)
    kizuna.initialize(lwf)
    kizuna.ruleBreak(wf)  # choose a waifu
    kizuna.recall(kizuna.waifus[wf.name].mids[0])
    # 等待 qt 线程响应
    time.sleep(1)
    kizuna.tell()

    for i in range(100):
        print(i + 1)
        time.sleep(1)

    kizuna.suspend()
