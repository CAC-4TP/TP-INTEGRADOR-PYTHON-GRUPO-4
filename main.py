import tkinter as tk
from tkinter import messagebox
import json

# Constantes de diseño
FUENTE_LOGO = ("Pacifico", 20)
FUENTE_TITULO = ("Ubuntu", 24, "bold")
FUENTE_TITULO_BENEFICIOS= ("Ubuntu", 12, "bold")
FUENTE_BENEFICIOS = ("Ubuntu", 10)
COLOR_CUADROS_BENEFICIOS = "LightSkyBlue1"
FUENTE_TEXTO = ("Ubuntu", 16)
FUENTE_TEXTO_TABLA = ("Ubuntu", 12, "bold")
FUENTE_BOTON = ("Ubuntu", 10, "bold")
COLOR_PRINCIPAL = "#000000"
COLOR_BOTON = "#007BFF"
COLOR_TEXTO_BOTON = "#FFFFFF"
ANCHO_BOTON = 10
ALTO_BOTON = 2
ALTURA_FRANJA = 80

# Variable global para la ventana actual
ventana_actual = None

# Funciones para manejar los movimientos: archivos json
def cargar_movimientos():
    try:
        with open('movimientos.json', 'r') as archivo:
            movimientos = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        movimientos = []
    return movimientos

def guardar_movimientos(movimientos):
    with open('movimientos.json', 'w') as archivo:
        json.dump(movimientos, archivo)

def cargar_servicios():
    try:
        with open('servicios.json', 'r') as archivo:
            servicios = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        servicios = []  # Devolver una lista vacía si el archivo no existe o está vacío
    if not isinstance(servicios, list):  # Verificar si servicios no es una lista
        servicios = []  # En caso de ser un diccionario, inicializar como lista vacía
    return servicios

def guardar_servicios(servicios):
    with open('servicios.json', 'w') as archivo:
        json.dump(servicios, archivo)

def mostrar_saldo():
    global saldo_actual# Variable global cumple la funcion de almacenar el saldo actual
    movimientos = cargar_movimientos()
    saldo_actual = sum(movimiento['monto'] for movimiento in movimientos if 'monto' in movimiento)
    label_saldo.config(text=f"Saldo: ${int(saldo_actual)}")  # Mostrar saldo como entero

def configurar_ventana(ventana):
    # Configuración de redimensionamiento de la ventana principal
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

    button_home = tk.Button(frame_inferior, text="HOME", font=FUENTE_BOTON, bg="white", fg=COLOR_BOTON, width=ANCHO_BOTON, height=ALTO_BOTON, state="disabled")
    button_home.pack(side=tk.LEFT, padx=5, pady=5)

    button_salir = tk.Button(frame_inferior, text="SALIR", font=FUENTE_BOTON, bg="white", fg=COLOR_BOTON, width=ANCHO_BOTON, height=ALTO_BOTON, command=ventana.destroy)
    button_salir.pack(side=tk.RIGHT, padx=5, pady=5)

def crear_ventana_principal():
    global ventana, label_saldo
    ventana = tk.Tk()
    ventana.title("Billetera Virtual")
    configurar_ventana(ventana)

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

    button_beneficios = tk.Button(frame_botones_principales, text="Beneficios", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=lambda: abrir_ventana(nueva_ventana_beneficios))
    button_beneficios.grid(row=2, column=1, padx=5, pady=2)
    
    button_eliminar_servicio = tk.Button(frame_botones_principales, text="Eliminar \n servicio", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=lambda: abrir_ventana(nueva_ventana_eliminar_servicio))
    button_eliminar_servicio.grid(row=2, column=0, padx=5, pady=2)

    mostrar_saldo()  # Actualizar el saldo al iniciar la aplicación

    ventana.mainloop()

def abrir_ventana(funcion_ventana):
    global ventana_actual
    if ventana_actual is not None:  # Cerrar la ventana actual si existe
        ventana_actual.destroy()
    ventana_actual = tk.Toplevel()
    funcion_ventana(ventana_actual)

def nueva_ventana_seleccionar_servicio(ventana_seleccionar):
    ventana_seleccionar.title("Seleccionar Servicio")
    configurar_ventana(ventana_seleccionar)

    tk.Label(ventana_seleccionar, text="Seleccione el servicio a pagar:", font=FUENTE_TEXTO).pack(pady=10)

    servicios = cargar_servicios()

    for servicio in servicios:
        tk.Button(ventana_seleccionar, 
                  text=servicio, 
                  font=FUENTE_BOTON, 
                  bg=COLOR_BOTON, 
                  fg="white", 
                  width=ANCHO_BOTON,
                  height=ALTO_BOTON,
                  command=lambda 
                  s=servicio: seleccionar_servicio(s)).pack(pady=5)

    tk.Button(ventana_seleccionar, text="Cancelar", font=FUENTE_BOTON, bg="white", fg=COLOR_BOTON, width=ANCHO_BOTON, height=ALTO_BOTON, command=ventana_seleccionar.destroy).pack(pady=10)

def nueva_ventana_ingresar_dinero(ventana_ingresar):
    ventana_ingresar.title("Ingresar Dinero")
    configurar_ventana(ventana_ingresar)

    tk.Label(ventana_ingresar, text="Ingrese el monto:", font=FUENTE_TEXTO).pack(pady=10)
    entry_monto = tk.Entry(ventana_ingresar, font=FUENTE_TEXTO)
    entry_monto.pack(pady=10)

    def guardar_ingreso():
        monto = entry_monto.get()
        if monto.isdigit():
            movimientos = cargar_movimientos()
            movimientos.append({"operacion": "Ingreso", "monto": int(monto), "detalle": "Dinero acreditado"})
            guardar_movimientos(movimientos)
            mostrar_saldo()
            messagebox.showinfo("Éxito", "El dinero ha sido ingresado correctamente.")
            ventana_ingresar.destroy()
   
        else:
            messagebox.showerror("Error", "Por favor, ingrese un monto válido.")

    tk.Button(ventana_ingresar, text="Guardar", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=guardar_ingreso).pack(pady=10)

# Modificación para que la función acepte un argumento
def consultar_movimientos(ventana_actual=None):
    if ventana_actual is not None:
        ventana_actual.destroy()
    
    ventana_movimientos = tk.Toplevel()
    ventana_movimientos.title("Movimientos")
    ventana_movimientos.geometry("620x600")  # Ajustar tamaño de la ventana principal
    configurar_ventana(ventana_movimientos)

    tk.Label(ventana_movimientos, text="Movimientos", font=FUENTE_TEXTO).pack(pady=5)

    movimientos = cargar_movimientos()
    # Este frame es para que la tabla quede centrada
    frame_movimientos = tk.Frame(ventana_movimientos)  # Ajustar tamaño del marco
    frame_movimientos.pack(pady=10)
    
    # Crear encabezados de la tabla
    headers = ["OPERACION", "MONTO", "DETALLE"]
    for i, header in enumerate(headers):
        label = tk.Label(frame_movimientos, text=header, font=FUENTE_TEXTO_TABLA, width=20, anchor='w')
        label.grid(row=0, column=i, padx=10, pady=5)
    # Crear filas de la tabla: for i significa que se va a iterar por cada elemento en la lista movimientos
    for i, movimiento in enumerate(movimientos, start=1):
        operacion = movimiento['operacion']
        monto = movimiento['monto']
        detalle = movimiento['detalle']
        
        # Esto es para alinear el texto a la izquierda
        tk.Label(frame_movimientos, text=operacion.capitalize(), font=FUENTE_TEXTO_TABLA, width=20, anchor='w').grid(row=i, column=0, padx=(0))
        tk.Label(frame_movimientos, text=f"${monto}", font=FUENTE_TEXTO_TABLA, width=20, anchor='w').grid(row=i, column=1, padx=(0))
        tk.Label(frame_movimientos, text=detalle, font=FUENTE_TEXTO_TABLA, width=20, anchor='w').grid(row=i, column=2, padx=(0))

    tk.Button(ventana_movimientos, text="Cerrar", font=FUENTE_BOTON, bg="white", fg=COLOR_BOTON, width=ANCHO_BOTON, height=ALTO_BOTON, command=ventana_movimientos.destroy).pack(pady=10)


def seleccionar_servicio(servicio):
    global ventana_actual, saldo_actual
    if ventana_actual is not None:
        ventana_actual.destroy()
    ventana_actual = tk.Toplevel()
    ventana_actual.title("Pagar Servicio")
    configurar_ventana(ventana_actual)

    tk.Label(ventana_actual, text=f"Pagar {servicio}", font=FUENTE_TITULO).pack(pady=10)
    tk.Label(ventana_actual, text="Ingrese el monto a pagar:", font=FUENTE_TEXTO).pack(pady=10)
    entry_monto = tk.Entry(ventana_actual, font=FUENTE_TEXTO)
    entry_monto.pack(pady=10)

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

def nueva_ventana_agregar_servicio(ventana_agregar):
    ventana_agregar.title("Agregar Servicio")
    configurar_ventana(ventana_agregar)

    tk.Label(ventana_agregar, text="Nombre del nuevo servicio:", font=FUENTE_TEXTO).pack(pady=10)
    entry_servicio = tk.Entry(ventana_agregar, font=FUENTE_TEXTO)
    entry_servicio.pack(pady=10)
    
 #FUNCION PARA AGREGAR SERVICIO, SI ES NUEVO, LO AGREGA, 
 #SI ESTA EN LA LISTA NO DEJA AGREGARLO
 #se registra en la tabla movimientos
    def agregar():
        servicio = entry_servicio.get()
        if servicio:
            servicios = cargar_servicios()
            if servicio not in servicios:
                servicios.append(servicio)
                movimientos = cargar_movimientos()
                movimientos.append({"operacion": "Servicio agregado", "monto": 0, "detalle": f"{servicio}"})
                guardar_movimientos(movimientos)
                guardar_servicios(servicios)
                messagebox.showinfo("Éxito", "El servicio ha sido agregado correctamente.")
                ventana_agregar.destroy()
            else:
                messagebox.showerror("Error", "El servicio ya existe.")
                ventana_agregar.destroy()
        else:
            messagebox.showerror("Error", "Por favor, ingrese un nombre de servicio.")
           
    tk.Button(ventana_agregar, text="Agregar", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=agregar).pack(pady=10)
    
def nueva_ventana_eliminar_servicio(ventana_eliminar):
    ventana_eliminar.title("Eliminar Servicio")
    configurar_ventana(ventana_eliminar)

    tk.Label(ventana_eliminar, text="Seleccione el servicio a eliminar:", font=FUENTE_TEXTO).pack(pady=10)

    servicios = cargar_servicios()

    for servicio in servicios:
        tk.Button(ventana_eliminar, 
                  text=servicio, 
                  font=FUENTE_BOTON, 
                  bg=COLOR_BOTON, 
                  fg="white", 
                  width=ANCHO_BOTON,
                  height=ALTO_BOTON,
                  command=lambda 
                  s=servicio: eliminar_servicio(s, ventana_eliminar)).pack(pady=5)

    tk.Button(ventana_eliminar, text="Cancelar", font=FUENTE_BOTON, bg="white", fg=COLOR_BOTON, width=ANCHO_BOTON, height=ALTO_BOTON, command=ventana_eliminar.destroy).pack(pady=10)

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
    else:
        messagebox.showerror("Error", "El servicio no existe.")
        
# Esta es la ventana de beneficios       
def nueva_ventana_beneficios(ventana_beneficios):
    ventana_beneficios.title("Beneficios")
    configurar_ventana(ventana_beneficios)

    # Crear marco principal con el fondo azul
    frame_principal = tk.Frame(ventana_beneficios, bg=COLOR_BOTON)
    frame_principal.pack(expand=True, fill="both")

    # Crear marcos para los beneficios (uno debajo del otro)
    frame_beneficio_1 = tk.Frame(frame_principal, bg=COLOR_CUADROS_BENEFICIOS, padx=20, pady=20)
    frame_beneficio_1.pack(fill="x", pady=15)  # Ajustar pack para expandir horizontalmente

    # Contenido del primer beneficio
    tk.Label(frame_beneficio_1, text="RECARGANDO TU CELULAR", font=FUENTE_TITULO_BENEFICIOS).pack(pady=(0, 10))
    tk.Label(frame_beneficio_1, text="Con la primera recarga que le hagas a tu celular, recibirás un 10% de descuento.", font=FUENTE_TEXTO).pack(pady=(0, 10))

    # Imagen del primer beneficio
    imagen_beneficio_1 = tk.PhotoImage(file="imagenes/claro.png")  # Reemplaza con la ruta de tu imagen
    imagen_beneficio_1 = imagen_beneficio_1.subsample(6)  # Redimensionar la imagen
    label_imagen_beneficio_1 = tk.Label(frame_beneficio_1, image=imagen_beneficio_1)
    label_imagen_beneficio_1.image = imagen_beneficio_1  # Guardar la referencia para evitar que el recolector de basura la elimine
    label_imagen_beneficio_1.pack(pady=(10, 0)) # Ajustar el espacio entre la imagen y el texto

    # Crear marco para el segundo beneficio
    frame_beneficio_2 = tk.Frame(frame_principal, bg=COLOR_CUADROS_BENEFICIOS, padx=20, pady=20)
    frame_beneficio_2.pack(fill="x", pady=20)  # Ajustar pack para expandir horizontalmente

    # Contenido del segundo beneficio
    tk.Label(frame_beneficio_2, text="Beneficio 2", font=FUENTE_TITULO_BENEFICIOS).pack(pady=(0, 10))
    tk.Label(frame_beneficio_2, text="Texto explicativo del beneficio 2...", font=FUENTE_TEXTO).pack()

    # Imagen del segundo beneficio
    imagen_beneficio_2 = tk.PhotoImage(file="imagenes/vea.png")  # Reemplaza con la ruta de tu imagen
    imagen_beneficio_2 = imagen_beneficio_2.subsample(6)  # Redimensionar la imagen
    label_imagen_beneficio_2 = tk.Label(frame_beneficio_2, image=imagen_beneficio_2)
    label_imagen_beneficio_2.image = imagen_beneficio_2  # Guardar la referencia para evitar que el recolector de basura la elimine
    label_imagen_beneficio_2.pack(pady=(10, 0))

    # Botones home y salir (sin repetición)
    frame_botones = tk.Frame(ventana_beneficios, bg=COLOR_BOTON, height=ALTURA_FRANJA)
    frame_botones.pack(fill="x", side="bottom")
    frame_botones.lower()

    button_home = tk.Button(frame_botones, text="HOME", font=FUENTE_BOTON, bg="white", fg=COLOR_BOTON, width=ANCHO_BOTON, height=ALTO_BOTON, state="disabled")
    button_home.pack(side=tk.LEFT, padx=5, pady=5)

    button_salir = tk.Button(frame_botones, text="SALIR", font=FUENTE_BOTON, bg="white", fg=COLOR_BOTON, width=ANCHO_BOTON, height=ALTO_BOTON, command=ventana_beneficios.destroy)
    button_salir.pack(side=tk.RIGHT, padx=5, pady=5)


crear_ventana_principal()




