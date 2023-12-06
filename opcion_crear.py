

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
from just_the_module import Save_module
##from main import *

def crear(root):# esta es la ventana de recepción de datos

    def on_enter(event):
        event.widget.invoke()

    def libreac():
        nonlocal entries
        def reac_selected(event):
            selected_option = reac_var.get()
            datos_reac = reactivos_cargados[selected_option]
            entries[0].delete(0,tk.END)
            entries[1].delete(0,tk.END)
            entries[2].delete(0,tk.END)
            entries[0].insert(tk.END,selected_option)
            entries[1].insert(tk.END,datos_reac["descripcion"])
            entries[2].insert(tk.END,datos_reac["peligro"])
        # PASO 1) CARGAR LOS DATOS DE UN ARCHIVO JSON
        with open('reactivos.json', 'r') as archivo:
            reactivos_cargados = json.load(archivo)
        lista_reactivos = list(reactivos_cargados)
        # PASO 2) SE CONTRUYE LA VENTANA
        lib_window = tk.Toplevel(second_window)
        lib_window.title(f"Libreria de reactivos PETRA")
        # WIDGETS
        #   LABEL
        lib_label = tk.Label(lib_window, text="Que reactivo desea agregar?", font=('Arial', 9)) # ETIQUETA
        lib_label.grid(row=0, column=0, padx=(5, 5), pady=(5, 5))
        reac_var = tk.StringVar()
        #   COMBOBOX-------------------------------------------------------------------------------------------------------------------------------------------------
        combo_reactivos = ttk.Combobox(lib_window, textvariable=reac_var, values=lista_reactivos)
        combo_reactivos.current(0)
        combo_reactivos.bind("<<ComboboxSelected>>", reac_selected)# en un combobox, la funcion trigger lleva "event" como argumento
        combo_reactivos.grid(row=1, column=0, padx=(5, 5), pady=(5, 5))
    def excelizar():
        nonlocal producto_actual,name
        no = no_prod_entry.get()
        name = name_prod_entry.get()
        f = Save_module()
        f.active_module(name,no,producto_actual)
    def option_selected(event): # ESTA FUNCION ES PARA EL COMBOBOX: REACTIVO, PASO, BANNER
        selected_option = opciones_var.get()
        
        for widget in option_frames.values():# PRIMERO SE BORRAN LOS WIDGETS
            widget.grid_forget()

        if selected_option == lista_opciones[0]:# Reactivos
            option_frames[lista_opciones[0]].grid(row=row, column=0, columnspan=2)
        elif selected_option == lista_opciones[1]:# Paso
            option_frames[lista_opciones[1]].grid(row=row, column=0, columnspan=2)
        elif selected_option == lista_opciones[2]:# Banner
            option_frames[lista_opciones[2]].grid(row=row, column=0, columnspan=2)

    def agregar_treeview_func():# ESTA FUNCION INICIALIZA EL TREEVIEW: BOTON:
        nonlocal counter, local_memory, chopciones, treeview_data, treeview, name
        # Entrys
        name = name_prod_entry.get()
        no = no_prod_entry.get()
        picto = picto_prod_entry.get()
        etiq = etiq_prod_entry.get()
        mues = mues_prod_entry.get()
        # Habilitar botones
        br.config(state=tk.NORMAL)
        bp.config(state=tk.NORMAL)
        bb.config(state=tk.NORMAL) 
        seleccion = []
        for opcion, valor in chopciones.items():
            if valor.get():
                seleccion.append(opcion)
            # Insert treeview data
        if name == "":
            tk.messagebox.showwarning(title="Campos vacios", message="No ha dado nombre al producto")
        elif no == "":
            tk.messagebox.showwarning(title="Campos vacios", message="No ha dado numero de inventario")
        elif etiq == "":
            tk.messagebox.showwarning(title="Campos vacios", message="No ha dado envase de producto")
        elif mues == "":
            tk.messagebox.showwarning(title="Campos vacios", message="No ha dado envase de control de calidad")
        elif len(seleccion) == 0:# SI EL ARRAY ESTA VACIO...
            tk.messagebox.showwarning(title="Campos vacios", message="No ha dado equipo de fabricación")
        else: # SI EL ENTRY DE NAME NO ESTÁ VACÍO
            if counter > 1:# Si counter no es el primer elemento, no hagas nada
                pass
            else:# SI EL CONTADOR ES 1 O 0
                if len(treeview_data) > 0 and len(treeview_data) < 4:
                    print("Si funcioné")
                    treeview_data = []
                    for item in treeview.get_children():
                        treeview.delete(item)
                treeview_data.append(["","end",counter,name,(no,picto,"","")])
                # ------------------ HOT NEW --------------------
                # ¿COMO AÑADIR UN PRIMER DATO A UN DICCIONARIO
                # EL PRIMER DATO AÑADIDO AL DICCIONARIO
                local_memory[name] = {"informacion":{'no inv':no,'pictogramas':picto}}
                # ¿COMO AÑADIR UN SEGUNDO Y N-ESIMO DATO A UN DICCIONARIO
                # EL DATO POSTERIOR AL PRIMERO
                
                local_memory[name]["Equipo a utilizar"] = {"Equipo a utilizar":f"{', '.join(seleccion)}"}
                treeview_data.append([1,"end",counter+1,"Equipo a utilizar",(seleccion[0],"","","")])
                treeview_data.append([1,"end",counter+2,"Envase",(etiq,mues,"","")])
                local_memory[name]["Envase"] = {"Envase_producto":etiq,"Envase_control":mues}
                
                print(local_memory)
                for item in treeview_data:
                    treeview.insert(parent=item[0], index=item[1], iid=item[2], text=item[3], values=item[4])
                    if item[0] == "" :
                        treeview.item(item[2], open=True) # Open parents
                counter += 3
                
    def agregar_r():# Cuando el boton Reactivo es seleccionado
        for widget in option_frames.values():
            widget.grid_forget()
        option_frames[lista_opciones[0]].grid(row=row, column=0, columnspan=2)
    def agregar_p():# Cuando el boton Reactivo es seleccionado
        for widget in option_frames.values():
            widget.grid_forget()
        option_frames[lista_opciones[1]].grid(row=row, column=0, columnspan=2)
    def agregar_b():# Cuando el boton Reactivo es seleccionado
        for widget in option_frames.values():
            widget.grid_forget()
        option_frames[lista_opciones[2]].grid(row=row, column=0, columnspan=2)
    def agregar_reactivo():# ESTA FUNCION AGARRA LA INFO EN LAS ENTRYBOXES DE REACTIVOS
        nonlocal counter, treeview, treeview_data, name, local_memory
        if counter == 1:# Si este es el primer elemento
            pass
        else:
            data = []
            for i,entry in enumerate(entries):
                data.append(entry.get())
            if data[1] == '':
                data[1] = "Sin descripcion"
            if data[2] == '':
                data[2] = "0"
            treeview.insert(parent=1,index="end",iid=counter,text=data[0],values=(data[1],data[2],data[3],data[4]))
            treeview_data.append(["1","end",counter,data[0],(data[1],data[2],data[3],data[4])])
            local_memory[name][data[0]] = {"descripcion":data[1],
                                           "peligro":data[2],
                                           "indicacion":data[3],
                                           "revision":data[4]}
        counter += 1
        element_counter.append("r")
        print(local_memory)

    def agregar_paso():
        nonlocal counter_paso, counter, treeview, treeview_data, element_counter, name, local_memory # utiliza el la variable que esta afuera de este metodo
        texto = paso_texto.get(1.0, "end-1c")
##        print(texto)
        treeview.insert(parent=1,index="end",iid=counter,text=f"Paso {counter_paso}",values=(texto))
        treeview_data.append(["1","end",counter,f"Paso {counter_paso}",(texto,"","","")])
        local_memory[name][f"Paso {counter_paso}"] = {"texto":texto}
        counter_paso += 1
        counter += 1
        element_counter.append("p")
        
    def agregar_banner():
        nonlocal counter_banner, counter, treeview, treeview_data, element_counter
        selected_option = banners_var.get()
##        print(selected_option)
        treeview.insert(parent=1,index="end",iid=counter,text=f"Banner {counter_banner}",values=(selected_option))
        treeview_data.append(["1","end",counter,f"Banner {counter_banner}",(selected_option,"","","")])
        local_memory[name][f"Banner {counter_banner}"] = selected_option
        counter_banner += 1
        counter += 1
        element_counter.append("b")

    def remove_last_item():
        nonlocal element_counter, counter_banner, counter_paso, la_borracion
        print('----------- borrar elemento ----------------')
        print(f'contador de elementos {element_counter}')
        print(f'counter_paso:{counter_paso}')
        selected_item = treeview.selection()  # Obtener el ítem seleccionado
        print(f'selected item : {selected_item[-1]}')
        print(int(selected_item[0]))
##        print(selected_item[0],element_counter)
        if int(selected_item[0]) > 3:
            if element_counter[int(selected_item[0])-4-la_borracion] == "b":
                counter_banner -= 1
                del element_counter[int(selected_item[0])-4-la_borracion]
    ##            element_counter.remove(int(selected_item[0])-1)
            elif element_counter[int(selected_item[0])-4-la_borracion] == "p":
                counter_paso -= 1
                del element_counter[int(selected_item[0])-4-la_borracion]
    ##            element_counter.remove(int(selected_item[0])-1)
            if selected_item:
                treeview.delete(selected_item[-1])  # Eliminar el último ítem seleccionado
            la_borracion += 1
        else:
            tk.messagebox.showwarning(title="Campos fijos", message="No se pueden borrar esos campos")   
    def actualizar_seleccion():
        nonlocal chopciones
        seleccion = []
        for opcion, valor in chopciones.items():
            if valor.get():
                seleccion.append(opcion)
        resultado.config(text=f"Seleccionaste: {', '.join(seleccion)}")
        
    def vaciar_treeview(): # Función para vaciar el TreeView

        nonlocal  treeview, counter_banner, counter_paso, treeview_data
        # Elimina todos los elementos del TreeView
        treeview.delete(*treeview.get_children())
        counter_banner = 0
        counter_paso = 0
        treeview_data
    def extract_treeview_data():
        nonlocal treeview, treeview_data, chopciones, producto_actual
        seleccion = []
        for opcion, valor in chopciones.items():
            if valor.get():
                seleccion.append(opcion)
        a = treeview.get_children()
        # NECESITAMOS ESCRIBIRLO EN FORMA DE DICCIONARIO
        with open('datos.json', 'r') as archivo:# extraer la info previa
            datos_cargados = json.load(archivo)# antigua info

        for i,item_id in enumerate(a):
            values = treeview.item(item_id, 'values')

        for i,j in enumerate(treeview_data):
            if i == 0: # Nombre del producto
                nombre_producto = j[3]
                datos_cargados[nombre_producto] = {}
                datos_cargados[nombre_producto]["Informacion"] = {'no inv':no_prod_entry.get(),'pictogramas':picto_prod_entry.get()}
            else:# ES REACTIVOS, PASOS Y BANNERS?
                if j[3][0] == '1' or j[3][0] == '2':
                    reactivo_nombre = j[3]  
                    descripcion = j[4][0]
                    peligro = j[4][1]
                    indicacion = j[4][2]
                    revision = j[4][3]
                    datos_cargados[nombre_producto][reactivo_nombre] = {
                                                    "descripcion":descripcion,
                                                    "peligro":peligro,
                                                    "indicacion":indicacion,
                                                    "revision":revision}
                if j[3][0] == 'P':
                    datos_cargados[nombre_producto][j[3]] = {"texto":j[4][0]}
                if j[3][0] == 'B':
                    banner = j[4][0][:2]
                    datos_cargados[nombre_producto][j[3]] = banner

        datos_cargados[nombre_producto]["Equipo a utilizar"] = {"Equipo a utilizar":f"{', '.join(seleccion)}"}
        envprod = etiq_prod_entry.get()
        envmues = mues_prod_entry.get()
        datos_cargados[nombre_producto]["Envase"] = {"Envase_producto":f"{envprod}" ,
                f"Envase_control":f"{envmues}"
                }
        producto_actual[nombre_producto] = datos_cargados[nombre_producto]
        with open('datos.json', 'w') as archivo:
            json.dump(datos_cargados,archivo)
        second_window.destroy()
    # ------PALETA DE COLORES---------------------------------------------------------------------------------------------------------------------------------------------------
    colores = ["#B5DEC9",
               "#9AC735",
               "#fc9fff",
               "#ff81e3",
               "#F3EBD4"
               ]
        
    # ------VARIABLES QUE CONTABILIZAN LOS BLOQUES DE TEXTO Y DE BANNERS--------------------------------------------------------------------------------------------------

    name = ''
    producto_actual = {}
    opciones_var = tk.StringVar() #GUARDA LAS VARIABLES DEL PRIMER COMBOBOX
    counter = 1             # CUENTA CUANTOS ELEMENTOS HAY EN EL TREEVIEW
    counter_paso = 1        # CUENTA EL NUMERO DE PASOS QUE HAY AGREGADOS AL TREEVIEW
    counter_banner = 1      # CUENTA EL NUMERO DE BANNERS QUE HAY AGREGADOS AL TREEVIEW
    treeview_data = []      # DONDE SE GUARDA LA INFORMACION MOSTRADA EN EL TREEVIEW    
    element_counter = []    # LISTA DE REGISTRO CUANDO SE AGREGA UN BANNER "b" O UN PASO "p"
    local_memory = {}       # DICCIONARIO DONDE SE GUARDAN TEMPORALMENTE LOSS CAMBIOS
    la_borracion = 0

    # ------WIDGETS DE MAIN WINDOW-------------------------------------------------------------------------------------------------------------------------------------------
        #                                                               FRAMES
    second_window = tk.Toplevel(root,bg="#046546")# 0
    second_window.title("Crear Metodo de Fabricación Estandar")
    # Make the app responsive
    second_window.columnconfigure(index=0, weight=1)
    second_window.columnconfigure(index=1, weight=1)
    second_window.columnconfigure(index=2, weight=1)
    second_window.rowconfigure(index=0, weight=1)
    second_window.rowconfigure(index=1, weight=1)
    second_window.rowconfigure(index=2, weight=1)
    data_n_tree = tk.Frame(second_window, bg="#9e9e9e") # 1
    data_n_tree.grid(row=0,column=0)
    botones = tk.Frame(second_window, bg="#9e9e9e")# 1
    botones.grid(row=2,column=0)
    datos = tk.Frame(data_n_tree, bg="#9e9e9e")# 2
    datos.grid(row=0,column=0)
    d1 = tk.LabelFrame(datos,text="Datos del producto",bg=colores[0])
    d1.grid(row=0,column=0,padx = 2, pady = 2)
    d2 = tk.Frame(datos,bg="#0D5A58")
    d2.grid(row=1,column=0)
    d3 = tk.LabelFrame(datos,text="Bloques",bg="#f0d943")
    d3.grid(row=2,column=0, padx=(5, 5), pady=(5, 5))
    d4 = tk.LabelFrame(d1,text="Equipo a utilizar",bg=colores[1])
    d4.grid(row=6,column=0)
    d5 = tk.Frame(d3,bg="#0D5A58")
    d5.grid(row=1,column=0)
    label = ttk.LabelFrame(datos, text="Crear Metodo de Fabricación Estandar")
    label.grid(row=0, column=0)
             
    # ------WIDGETS-------------------------------------------------------------------------------------------------------------------------------------------------------
        # NOMBRE DEL PRODUCTO                                           ENTRYS Y LABELS
    # ETIQUETA
    name_prod = tk.Label(d1, text="Nombre del productos", font=('Arial', 9),bg=colores[1],fg="#ffffff")
    name_prod.grid(row=1, column=0)
    # ENTRY        
    name_prod_entry = ttk.Entry(d1,font=("Helvetica",15))
    name_prod_entry.grid(row=1, column=1)
    # ----------------------------------------------------------------------
        # NO DE INVENTARIO
    # ETIQUETA
    no_prod = tk.Label(d1, text="No. Inv.", font=('Arial', 9),bg=colores[1],fg="#ffffff")
    no_prod.grid(row=2, column=0)
    # ENTRY                    
    no_prod_entry = ttk.Entry(d1,font=("Helvetica",15))
    no_prod_entry.grid(row=2, column=1)
    # ----------------------------------------------------------------------
        # PICTOGRAMA DEL PRODUCTO
    # ETIQUETA
    picto_prod = tk.Label(d1, text="Str pictogramas max 3", font=('Arial', 9),bg=colores[1],fg="#ffffff")
    picto_prod.grid(row=3, column=0)
    # ENTRY                    
    picto_prod_entry = ttk.Entry(d1,font=("Helvetica",15))
    picto_prod_entry.grid(row=3, column=1)
    # ----------------------------------------------------------------------
        # ENVASE 
    # ETIQUETA
    etiq_prod = tk.Label(d1, text="Envasar en: ", font=('Arial', 9),bg=colores[1],fg="#ffffff")
    etiq_prod.grid(row=4, column=0)
    # ENTRY                    
    etiq_prod_entry = ttk.Entry(d1,font=("Helvetica",15))
    etiq_prod_entry.grid(row=4, column=1)
    # ----------------------------------------------------------------------
        # PASAR MUESTRA EN 
    # ETIQUETA
    mues_prod = tk.Label(d1, text="Pasar Muestra en: ", font=('Arial', 9),bg=colores[1],fg="#ffffff")
    mues_prod.grid(row=5, column=0)
    # ENTRY                    
    mues_prod_entry = ttk.Entry(d1,font=("Helvetica",15))
    mues_prod_entry.grid(row=5, column=1)
    # ----------------------------------------------------------------------
        # CHebuttons menu: EQUIPO A UTILIZAR
    # CODIGO PROVISTO POR CHATGPT-------------------------------------------------------
    chopciones = {}
    chopcion1 = tk.Checkbutton(d4, text="Dispersor",bg=colores[1])
    chopcion2 = tk.Checkbutton(d4, text="Reactor",bg=colores[1])
    chopcion3 = tk.Checkbutton(d4, text="Tina",bg=colores[1])    
    chopcion4 = tk.Checkbutton(d4, text="Tambor de proceso",bg=colores[1])
    # Agregar las casillas de verificación al diccionario y asignarles una variable de control
    chopciones["Dispersor"] = tk.BooleanVar()
    chopciones["Reactor"] = tk.BooleanVar()
    chopciones["Tina"] = tk.BooleanVar()
    chopciones["Tambor de proceso"] = tk.BooleanVar()

    chopcion1.config(variable=chopciones["Dispersor"], command=actualizar_seleccion)
    chopcion2.config(variable=chopciones["Reactor"], command=actualizar_seleccion)
    chopcion3.config(variable=chopciones["Tina"], command=actualizar_seleccion)
    chopcion4.config(variable=chopciones["Tambor de proceso"], command=actualizar_seleccion)
    
    # Colocar las casillas de verificación en la ventana
    chopcion1.grid(row=0,column=0)
    chopcion2.grid(row=0,column=1)
    chopcion3.grid(row=1,column=0)
    chopcion4.grid(row=1,column=1)
    
    resultado = tk.Label(second_window, text="", pady=10)
    resultado.grid(row=1,column=0)

    #-------------------------------------------------------------------------------------------
    
    ###### AQUI EMPIEZA LA LISTA DE OPCIONES A AÑADIR AL TREEVIEW #######
        #Boton
    # Se agrega información al treeview de los d2 basicos
    name_no_picto_treeview = tk.Button(d2,text='Iniciar metodo',bg=colores[1],fg="#ffffff",command=agregar_treeview_func)
    name_no_picto_treeview.grid(row=5,column=1)
    name_no_picto_treeview.bind("<Return>", on_enter)
    opciones_label = tk.Label(d3, text="Añadir al metodo", font=('Arial', 9)) # ETIQUETA
    opciones_label.grid(row=0, column=0)
     
    option_frames = {}      # DICCIONARIO : AQUI GUARDAN WIDGETS TIPO FRAME
    row = 6                 # ULTIMA FILA LIBRE DESPUES DE LOS CAMPOS DE NOMBRE, NO DE INV, Y PICTOGRAMAS
    # --BOTONES: 'reactivo','texto','banner' --------------------------------------------------------------------------------------------------------------------
    br = tk.Button(d5,text="Reactivo",command=agregar_r,bg=colores[1], state=tk.DISABLED)
    br.grid(row=0, column=0)
    br.bind("<Return>", on_enter)
    bp = tk.Button(d5,text="Paso",command=agregar_p,bg=colores[1], state=tk.DISABLED)
    bp.grid(row=0, column=1)
    bp.bind("<Return>", on_enter)
    bb = tk.Button(d5,text="Banner",command=agregar_b,bg=colores[1], state=tk.DISABLED)
    bb.grid(row=0, column=2)
    bb.bind("<Return>", on_enter)
    # --COMBOBOX-------------------------------------------------------------------------------------------------------------------------------------------------
    lista_opciones = ['reactivo','texto','banner']
##    opciones = ttk.Combobox(d3, textvariable=opciones_var, values=lista_opciones)
##    opciones.current(0)
##    opciones.bind("<<ComboboxSelected>>", option_selected)
##    opciones.grid(row=0, column=1)
    # --COMBOBOX------------------------------------------------OPCION 1-----------------------------------------------------------------------------------------
    ############# Option 1 content                                                                      #REACTIVO
    option_frames[lista_opciones[0]] = tk.Frame(d3) # CAMPOS DE LA OPCION 1 "REACTIVOS"
    specs = ['No. Inv.','descripcion','pictogramas','indicaciones','revision']
    # LISTA DONDE SE GUARDA LAS VARIABLES INGRESADAS EN LOS ENTRIES DE LA OPCION 1
    entries = []
    for i,j in enumerate(specs):# PARA CADA ESPECIFICACION DE "REACTIVOS"...
        tk.Label(option_frames[lista_opciones[0]], text=j).grid(row=row+i, column=0)# AÑADES AL FRAME "REACTIVOS" UNA ETIQUETA...
        entry = tk.Entry(option_frames[lista_opciones[0]])# AÑADES AL FRAME "REACTIVOS" UN ENTRY...
        entry.grid(row=row+i, column=1)# SE POSICIONA EL ENTRY...
        entries.append(entry)# ESTE ENTRY TAMBIEN SE AÑADE A # LISTA DONDE SE GUARDA LAS VARIABLES INGRESADAS EN LOS ENTRIES DE LA OPCION 1
    # BOTON QUE AGREGA LA INFORMACION DE LOS CAMPOS DE LA OPCION REACTIVOS" AN TREEVIEW Y PROXIMAMENTE AL ARCHIVO 
    agr = tk.Button(option_frames[lista_opciones[0]],text="agregar",command=agregar_reactivo)
    agr.grid(row=row+len(specs), column=0)
    agr.bind("<Return>", on_enter)
    ttk.Button(option_frames[lista_opciones[0]],text="Libreria de Reactivos",command=libreac).grid(row=row+len(specs), column=1)
    # --COMBOBOX------------------------------------------------OPCION 2-----------------------------------------------------------------------------------------
    ############# Option 2 content                                                                      # TEXTO
    option_frames[lista_opciones[1]] = tk.Frame(d3)
    tk.Label(option_frames[lista_opciones[1]], text="Agregar texto").grid(row=row, column=0)# ETIQUETA
    paso_texto = tk.Text(option_frames[lista_opciones[1]],width=30,height=10)# WIDGET DE TEXTO
    paso_texto.grid(row=row, column=1)# POSICION DEL WIDGET
    # BOTON QUE AGREGA EL TEXTO AL TREEVIEW
    tk.Button(option_frames[lista_opciones[1]],text="agregar",command=agregar_paso).grid(row=row+len(specs), column=0)
    # --COMBOBOX------------------------------------------------OPCION 3-----------------------------------------------------------------------------------------
    ############# Option 3 content                                                                      # BANNER
    option_frames[lista_opciones[2]] = tk.Frame(d3)
    banners_var = tk.StringVar()
    # OPCIONES DE LOS BANNERS
    lista_banners = ['b1 BANNER DE PREPARACION ',
                     'b2 BANNER DE EPP',
                     'b3 BANNER DE PESE, CALCULE, ANOTE, AÑADA, TIRE',
                     'b4 BANNER DE MEZCLAR EN 4 PARTES',
                     'b5 BANNER DE advert. de explosion',
                     'b6 ADVERTENCIA DEL TDI',
                     'b7 CONSIDERACIONES BÁSICAS ANTES DE EMPEZAR EL PROCESO',
                     'b8 MANTENGA LIMPIO SU REACTOR',
                     'b9 PASE MUESTRA A CALIDAD'
                     ]
    tk.Label(option_frames[lista_opciones[2]], text="Agregar Banner").grid(row=row, column=0)# ETIQUETA 
    banner_combo = ttk.Combobox(option_frames[lista_opciones[2]], textvariable=banners_var, values=lista_banners)# MENU COMBOBOX
    banner_combo.current(0)
    banner_combo.grid(row=row, column=1)
    # BOTON QUE AGREGA EL TEXTO AL TREEVIEW
    ttk.Button(option_frames[lista_opciones[2]],text="Agregar",command=agregar_banner).grid(row=row+len(specs), column=0)
    # -------------------------------------------------------------------------- TREEVIEW -------------------------------------------------
    # Create a Frame for the Treeview
    treeFrame = ttk.Frame(data_n_tree)
    treeFrame.grid(row=0, column=1)

    # Scrollbar
    treeScroll = ttk.Scrollbar(treeFrame)
    treeScroll.pack(side="right", fill="y")

    # Treeview
    treeview = ttk.Treeview(treeFrame, selectmode="extended", yscrollcommand=treeScroll.set, columns=(1, 2, 3, 4), height=12)
    treeview.pack(expand=True, fill="both")
    treeScroll.config(command=treeview.yview)

    # Treeview columns
    treeview.column("#0", width=100)
    treeview.column(1, anchor="w", width=100)
    treeview.column(2, anchor="w", width=100)
    treeview.column(3, anchor="w", width=100)
    treeview.column(4, anchor="w", width=100)

    # Treeview headings
    treeview.heading("#0", text="Nombre", anchor="center")
    treeview.heading(1, text="Descripcion", anchor="center")
    treeview.heading(2, text="Pictogramas", anchor="center")
    treeview.heading(3, text="Indicacion", anchor="center")
    treeview.heading(4, text="revision", anchor="center")

    # AGREGAR AL TREEVIEW
    agregar_treeview = tk.Button(botones,text='Agregar  al treeview',command=agregar_treeview_func).grid(row=1,column=0)
    # ELIMINAR EL ULTIMO ELEMENTO AÑADIDO AL TREEVIEW
    remove_button = tk.Button(botones, text="Quitar ultimo elemento", command=remove_last_item).grid(row=1,column=1)
    # MOSTRAR LA INFORMACION CONTENIDA EN EL TREEVIEW
    show_button = tk.Button(botones, text="Guardar Informacion", command=extract_treeview_data)
    show_button.grid(row=1,column=2)
    # CREAR EL EXCEL
    show_button = tk.Button(botones, text="Crear el archivo EXCEL", command=excelizar)
    show_button.grid(row=1,column=3)
    # Crear un botón para vaciar el TreeView
    boton_vaciar = tk.Button(botones, text="Vaciar TreeView", command=vaciar_treeview)
    boton_vaciar.grid(row=1,column=4)

    # Sizegrip
    sizegrip = ttk.Sizegrip(second_window)
    sizegrip.grid(row=100, column=100, padx=(0, 5), pady=(0, 5))

    # Center the window, and set minsize
    second_window.update()
    second_window.minsize(second_window.winfo_width(), second_window.winfo_height())
    x_cordinate = int((second_window.winfo_screenwidth()/2) - (second_window.winfo_width()/2))
    y_cordinate = int((second_window.winfo_screenheight()/2) - (second_window.winfo_height()/2))
    second_window.geometry("+{}+{}".format(x_cordinate, y_cordinate))
