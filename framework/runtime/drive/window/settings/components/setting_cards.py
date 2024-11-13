from typing import Union

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtGui import QIcon
from qfluentwidgets import *

from framework.live_data.live_data import LiveData, RangeLiveData
from framework.runtime.model_info import ModelInfo


class StyledSettingCard(SettingCard):

    def __init__(self, icon: Union[str, QIcon, FluentIconBase], title):
        super().__init__(icon, title)
        self.setContentsMargins(10, 10, 10, 10)


class SpinSettingCard(StyledSettingCard):

    def __init__(self, configItem: RangeLiveData, icon, title):
        super().__init__(icon, title)
        self.configItem = configItem
        sb = SpinBox()
        sb.setMinimumWidth(150)
        sb.setSingleStep(10)
        sb.setRange(*configItem.range)
        sb.setValue(configItem.value)
        self.hBoxLayout.addWidget(sb)

        sb.valueChanged.connect(self.setValue)

    def setValue(self, value):
        self.configItem.value = value


class DoubleSpinSettingCard(StyledSettingCard):

    def __init__(self, configItem: RangeLiveData, icon, title):
        super().__init__(icon, title)
        self.configItem = configItem
        dsb = DoubleSpinBox()
        dsb.setSingleStep(0.01)
        dsb.setRange(*configItem.range)
        dsb.setValue(configItem.value)
        self.hBoxLayout.addWidget(dsb)
        dsb.setMinimumWidth(150)

        dsb.valueChanged.connect(self.setValue)

    def setValue(self, value):
        self.configItem.value = value


class GroupItemDoubleSpin(QWidget):

    def __init__(self, configItem: RangeLiveData, title):
        super().__init__()
        self.configItem = configItem

        hBoxLayout = QHBoxLayout()
        hBoxLayout.setContentsMargins(48, 12, 48, 12)

        dsb = DoubleSpinBox()
        dsb.setMinimumWidth(150)
        dsb.setSingleStep(0.01)
        # TODO
        dsb.setRange(*configItem.range)
        dsb.setValue(configItem.value)

        hBoxLayout.addWidget(BodyLabel(title))
        hBoxLayout.addStretch(1)
        hBoxLayout.addWidget(dsb)

        self.setLayout(hBoxLayout)

        dsb.valueChanged.connect(self.setValue)

    def setValue(self, value):
        self.configItem.value = value


class ChangeModelSettingCard(StyledSettingCard):

    def __init__(self, configItem: LiveData, modelList: list[ModelInfo], icon, title):
        super().__init__(icon, title)
        self.configItem = configItem
        self.modelList = modelList

        self.cb = ComboBox()
        self.cb.addItems([i.name for i in modelList])
        self.cb.setCurrentText(configItem.value.name)
        self.btn_change = PrimaryPushButton("切换")
        self.btn_change.released.connect(self.changeModel)
        self.hBoxLayout.addWidget(self.cb)
        self.hBoxLayout.addSpacing(10)
        self.hBoxLayout.addWidget(self.btn_change)

    def changeModel(self):
        name = self.cb.currentText()
        model_info = None
        for mi in self.modelList:
            if mi.name == name:
                model_info = mi
                break
        if model_info is None:
            raise RuntimeError(f"no such model `{name}`")

        self.configItem.value = model_info


class TextSettingCard(StyledSettingCard):

    def __init__(self, configItem: LiveData, icon: Union[str, QIcon, FluentIconBase], title):
        super().__init__(icon, title)
        self.item = configItem
        self.lineEdit = LineEdit()
        self.lineEdit.setMinimumWidth(400)
        self.hBoxLayout.addWidget(self.lineEdit)
        self.lineEdit.setText(configItem.value)
        self.lineEdit.cursorPositionChanged.connect(self.setValue)

    def setValue(self, value):
        self.item.value = self.lineEdit.text()


class SliderSettingCard(StyledSettingCard):

    def __init__(self, configItem: RangeLiveData, icon: Union[str, QIcon, FluentIconBase], title):
        super().__init__(icon, title)
        self.configItem = configItem
        self.slider = Slider(Qt.Horizontal, self)
        self.valueLabel = QLabel(self)
        self.slider.setMinimumWidth(268)

        self.slider.setSingleStep(1)
        self.slider.setRange(*configItem.range)
        self.slider.setValue(configItem.value)
        self.valueLabel.setNum(configItem.value)

        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.valueLabel, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(6)
        self.hBoxLayout.addWidget(self.slider, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)

        self.valueLabel.setObjectName('valueLabel')
        self.slider.valueChanged.connect(self.setValue)

    def setValue(self, value):
        self.configItem.value = value
        self.valueLabel.setNum(value)
