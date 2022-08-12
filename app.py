import json
import threading
from tkinter.tix import FileSelectBox
import requests
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from kivymd.uix.list import OneLineListItem
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.filemanager import MDFileManager
import socket
import datetime


Window.size = (360, 600)
class PocketApi(Screen):
    pass

class Parameters(Screen):
    pass

class Edit(Screen):
    pass

class PortDialogContent(BoxLayout):
    pass

class ChooseTheme(BoxLayout):
    pass

class DownloadApi(BoxLayout):
    pass

sm = ScreenManager()
sm.add_widget(PocketApi(name='pocket-api'))
sm.add_widget(Parameters(name='parameters'))


class PocketApiApp(MDApp):
    dict = {'port': 5555, 'data': {}}
    def choose_port(self, obj):
            self.dialog = MDDialog(text= 'Port', type= 'custom', content_cls = PortDialogContent(),
                                    buttons= [MDFlatButton(text= 'Cancel', on_release=self.close_dialog), MDFlatButton(text= 'Choose', on_release=self.set_port)],)
            self.dialog.open()
    def close_dialog(self, obj):
        self.dialog.dismiss()
    def set_port(self, obj):
        port_num = self.dialog.content_cls.ids.portNumber.text
        if len(port_num)<1:
            return
        elif int(port_num) < 1024 or int(port_num) > 65535:
            self.dialog.content_cls.ids.portNumber.error = True
            return
        else:
            self.dict['port'] = int(port_num)
            self.dialog.dismiss()

    def set_theme(self, obj):
        theme = self.theme_cls.theme_style
        self.dialog = MDDialog(text= 'Port', type= 'custom', content_cls = ChooseTheme(),
                                    buttons= [MDFlatButton(text= 'ok', on_release=self.close_dialog)],)
        if theme == 'Light':
            self.dialog.content_cls.ids.checkLight.active =True
        else:
            self.dialog.content_cls.ids.checkDark.active = True
        self.dialog.open()
    

    def light_mode(self):
        self.theme_cls.theme_style = "Light"

    def dark_mode(self):
        self.theme_cls.theme_style = "Dark"


    def load_file(self, obj):
        path = '/'
        self.manager_open = False
        self.file_manager = MDFileManager(exit_manager= self.exit_manager, select_path= self.select_path)
        self.file_manager.show(path)


    def download_api(self, obj):
        self.dialog = MDDialog(text= 'Get API', type= 'custom', content_cls = DownloadApi(),
                                    buttons= [MDFlatButton(text= 'Cancel', on_release=self.close_dialog), MDFlatButton(text= 'Download', on_release=self.download)],)
        self.dialog.open()

    def select_path(self, path):
        try:
            with open(path, 'r') as f:
                self.dict['data']= json.load(f)
        except Exception as e:
            MDDialog(text= f'{e}').open()

        self.exit_manager()

    def select_folder(self, path):
        if not self.file_name:
            self.file_name = '\data.json'
        try:
            with open(path+f'\{self.file_name}', 'w') as f:
                json.dump(self.json_content, f)
        except Exception as e:
            MDDialog(text= f'{e}').open()
        self.exit_manager()
        self.close_dialog(self)
   
    def create_api(self):
        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM)
        host = socket.gethostbyname(socket.gethostname())
        try:
            sock.bind((host, self.dict['port']))
        except Exception as e:
            MDDialog(text= f'{e}').open()
            self.running = False
            return

        while self.running:
            data = json.dumps(self.dict['data'])
            date = datetime.datetime.today()
            headers_data = f'HTTP/1.1 200 OK\r\nDate: {date}\r\nServer: pocket-api socket server\r\nContent-Type: application/json; charset = utf-8\r\n\r\n{data}'.encode('Utf8')
            sock.listen(5)
            client, addr= sock.accept()
            client.recv(1024)
            client.send(headers_data)
            client.close()

    def run_api(self):
        self.running = True
        self.thread = threading.Thread(target=self.create_api, daemon=True)
        self.thread.start()
        self.main_screen = self.root.get_screen('pocket-api')
        self.button = self.main_screen.ids.api_button
        self.button.text = 'stop server'
        self.button.on_release = self.stop_api
        host = socket.gethostbyname(socket.gethostname())
        port = self.dict.get('port')
        self.main_screen.ids.local.text = f'localhost:{port}'
        self.main_screen.ids.network.text = f'{host}:{port}'

        

        


    def stop_api(self):
        self.running = False
        self.thread.join(timeout= 2.0)
        self.button.text = 'run server'
        self.button.on_release = self.run_api
        self.main_screen.ids.local.text = ''
        self.main_screen.ids.network.text = ''

    

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()

    def download(self, obj):
        url = self.dialog.content_cls.ids.urlEntry.text
        self.file_name = self.dialog.content_cls.ids.fileName.text
        try:
            content = requests.get(url).content
            self.json_content = json.loads(content)
            self.file_manager = MDFileManager(exit_manager = self.exit_manager, select_path= self.select_folder)
            self.file_manager.show('/')
        except Exception as e:
            MDDialog(text= f'{e}').open()



    def set_screen(self, next_screen):
        self.root.current = next_screen

    def edit_screen(self, obj):
        editscreen = self.root.get_screen('edit')
        editscreen.ids.code_input.text =  json.dumps(self.dict.get('data'))
        self.root.current = 'edit'

    def edit_data(self):
        editscreen = self.root.get_screen('edit')
        new_data = editscreen.ids.code_input.text
        try:
            self.dict['data']= json.loads(new_data)
            self.root.current = 'pocket-api'
        except Exception as e:
            MDDialog(text= f'Warning json format is not valid: {e}').open()
            return

    def build(self):
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.primary_hue = '200'
        screen = Builder.load_file("app.kv")
        return screen

    def on_start(self):
        parameters_list = {'Select theme': self.set_theme, 'Set port': self.choose_port, 'Edit data': self.edit_screen, 'Download an API': self.download_api, 'Load file': self.load_file}
        paramscreen = self.root.get_screen('parameters')
        for key in parameters_list:
            paramscreen.ids.parameters.add_widget(OneLineListItem(text= key,on_press= parameters_list.get(key)))
     

PocketApiApp().run()