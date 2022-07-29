from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivymd.uix.list import OneLineListItem



Window.size = (360, 600)
parameters_list = ['theme', 'port', 'load file', 'download an api', 'edit']
class PocketApi(Screen):
    pass

class Parameters(Screen):
    pass

class Edit(Screen):
    pass

sm = ScreenManager()
sm.add_widget(PocketApi(name='pocket-api'))
sm.add_widget(Parameters(name='parameters'))


class PocketApiApp(MDApp):
    def set_port():
        pass
    def set_theme():
        pass
    def load_file():
        pass
    def download_api():
        pass
    def edit():
        pass
    def build(self):
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.primary_hue = '200'
        screen = Builder.load_file("app.kv")
        return screen

    def set_screen(self, next_screen):
        self.root.current = next_screen

    def on_start(self):
        paramscreen = MDApp.get_running_app().root.get_screen('parameters')
        for i in range(5):
            item = OneLineListItem(text='Item ' + str(i))
            item.bind(on_release= lambda x: print(i))
            paramscreen.ids.parameters.add_widget(item)
    
    

PocketApiApp().run()