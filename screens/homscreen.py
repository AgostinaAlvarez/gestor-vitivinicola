from kivy.uix.stacklayout import StackLayout
from kivy.metrics import dp
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from datetime import datetime
from database.db import connect_to_db
from api.api import get_tareas_home
from kivy.uix.modalview import ModalView

class HeaderScreen (BoxLayout):
    pass



class CustomLabel (Label):
    pass


class TareaCard (BoxLayout):
    pass

def fecha_de_hoy():
    fecha_actual = datetime.today()

    # Diccionario para mapear los nombres de los días de la semana y meses
    dias_semana = [
        'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'
    ]

    meses = [
        'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
        'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
    ]

    # Obtener el día de la semana, el día del mes y el mes
    nombre_dia_semana = dias_semana[fecha_actual.weekday()]
    numero_dia_mes = fecha_actual.day
    nombre_mes = meses[fecha_actual.month - 1]  # Restamos 1 porque los índices de la lista comienzan desde 0

    # Obtener el año
    anio = fecha_actual.year

    # Formatear la fecha como "Día de la semana día de mes de año"
    fecha_formateada = f"{nombre_dia_semana} {numero_dia_mes} de {nombre_mes} de {anio}"

    return fecha_formateada

def get_tareas_programadas():
    conection = connect_to_db()
    dataTareas = get_tareas_home(conection)
    return dataTareas

class HomeScreen (BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        dataTareas = get_tareas_programadas()
        print('estas sonn las tareas')
        print(dataTareas)
        fecha_formateada = fecha_de_hoy()

        header = HeaderScreen()
        self.add_widget(header)

        lblDate = CustomLabel(text=fecha_formateada,color=(0, 0, 0, 1))
        self.add_widget(lblDate)

        lblRend = CustomLabel(text='Rendimientos',color=(0, 0, 0, 1))
        self.add_widget(lblRend)

        lblTasks = CustomLabel(text='Tareas programadas',color=(0, 0, 0, 1))
        self.add_widget(lblTasks)

        for tarea in dataTareas:
            idTarea, nombre, descipcion, fecha_creacion, fecha_limite, prioridad, estado = tarea
            #bxLyt = BoxLayout(size_hint=(1,None),height=dp(200),orientation='vertical')
            bxLyt = TareaCard()
            lblNombre = Label(text=nombre, color=(0,0,0,1))
            lblPrioridad = Label(text="prioridad:"+prioridad, color=(0,0,0,1))
            lblEstado = Label(text=estado, color=(0,0,0,1))
            btnVer = Button(text='ver',size_hint=(1,None),height=dp(40))
            btnVer.bind(on_release=self.open_modal)
            bxLyt.add_widget(lblNombre)
            bxLyt.add_widget(lblPrioridad)
            bxLyt.add_widget(lblEstado)
            bxLyt.add_widget(btnVer)
            self.add_widget(bxLyt)

        margn = Label(size_hint=(1,None),height=dp(50))
        self.add_widget(margn)

    def open_modal(self, instance):
        modal = ModalView(size_hint=(None, None), size=(800, 500))
        modalBox = BoxLayout(orientation='vertical')
        modal_label = Label(text="Esto es un modal")
        modal_button = Button(text="Cerrar modal")
        modal_button.bind(on_release=modal.dismiss)
        modalBox.add_widget(modal_label)
        modalBox.add_widget(modal_button)
        modal.add_widget(modalBox)
        modal.open()
