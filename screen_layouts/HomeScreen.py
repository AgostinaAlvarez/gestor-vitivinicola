

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen,ScreenManager
from components.components import BoxLytComponent,StackComponent,HeaderComponent
from kivy.uix.scrollview import ScrollView
from kivy.uix.stacklayout import StackLayout
from api.api import get_tareas_home
from database.db import connect_to_db

class HomeScreennTaskCard (BoxLayout):
    pass


def getTasks():
    connection = connect_to_db()
    tasks = get_tareas_home(connection)
    return tasks

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #PRIMERA PANTALLA
        first_screen = Screen(name='home_first_screen')
        first_screen_scroll_view = ScrollView()
        first_screen_box_lyt = BoxLytComponent()
        first_screen_stack_lyt = StackComponent(spacing=dp(20))

        first_screen_header = HeaderComponent()
        first_screen_header.ids.header_icon.icon = 'home'
        first_screen_header.ids.header_label.text = 'Home Screen'

        btn1 = Button(text='Ir a la segunda pantalla', size_hint=(1,None),height=dp(100))
        btn1.bind(on_release=self.switch_second_screen)
        tasks = getTasks()
        print(tasks)
        for task in tasks:
            idTask, titulo, descripcion, fecha_creciacion, fecha_limite, prioridad, estado = task
            taskCard = HomeScreennTaskCard()
            titleTaskCard = Label(text=f"{titulo}",size_hint=(1,None),height=dp(40))
            priorityLbl = Label(text=f"Prioridad: {prioridad}",size_hint=(1,None),height=dp(40))
            stateLbl = Label(text=f"Estado: {estado}",size_hint=(1,None),height=dp(40))
            buttonTaskCard = Button(text='ver tarea',size_hint=(.8,None),height=dp(40),pos_hint={'center_x': 0.5})
            taskCard.add_widget(titleTaskCard)
            taskCard.add_widget(priorityLbl)
            taskCard.add_widget(buttonTaskCard)
            first_screen_stack_lyt.add_widget(taskCard)

        first_screen_box_lyt.add_widget(first_screen_header)

        first_screen_box_lyt.add_widget(btn1)
        first_screen_box_lyt.add_widget(first_screen_stack_lyt)
        first_screen_scroll_view.add_widget(first_screen_box_lyt)
        first_screen.add_widget(first_screen_scroll_view)

        #SEGUNDA PANTALLA
        second_screen = Screen(name='home_second_screen')
        second_screen_scroll_view = ScrollView()
        second_screen_box_lyt = BoxLytComponent()

        second_screen_header = HeaderComponent()
        second_screen_header.ids.header_icon.icon = 'home'
        second_screen_header.ids.header_label.text = 'segunda pantalla'

        btn2 = Button(text='Segunda pantalla', size_hint=(1,None),height=dp(100))
        btn3 = Button(text='Ir atras', size_hint=(1,None),height=dp(100))
        btn3.bind(on_release=self.switch_first_screen)


        second_screen_box_lyt.add_widget(second_screen_header)
        second_screen_box_lyt.add_widget(btn2)
        second_screen_box_lyt.add_widget(btn3)

        # Remover el componente de su padre actual antes de agregarlo a otro widget
        second_screen.remove_widget(second_screen_box_lyt)
        second_screen_scroll_view.add_widget(second_screen_box_lyt)
        second_screen.add_widget(second_screen_scroll_view)

        self.sm = ScreenManager()
        self.sm.add_widget(first_screen)
        self.sm.add_widget(second_screen)
        self.add_widget(self.sm)

    def switch_second_screen(self,instance):
        self.sm.current = 'home_second_screen'

    def switch_first_screen(self,instance):
        self.sm.current = 'home_first_screen'
