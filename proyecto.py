import tkinter as tk
import mysql.connector
from tkinter import ttk,messagebox
from tkinter import *


def login():
    usuario_ingresado = usuario.get()
    contrasena_ingresada = contrasena.get()
    mysqlC = mysql.connector.connect(host="localhost",user="root",password="",database="mysql")
    micursos=mysqlC.cursor()
    try:
        micursos.execute(f"SELECT * FROM usuarios WHERE usuario = '{usuario_ingresado}' and contrasena='{contrasena_ingresada}'")
        consulta = micursos.fetchone()

        if consulta:
            rol = consulta[5]

            if rol == "admin":
                segunda_ventana()

            elif rol == "empleado":
                pass
        else:
            messagebox.showinfo("Error al inicio de sesion")

    except Exception as e: 
        print(e)
        mysqlC.rollback()
        mysqlC.close()


def segunda_ventana():
    ventana_login.withdraw()
    
    ventana_sec = tk.Toplevel(ventana_login)
    ventana_sec.title("Segunda Ventana")
    
    def regresar_a_principal():
        ventana_sec.destroy()  
        ventana_login.deiconify()  

    boton_regresar = tk.Button(ventana_sec, text="Regresar a la ventana principal", command=regresar_a_principal)
    boton_regresar.pack(pady=20)

global id
global nombre
global apellido
global contrasena
global usuario

ventana_login = tk.Tk()
ventana_login.title("Login")


labelusuario = tk.Label(ventana_login, text="Usuario", font=("Arial", 12))
labelusuario.place(x=100, y=80)

labelcontrasena = tk.Label(ventana_login, text="Contrasena", font=("Arial", 12))
labelcontrasena.place(x=100, y=110)

usuario = tk.Entry(ventana_login)
usuario.place(x=270, y=80)

contrasena = tk.Entry(ventana_login)
contrasena.place(x=270, y=110)

tk.Button(ventana_login,text="Login",command=login, height=1, width=5, font=("Arial",12)).place(x=250,y=170)

ventana_login.mainloop()

