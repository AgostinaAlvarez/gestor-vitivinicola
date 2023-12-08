from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from screens.viniedoscreen import ViniedoScreen
from screens.homscreen import HomeScreen
from database.db import connect_to_db,fetch_data_from_table
from api.api import get_viniedos
import uuid
class MainScreen (BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def switch_screen(self, screen_name):
        self.ids.scr_mngr.current = screen_name  # Cambiar a la pantalla especificada por el nombre

class MainApp(MDApp):
    def build(self):
        return MainScreen()

MainApp().run()