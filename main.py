import tkinter as tk
from tkinter import messagebox
import json

# Constantes de diseño
FUENTE_LOGO = ("Pacifico", 20)
FUENTE_TITULO = ("Ubuntu", 24, "bold")
FUENTE_TEXTO = ("Ubuntu", 16)
FUENTE_TEXTO_TABLA = ("Ubuntu", 12, "bold")
FUENTE_BOTON = ("Ubuntu", 10, "bold")
COLOR_PRINCIPAL = "#000000"
COLOR_BOTON = "#007BFF"
COLOR_TEXTO_BOTON = "#FFFFFF"
ANCHO_BOTON = 10
ALTO_BOTON = 2
ALTURA_FRANJA = 80

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
    movimientos = cargar_movimientos()
    saldo = sum(movimiento['monto'] for movimiento in movimientos if 'monto' in movimiento)
    label_saldo.config(text=f"Saldo: ${int(saldo)}")  # Mostrar saldo como entero

def configurar_ventana(ventana):
    # Configuración de redimensionamiento de la ventana principal
    ventana.resizable(True, True)  # Permitir redimensionamiento horizontal y vertical
    ventana.minsize(350, 500)  # Establecer tamaño mínimo para evitar que la ventana se haga demasiado pequeña

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

    button_ingresar = tk.Button(frame_botones_principales, text="Ingresar \n dinero", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=nueva_ventana_ingresar_dinero)
    button_ingresar.grid(row=0, column=0, padx=5, pady=2)

    button_consultar = tk.Button(frame_botones_principales, text="Movimientos", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=consultar_movimientos)
    button_consultar.grid(row=0, column=1, padx=5, pady=2)

    button_pagar = tk.Button(frame_botones_principales, text="Pagar \n servicio", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=nueva_ventana_seleccionar_servicio)
    button_pagar.grid(row=1, column=0, padx=5, pady=2)

    button_agregar_servicio = tk.Button(frame_botones_principales, text="Agregar \n servicio", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=nueva_ventana_agregar_servicio)
    button_agregar_servicio.grid(row=1, column=1, padx=5, pady=2)

    button_beneficios = tk.Button(frame_botones_principales, text="Beneficios", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON)
    button_beneficios.grid(row=2, column=1, padx=5, pady=2)
    
    button_eliminar_servicio = tk.Button(frame_botones_principales, text="Eliminar \n servicio", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=nueva_ventana_eliminar_servicio)
    button_eliminar_servicio.grid(row=2, column=0, padx=5, pady=2)

    mostrar_saldo()  # Actualizar el saldo al iniciar la aplicación

    ventana.mainloop()

def nueva_ventana_seleccionar_servicio():
    ventana_seleccionar = tk.Toplevel()
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

def nueva_ventana_ingresar_dinero():
    ventana_ingresar = tk.Toplevel()
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
            messagebox.showinfo("Ingreso exitoso", "Acreditación exitosa.")
            ventana_ingresar.destroy()
        else:
            messagebox.showerror("Error", "Por favor, ingrese un monto válido.")

    tk.Button(ventana_ingresar, text="Aceptar", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=guardar_ingreso).pack(pady=10)
    tk.Button(ventana_ingresar, text="Cancelar", font=FUENTE_BOTON, bg="white", fg=COLOR_BOTON, width=ANCHO_BOTON, height=ALTO_BOTON, command=ventana_ingresar.destroy).pack(pady=10)

def nueva_ventana_agregar_servicio():
    ventana_agregar_servicio = tk.Toplevel()
    ventana_agregar_servicio.title("Agregar Servicio")
    configurar_ventana(ventana_agregar_servicio)

    tk.Label(ventana_agregar_servicio, text="Ingrese el nombre del servicio:", font=FUENTE_TEXTO).pack(pady=10)
    entry_servicio = tk.Entry(ventana_agregar_servicio, font=FUENTE_TEXTO)
    entry_servicio.pack(pady=10)

    def guardar_servicio():
        servicio = entry_servicio.get()
        if servicio:
            servicios = cargar_servicios()
            if servicio not in servicios:  # Verificar si el servicio ya existe
                servicios.append(servicio)
                guardar_servicios(servicios)
                movimientos = cargar_movimientos()
                movimientos.append({"operacion": "Servicio Agregado", "monto": 0, "detalle": f"'{servicio}'"})
                guardar_movimientos(movimientos)
                mostrar_saldo()
                messagebox.showinfo("Éxito", "El servicio se agregó correctamente.")
            else:
                messagebox.showwarning("Advertencia", "El servicio ya existe.")
            ventana_agregar_servicio.destroy()
        else:
            messagebox.showerror("Error", "Por favor, ingrese un nombre de servicio válido.")

    tk.Button(ventana_agregar_servicio, text="Aceptar", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=guardar_servicio).pack(pady=10)
    tk.Button(ventana_agregar_servicio, text="Cancelar", font=FUENTE_BOTON, bg="white", fg=COLOR_BOTON, width=ANCHO_BOTON, height=ALTO_BOTON, command=ventana_agregar_servicio.destroy).pack(pady=10)

def nueva_ventana_eliminar_servicio():
    ventana_eliminar = tk.Toplevel()
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
                  s=servicio: eliminar_servicio(s)).pack(pady=5)

    tk.Button(ventana_eliminar, text="Cancelar", font=FUENTE_BOTON, bg="white", fg=COLOR_BOTON, width=ANCHO_BOTON, height=ALTO_BOTON, command=ventana_eliminar.destroy).pack(pady=10)

def eliminar_servicio(servicio):
    servicios = cargar_servicios()
    servicios = [s for s in servicios if s != servicio]
    guardar_servicios(servicios)
    movimientos = cargar_movimientos()
    movimientos.append({"operacion": "Servicio Eliminado", "monto": 0, "detalle": f"Se eliminó el servicio '{servicio}'"})
    guardar_movimientos(movimientos)
    mostrar_saldo()
    messagebox.showinfo("Éxito", "El servicio ha sido eliminado correctamente.")

def seleccionar_servicio(servicio):
    ventana_pago = tk.Toplevel()
    ventana_pago.title("Pagar Servicio")
    configurar_ventana(ventana_pago)

    tk.Label(ventana_pago, text=f"Pagar {servicio}", font=FUENTE_TEXTO).pack(pady=10)
    tk.Label(ventana_pago, text="Ingrese el monto:", font=FUENTE_TEXTO).pack(pady=10)
    entry_monto = tk.Entry(ventana_pago, font=FUENTE_TEXTO)
    entry_monto.pack(pady=10)

    def procesar_pago():
        monto = entry_monto.get()
        if monto.isdigit():
            movimientos = cargar_movimientos()
            movimientos.append({"operacion": "Pago", "monto": -int(monto), "detalle": f"Pago del servicio '{servicio}'"})
            guardar_movimientos(movimientos)
            mostrar_saldo()
            messagebox.showinfo("Pago exitoso", "El servicio ha sido pagado correctamente.")
            ventana_pago.destroy()
        else:
            messagebox.showerror("Error", "Por favor, ingrese un monto válido.")

    tk.Button(ventana_pago, text="Aceptar", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=procesar_pago).pack(pady=10)
    tk.Button(ventana_pago, text="Cancelar", font=FUENTE_BOTON, bg="white", fg=COLOR_BOTON, width=ANCHO_BOTON, height=ALTO_BOTON, command=ventana_pago.destroy).pack(pady=10)
    
def consultar_movimientos():
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
        
        # Esto es para centrar el texto en la celda
        tk.Label(frame_movimientos, text=operacion.capitalize(), font=FUENTE_TEXTO_TABLA, width=20, anchor='w').grid(row=i, column=0, padx=(0))
        tk.Label(frame_movimientos, text=f"${monto}", font=FUENTE_TEXTO_TABLA, width=20, anchor='w').grid(row=i, column=1, padx=(0))
        tk.Label(frame_movimientos, text=detalle, font=FUENTE_TEXTO_TABLA, width=20, anchor='w').grid(row=i, column=2, padx=(0))


    tk.Button(ventana_movimientos, text="Cerrar", font=FUENTE_BOTON, bg="white", fg=COLOR_BOTON, width=ANCHO_BOTON, height=ALTO_BOTON, command=ventana_movimientos.destroy).pack(pady=10)


# Iniciar la aplicación
crear_ventana_principal()
