from pystray import Icon, Menu, MenuItem

from framework.live_data.live_data import LiveData
from framework.runtime.drive.setting_manager_impl import create_image, CheckableData

if __name__ == '__main__':
    image = create_image()

    ld = LiveData(False)


    def switch():
        ld.value = not ld.value


    icon = Icon(
        "test",
        image,
        menu=Menu(
            MenuItem("checkable", switch, checked=CheckableData(ld)),
            MenuItem("quit", quit),
        )
    )

    icon.run()
