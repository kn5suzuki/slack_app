import japanize_kivy
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import datetime, time

from slack_tools import create_channel_dict, get_channel_members, get_conversations_list, create_members_dict, get_replies_list
from app_tools.widgets import TextScrollView, SelectAndActionField, InputField, SelectField


class CountKeywordBlock(BoxLayout):
    def __init__(self, client, channels_list, members_list) -> None:
        super().__init__()
        self.client = client
        self.orientation = 'vertical'
        self.spacing = 20
        self.padding = (10, 20, 10, 20)  # left, top, right, bottom
        self.member_info = members_list
        self.channel_dict = create_channel_dict(channels_list)
        self.member_dict = create_members_dict(members_list)

        self.add_widget(Label(text="機能4：チャンネル内で各メンバーが特定のメッセージを何回発言したかカウントする", size_hint_y=None, height=50))

        self.input_keyword_field = InputField("キーワード", multiline=False, default_text="")
        self.add_widget(self.input_keyword_field)

        self.select_month_field = SelectField('月', [f'{i}' for i in range(1, 13)])
        self.add_widget(self.select_month_field)

        self.select_channel_field = SelectAndActionField('チャンネル', self.channel_dict.keys(), '検索', self.get_channel_information)
        self.add_widget(self.select_channel_field)

        # self.button = MyButton(text='チャンネル情報を取得', on_press=self.get_members,
        #                        height=80, width=300)
        # self.add_widget(self.button)
        self.result_field = TextScrollView(height=1000)
        self.add_widget(self.result_field)

        self.result = Label()
        self.add_widget(self.result)


    def get_channel_information(self, instance):
        self.result_field.delete_text()
        channel_members = []
        try:
            channel_id = self.channel_dict[self.select_channel_field.dropdown.main_button.text]
        except KeyError:
            self.members_field.set_text("チャンネルを選択してください")
            return -1
        try:
            all_channel_members = get_channel_members(self.client, channel_id)
            conversations = get_conversations_list(self.client, channel_id)
        except Exception as e:
            self.members_field.set_text(f"検索に失敗しました\n{e}")
            return -1

        channel_members = {member: 0 for member in all_channel_members}
        target_month = datetime.datetime.strptime(self.select_month_field.get_input(), "%m").month
        target_word = self.input_keyword_field.get_input()
        for conversation in conversations:
            text = conversation["text"]
            ts = conversation["ts"]
            created_date = datetime.datetime.fromtimestamp(float(ts))
            if created_date.month == target_month:
                try:
                    channel_members[conversation["user"]] += text.count(target_word)
                    print(conversation["user"], text, text.count(target_word))
                    replies = get_replies_list(self.client, channel_id, ts)
                    for reply in replies:
                        text = reply["text"]
                        channel_members[reply["user"]] += text.count(target_word)
                except Exception as e:
                    print(e)
            time.sleep(0.1)

        sorted_result = sorted(channel_members.items(), key=lambda x: x[1], reverse=True)
        results_text = ""
        for member, count_result in sorted_result:
            if self.member_dict[member]:
                results_text += f'{self.member_dict[member]}: {count_result}回\n'
        self.result_field.set_text(results_text)
