from slack_sdk.web import WebClient
from dotenv import load_dotenv
import os
import japanize_kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from kivy.logger import Logger, LOG_LEVELS

from app_tools.send_message_block import SendMessageBlock
from app_tools.remind_reaction_block import RemindReactionBlock
from app_tools.remind_reply_block import RemindReplyBlock

from slack_tools import get_active_sorted_channels, get_all_members
from app_tools.widgets import InputAndActionField, MyButton

Logger.setLevel(LOG_LEVELS["warning"])
Config.set('kivy', 'log_level', 'warning')
class Header(BoxLayout):
    def __init__(self, manager) -> None:
        super().__init__()
        self.manager = manager
        self.size_hint_y = None
        self.height = 80
        self.orientation = 'horizontal'
        self.add_widget(Button(text='機能1',
                        on_press=self.go_to_screen1))
        self.add_widget(Button(text='機能2',
                        on_press=self.go_to_screen2))
        self.add_widget(Button(text='機能3',
                        on_press=self.go_to_screen3))

    def go_to_screen1(self, *args):
        self.manager.current = 'screen1'

    def go_to_screen2(self, *args):
        self.manager.current = 'screen2'

    def go_to_screen3(self, *args):
        self.manager.current = 'screen3'

class Top(Screen):
    def __init__(self, decide_token_field, **args):
        super().__init__(**args)

        self.wrapper = BoxLayout(orientation='vertical')
        self.wrapper.add_widget(Label(text='Welcome to App!', font_size="30pt", size_hint_y=None, height=1000))
        self.wrapper.add_widget(decide_token_field)

        self.add_widget(self.wrapper)

class Screen1(Screen):
    def __init__(self, client, channels_list, **args):
        super().__init__(**args)
        self.add_widget(SendMessageBlock(client, channels_list))


class Screen2(Screen):
    def __init__(self, client, channels_list, members_list, **args):
        super().__init__(**args)
        self.add_widget(RemindReactionBlock(
            client, channels_list, members_list))


class Screen3(Screen):
    def __init__(self, client, channels_list, members_list, **args):
        super().__init__(**args)
        self.add_widget(RemindReplyBlock(
            client, channels_list, members_list))


class MyApp(App):
    def __init__(self) -> None:
        super().__init__()

    def build(self):
        Window.size = (1000, 800)

        self.decide_token_field = BoxLayout(orientation='vertical')
        self.input_token_field = InputAndActionField('トークン', '決定', self.decide_token)
        self.error_field = Label(text='')

        self.decide_token_field.add_widget(self.input_token_field)
        self.decide_token_field.add_widget(self.error_field)

        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(Top(self.decide_token_field, name="top"))
        self.wrapper = BoxLayout(orientation='vertical', spacing=20)
        self.wrapper.add_widget(self.screen_manager)
        return self.wrapper

    def decide_token(self, instance):
        self.client = WebClient(token=self.input_token_field.get_input())
        self.channels_list = get_active_sorted_channels(self.client)
        self.members_list = get_all_members(self.client)

        self.screen_manager.add_widget(Screen1(self.client, self.channels_list, name="screen1"))
        self.screen_manager.add_widget(
            Screen2(self.client, self.channels_list, self.members_list, name="screen2"))
        self.screen_manager.add_widget(
            Screen3(self.client, self.channels_list, self.members_list, name="screen3"))
        self.screen_manager.current = 'screen1'

        self.wrapper.clear_widgets()
        self.wrapper.add_widget(Header(self.screen_manager))
        self.wrapper.add_widget(self.screen_manager)


if __name__ == '__main__':
    app = MyApp()
    app.run()
