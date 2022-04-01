from kivymd.app import MDApp
from kivy.lang import Builder

kv = """
Screen:
    MDTextField:
        hint_text: 'Enter you password'
        helper_text: 'Forgot your password?'
        helper_text_mode: "on_focus" 
        pos_hint: {'center_x': 0.5, 'center_y': 0.7}
        size_hint_x: None
        width: 300
        icon_right: "account-search"
        required: True
    MDLabel:
        text: ""
        id: txt
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
    MDRaisedButton:
        text: 'Action Button'
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        on_press:
            app.action()
    MDRoundFlatButton:
        text: 'MDRoundFlatButton'
        pos_hint: {'center_x': 0.5, 'center_y': 0.4}
    MDRectangleFlatButton:
        text: 'MDRectangleFlatButton'
        pos_hint: {'center_x': 0.5, 'center_y': 0.3}
    MDRectangleFlatIconButton:
        text: 'MDRectangleFlatIconButton'
        pos_hint: {'center_x': 0.5, 'center_y': 0.2}
        width: dp(230)
        icon: 'google'
    MDFillRoundFlatIconButton:
        text: 'MDFillRoundFlatIconButton'
        pos_hint: {'center_x': 0.5, 'center_y': 0.1}
        width: dp(230)
        icon: 'google'
    MDFloatingActionButtonSpeedDial:
        data: app.data
        rotation_root_button: True
    BoxLayout:
        orientation: 'vertical'
        MDToolbar:
            title: "MDToolbar"
            left_action_items: [["menu", lambda x: nav_draw.set_state()]]
        Widget:

    MDNavigationDrawer:
        id: nav_draw
        orientation: "vertical"
        padding: "8dp"
        spacing: "8dp"

        AnchorLayout:
            anchor_x: "left"
            size_hint_y: None
            height: avatar.height
            Image:
                id: avatar
                size_hint: None, None
                size: "56dp", "56dp"
                source: "data/logo/kivy-icon-256.png"
        MDLabel:
            text: "Kaustubh Gupta"
            font_style: "Button"
            size_hint_y: None
            height: self.texture_size[1]

        MDLabel:
            text: "youreamil@gmail.com"
            font_style: "Caption"
            size_hint_y: None
            height: self.texture_size[1]

        ScrollView:
            MDList:
                OneLineAvatarListItem:
                    on_press:
                        nav_draw.set_state("close")
                    text: "Home"
                    IconLeftWidget:
                        icon: "home"
                OneLineAvatarListItem:
                    on_press:
                        nav_draw.set_state("close")
                    text: "About"
                    IconLeftWidget:
                        icon: 'information'

        Widget:
"""


class Main(MDApp):
    data = {
        'language-python': 'Python',
        'language-php': 'PHP',
        'language-cpp': 'C++',
    }

    def action(self):
        label = self.root.ids.txt
        label.text = "This text is displayed after pressing button"

    def build(self):
        return Builder.load_string(kv)


Main().run()