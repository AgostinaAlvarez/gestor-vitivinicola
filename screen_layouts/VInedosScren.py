

from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.uix.scrollview import ScrollView
from components.components import BoxLytComponent,StackComponent,HeaderComponent
from kivy.metrics import dp
from kivy.uix.button import Button
from api.api import get_viniedos,datos_viniedos,get_parcelas_by_viniedo,datos_parcela,datos_parcela_prueba
from database.db import connect_to_db
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt
from kivymd.uix.datatables import MDDataTable


def getViniedos ():
    connection = connect_to_db()
    viniedos = get_viniedos(connection)
    return viniedos

def getViniedoDetail(identificador):
    connection = connect_to_db()
    datosViniedo = datos_viniedos(connection,identificador)
    return datosViniedo


def getParcelas (identificador):
    connection = connect_to_db()
    parcelas = get_parcelas_by_viniedo(connection,identificador)
    return parcelas

def getDataParcela (identificador):
    connection = connect_to_db()
    dataParcela = datos_parcela(connection, identificador)
    return dataParcela

class ViniedoCard (BoxLayout):
    pass

class ViniedoDetail (BoxLayout):
    pass

class ViniedosScreen (Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        viniedos = getViniedos()
        print('viniedos')
        print(viniedos)
        #PRIMERA PANTALLA

        first_screen = Screen(name='viniedos_first_screen')
        first_screen_scroll_view = ScrollView()
        first_screen_box_lyt = BoxLytComponent()

        first_screen_header = HeaderComponent()
        first_screen_header.ids.header_icon.icon = 'land-plots'
        first_screen_header.ids.header_label.text = 'Viniedos Screen'


        #componente stack layout:
        first_screen_stack_lyt = StackComponent(spacing=dp(20))

        for viniedo in viniedos:
            idViniedo, nombre, superficie, provincia, localidad, pais = viniedo
            card = ViniedoCard()
            title_card = Label(text=f"{nombre}", size_hint=(1, None), height=dp(40))
            ubi_card = Label(text=f"{provincia} {localidad}", size_hint=(1, None), height=dp(40))
            btn_card = Button(text="ver", size_hint=(.8, None), height=dp(40), pos_hint={'center_x': 0.5})
            btn_card.bind(on_release=lambda instance, identificador=idViniedo: self.show_vinedo_details(identificador))

            card.add_widget(title_card)
            card.add_widget(ubi_card)
            card.add_widget(btn_card)
            first_screen_stack_lyt.add_widget(card)

        first_screen_box_lyt.add_widget(first_screen_header)
        first_screen_box_lyt.add_widget(first_screen_stack_lyt)

        first_screen_scroll_view.add_widget(first_screen_box_lyt)

        first_screen.add_widget(first_screen_scroll_view)


        #SEGUNDA PANTALLA
        detail_screen = Screen(name='viniedos_detail_screen')
        #scroll component
        detail_screen_scroll_view = ScrollView()
        #box component
        self.detail_screen_box_lyt = BoxLytComponent()

        self.detail_screen_header = HeaderComponent()
        self.detail_screen_header.ids.header_icon.icon = 'land-plots'
        self.detail_screen_header.ids.header_label.text = 'Viniedo..'

        self.detail_screen_box_lyt.add_widget(self.detail_screen_header)
        btnVolverAtras = Button(text="volver atras",size_hint=(1,None),height=dp(50))
        btnVolverAtras.bind(on_release=self.switch_first_screen)
        self.detail_screen_box_lyt.add_widget(btnVolverAtras)

        #STACK LAYOUT PARA EL COSO DEBAJO DEl HEADER
        self.detail_screen_detailstack = StackComponent()
        #columna izquierda
        self.detail_screen_detailstack_left = ViniedoCard(width=dp(500))
        self.detail_screen_detailstack_left_ttl = Label(size_hint=(1,None),height=dp(30),color=(0,0,0,1),text="Datos:")
        self.detail_screen_detailstack_left_ubi = Label(size_hint=(1,None),height=dp(30),color=(0,0,0,1))
        self.detail_screen_detailstack_left_sup = Label(size_hint=(1,None),height=dp(30),color=(0,0,0,1))
        self.detail_screen_detailstack_left.add_widget(self.detail_screen_detailstack_left_ttl)
        self.detail_screen_detailstack_left.add_widget(self.detail_screen_detailstack_left_ubi)
        self.detail_screen_detailstack_left.add_widget(self.detail_screen_detailstack_left_sup)

        #columna derecha
        self.detail_screen_detailstack_right = BoxLayout(orientation='vertical', size_hint=(None, None), height=dp(500), width=dp(600))


        self.detail_screen_detailstack.add_widget(self.detail_screen_detailstack_left)
        self.detail_screen_detailstack.add_widget(self.detail_screen_detailstack_right)

        self.detail_screen_box_lyt.add_widget(self.detail_screen_detailstack)

        #------------

        #Esto es lo q va despues:
        btnTest = Button(text="boton de pueba",size_hint=(1,None),height=dp(50))
        self.detail_screen_box_lyt.add_widget(btnTest)

        #listado de parcelas
        self.detail_screen_parcelas_label = Label(text="Parcelas:",color=(0,0,0,1),size_hint=(1,None),height=dp(40))
        self.detail_screen_box_lyt.add_widget(self.detail_screen_parcelas_label)

        self.detail_screen_parcelas_stack = StackComponent()

        self.detail_screen_box_lyt.add_widget(self.detail_screen_parcelas_stack)
        #tabla de actividades

        self.detail_screen_data_tables = MDDataTable(
            size_hint=(1, None),
            height= dp(400),
            use_pagination=True,
            check=True,
            # name column, width column, sorting function column(optional), custom tooltip
            column_data=[
                ("Parcela", dp(30)),
                ("Nombre", dp(60)),
                ("Descripcion", dp(30)),
                ("Fecha Inicio", dp(30)),
                ("Fecha Finalizacion", dp(30)),

            ],
        )
        self.detail_screen_box_lyt.add_widget(self.detail_screen_data_tables)


        detail_screen.remove_widget(self.detail_screen_box_lyt)
        detail_screen_scroll_view.add_widget(self.detail_screen_box_lyt)
        detail_screen.add_widget(detail_screen_scroll_view)


        #Tercera pantalla

        parcela_screen = Screen(name='parcela_detail_screen')
        parcela_screen_scroll_view = ScrollView()
        self.parcela_screen_box_lyt = BoxLytComponent()

        self.parcela_screen_header = HeaderComponent()

        self.parcela_screen_box_lyt.add_widget(self.parcela_screen_header)

        self.parcela_screen_ubi = Label(color=(0,0,0,1),size_hint=(1,None),height=dp(40))
        self.parcela_screen_localidad = Label(color=(0,0,0,1),size_hint=(1,None),height=dp(40))
        self.parcela_screen_sup = Label(color=(0,0,0,1),size_hint=(1,None),height=dp(40))

        self.testbbt = Button(text='volver atras',size_hint=(1,None),height=dp(50))

        self.landTypes = StackComponent()

        self.actividadesParcelas = MDDataTable(
            size_hint=(.9, None),
            pos_hint={'center_x': 0.5},
            height=dp(400),
            use_pagination=True,
            check=True,
            # name column, width column, sorting function column(optional), custom tooltip
            column_data=[
                ("Descripcion", dp(60)),
                ("Detalle", dp(60)),
                ("Fecha Inicio", dp(40)),
                ("Fecha Finalizacion", dp(40)),
                ("Estado", dp(30))
            ],
            row_data=[]
        )



        self.parcela_screen_box_lyt.add_widget(self.testbbt)
        self.parcela_screen_box_lyt.add_widget(self.parcela_screen_localidad)
        self.parcela_screen_box_lyt.add_widget(self.parcela_screen_ubi)
        self.parcela_screen_box_lyt.add_widget(self.parcela_screen_sup)
        self.parcela_screen_box_lyt.add_widget(self.landTypes)
        self.parcela_screen_box_lyt.add_widget(self.actividadesParcelas)


        parcela_screen_scroll_view.add_widget(self.parcela_screen_box_lyt)
        parcela_screen.add_widget(parcela_screen_scroll_view)


        self.sm = ScreenManager()
        #AGREGAR EL SCREEENN DE LA SEGUNNDA PANTALLA POR ESO SE ROMPE //HREF DEL VINIEDO SCREEN = self.pantalla_dos
        self.sm.add_widget(first_screen)
        self.sm.add_widget(detail_screen)
        self.sm.add_widget(parcela_screen)
        self.add_widget(self.sm)


    def show_vinedo_details(self,identificador):
        #id del viniedo
        vinedo_id = identificador
        viniedo = getViniedoDetail(vinedo_id)
        print(viniedo)
        parcelas = getParcelas(vinedo_id)
        print(parcelas)

        self.detail_screen_header.ids.header_label.text = f"{viniedo[0][1]}"
        self.detail_screen_detailstack_left_ubi.text = f"{viniedo[0][3]} - {viniedo[0][4]} ({viniedo[0][5]})"
        self.detail_screen_detailstack_left_sup.text = f"Superficie: {viniedo[0][2]} Hectareas"
        self.parcela_screen_localidad.text = f"{viniedo[0][3]} - {viniedo[0][4]} ({viniedo[0][5]})"
        if(viniedo[0][6] is None):
            print('no hay coordenadas')
            if self.detail_screen_detailstack_right:
                self.detail_screen_detailstack_right.clear_widgets()
            self.detail_screen_detailstack_right.add_widget(Label(text="no hay mapa disponible",color=(0,0,0,1)))

        else:
            print('si hay coordenadas')
            cadena_coordenadas = viniedo[0][6].split('((')[1].split('))')[0]
            print('cadena de coordenadas')
            print(cadena_coordenadas)
            coordenadas = [list(map(float, punto.split())) for punto in cadena_coordenadas.split(',')]
            print('coordenadas:')
            print(coordenadas)
            colores_hex = ['#4F6F52', '#86A789', '#D6D46D', '#A2C579', '#4F6F52', '#748E63', '#748E63', '#B0D9B1',
                           '#5C8374']

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

                    ax.fill(x_parcela, y_parcela, color,label=parcela[2])  # Rellena el área de la parcela

            ax.legend(loc='upper left')
            # Ocultar etiquetas en el eje x
            ax.set_xticks([])  # Establece las marcas en blanco para ocultar las etiquetas del eje x
            # Ocultar etiquetas en el eje y
            ax.set_yticks([])  # Establece las marcas en blanco para ocultar las etiquetas del eje y

            # Crear un lienzo de Matplotlib para Kivy
            canvas = FigureCanvasKivyAgg(fig)
            canvas.size_hint= (1,1)
            if self.detail_screen_detailstack_right:
                self.detail_screen_detailstack_right.clear_widgets()

            self.detail_screen_detailstack_right.add_widget(canvas)

        self.detail_screen_parcelas_stack.clear_widgets()

        for parcela in parcelas:
            id_parcela, id_viniedo, nombre, superficie, latitud, longitud, coordenadas = parcela
            parcelaConteiner = ViniedoCard(size_hint=(.5,None))
            parcelaName = Label(text=f"{nombre}",size_hint=(1,None),height=dp(30))
            parcelaSup = Label(text=f"Superficie: {superficie} Hectareas",size_hint=(1,None),height=dp(30))
            parcelaVerBtn = Button(text="ver parcela", size_hint=(.8,None),height=dp(30),pos_hint={'center_x': 0.5} )
            #parcelaVerBtn.bind(on_release=lambda instance: self.show_parcela_detail(idViniedo=vinedo_id, parcela=parcela))  # Asociar función esto se asocia desde el lado de las funcionnes al botón
            parcelaVerBtn.bind(on_release=lambda instance, p=parcela: self.show_parcela_detail(idViniedo=vinedo_id, parcela=p))

            #agregar elementos para el card
            parcelaConteiner.add_widget(parcelaName)
            parcelaConteiner.add_widget(parcelaSup)
            #parcelaConteiner.add_widget(parcelaUbi)
            parcelaConteiner.add_widget(parcelaVerBtn)
            self.detail_screen_parcelas_stack.add_widget(parcelaConteiner)

        self.sm.current = 'viniedos_detail_screen'

    def switch_first_screen (self,instance):
        self.sm.current = 'viniedos_first_screen'


    def show_parcela_detail(self,idViniedo,parcela):
        print('parceela')
        print(parcela)
        print(parcela[0])
        datosParcela = getDataParcela(parcela[0])
        print('data de la parcela')
        print(datosParcela)
        suelosData = datosParcela["suelos"]
        tareasData = datosParcela["tareas"]


        self.landTypes.clear_widgets()
        for suelos in suelosData:
            nombre, descripcion, composicion, drenaje, pH, retencionAgua, texturaSuelo, capacidadAireacion, propiedadesViticultura = suelos
            cardSuelo = ViniedoCard(size_hint=(.5,None))
            nombreLbl = Label(size_hint=(1,None),height=dp(30),text=f"{nombre}",color=(0,0,0,1))
            descripcionLbl = Label(text=f"{descripcion}",size_hint_y=None, height=dp(100), text_size=(600, None), halign='center')
            composicionLbl = Label(size_hint=(1,None),height=dp(30),text=f"Composicion: {composicion}",color=(0,0,0,1))
            drenajeLbl = Label(size_hint=(1,None),height=dp(30),text=f"Drenaje: {drenaje}",color=(0,0,0,1))
            phLabel = Label(size_hint=(1,None),height=dp(30),text=f"pH: {pH}",color=(0,0,0,1))
            retencionLbl = Label(size_hint=(1,None),height=dp(30),text=f"Retencion de Agua: {retencionAgua}",color=(0,0,0,1))
            texturaSueloLbl = Label(size_hint=(1,None),height=dp(30),text=f"Textura de Suelo: {texturaSuelo}",color=(0,0,0,1))
            capacidadAireacionLbl = Label(size_hint=(1,None),height=dp(30),text=f"Capacidad de Aireacion: {capacidadAireacion}",color=(0,0,0,1))
            propiedadesViticulturaLbl = Label(text=f"{propiedadesViticultura}",size_hint_y=None, height=dp(130), text_size=(600, None), halign='center')

            cardSuelo.add_widget(nombreLbl)
            cardSuelo.add_widget(descripcionLbl)
            cardSuelo.add_widget(composicionLbl)
            cardSuelo.add_widget(drenajeLbl)
            cardSuelo.add_widget(phLabel)
            cardSuelo.add_widget(retencionLbl)
            cardSuelo.add_widget(texturaSueloLbl)
            cardSuelo.add_widget(capacidadAireacionLbl)
            cardSuelo.add_widget(propiedadesViticulturaLbl)

            self.landTypes.add_widget(cardSuelo)


        # Luego, asignar los nuevos datos (tareasData) a row_data de la tabla
        self.actividadesParcelas.row_data = tareasData

        self.parcela_screen_header.ids.header_label.text = parcela[2]
        self.parcela_screen_ubi.text = f"{parcela[5]}, {parcela[4]}"
        self.parcela_screen_sup.text = f"Superficie: {parcela[3]} Hectareas"

        self.testbbt.bind(on_release=lambda instance, identificador=idViniedo: self.show_vinedo_details(identificador))# Asociar función esto se asocia desde el lado de las funcionnes al botón

        self.sm.current = 'parcela_detail_screen'
