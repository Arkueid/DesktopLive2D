from qfluentwidgets import ExpandGroupSettingCard, FluentIcon, RangeSettingCard, RangeConfigItem, RangeValidator

from framework.live_data.live_data import BiasRangeLiveData, RangeLiveData
from framework.runtime.app_config import Configuration
from framework.runtime.drive.window.settings.components.base_designs import ScrollDesign
from framework.runtime.drive.window.settings.components.icon_design import IconDesign
from framework.runtime.drive.window.settings.components.setting_cards import SpinSettingCard, \
    GroupItemDoubleSpin, DoubleSpinSettingCard, SliderSettingCard


class AppSetting(ScrollDesign, IconDesign):

    def __init__(self, appConfig: Configuration):
        super().__init__()
        self.resource_dir = appConfig.resourceDir.value

        self.card_width = SpinSettingCard(BiasRangeLiveData(appConfig.windowSize, (0, 65535), 0),
                                          self.icon("width.svg"), "画布宽度")
        self.card_height = SpinSettingCard(BiasRangeLiveData(appConfig.windowSize, (0, 65535), 1),
                                           self.icon("height.svg"), "画布高度")
        self.card_fps = SpinSettingCard(RangeLiveData(appConfig.fps, (30, 120)), self.icon("fps.svg"), "FPS")

        self.card_group_drawCenter = ExpandGroupSettingCard(self.icon("draw_center.svg"), "绘制中心")
        self.card_group_drawCenter.setContentsMargins(20, 10, 20, 10)
        self.card_drawX = GroupItemDoubleSpin(BiasRangeLiveData(appConfig.drawPos, (-2.0, 2.0), 0), "X")
        self.card_drawY = GroupItemDoubleSpin(BiasRangeLiveData(appConfig.drawPos, (-2.0, 2.0), 1), "Y")
        self.card_group_drawCenter.addGroupWidget(self.card_drawX)
        self.card_group_drawCenter.addGroupWidget(self.card_drawY)

        self.card_motion_interval = SpinSettingCard(RangeLiveData(appConfig.motionInterval, (-1, 65535)),
                                                    self.icon("motion_interval.svg"), "动作频率")
        self.card_lip_sync = DoubleSpinSettingCard(RangeLiveData(appConfig.lipSyncN, (0, 65535)), FluentIcon.SETTING,
                                                   "口型同步幅度")
        self.card_scale = DoubleSpinSettingCard(RangeLiveData(appConfig.scale, (0.1, 65535)), self.icon("scale.svg"),
                                                "缩放比例")
        self.card_volume = SliderSettingCard(RangeLiveData(appConfig.volume, (0, 100)), self.icon("volume.svg"), "音量")
        self.card_volume.setContentsMargins(10, 10, 20, 10)

        self.vBoxLayout.addWidget(self.card_width)
        self.vBoxLayout.addWidget(self.card_height)
        self.vBoxLayout.addWidget(self.card_fps)
        self.vBoxLayout.addWidget(self.card_group_drawCenter)
        self.vBoxLayout.addWidget(self.card_motion_interval)
        self.vBoxLayout.addWidget(self.card_lip_sync)
        self.vBoxLayout.addWidget(self.card_scale)
        self.vBoxLayout.addWidget(self.card_volume)
