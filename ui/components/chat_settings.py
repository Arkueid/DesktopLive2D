from ui.components.design.api_settings_design import ApiSettingsDesign
from config import Configuration
from ui.components.design.icon_design import IconDesign


class ApiSettings(ApiSettingsDesign):

    def __init__(self, config: Configuration):
        super().__init__(config)
        self.config = config

        self.setObjectName("api_settings")

    def setup(self):
        pass
