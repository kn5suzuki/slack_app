from kivy.uix.widget import Widget
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput


class MyDropdown(Widget):
    def __init__(self, options) -> None:
        super().__init__()
        self.dropdown = DropDown()
        self.options = options
        for option in self.options:
            btn = Button(text=option, size_hint_y=None, height=50)
            btn.bind(on_release=lambda btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(btn)
        self.main_button = Button(text='選択')
        self.main_button.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=self.on_dropdown_select)

    def on_dropdown_select(self, dropdown, value):
        self.main_button.text = value

    def get_value(self):
        return self.main_button.text

class MyButton(BoxLayout):
    def __init__(self, text, on_press, height=80, width=100) -> None:
        super().__init__()
        self.size_hint_y = None
        self.height = height
        self.add_widget(Label())
        self.add_widget(Button(text=text, on_press=on_press,
                        size_hint_x=None, width=width))
        self.add_widget(Label())

class TextScrollView(BoxLayout):
    def __init__(self, height=300, do_scroll_x=False, do_scroll_y=True) -> None:
        super().__init__()
        self.size_hint_y = None
        self.height = height
        # self.scroll_view = BoxLayout(size_hint_y=None, height=height)
        self.content = ScrollView(
            do_scroll_x=do_scroll_x, do_scroll_y=do_scroll_y)
        self.label = Label()
        if do_scroll_x:
            self.label.size_hint_x = None
        if do_scroll_y:
            self.label.size_hint_y = None
        self.label.bind(texture_size=self.label.setter('size'))
        self.content.add_widget(self.label)
        self.add_widget(self.content)

    def set_text(self, text):
        self.label.text = text

    def add_text(self, text):
        self.label.text += text

    def delete_text(self):
        self.label.text = ""


class WidgetScrollView(BoxLayout):
    def __init__(self, height=300) -> None:
        super().__init__()
        self.size_hint_y = None
        self.height = height

        self.content = ScrollView()
        self.layout = BoxLayout(
            orientation='vertical', size_hint_y=None, spacing=5)
        self.layout.bind(minimum_height=self.layout.setter('height'))
        self.content.add_widget(self.layout)
        self.add_widget(self.content)

    def my_add_widget(self, widget):
        self.layout.add_widget(widget)

    def my_clear_widgets(self):
        self.layout.clear_widgets()

class InputField(BoxLayout):
    def __init__(self, label, multiline=False, default_text="", height=80) -> None:
        super().__init__()
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = height

        self.label = Label(text=label, size_hint_x=None, width=200)
        self.input = TextInput(text=default_text, multiline=multiline)

        self.add_widget(self.label)
        self.add_widget(self.input)

    def get_input(self):
        return self.input.text

class InputAndActionField(BoxLayout):
    def __init__(self, label, button_text, on_press, multiline=False, default_text="", height=80) -> None:
        super().__init__()
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = height

        self.on_press = on_press

        self.label = Label(text=label, size_hint_x=None, width=200)
        self.input = TextInput(text=default_text, multiline=multiline)
        self.button = Button(text=button_text, size_hint_y=None,
                             size_hint_x=None, height=height, width=200, on_press=self.on_press)

        self.add_widget(self.label)
        self.add_widget(self.input)
        self.add_widget(self.button)

    def get_input(self):
        return self.input.text

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

class SelectField(BoxLayout):
    def __init__(self, label, options) -> None:
        super().__init__()
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 80

        self.label = Label(text=label, size_hint_x=None, width=200)
        self.dropdown = MyDropdown(options)

        self.add_widget(self.label)
        self.add_widget(self.dropdown.main_button)

    def get_input(self):
        return self.dropdown.get_value()

class SelectAndActionField(BoxLayout):
    def __init__(self, label, options, text, on_press, height=80) -> None:
        super().__init__()
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = height

        self.on_press = on_press

        self.label = Label(text=label, size_hint_x=None, width=200)
        self.dropdown = MyDropdown(options)
        self.button = Button(text=text, size_hint_y=None,
                             size_hint_x=None, height=height, width=200, on_press=self.on_press)

        self.add_widget(self.label)
        self.add_widget(self.dropdown.main_button)
        self.add_widget(self.button)