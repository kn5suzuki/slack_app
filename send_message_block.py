import japanize_kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

from slack_tools import get_all_channels, create_channel_dict, send_message_to_channel
from widgets import MyDropdown, MyButton


class SelectChannelField(BoxLayout):
    def __init__(self, channel_names) -> None:
        super().__init__()
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 80

        self.label = Label(text='チャンネル', size_hint_x=None, width=200)
        self.dropdown = MyDropdown(
            channel_names)

        self.add_widget(self.label)
        self.add_widget(self.dropdown.main_button)


class MessageInputField(BoxLayout):
    def __init__(self) -> None:
        super().__init__()
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 200

        self.label = Label(text='メッセージ', size_hint_x=None, width=200)
        self.message_input = TextInput(multiline=True)

        self.add_widget(self.label)
        self.add_widget(self.message_input)


class SendMessageBlock(BoxLayout):
    def __init__(self, client, channels_list) -> None:
        super().__init__()
        self.client = client
        self.orientation = 'vertical'
        self.spacing = 20
        self.channel_dict = create_channel_dict(channels_list)

        self.select_channel_field = SelectChannelField(
            self.channel_dict.keys())
        self.message_input_field = MessageInputField()
        self.result_label = Label()

        self.add_widget(Label(text="機能1：メッセージ送信", size_hint_y=None, height=50))
        self.add_widget(self.select_channel_field)
        self.add_widget(self.message_input_field)
        self.add_widget(MyButton(text='送信', on_press=self.send_message,
                        height=80, width=300))
        self.add_widget(self.result_label)

    def send_message(self, instance):
        try:
            channel_id = self.channel_dict[self.select_channel_field.dropdown.main_button.text]
        except KeyError:
            self.result_label.text = "チャンネルを選択してください"
            return -1
        message = self.message_input_field.message_input.text
        if message == "":
            self.result_label.text = "メッセージを入力してください"
            return -1
        result = send_message_to_channel(
            self.client, channel_id=channel_id, message=message)
        self.select_channel_field.dropdown.main_button.text = '選択'
        self.message_input_field.message_input.text = ""
        self.result_label.text = result
