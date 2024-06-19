# CREAR BILLETERA VIRTUAL

# MENU PRINCIPAL: LOGO, SALDO, BOTON INGRESAR DINERO, 
# BOTON PAGAR SERVICIO, BOTON MOVIMIENTOS, BOTON AGREGAR O ELIMINAR SERVICIO, BOTON SALIR
# MENU DE SERVICIOS: SE LISTAN LOS SERVICIOS EN BOTONES: LUZ, AGUA, GAS Y 
# HAY UN BOTON PARA INGRESAR EL MONTO LUEGO DE SELECCIONAR EL SERVICIO
# OTRO BOTON QUE ME PERMITA AGREGAR OTRO SERVICIO O ELIMINARLO. LUEGO, VUELVE AL MENU PRINCIPAL
# MENU DE MOVIMIENTOS: SE LISTAN LOS MOVIMIENTOS REALIZADOS EN UNA TABLA.
# BOTON PARA VOLVER AL MENU PRINCIPAL
# UTILIZAMOS JSON PARA GUARDAR LOS DATOS DE LOS SERVICIOS Y LOS MOVIMIENTOS
import tkinter as tk
from tkinter import messagebox
import json

# Constantes de diseño
FUENTE_LOGO = ("Pacifico", 20)
FUENTE_TITULO = ("Ubuntu", 24, "bold")
FUENTE_TEXTO = ("Ubuntu", 16)
FUENTE_BOTON = ("Ubuntu", 10, "bold")
COLOR_PRINCIPAL = "#000000"
COLOR_BOTON = "#007BFF"
COLOR_TEXTO_BOTON = "#FFFFFF"
ANCHO_BOTON = 10
ALTO_BOTON = 2
ALTURA_FRANJA = 80

# Funciones para manejar los movimientos
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

def guardar_servicios(servicios):
    with open('servicios.json', 'w') as archivo:
        json.dump(servicios, archivo)

# Función para mostrar el saldo
def mostrar_saldo():
    movimientos = cargar_movimientos()
    saldo = sum(movimiento['monto'] if movimiento.get('tipo') == 'ingreso' else -movimiento['monto'] for movimiento in movimientos if 'monto' in movimiento and 'tipo' in movimiento)
    label_saldo.config(text=f"Saldo: ${saldo:.2f}")

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

 
    # Saldo
    label_saldo = tk.Label(ventana, text="Saldo: $0", font=FUENTE_TITULO)
    label_saldo.pack(pady=(8, 10))

    # Frame para los botones principales
    frame_botones_principales = tk.Frame(ventana)
    frame_botones_principales.pack()

    # Botones principales
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


    # Crear un frame para la franja azul
    frame_inferior = tk.Frame(ventana, bg="#007BFF", height=ALTURA_FRANJA)
    frame_inferior.pack(fill="x", side="bottom")

    # Colocar la franja azul detrás de los botones "HOME" y "SALIR"
    frame_inferior.lower()

    # Botón HOME desactivado en el menu principal
    button_home = tk.Button(frame_inferior, text="HOME", font=FUENTE_BOTON, bg="white", fg="#007BFF", width=ANCHO_BOTON, height=ALTO_BOTON, state="disabled")
    button_home.pack(side=tk.LEFT, padx=5, pady=5)

    button_salir = tk.Button(frame_inferior, text="SALIR", font=FUENTE_BOTON, bg="white", fg="#007BFF", width=ANCHO_BOTON, height=ALTO_BOTON, command=ventana.destroy)
    button_salir.pack(side=tk.RIGHT, padx=5, pady=5)

    mostrar_saldo()  # Actualizar el saldo al iniciar la aplicación

    ventana.mainloop()

# Funciones para las diferentes ventanas emergentes
def nueva_ventana_ingresar_dinero():
    ventana_ingresar = tk.Toplevel()
    ventana_ingresar.title("Ingresar Dinero")
    ventana_ingresar.geometry("350x200")

    def ingresar():
        monto = entry_monto.get()
        if monto:
            try:
                monto = float(monto)
                movimientos = cargar_movimientos()
                movimientos.append({"tipo": "ingreso", "monto": monto})
                guardar_movimientos(movimientos)
                messagebox.showinfo("Éxito", f"Se ha ingresado ${monto}.")
                ventana_ingresar.destroy()
                mostrar_saldo()
                consultar_movimientos()  # Actualizar la lista de movimientos
            except ValueError:
                messagebox.showerror("Error", "Debe ingresar un monto válido.")
        else:
            messagebox.showerror("Error", "Debe ingresar un monto.")

    tk.Label(ventana_ingresar, text="Ingrese el monto a ingresar:", font=FUENTE_TEXTO).pack(pady=10)
    entry_monto = tk.Entry(ventana_ingresar, font=FUENTE_TEXTO)
    entry_monto.pack(pady=10)
    tk.Button(ventana_ingresar, text="Ingresar", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", command=ingresar).pack(pady=20)
    tk.Button(ventana_ingresar, text="HOME", font=FUENTE_BOTON, bg="white", fg="#007BFF", width=ANCHO_BOTON, height=ALTO_BOTON, command=ventana_ingresar.destroy).pack(pady=5)

def nueva_ventana_agregar_servicio():
    ventana_agregar = tk.Toplevel()
    ventana_agregar.title("Agregar Servicio")
    ventana_agregar.geometry("350x200")

    def agregar_servicio(servicio):
        if servicio:
            servicios = cargar_servicios()
            servicios.append(servicio)
            guardar_servicios(servicios)
            messagebox.showinfo("Éxito", f"Se ha agregado el servicio {servicio}.")
            ventana_agregar.destroy()
        else:
            messagebox.showerror("Error", "Debe ingresar el nombre del servicio.")

    tk.Label(ventana_agregar, text="Ingrese el nombre del servicio:", font=FUENTE_TEXTO).pack(pady=10)
    entry_servicio = tk.Entry(ventana_agregar, font=FUENTE_TEXTO)
    entry_servicio.pack(pady=10)
    tk.Button(ventana_agregar, text="Agregar Servicio", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", command=lambda: agregar_servicio(entry_servicio.get())).pack(pady=20)
    tk.Button(ventana_agregar, text="HOME", font=FUENTE_BOTON, bg="white", fg="#007BFF", width=ANCHO_BOTON, height=ALTO_BOTON, command=ventana_agregar.destroy).pack(pady=5)

def nueva_ventana_eliminar_servicio():
    ventana_eliminar = tk.Toplevel()
    ventana_eliminar.title("Eliminar Servicio")
    ventana_eliminar.geometry("350x300")

    def eliminar_servicio(servicio):
        servicios = cargar_servicios()
        if servicio in servicios:
            servicios.remove(servicio)
            guardar_servicios(servicios)
            messagebox.showinfo("Éxito", f"Se ha eliminado el servicio {servicio}.")
            ventana_eliminar.destroy()
        else:
            messagebox.showerror("Error", f"No se encontró el servicio {servicio}.")

    tk.Label(ventana_eliminar, text="Seleccione el servicio a eliminar:", font=FUENTE_TEXTO).pack(pady=10)

    frame_servicios = tk.Frame(ventana_eliminar)
    frame_servicios.pack()

    servicios = cargar_servicios()

    for idx, servicio in enumerate(servicios):
        tk.Button(frame_servicios, text=servicio, font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON,
                  command=lambda s=servicio: eliminar_servicio(s)).grid(row=idx, column=0, padx=5, pady=2)

    tk.Button(ventana_eliminar, text="HOME", font=FUENTE_BOTON, bg="white", fg="#007BFF", width=ANCHO_BOTON, height=ALTO_BOTON, command=ventana_eliminar.destroy).pack(pady=5)


def nueva_ventana_seleccionar_servicio():
    ventana_seleccionar = tk.Toplevel()
    ventana_seleccionar.title("Seleccionar Servicio")
    ventana_seleccionar.geometry("350x200")

    tk.Label(ventana_seleccionar, text="Seleccione el servicio a pagar:", font=FUENTE_TEXTO).pack(pady=10)

    servicios = cargar_servicios()

    for servicio in servicios:
        tk.Button(ventana_seleccionar, text=servicio, font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON,
                  command=lambda s=servicio: seleccionar_servicio(s)).pack(pady=5)

    tk.Button(ventana_seleccionar, text="HOME", font=FUENTE_BOTON, bg="white", fg="#007BFF", width=ANCHO_BOTON, height=ALTO_BOTON, command=ventana_seleccionar.destroy).pack(pady=5)


    def seleccionar_servicio(servicio):
        ventana_seleccionar.destroy()
        nueva_ventana_pagar_servicio(servicio)

    tk.Label(ventana_seleccionar, text="Seleccione el servicio a pagar:", font=FUENTE_TEXTO).pack(pady=10)

    tk.Button(ventana_seleccionar, text="LUZ", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=lambda: seleccionar_servicio("LUZ")).pack(pady=5)
    tk.Button(ventana_seleccionar, text="AGUA", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=lambda: seleccionar_servicio("AGUA")).pack(pady=5)
    tk.Button(ventana_seleccionar, text="GAS", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON, command=lambda: seleccionar_servicio("GAS")).pack(pady=5)
    tk.Button(ventana_seleccionar, text="HOME", font=FUENTE_BOTON, bg="white", fg="#007BFF", width=ANCHO_BOTON, height=ALTO_BOTON, command=ventana_seleccionar.destroy).pack(pady=5)

def nueva_ventana_pagar_servicio(servicio):
    ventana_pagar = tk.Toplevel()
    ventana_pagar.title(f"Pagar {servicio}")
    ventana_pagar.geometry("350x200")
    
def pagar(servicio):
    ventana_pagar = tk.Toplevel()
    ventana_pagar.title(f"Pagar {servicio}")
    ventana_pagar.geometry("350x200")

    def realizar_pago():
        monto = entry_monto.get()
        if monto:
            try:
                monto = float(monto)
                movimientos = cargar_movimientos()
                movimientos.append({"tipo": "egreso", "monto": monto, "servicio": servicio})
                guardar_movimientos(movimientos)
                messagebox.showinfo("Éxito", f"Se ha pagado ${monto} por el servicio {servicio}.")
                ventana_pagar.destroy()
                mostrar_saldo()
            except ValueError:
                messagebox.showerror("Error", "Debe ingresar un monto válido.")
        else:
            messagebox.showerror("Error", "Debe ingresar un monto.")

    tk.Label(ventana_pagar, text=f"Ingrese el monto a pagar por {servicio}:", font=FUENTE_TEXTO).pack(pady=10)
    entry_monto = tk.Entry(ventana_pagar, font=FUENTE_TEXTO)
    entry_monto.pack(pady=10)
    tk.Button(ventana_pagar, text="Pagar", font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", command=realizar_pago).pack(pady=20)
    tk.Button(ventana_pagar, text="HOME", font=FUENTE_BOTON, bg="white", fg="#007BFF", width=ANCHO_BOTON, height=ALTO_BOTON, command=ventana_pagar.destroy).pack(pady=5)

def nueva_ventana_seleccionar_servicio():
    ventana_seleccionar = tk.Toplevel()
    ventana_seleccionar.title("Seleccionar Servicio")
    ventana_seleccionar.geometry("350x200")

    tk.Label(ventana_seleccionar, text="Seleccione el servicio a pagar:", font=FUENTE_TEXTO).pack(pady=10)

    servicios = cargar_servicios()

    for servicio in servicios:
        tk.Button(ventana_seleccionar, text=servicio, font=FUENTE_BOTON, bg=COLOR_BOTON, fg="white", width=ANCHO_BOTON, height=ALTO_BOTON,
                  command=lambda s=servicio: pagar(s)).pack(pady=5)

    tk.Button(ventana_seleccionar, text="HOME", font=FUENTE_BOTON, bg="white", fg="#007BFF", width=ANCHO_BOTON, height=ALTO_BOTON, command=ventana_seleccionar.destroy).pack(pady=5)
def consultar_movimientos():
    ventana_movimientos = tk.Toplevel()
    ventana_movimientos.title("Movimientos")
    ventana_movimientos.geometry("400x500")

    movimientos = cargar_movimientos()

    print("Movimientos cargados:", movimientos)  # Verificar qué datos se están cargando

    if not movimientos:
        tk.Label(ventana_movimientos, text="No hay movimientos para mostrar.", font=FUENTE_TEXTO).pack(pady=20)
    else:
        frame_movimientos = tk.Frame(ventana_movimientos)
        frame_movimientos.pack(pady=20)

        tk.Label(frame_movimientos, text="Tipo", font=FUENTE_TEXTO, width=15, borderwidth=1, relief="solid").grid(row=0, column=0)
        tk.Label(frame_movimientos, text="Monto", font=FUENTE_TEXTO, width=15, borderwidth=1, relief="solid").grid(row=0, column=1)
        tk.Label(frame_movimientos, text="Servicio", font=FUENTE_TEXTO, width=15, borderwidth=1, relief="solid").grid(row=0, column=2)

        for idx, movimiento in enumerate(movimientos, start=1):
            # Asegúrate de manejar los casos donde las claves no existan
            tipo = movimiento.get("tipo", "-")
            monto = movimiento.get("monto", "-")
            servicio = movimiento.get("servicio", "-")

            tk.Label(frame_movimientos, text=tipo, font=FUENTE_TEXTO, width=15, borderwidth=1, relief="solid").grid(row=idx, column=0)
            tk.Label(frame_movimientos, text=f"${monto:.2f}", font=FUENTE_TEXTO, width=15, borderwidth=1, relief="solid").grid(row=idx, column=1)
            tk.Label(frame_movimientos, text=servicio, font=FUENTE_TEXTO, width=15, borderwidth=1, relief="solid").grid(row=idx, column=2)

    tk.Button(ventana_movimientos, text="HOME", font=FUENTE_BOTON, bg="white", fg="#007BFF", width=ANCHO_BOTON, height=ALTO_BOTON, command=ventana_movimientos.destroy).pack(pady=5)

def main():
    crear_ventana_principal()

if __name__ == "__main__":
    main()
