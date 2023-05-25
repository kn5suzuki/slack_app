import japanize_kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color

import threading

from slack_tools import create_channel_dict, get_channel_members, get_conversations_list, create_members_dict, send_response
from widgets import MyDropdown, TextScrollView, WidgetScrollView, SelectAndActionField, InputField

class ConversationElement(BoxLayout):
    def __init__(self, client, member_dict, channel_id, channel_members, text, ts, reactors) -> None:
        super().__init__()
        self.size_hint_y = None
        with self.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect, size=self.update_rect)

        self.client = client
        self.member_dict = member_dict
        self.channel_id = channel_id
        self.channel_members = channel_members
        self.text = text
        self.ts = ts
        self.reactors = reactors
        self.add_widget(Label(text=self.extract_text(self.text)))
        self.add_widget(
            Label(text=f'リアクション:{len(self.reactors)}/{len(self.channel_members)}'))
        self.add_widget(Button(text="詳細", size_hint_x=None,
                        width=200, on_press=self.show_detail))
        self.add_widget(Button(text="リマインド", size_hint_x=None,
                        width=200, on_press=self.send_reminder))

    def extract_text(self, text):
        if not text:
            return ""

        lines = text.split('\n')
        if len(lines) >= 3:
            lines = [line[:20] for line in lines[:2]]
            return '\n'.join(lines)
        else:
            lines = [line[:20] for line in lines]
            return '\n'.join(lines)

    def show_detail(self, instance):
        conversation_detail = self.parent.parent.parent.parent.conversation_detail
        conversation_detail.clear_widgets()
        text_field = TextScrollView(height=150, do_scroll_x=True)
        text_field.set_text(self.text)
        reactors_field = TextScrollView(height=150)
        reactors_text = "リアクションした人\n"
        for reactor in self.reactors:
            reactors_text += f'・{self.member_dict[reactor]}\n'
        reactors_field.set_text(reactors_text)
        conversation_detail.add_widget(text_field)
        conversation_detail.add_widget(reactors_field)

    def send_reminder(self, instance):
        result = self.parent.parent.parent.parent.result
        mention_list = []
        for member in self.channel_members:
            if member not in self.reactors:
                mention_list.append(member)
        send_response(self.client, self.channel_id,
                      self.ts, "リアクションお願いします！", mention_list)
        result.text = "リマインドを送信しました"

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class RemindReactionBlock(BoxLayout):
    def __init__(self, client, channels_list, members_list) -> None:
        super().__init__()
        self.client = client
        self.orientation = 'vertical'
        self.spacing = 20
        self.padding = (10, 20, 10, 20)  # left, top, right, bottom
        self.member_info = members_list
        self.channel_dict = create_channel_dict(channels_list)
        self.member_dict = create_members_dict(members_list)

        self.add_widget(Label(text="機能2：メッセージを検索し、リアクションがない人にリマインド", size_hint_y=None, height=50))

        self.input_keyword_field = InputField("キーワード", multiline=False, default_text="【集計対象】")
        self.add_widget(self.input_keyword_field)

        self.select_channel_field = SelectAndActionField('チャンネル', self.channel_dict.keys(), '情報を取得', self.get_channel_information)
        self.add_widget(self.select_channel_field)

        # self.button = MyButton(text='チャンネル情報を取得', on_press=self.get_members,
        #                        height=80, width=300)
        # self.add_widget(self.button)

        self.members_field = TextScrollView(height=200)
        self.add_widget(self.members_field)

        self.conversations_field = WidgetScrollView(height=600)
        self.add_widget(self.conversations_field)

        self.conversation_detail = BoxLayout()
        self.add_widget(self.conversation_detail)

        self.result = Label()
        self.add_widget(self.result)


    def get_channel_information(self, instance):
        self.conversations_field.my_clear_widgets()
        channel_members = []
        try:
            channel_id = self.channel_dict[self.select_channel_field.dropdown.main_button.text]
        except KeyError:
            self.members_field.set_text("チャンネルを選択してください")
            return -1
        all_channel_members = get_channel_members(self.client, channel_id)
        conversations = get_conversations_list(self.client, channel_id)
        channel_members = []
        members_text = ""
        for member in all_channel_members:
            member_name = self.member_dict[member]
            if member_name:
                members_text += f'{member_name}\n'
                channel_members.append(member)
        self.members_field.set_text(members_text)
        for conversation in conversations:
            text = conversation["text"]
            ts = conversation["ts"]
            if self.input_keyword_field.get_input() in text:
                reactors = []
                if 'reactions' in conversation:
                    for reaction in conversation['reactions']:
                        reactors += reaction['users']
                self.conversations_field.my_add_widget(
                    ConversationElement(self.client, self.member_dict, channel_id, channel_members, text, ts, reactors))
