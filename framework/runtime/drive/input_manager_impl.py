import glfw

from framework.constant import Mouse
from framework.runtime.core.input_manager import InputManager, MouseEvent
from framework.runtime.core.manager import Manager
from framework.runtime.core.window_manager import WindowManager


class InputManagerImpl(InputManager):

    def __init__(self):
        super().__init__()
        self.handle = None
        self.lastClickAtX = None
        self.lastClickAtY = None
        self.moved = False

    def doInitialize(self):
        wm: WindowManager = Manager.getManager(WindowManager.name)
        self.handle = wm.getWindow("scene").handle
        glfw.set_mouse_button_callback(self.handle, self.dispatchMouseButtonEvent)

    def processInput(self):
        self.detectMouseMotion()
        glfw.poll_events()

    def detectMouseMotion(self):
        x, y = glfw.get_cursor_pos(self.handle)
        me = MouseEvent()
        me.x = x
        me.y = y
        me.type = Mouse.Event.MOVE
        self.dispatchMouseEvent(me)

        # 还未释放鼠标
        if self.lastClickAtX is not None and self.lastClickAtY is not None:
            v = self.wPos.value
            dx = x - self.lastClickAtX
            dy = y - self.lastClickAtY
            self.wPos.value = (int(v[0] + dx), int(v[1] + dy))
            if dx > 2 or dy > 2:  # 防止移动窗口时触发 对话框
                self.moved = True

    def dispatchMouseButtonEvent(self, _, button, action, __):
        if action == glfw.RELEASE:
            if not self.moved:
                x, y = glfw.get_cursor_pos(self.handle)
                if self.lastClickAtX is None or self.lastClickAtY is None:
                    return
                # 不是 移动窗口的操作 并且 鼠标没有移动过（长按移动视为取消点击）
                if abs(x - self.lastClickAtX) < 5 and abs(y - self.lastClickAtY) < 5:
                    me = MouseEvent()
                    me.x = x
                    me.y = y
                    me.type = Mouse.Event.RELEASE
                    if button == glfw.MOUSE_BUTTON_LEFT:
                        me.button = Mouse.Button.LEFT
                    elif button == glfw.MOUSE_BUTTON_RIGHT:
                        me.button = Mouse.Button.RIGHT
                    elif button == glfw.MOUSE_BUTTON_MIDDLE:
                        me.button = Mouse.Button.MIDDLE
                    self.dispatchMouseEvent(me)
            # 鼠标释放，代表一次操作执行完毕，重置变量
            self.lastClickAtX = None
            self.lastClickAtY = None
            self.moved = False
        elif action == glfw.PRESS:
            self.lastClickAtX, self.lastClickAtY = glfw.get_cursor_pos(self.handle)

    def makeTransparent(self, value):
        pass
