import tkinter as tk
from tkinter import messagebox
import json
########################################################################################
# Constantes de diseño: Define fuentes
# (FUENTE_LOGO, FUENTE_TITULO, FUENTE_TEXTO) y colores que se utilizarán en la interfaz.
########################################################################################
FUENTE_LOGO = ("Pacifico", 20)
FUENTE_TITULO = ("Ubuntu", 24, "bold")
FUENTE_TEXTO = ("Ubuntu", 16)

COLOR_PRINCIPAL = "#000000"
COLOR_BARRA_SCROLL = "#007BFF"

FUENTE_TITULO_BENEFICIOS = ("Ubuntu", 12, "bold underline")
FUENTE_BENEFICIOS = ("Ubuntu", 10)
COLOR_CUADROS_BENEFICIOS = "#e1e1f9"

FUENTE_TEXTO_TABLA = ("Ubuntu", 10, "bold")

FUENTE_BOTON = ("Ubuntu", 10, "bold")
COLOR_BOTON = "#007BFF"
COLOR_TEXTO_BOTON = "#FFFFFF"
ANCHO_BOTON = 10
ALTO_BOTON = 2

ALTURA_FRANJA = 80


# Variable global para la ventana actual: esta en none porque no hay ventana inicialmente
ventana_actual = None

##########################################################################################
# Funciones de Manejo de Archivos JSON
#########################################################################################
# Intenta cargar movimientos desde 'movimientos.json', devuelve lista vacía si hay error.
# Maneja excepciones de archivo no encontrado o JSON malformado.

def cargar_movimientos():
    try:
        with open('movimientos.json', 'r') as archivo:
            movimientos = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        movimientos = []
    return movimientos

# Guarda la lista de movimientos en 'movimientos.json'.
def guardar_movimientos(movimientos):
    with open('movimientos.json', 'w') as archivo:
        json.dump(movimientos, archivo)

# Intenta cargar servicios desde 'servicios.json', devuelve lista vacía si hay error. 
# Convierte el resultado a lista si es un diccionario.

def cargar_servicios():
    try:
        with open('servicios.json', 'r') as archivo:
            servicios = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        servicios = []  # Devolver una lista vacía si el archivo no existe o está vacío
    if not isinstance(servicios, list):  # Verificar si servicios no es una lista
        servicios = []  # En caso de ser un diccionario, inicializar como lista vacía
    return servicios

# Guarda la lista de servicios en 'servicios.json'.

def guardar_servicios(servicios):
    with open('servicios.json', 'w') as archivo:
        json.dump(servicios, archivo)
#############################################################################################
# Función mostrar_saldo
#############################################################################################

# Calcula y muestra el saldo: Lee los movimientos, 
# suma los montos y actualiza la interfaz con el saldo calculado.


def mostrar_saldo():
    global saldo_actual# Variable global cumple la funcion de almacenar el saldo actual
    movimientos = cargar_movimientos() # Carga los movimientos desde el archivo JSON
    saldo_actual = sum(movimiento['monto'] for movimiento in movimientos if 'monto' in movimiento) 
    # Suma los montos de los movimientos que tengan el atributo 'monto' 
    # y los almacena en la variable global saldo_actual
    label_saldo.config(text=f"Saldo: ${int(saldo_actual)}")
    
##############################################################################################
#  Funciones para Configurar y Crear Ventanas
##############################################################################################

# Configura propiedades de redimensionamiento y tamaño mínimo de la ventana.
# Crea y configura elementos visuales como logo, botones y barras.

def configurar_ventana(ventana, principal=False): 
    ventana.resizable(True, True)  # Permitir redimensionamiento horizontal y vertical
    ventana.minsize(350, 550)  # Establecer tamaño mínimo para evitar que la ventana se haga demasiado pequeña

    frame_contenedor = tk.Frame(ventana, bg=COLOR_BOTON, height=ALTURA_FRANJA)
    frame_contenedor.pack(fill="x")

    logo = tk.PhotoImage(file="imagenes/logo.png")
    logo = logo.subsample(4)  # Redimensionar la imagen

    label_logo_texto = tk.Label(frame_contenedor, image=logo, text="PayPy", font=FUENTE_LOGO, bg=COLOR_BOTON, fg="white", compound="top", padx=5, pady=10)
    label_logo_texto.image = logo  # Para evitar que el garbage collector elimine la imagen
    label_logo_texto.pack(pady=(10, 0))
    
    frame_inferior = tk.Frame(ventana, bg=COLOR_BOTON, height=ALTURA_FRANJA)
    frame_inferior.pack(fill="x", side="bottom")
    frame_inferior.lower()  # lower es un método que coloca un widget debajo de otro

    texto_boton = "SALIR" if principal else "HOME"
    button_salir = tk.Button(frame_inferior, text=texto_boton, font=FUENTE_BOTON, bg="white", fg=COLOR_BOTON, width=ANCHO_BOTON, height=ALTO_BOTON, command=ventana.destroy)
    button_salir.pack(pady=(10, 10))

# Crea la ventana principal de la aplicación con botones para diversas funcionalidades.
# Llama a mostrar_saldo para mostrar el saldo inicial al iniciar la aplicación

def crear_ventana_principal():
    global ventana, label_saldo
    ventana = tk.Tk()
    ventana.title("Billetera Virtual")
    configurar_ventana(ventana, principal=True)

    label_saldo = tk.Label(ventana, text="Saldo: $0", font=FUENTE_TITULO)
    label_saldo.pack(pady=(8, 10))

    frame_botones_principales = tk.Frame(ventana)
    frame_botones_principales.pack()

    button_ingresar = tk.Button(frame_botones_principales, text="Ingresar \n dinero", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=lambda: abrir_ventana(nueva_ventana_ingresar_dinero))
    button_ingresar.grid(row=0, column=0, padx=5, pady=2)

    button_consultar = tk.Button(frame_botones_principales, text="Movimientos", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=lambda: abrir_ventana(consultar_movimientos))
    button_consultar.grid(row=0, column=1, padx=5, pady=2)

    button_pagar = tk.Button(frame_botones_principales, text="Pagar \n servicio", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=lambda: abrir_ventana(nueva_ventana_seleccionar_servicio))
    button_pagar.grid(row=1, column=0, padx=5, pady=2)

    button_agregar_servicio = tk.Button(frame_botones_principales, text="Agregar \n servicio", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=lambda: abrir_ventana(nueva_ventana_agregar_servicio))
    button_agregar_servicio.grid(row=1, column=1, padx=5, pady=2)
    
    button_actualizar_servicio = tk.Button(frame_botones_principales, text="Actualizar \n servicio", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=lambda: abrir_ventana(nueva_ventana_actualizar_servicio))
    button_actualizar_servicio.grid(row=2, column=0, padx=5, pady=2)

    button_eliminar_servicio = tk.Button(frame_botones_principales, text="Eliminar \n servicio", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=lambda: abrir_ventana(nueva_ventana_eliminar_servicio))
    button_eliminar_servicio.grid(row=2, column=1, padx=5, pady=2)

    button_beneficios = tk.Button(frame_botones_principales, text="Beneficios", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=lambda: abrir_ventana(nueva_ventana_beneficios))
    button_beneficios.grid(row=3, column=0, columnspan=2, padx=5, pady=2)

    mostrar_saldo()  # Actualizar el saldo al iniciar la aplicación

    ventana.mainloop()  # Ejecuta el bucle principal de la ventana

#######################################################################################################
# Abre una nueva ventana secundaria y cierra la ventana anterior si existe.

def abrir_ventana(funcion_ventana):
    global ventana_actual
    if ventana_actual is not None:  # Cerrar la ventana actual si existe
        ventana_actual.destroy()
    ventana_actual = tk.Toplevel()
    funcion_ventana(ventana_actual)
    
########################################################################################################
 # Funciones Específicas para Operaciones (Ingresar dinero, pagar servicio, etc.)
######################################################################################################

# Crea una ventana para seleccionar un servicio a pagar con botones para cada servicio.

def nueva_ventana_seleccionar_servicio(ventana_seleccionar):
    ventana_seleccionar.title("Seleccionar Servicio")
    configurar_ventana(ventana_seleccionar, principal=False)

    tk.Label(ventana_seleccionar, text="Seleccione el servicio a pagar:", font=FUENTE_TEXTO).pack(pady=10)
    # Cargar los servicios disponibles desde el archivo JSON
    servicios = cargar_servicios()

    # Crear botones para cada servicio
    for servicio in servicios:
     tk.Button(ventana_seleccionar, text=servicio, font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white",
        width=ANCHO_BOTON, height=ALTO_BOTON, command=lambda 
        s=servicio: seleccionar_servicio(s)).pack(pady=5)
    
#########################################################################################################
# Crea una ventana para ingresar dinero con validación de entrada y actualización del saldo.

def nueva_ventana_ingresar_dinero(ventana_ingresar):
    ventana_ingresar.title("Ingresar Dinero")
    configurar_ventana(ventana_ingresar)

    tk.Label(ventana_ingresar, text="Ingrese el monto:", font=FUENTE_TEXTO).pack(pady=10)# este es el label que me permite poner el monto
    entry_monto = tk.Entry(ventana_ingresar, font=FUENTE_TEXTO)
    entry_monto.pack(pady=10)

    # Incluye la lógica para guardar el ingreso y actualizar el saldo.
    def guardar_ingreso():
        monto = entry_monto.get()
        if monto.isdigit(): # si el valor ingresado es un número entero
            movimientos = cargar_movimientos() # cargar los movimientos actuales
            
            # Agregar el ingreso al final de la lista de movimientos
            movimientos.append({"operacion": "Ingreso", "monto": int(monto), "detalle": "Dinero acreditado"})
            guardar_movimientos(movimientos) # guardar los movimientos actualizados
            mostrar_saldo()
            messagebox.showinfo("Éxito", "El dinero ha sido ingresado correctamente.")
            ventana_ingresar.destroy()
   
        else:
            messagebox.showerror("Error", "Por favor, ingrese un monto válido.")

    tk.Button(ventana_ingresar, text="Confirmar", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=guardar_ingreso).pack(pady=10)



# Configura una ventana para consultar los movimientos realizados.
# Muestra una tabla con los movimientos.
def consultar_movimientos(ventana_actual=None):
    if ventana_actual is not None:
        ventana_actual.destroy()
    
    ventana_movimientos = tk.Toplevel()
    ventana_movimientos.title("Movimientos")
    ventana_movimientos.geometry("620x600")  # Ajustar tamaño de la ventana principal
    configurar_ventana(ventana_movimientos)

    tk.Label(ventana_movimientos, text="Movimientos", font=FUENTE_TEXTO).pack(pady=5)# este label es para poner el titulo de la ventana

    movimientos = cargar_movimientos()
    
    # Crear un canvas para contener el frame con los movimientos y una scrollbar
    canvas = tk.Canvas(ventana_movimientos)
    frame_movimientos = tk.Frame(canvas)
    scrollbar = tk.Scrollbar(ventana_movimientos, orient="vertical", command=canvas.yview, bg=COLOR_BARRA_SCROLL)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=frame_movimientos, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    frame_movimientos.bind("<Configure>", on_frame_configure)

    # Crear encabezados de la tabla
    headers = ["OPERACION", "MONTO", "DETALLE"]
    for i, header in enumerate(headers):
        label = tk.Label(frame_movimientos, text=header, font=FUENTE_TEXTO_TABLA, width=20, anchor='w')
        label.grid(row=0, column=i, padx=10, pady=5)
    
    # Crear filas de la tabla
    for i, movimiento in enumerate(movimientos, start=1):
        operacion = movimiento.get('operacion', 'Operación no registrada')  # Obtener la operación o un mensaje alternativo
        monto = movimiento.get('monto', 'Monto no registrado')  # Obtener el monto o un mensaje alternativo
        detalle = movimiento.get('detalle', 'Detalle no registrado')  # Obtener el detalle o un mensaje alternativo
        
        # Esto es para alinear el texto a la izquierda
        tk.Label(frame_movimientos, text=operacion.capitalize(), font=FUENTE_TEXTO_TABLA, width=20, anchor='w').grid(row=i, column=0, padx=(0))
        tk.Label(frame_movimientos, text=f"${monto}", font=FUENTE_TEXTO_TABLA, width=20, anchor='w').grid(row=i, column=1, padx=(0))
        tk.Label(frame_movimientos, text=detalle, font=FUENTE_TEXTO_TABLA, width=20, anchor='w').grid(row=i, column=2, padx=(0))


# Configura una ventana para pagar un servicio seleccionado.
# Incluye la lógica para pagar el servicio y actualizar el saldo.
def seleccionar_servicio(servicio):
    global ventana_actual, saldo_actual
    if ventana_actual is not None: # Si hay una ventana abierta, cerrarla
        ventana_actual.destroy()
    ventana_actual = tk.Toplevel()
    ventana_actual.title("Pagar Servicio")
    configurar_ventana(ventana_actual)

    tk.Label(ventana_actual, text=f"Pagar {servicio}", font=FUENTE_TITULO).pack(pady=10)
    tk.Label(ventana_actual, text="Ingrese el monto a pagar:", font=FUENTE_TEXTO).pack(pady=10)
    entry_monto = tk.Entry(ventana_actual, font=FUENTE_TEXTO)
    entry_monto.pack(pady=10)

    # Esta funcion se encarga de pagar el servicio, 
    # si el monto es menor o igual al saldo actual, se actualiza el saldo y se guarda el movimiento
    # si el monto es mayor al saldo actual, no se actualiza el saldo y se muestra un mensaje de error
    def pagar():
        global saldo_actual
        monto = float(entry_monto.get())
        if monto <= saldo_actual:
            saldo_actual -= monto
            movimientos = cargar_movimientos()
            movimientos.append({"operacion": "Pago de servicio", "monto": -monto, "detalle": f"{servicio}"})
            guardar_movimientos(movimientos)
            mostrar_saldo()
            messagebox.showinfo("Éxito", "El servicio ha sido pagado correctamente.")
            ventana_actual.destroy()
        else:
            messagebox.showerror("Error", "Saldo insuficiente.")
            ventana_actual.destroy()

    tk.Button(ventana_actual, text="Pagar", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=pagar).pack(pady=10)

# Esta ventana permite agregar un nuevo servicio a la lista de servicios.
def nueva_ventana_agregar_servicio(ventana_agregar):
    ventana_agregar.title("Agregar Servicio")
    configurar_ventana(ventana_agregar)

    tk.Label(ventana_agregar, text="Nombre del nuevo servicio:", font=FUENTE_TEXTO).pack(pady=10)
    entry_servicio = tk.Entry(ventana_agregar, font=FUENTE_TEXTO)
    entry_servicio.pack(pady=10)
    
 #FUNCION PARA AGREGAR SERVICIO, SI ES NUEVO, LO AGREGA, 
 #SI ESTA EN LA LISTA NO DEJA AGREGARLO, sin importar si esta en mayuscula o minuscula.
 # Por eso se puso un condicional que convierte todo a minuscula para que sea case-insensitive
 
    def agregar():
        servicio = entry_servicio.get()
        if servicio:
            servicios = cargar_servicios()
             # Convertir todos los servicios existentes a minúsculas para que sean case-insensitive
            servicios_lower = [s.lower() for s in servicios] 
             # Convierte el servicio ingresado a minúsculas para compararlo de manera case-insensitive
            if servicio.lower() not in servicios_lower: # Si el servicio no existe, lo agrega
                servicios.append(servicio)
                #se registra en la tabla movimientos
                movimientos = cargar_movimientos()  
                movimientos.append({"operacion": "Nuevo servicio", "monto": 0, "detalle": f"{servicio}"})
                guardar_movimientos(movimientos)
                guardar_servicios(servicios)
                messagebox.showinfo("Éxito", "El servicio ha sido agregado correctamente.")
                ventana_agregar.destroy()

            else:# SI SE REPITE ME SALE EL MJE DE ERROR
                messagebox.showerror("Error", "El servicio ya existe.")
                ventana_agregar.destroy()
                
        else:# SI ESTA VACÍO ME SALE EL MJE DE ERROR
            messagebox.showerror("Error", "Debe ingresar un nombre de servicio.")
            ventana_agregar.destroy()
            
            
    tk.Button(ventana_agregar, text="Agregar", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=agregar).pack(pady=10)

# Esta ventana permite eliminar un servicio de la lista de servicios.
def nueva_ventana_eliminar_servicio(ventana_eliminar):
    ventana_eliminar.title("Eliminar Servicio")
    configurar_ventana(ventana_eliminar)

    tk.Label(ventana_eliminar, text="Seleccione el servicio a eliminar:", font=FUENTE_TEXTO).pack(pady=10)

    servicios = cargar_servicios()
  
    for servicio in servicios:
        tk.Button(ventana_eliminar, text=servicio, font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, 
                  height=ALTO_BOTON, command=lambda s=servicio: eliminar_servicio(s, ventana_eliminar)).pack(pady=5)


# FUNCION PARA ELIMINAR SERVICIO
def eliminar_servicio(servicio, ventana_eliminar):
    servicios = cargar_servicios()
    if servicio in servicios:
        servicios.remove(servicio)
        movimientos = cargar_movimientos()
        movimientos.append({"operacion": "Eliminación de servicio", "monto": 0, "detalle": f"{servicio}"})
        guardar_movimientos(movimientos)
        guardar_servicios(servicios)
        messagebox.showinfo("Éxito", "El servicio ha sido eliminado correctamente.")
        ventana_eliminar.destroy()
   
        
# actualizar servicios
def abrir_ventana(funcion_ventana):
    global ventana_actual
    if ventana_actual is not None:
        ventana_actual.destroy()
    ventana_actual = tk.Toplevel()
    funcion_ventana(ventana_actual)
    ventana_actual.protocol("WM_DELETE_WINDOW", lambda: on_closing(funcion_ventana))
    
# Esta funcion on_closing se encarga de cerrar la ventana actual y liberar el recurso de la ventana.
def on_closing(funcion_ventana):
    global ventana_actual
    ventana_actual.destroy()
    ventana_actual = None
    
####################################################################################################
# Ventanas y Funciones para Beneficios y Actualización de Servicios
####################################################################################################
def nueva_ventana_beneficios(ventana_beneficios):
    ventana_beneficios.title("Beneficios")
    ventana_beneficios.geometry("300x600")  # Ajustar la geometría de la ventana
    configurar_ventana(ventana_beneficios)

    # Título de beneficios con fuente y subrayado
    tk.Label(ventana_beneficios, text="Beneficios de la Billetera Virtual", font=FUENTE_TITULO_BENEFICIOS, wraplength=280).pack(pady=10)

    beneficios = [
        "😊 Facilidad de uso: realiza pagos de manera sencilla y rápida.",
        "🔒 Seguridad: protege tu información personal y financiera.",
        "🌍 Accesibilidad: disponible en todo momento y lugar.",
        "📊 Control: mantén un registro de tus movimientos financieros.",
        "⏳ Ahorro de tiempo: evita filas y trámites presenciales."
    ]

    frame_beneficios = tk.Frame(ventana_beneficios, bg=COLOR_CUADROS_BENEFICIOS)
    frame_beneficios.pack(fill="both", expand=True, padx=10, pady=10)

    # Cambiar la fuente y tamaño del texto para beneficios
    for beneficio in beneficios:
        tk.Label(frame_beneficios, text=beneficio, font=("Roboto Medium", 11), wraplength=300, justify="left", anchor="w", bg=COLOR_CUADROS_BENEFICIOS).pack(pady=5, padx=10, anchor="w")

    # Cambiar la fuente y agregar emojis a cada oración
    for beneficio in beneficios:
        tk.Label(frame_beneficios, text=beneficio, font=FUENTE_BENEFICIOS, wraplength=280, justify="left", anchor="w", bg=COLOR_CUADROS_BENEFICIOS).pack(pady=5, padx=10, anchor="w")

    # Botones home y salir
    frame_botones = tk.Frame(ventana_beneficios, bg=COLOR_BOTON, height=ALTURA_FRANJA)
    frame_botones.pack(fill="x", side="bottom")
    frame_botones.lower()

    ventana_beneficios.mainloop()
##################################################################################################
# Crea una ventana para actualizar un servicio seleccionado.
# Permite cambiar el nombre del servicio y registra el cambio en movimientos.

def nueva_ventana_actualizar_servicio(ventana_actualizar):
    ventana_actualizar.title("Actualizar Servicio")
    configurar_ventana(ventana_actualizar)

    tk.Label(ventana_actualizar, text="Seleccione el servicio a actualizar:", font=FUENTE_TEXTO).pack(pady=10)

    servicios = cargar_servicios()

    for servicio in servicios:
        tk.Button(ventana_actualizar, text=servicio, font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, 
             height=ALTO_BOTON, command=lambda s=servicio: abrir_ventana(lambda v: ventana_actualizar_servicio(v, s))).pack(pady=5)


# Esta ventana permite actualizar un servicio de la lista de servicios, 
# si cambio de nombre por ejemplo, permite modificarlo
def ventana_actualizar_servicio(ventana_actualizar, servicio):
    ventana_actualizar.title(f"Actualizar {servicio}")
    configurar_ventana(ventana_actualizar)

    tk.Label(ventana_actualizar, text=f"Ingrese el nuevo nombre para {servicio}:", font=FUENTE_TEXTO).pack(pady=10)
    entry_nuevo_servicio = tk.Entry(ventana_actualizar, font=FUENTE_TEXTO)
    entry_nuevo_servicio.pack(pady=10)
    
    # Esta funcion actualiza el servicio seleccionado y lo guarda en la lista de servicios
    def actualizar():
        nuevo_servicio = entry_nuevo_servicio.get()
        if nuevo_servicio:
            servicios = cargar_servicios()
            if servicio in servicios:
                servicios.remove(servicio)
                servicios.append(nuevo_servicio)
                guardar_servicios(servicios)                
                movimientos = cargar_movimientos()
                movimientos.append({"operacion": "Actualización", "monto": 0, "detalle": f"{servicio} cambió a {nuevo_servicio}"})
                guardar_movimientos(movimientos)               
            
                messagebox.showinfo("Éxito", "El servicio ha sido actualizado correctamente.")
                ventana_actualizar.destroy() 
     
    tk.Button(ventana_actualizar, text="Actualizar", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=actualizar).pack(pady=10)

crear_ventana_principal()


















