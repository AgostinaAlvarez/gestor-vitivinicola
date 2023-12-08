from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from database.db import connect_to_db
from api.api import get_viniedos
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
import uuid
from api.api import get_parcelas_by_viniedo, datos_viniedos
from database.db import connect_to_db

from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg

import matplotlib.pyplot as plt

class ScrollView(ScrollView):
    pass

class ViniedoScrInit (BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        btnTest = Button(text='hola',size_hint=(1,None),height=dp(100))
        self.add_widget(btnTest)

class ViniedoScrDetail (BoxLayout):
    pass

class ViniedoScrNew (BoxLayout):
    pass

#ESTAS SE QUEDAN

class HeaderViniedo(BoxLayout):
    pass


class ContainerBLScr (BoxLayout):
    pass

class CardViniedo(BoxLayout):
    pass

class CustomLabel(Label):
    pass

#--------
def get_data_viniedos ():
    conection = connect_to_db()
    dataViniedos = get_viniedos(conection)
    return dataViniedos

class ViniedoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        #Obtengo la data de los viniedos
        self.data = get_data_viniedos()

        print(self.data)
        #nuevo_uuid = uuid.uuid4()
        #print('id')
        #print(nuevo_uuid)

        # boton pata crear un nuevo vinedo
        btn_new = Button(text='nuevo vinedo', size_hint=(1, None), height=dp(40))
        btn_new.bind(on_release=self.switch_screen_new)

        # PANTALLA 1

        scr_vnd_list = Screen(name='scr_vnd_list')
        box_layout_1 = ContainerBLScr()
        header_pantalla1 = HeaderViniedo()
        header_pantalla1.ids.my_label.text = "Viniedos"  # Reemplaza 'my_label' con el id real de tu Label en el .kv
        box_layout_1.add_widget(header_pantalla1)
        box_layout_1.add_widget(btn_new)
        for user in self.data:
            id, nombre, superficie, localidad, pais, provincia = user
            #card
            card = CardViniedo()
            #contenido dentro de la card
            lbl_nombre = Label(text=nombre,color=(0,0,0,1), font_size=dp(18))
            lbl_ubi = Label(text=f"{provincia} - {localidad}", color=(0,0,0,1))
            btn_ver = Button(text="ver detalles",size_hint=(.8,None),pos_hint={'center_x':0.5},height=dp(40))
            btn_ver.bind(on_release=lambda instance, identificador=id: self.show_vinedo_details(identificador))  # Asociar función esto se asocia desde el lado de las funcionnes al botón

            card.add_widget(lbl_nombre)
            card.add_widget(lbl_ubi)
            card.add_widget(btn_ver)

            box_layout_1.add_widget(card)


            # Botón para abrir el modal
        btn_open_modal = Button(text="Abrir Modal",size_hint=(1,None),height=dp(40))
        btn_open_modal.bind(on_release=self.open_modal)
        box_layout_1.add_widget(btn_open_modal)

        box_scroll_1 = ScrollView()
        box_scroll_1.add_widget(box_layout_1)

        scr_vnd_list.add_widget(box_scroll_1)

        # Pantalla 2: scr_vnd_detail

        self.scr_vnd_detail = Screen(name='scr_vnd_detail')

        box_layout_2 = ContainerBLScr()
        self.header_name = HeaderViniedo()
        self.label_name = CustomLabel()
        self.label_sup = CustomLabel()
        self.label_ubi = CustomLabel()

        btn_go_back = Button(text="Volver atrás",size_hint=(1,None),height=dp(40))
        btn_go_back.bind(on_release=self.switch_screen_vnd)

        self.layoutCanv = BoxLayout(orientation='vertical', size_hint=(None, None), height=dp(500),width=dp(500))

        btnt = Button(text='test', size_hint=(1, None), height=dp(30))

        box_layout_2.add_widget(btn_go_back)
        box_layout_2.add_widget(self.header_name)
        box_layout_2.add_widget(self.label_name)
        box_layout_2.add_widget(self.label_ubi)
        box_layout_2.add_widget(self.label_sup)
        box_layout_2.add_widget(self.layoutCanv)
        box_layout_2.add_widget(btnt)


        self.box_scroll_2 = ScrollView()
        self.box_scroll_2.add_widget(box_layout_2)
        self.scr_vnd_detail.add_widget(self.box_scroll_2)

        #pantalla de nuevo vinedo
        self.scr_vinedo_new = Screen(name='scr_vinedo_new')
        box_layout_3 = BoxLayout(orientation='vertical')
        btn_test = Button(text='nuevo vinedp')
        box_layout_3.add_widget(btn_test)

        btn_volver_atras = Button(text='volver atras')
        btn_volver_atras.bind(on_release=self.switch_screen_vnd)
        box_layout_3.add_widget(btn_volver_atras)

        self.scr_vinedo_new.add_widget(box_layout_3)

        self.sm = ScreenManager()
        self.sm.add_widget(scr_vnd_list)
        self.sm.add_widget(self.scr_vinedo_new)
        self.sm.add_widget(self.scr_vnd_detail)

        self.add_widget(self.sm)
    def show_vinedo_details(self,identificador):
        #id del viniedo
        vinedo_id = identificador

        #conexion a la base de datos
        connection = connect_to_db()
        #info de las parcelas de este viniedo
        parcelas = get_parcelas_by_viniedo(connection,identificador)
        #mas data del viniedo
        viniedo_info = datos_viniedos(connection,identificador)

        # Iterar a través de la lista de datos
        for item in viniedo_info:
            # Verificar si la posición del polígono es None
            if item[-1] is None:
                print("La posición del POLYGON es nula")
                # Eliminar el canvas si existe en self.layoutCanv y reemplaza x unn label
                if self.layoutCanv.children:
                    self.layoutCanv.clear_widgets()
                self.layoutCanv.add_widget(Label(text='no hay',color=(0,0,0,1)))
            else:
                # Si no es nula, realizar las operaciones para obtener las coordenadas
                cadena_coordenadas = item[-1].split('((')[1].split('))')[0]
                #COORDENADAS DEL VINIEDO:
                coordenadas = [list(map(float, punto.split())) for punto in cadena_coordenadas.split(',')]
                colores_hex = ['#4F6F52','#86A789','#D6D46D','#A2C579','#4F6F52','#748E63','#748E63','#B0D9B1','#5C8374']

                # Separar coordenadas en x e y
                x = [coord[0] for coord in coordenadas]
                y = [coord[1] for coord in coordenadas]

                # Crear una figura de Matplotlib (La figura del viniedo)
                fig, ax = plt.subplots()
                # Colorear el área del polígono pertenneciente al viniedo
                ax.fill(x, y, '#9EC8B9')  # Cambia 'lightblue' por el color que desees
                for i, parcela in enumerate(parcelas):
                    coordenadas_str = parcela[-1]
                    if coordenadas_str is not None:
                        coordenadas_lista = coordenadas_str.split('((')[1].split('))')[0]
                        coordenadas_lista = [list(map(float, punto.split())) for punto in coordenadas_lista.split(',')]

                        x_parcela = [coord[0] for coord in coordenadas_lista]
                        y_parcela = [coord[1] for coord in coordenadas_lista]
                        # Asignar un color a la parcela
                        color = colores_hex[i % len(colores_hex)]
                        ax.fill(x_parcela, y_parcela, color)  #Rellena el área de la parcela

                # Ocultar etiquetas en el eje x
                ax.set_xticks([])  # Establece las marcas en blanco para ocultar las etiquetas del eje x
                # Ocultar etiquetas en el eje y
                ax.set_yticks([])  # Establece las marcas en blanco para ocultar las etiquetas del eje y

                # Crear un lienzo de Matplotlib para Kivy
                canvas = FigureCanvasKivyAgg(fig)

                # Eliminar el canvas si existe en self.layoutCanv
                if self.layoutCanv.children:
                    self.layoutCanv.clear_widgets()
                self.layoutCanv.add_widget(canvas)

        for vinedo in self.data:
            if vinedo[0] == vinedo_id:
                id, nombre, superficie, localidad, pais, provincia = vinedo
                self.header_name.ids.my_label.text = f"{nombre}"  # Reemplaza 'my_label' con el id real de tu Label en el .kv
                self.label_name.text = f"Nombre: {nombre}"
                self.label_sup.text = f"Superficie: {superficie} Hectareas"
                self.label_ubi.text = f"{localidad} - {provincia}"
                break
        self.sm.current = 'scr_vnd_detail'

    def switch_screen_vnd(self, instance):
        self.sm.current = 'scr_vnd_list'
    def switch_screen_new(self,instance):
        self.sm.current = 'scr_vinedo_new'
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

