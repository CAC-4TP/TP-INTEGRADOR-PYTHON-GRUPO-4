import tkinter as tk
from tkinter import messagebox
import json

# Constantes de diseño
FUENTE_LOGO = ("Pacifico", 20)
FUENTE_TITULO = ("Ubuntu", 24, "bold")
FUENTE_TEXTO = ("Ubuntu", 16)
FUENTE_TEXTO_TABLA = ("Ubuntu", 14)
FUENTE_BOTON = ("Ubuntu", 10, "bold")
COLOR_PRINCIPAL = "#000000"
COLOR_BOTON = "#007BFF"
COLOR_TEXTO_BOTON = "#FFFFFF"
ANCHO_BOTON = 10
ALTO_BOTON = 2
ALTURA_FRANJA = 80

# Funciones para manejar los movimientos: archivos json

# Función para cargar los movimientos
def cargar_movimientos():
    try:
        with open('movimientos.json', 'r') as archivo:
            movimientos = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        movimientos = []
    return movimientos

# Función para guardar los movimientos en un archivo json
def guardar_movimientos(movimientos):
    with open('movimientos.json', 'w') as archivo:
        json.dump(movimientos, archivo)

# Funciones para manejar los servicios
def cargar_servicios():
    try:
        with open('servicios.json', 'r') as archivo:
            servicios = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        servicios = []  # Devolver una lista vacía si el archivo no existe o está vacío
    if not isinstance(servicios, list):  # Verificar si servicios no es una lista
        servicios = []  # En caso de ser un diccionario, inicializar como lista vacía
    return servicios

# Función para guardar los servicios en un archivo json
def guardar_servicios(servicios):
    with open('servicios.json', 'w') as archivo:
        json.dump(servicios, archivo)

# Función para mostrar el saldo
def mostrar_saldo():
    movimientos = cargar_movimientos()
    saldo = sum(movimiento['monto'] if movimiento.get('tipo') == 'ingreso' else -movimiento['monto'] for movimiento in movimientos if 'monto' in movimiento and 'tipo' in movimiento)
    label_saldo.config(text=f"Saldo: ${int(saldo)}")  # Mostrar saldo como entero

# Función para crear la ventana principal
def crear_ventana_principal():
    global ventana, label_saldo
    ventana = tk.Tk()
    ventana.title("Billetera Virtual")
    ventana.geometry("350x500")

    # Crear un frame para contener el logo y el canvas azul
    frame_contenedor = tk.Frame(ventana, bg="#007BFF", height=ALTURA_FRANJA)
    frame_contenedor.pack(fill="x")

    # Cargar la imagen
    logo = tk.PhotoImage(file="imagenes/logo.png")
    logo = logo.subsample(4)  # Redimensionar la imagen

    # Crear el label para el logo y el texto dentro del frame
    label_logo_texto = tk.Label(frame_contenedor, image=logo, text="PayPy", font=FUENTE_LOGO, bg="#007BFF", fg="white", compound="top", padx=5, pady=10)
    label_logo_texto.pack(pady=(10, 0))

    # Este es el label que muestra el saldo
    label_saldo = tk.Label(ventana, text="Saldo: $0", font=FUENTE_TITULO)
    label_saldo.pack(pady=(8, 10))

    # Frame para los botones principales: 
    # el frame es el contenedor de los botones
    frame_botones_principales = tk.Frame(ventana)
    frame_botones_principales.pack()

    ####################### Botones principales#####################
    # Boton para ingresar dinero
    button_ingresar = tk.Button(frame_botones_principales, text="Ingresar \n dinero", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=nueva_ventana_ingresar_dinero)
    button_ingresar.grid(row=0, column=0, padx=5, pady=2)

    # Boton para consultar movimientos
    button_consultar = tk.Button(frame_botones_principales, text="Movimientos", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=consultar_movimientos)
    button_consultar.grid(row=0, column=1, padx=5, pady=2)

    # Boton para pagar servicios
    button_pagar = tk.Button(frame_botones_principales, text="Pagar \n servicio", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=nueva_ventana_seleccionar_servicio)
    button_pagar.grid(row=1, column=0, padx=5, pady=2)

    # Boton para agregar servicios
    button_agregar_servicio = tk.Button(frame_botones_principales, text="Agregar \n servicio", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=nueva_ventana_agregar_servicio)
    button_agregar_servicio.grid(row=1, column=1, padx=5, pady=2)

    # Boton para ver los beneficios
    button_beneficios = tk.Button(frame_botones_principales, text="Beneficios", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON)
    button_beneficios.grid(row=2, column=1, padx=5, pady=2)
    
    # Boton para eliminar servicios
    button_eliminar_servicio = tk.Button(frame_botones_principales, text="Eliminar \n servicio", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=nueva_ventana_eliminar_servicio)
    button_eliminar_servicio.grid(row=2, column=0, padx=5, pady=2)

    # Crear un frame para la franja azul que esta detrás de los botones
    frame_inferior = tk.Frame(ventana, bg="#007BFF", height=ALTURA_FRANJA)
    frame_inferior.pack(fill="x", side="bottom")

    # Colocar la franja azul detrás de los botones "HOME" y "SALIR"
    frame_inferior.lower() #lower es un método que coloca un widget debajo de otro

    # Botón HOME desactivado en el menu principal
    button_home = tk.Button(frame_inferior, text="HOME", font=FUENTE_BOTON, bg="white", fg="#007BFF", width=ANCHO_BOTON, height=ALTO_BOTON, state="disabled")
    button_home.pack(side=tk.LEFT, padx=5, pady=5)
    # Botón SALIR
    button_salir = tk.Button(frame_inferior, text="SALIR", font=FUENTE_BOTON, bg="white", fg="#007BFF", width=ANCHO_BOTON, height=ALTO_BOTON, command=ventana.destroy)
    button_salir.pack(side=tk.RIGHT, padx=5, pady=5)

    mostrar_saldo()  # Actualizar el saldo al iniciar la aplicación

    ventana.mainloop()

############### Funciones para las diferentes ventanas emergentes###############

# Ventana para seleccionar el servicio a pagar
def nueva_ventana_seleccionar_servicio():
    ventana_seleccionar = tk.Toplevel()
    ventana_seleccionar.title("Seleccionar Servicio")
    ventana_seleccionar.geometry("350x200")

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

    tk.Button(ventana_seleccionar, text="Cancelar", font=FUENTE_BOTON, bg="white", fg="#007BFF", width=ANCHO_BOTON, height=ALTO_BOTON, command=ventana_seleccionar.destroy).pack(pady=10)

# Ventana para agregar dinero
def nueva_ventana_ingresar_dinero():
    ventana_ingresar = tk.Toplevel()
    ventana_ingresar.title("Ingresar Dinero")
    ventana_ingresar.geometry("350x200")

    tk.Label(ventana_ingresar, text="Ingrese el monto a ingresar:", font=FUENTE_TEXTO).pack(pady=10)

    entry_monto = tk.Entry(ventana_ingresar, font=FUENTE_TEXTO)
    entry_monto.pack(pady=10)

    def ingresar_dinero():
        monto = entry_monto.get()
        if monto.isdigit():
            nuevo_movimiento = {
                "tipo": "ingreso",
                "monto": int(monto)  # Convertir a entero
            }
            movimientos = cargar_movimientos()
            movimientos.append(nuevo_movimiento)
            guardar_movimientos(movimientos)
            mostrar_saldo()
            ventana_ingresar.destroy()
        else:
            messagebox.showerror("Error", "Ingrese un monto válido.")

    tk.Button(ventana_ingresar, text="Ingresar", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=ingresar_dinero).pack(pady=10)
    tk.Button(ventana_ingresar, text="Cancelar", font=FUENTE_BOTON, bg="white", fg="#007BFF", width=ANCHO_BOTON, height=ALTO_BOTON, command=ventana_ingresar.destroy).pack(pady=10)

# Función para consultar los movimientos
def consultar_movimientos():
    ventana_movimientos = tk.Toplevel()
    ventana_movimientos.title("Movimientos")
    ventana_movimientos.geometry("400x300")

    frame_movimientos = tk.Frame(ventana_movimientos)
    frame_movimientos.pack(pady=10)

    tk.Label(frame_movimientos, text="Tipo", font=FUENTE_TEXTO_TABLA, width=15).grid(row=0, column=0)
    tk.Label(frame_movimientos, text="Monto", font=FUENTE_TEXTO_TABLA, width=15).grid(row=0, column=1)

    movimientos = cargar_movimientos()
    for i, movimiento in enumerate(movimientos, start=1):
        tipo = movimiento.get("tipo", "")
        monto = movimiento.get("monto", 0)
        tk.Label(frame_movimientos, text=tipo, font=FUENTE_TEXTO_TABLA, width=15).grid(row=i, column=0)
        tk.Label(frame_movimientos, text=str(int(monto)), font=FUENTE_TEXTO_TABLA, width=15).grid(row=i, column=1)  # Mostrar monto como entero

    tk.Button(ventana_movimientos, text="Cerrar", font=FUENTE_BOTON, bg="white", fg="#007BFF", width=ANCHO_BOTON, height=ALTO_BOTON, command=ventana_movimientos.destroy).pack(pady=10)

# Ventana para agregar un servicio
def nueva_ventana_agregar_servicio():
    ventana_agregar_servicio = tk.Toplevel()
    ventana_agregar_servicio.title("Agregar Servicio")
    ventana_agregar_servicio.geometry("350x200")

    tk.Label(ventana_agregar_servicio, text="Nombre del nuevo servicio:", font=FUENTE_TEXTO).pack(pady=10)

    entry_servicio = tk.Entry(ventana_agregar_servicio, font=FUENTE_TEXTO)
    entry_servicio.pack(pady=10)

    def agregar_servicio():
        nuevo_servicio = entry_servicio.get().strip()
        if nuevo_servicio:
            servicios = cargar_servicios()
            servicios.append(nuevo_servicio)
            guardar_servicios(servicios)
            ventana_agregar_servicio.destroy()
        else:
            messagebox.showerror("Error", "Ingrese un nombre de servicio válido.")

    tk.Button(ventana_agregar_servicio, text="Agregar", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=agregar_servicio).pack(pady=10)
    tk.Button(ventana_agregar_servicio, text="Cancelar", font=FUENTE_BOTON, bg="white", fg="#007BFF", width=ANCHO_BOTON, height=ALTO_BOTON, command=ventana_agregar_servicio.destroy).pack(pady=10)

# Ventana para eliminar un servicio
def nueva_ventana_eliminar_servicio():
    ventana_eliminar_servicio = tk.Toplevel()
    ventana_eliminar_servicio.title("Eliminar Servicio")
    ventana_eliminar_servicio.geometry("350x200")

    tk.Label(ventana_eliminar_servicio, text="Seleccione el servicio a eliminar:", font=FUENTE_TEXTO).pack(pady=10)

    servicios = cargar_servicios()

    def eliminar_servicio(servicio):
        servicios.remove(servicio)
        guardar_servicios(servicios)
        ventana_eliminar_servicio.destroy()

    for servicio in servicios:
        tk.Button(ventana_eliminar_servicio, text=servicio, font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=lambda s=servicio: eliminar_servicio(s)).pack(pady=5)

    tk.Button(ventana_eliminar_servicio, text="Cancelar", font=FUENTE_BOTON, bg="white", fg="#007BFF", width=ANCHO_BOTON, height=ALTO_BOTON, command=ventana_eliminar_servicio.destroy).pack(pady=10)

# Función para seleccionar un servicio y pagar
def seleccionar_servicio(servicio):
    ventana_seleccionar_servicio = tk.Toplevel()
    ventana_seleccionar_servicio.title(f"Pagar {servicio}")
    ventana_seleccionar_servicio.geometry("350x200")

    tk.Label(ventana_seleccionar_servicio, text=f"Pago del servicio: {servicio}", font=FUENTE_TEXTO).pack(pady=10)
    tk.Label(ventana_seleccionar_servicio, text="Ingrese el monto a pagar:", font=FUENTE_TEXTO).pack(pady=10)

    entry_monto = tk.Entry(ventana_seleccionar_servicio, font=FUENTE_TEXTO)
    entry_monto.pack(pady=10)

    def pagar_servicio():
        monto = entry_monto.get()
        if monto.isdigit():
            nuevo_movimiento = {
                "tipo": "egreso",
                "monto": int(monto)  # Convertir a entero
            }
            movimientos = cargar_movimientos()
            movimientos.append(nuevo_movimiento)
            guardar_movimientos(movimientos)
            mostrar_saldo()
            ventana_seleccionar_servicio.destroy()
        else:
            messagebox.showerror("Error", "Ingrese un monto válido.")

    tk.Button(ventana_seleccionar_servicio, text="Pagar", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=pagar_servicio).pack(pady=10)
    tk.Button(ventana_seleccionar_servicio, text="Cancelar", font=FUENTE_BOTON, bg="white", fg="#007BFF", width=ANCHO_BOTON, height=ALTO_BOTON, command=ventana_seleccionar_servicio.destroy).pack(pady=10)

if __name__ == "__main__":
    crear_ventana_principal()
