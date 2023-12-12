from kivy.config import Config
# Obtener las dimensiones de la pantalla
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '850')


from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
from screen_layouts.HomeScreen import HomeScreen
from screen_layouts.VInedosScren import ViniedosScreen
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp



class MainScreen (BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def switch_screen(self,screen_name):
        #cambiar la pantalla que se ve
        self.ids.screen_manager.current = screen_name

class MainVitiApp(MDApp):
    def build(self):
        return MainScreen()



MainVitiApp().run()