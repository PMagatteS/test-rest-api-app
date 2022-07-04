from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDFillRoundFlatButton

Window.size = (360, 600)

s ="""
Screen:
    BoxLayout:
        orientation: 'vertical'
        MDToolbar:
            title: 'Rest api'"""

class PocketApiApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.primary_hue = '200'
        label = MDLabel(text= 'build your api', halign= 'center',theme_text_color= 'Primary', text_color= (0,0,1,1))
        button = MDFillRoundFlatButton(text= 'test button', halign= 'center')
        screen = Builder.load_file("app.kv")
        #screen.add_widget(label)
        #screen.add_widget(button)
        return screen
PocketApiApp().run()