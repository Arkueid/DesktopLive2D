from chat.data.entity import Message
from config import Configuration
from ui.components.design.chat_settings_design import ChatSettingsDesign


class ChatSettings(ChatSettingsDesign):

    def __init__(self, config: Configuration):
        super().__init__(config)
        self.config = config

        self.setObjectName("api_settings")

    def setup(self):
        self.updateArchive()

    def updateArchive(self):
        self.messageArchive.setChatIds(Message.chatIds(), Message.DataSource)
