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
                ventana_registro_libros()
        else:
            messagebox.showinfo("Error al inicio de sesion")

    except Exception as e: 
        print(e)
        mysqlC.rollback()
        mysqlC.close()

def registrar():
    nombreAdd = nombre.get()
    apellidoAdd = apellido.get()
    usuarioAdd = usuario.get()    
    contrasenaAdd = contrasena.get()
    rolAdd = rol.get()
    
    mysqlC = mysql.connector.connect(host="localhost",user="root",password="",database="mysql")
    micursos=mysqlC.cursor()

    try:
        micursos.execute(f"insert into usuarios(id, nombre, apellido, usuario, contrasena, rol) values('{nombreAdd}','{apellidoAdd}','{usuarioAdd}', '{contrasenaAdd}', '{rolAdd}')")
        mysqlC.commit()
        nombre.delete(0,END)
        apellido.delete(0,END)
        usuario.delete(0,END)
        contrasena.delete(0,END)
        rol.delete(0,END)
        messagebox.showinfo("informacion","usuario agregado")
        
    except Exception as e:
        print(e)
        mysqlC.rollback()
        mysqlC.close()

def delete():
    idAdd = idusuario.get()
    mysqlC = mysql.connector.connect(host="localhost",user="root",password="",database="mysql")
    micursos=mysqlC.cursor()
    try:
        micursos.execute(f"DELETE FROM USUARIOS WHERE id={idAdd}")
        mysqlC.commit()
        nombre.delete(0,END)
        apellido.delete(0,END)
        usuario.delete(0,END)
        contrasena.delete(0,END)
        rol.delete(0,END)
        messagebox.showinfo("informacion","usuario eliminado")
    except Exception as e:
        print(e)
        mysqlC.rollback()
        mysqlC.close()


def segunda_ventana():
    ventana_login.withdraw()
    
    ventana_sec = tk.Toplevel(ventana_login)
    ventana_sec.title("Segunda Ventana")
    ventana_sec.geometry("700x700")
    
    def regresar_a_principal():
        ventana_sec.destroy()  
        ventana_login.deiconify()
    
    def mostrarusuarios():
        mysqlC = mysql.connector.connect(host="localhost",user="root",password="",database="mysql")
        micursos=mysqlC.cursor()
        micursos.execute("select * from usuarios")
        lista_usuarios = micursos.fetchall()
        listbox1.delete(*listbox1.get_children())

        for (id,nombre,apellido,usuario, contrasena,rol) in lista_usuarios:
            listbox1.insert("","end",values=(id,nombre,apellido,usuario,contrasena,rol))
            micursos.close()
            mysqlC.close()

    tk.Label(ventana_sec, text="Nombre:", font=("Arial", 12)).place(x=100, y=80)
    tk.Label(ventana_sec, text="Apellido:", font=("Arial", 12)).place(x=100, y=110)
    tk.Label(ventana_sec, text="Usuario:", font=("Arial", 12)).place(x=100, y=140)
    tk.Label(ventana_sec, text="Contrasena:", font=("Arial", 12)).place(x=100, y=170)
    tk.Label(ventana_sec, text="Rol:", font=("Arial", 12)).place(x=100, y=200)
    tk.Label(ventana_sec, text="ID", font=("Arial", 12)).place(x=100, y=400 )
    
    global idusuario, nombre, apellido, usuario, contrasena, rol
    idusuario = tk.Entry(ventana_sec)
    idusuario.place(x=200, y=400)
    nombre = tk.Entry(ventana_sec)
    nombre.place(x=200, y=80)
    apellido = tk.Entry(ventana_sec)
    apellido.place(x=200, y=110)
    usuario = tk.Entry(ventana_sec)
    usuario.place(x=200, y=140)
    contrasena = tk.Entry(ventana_sec, show="*")
    contrasena.place(x=200, y=170)
    rol = tk.Entry(ventana_sec)
    rol.place(x=200, y=200)
    
    tk.Button(ventana_sec, text="Registrar Usuario", command=registrar).place(x=200, y=250)
    tk.Button(ventana_sec, text="Regresar a la ventana principal", command=regresar_a_principal).place(x=150, y=300)
    tk.Button(ventana_sec, text="Delete", command=delete).place(x=150, y=420)

    columnas = ("Id","Nombre","Apellido","Usuario", "Contraseña", "Rol")
    listbox1 = ttk.Treeview(ventana_sec,columns=columnas,show="headings")
    for col in columnas:
        listbox1.heading(col, text=col)
        listbox1.grid(row=1, column=0, columnspan=1)
        listbox1.place(x=0, y=450)
    mostrarusuarios()
        
##libros

def ventana_registro_libros(): 
    ventana_login.withdraw()

    ventana_libros = tk.Toplevel(ventana_login)
    ventana_libros.title("Registrar libros")
    ventana_libros.geometry("400x400")

    def regresar_prin():
        ventana_libros.destroy()
        ventana_login.deiconify()
    
    tk.Label(ventana_libros, text="ID: ", font=("Arial",12)).place(x=100, y=80)
    tk.Label(ventana_libros, text="Titulo: ", font=("Arial",12)).place(x=100, y=80)
    tk.Label(ventana_libros, text="Autor: ", font=("Arial",12)).place(x=100, y=140)
    tk.Label(ventana_libros, text="Editorial: ", font=("Arial",12)).place(x=100, y=17)
    tk.Label(ventana_libros, text="Año de publicacion: ", font=("Arial",12)).place(x=100, y=200)
    tk.Label(ventana_libros, text="Precio: ", font=("Arial",12)).place(x=100, y=400)
    tk.Button(ventana_libros, text="Registrar libro", command=registrar_libro).place(x=150, y=300)
    tk.Button(ventana_libros, text="Regresar a ventana principal", command=regresar_prin)


    global idlibro, titulo, autor, editorial, ano_publicacion, precio
    idlibro = tk.Entry(ventana_registro_libros)
    idlibro.place(x=200, y=80)
    titulo = tk.Entry(ventana_registro_libros)
    titulo.place(x=200, y=80)
    autor = tk.Entry(ventana_registro_libros)
    autor.place(x=200, y=110)
    editorial = tk.Entry(ventana_registro_libros)
    editorial.place(x=200, y=140)
    ano_publicacion = tk.Entry(ventana_registro_libros)
    ano_publicacion.place(x=200, y=140)
    precio = tk.Entry(ventana_registro_libros)
    precio.place(x=200, y=140)
    contrasena = tk.Entry(ventana_registro_libros, show="*")
    contrasena.place(x=200, y=170)
    rol = tk.Entry(ventana_registro_libros)
    rol.place(x=200, y=200)
    
    columnas = ("Id","Titulo","Autor","Editorial", "Año de publicacion", "Precio")
    listbox = ttk.Treeview(ventana_registro_libros,columns=columnas,show="headings")

    for col in columnas:
        listbox.heading(col, text=col)
        listbox.grid(row=1, column=0, columnspan=1)
        listbox.place(x=0, y=300)


def registrar_libro():
    titulo_add = titulo.get()
    autor_add = autor.get()
    editorial_add = editorial.get()
    ano_publicacion_add = ano_publicacion.get()
    precio_add = precio.get()
    
    mysqlC = mysql.connector.connect(host="localhost",user="root",password="",database="mysql")
    micursos=mysqlC.cursor()
    
    try:
        micursos.execute(f"insert into libros(id,titulo,autor,editorial, ano_publicacion, precio) values('{titulo_add}','{autor_add}','{editorial_add}', '{ano_publicacion_add}', '{precio_add}')")
        mysqlC.commit()
        titulo.delete(0,END)
        autor.delete(0,END)
        editorial.delete(0,END)
        ano_publicacion.delete(0,END)
        precio.delete(0,END)
        messagebox.showinfo("Libro registrado correctamente")

    except Exception as e:
        print(e)
        mysqlC.rollback()
        mysqlC.close()

def mostrar_libros():
    mysqlC = mysql.connector.connect(host="localhost",user="root",password="",database="mysql")
    micursos=mysqlC.cursor()
    micursos.execute("select * from libros")
    lista_libros = micursos.fetchall()
    
    columnas = ("Id","Titulo","Autor","Editorial", "Año de publicacion", "Precio")
    listbox = ttk.Treeview(ventana_registro_libros,columns=columnas,show="headings")

    for (id,titulo,autor,editorial, ano_publicacion, precio) in enumerate(lista_libros,start=1):
        listbox.insert("","end",values=(id,titulo,autor,editorial, ano_publicacion, precio))
        mysqlC.close()


def delete_libro():
    id_libro = idlibro.get()
    mysqlC = mysql.connector.connect(host="localhost",user="root",password="",database="mysql")
    micursos=mysqlC.cursor()
    try:
        micursos.execute(f"DELETE FROM libros WHERE id={id_libro}")
        mysqlC.commit()
        titulo.delete(0,END)
        autor.delete(0,END)
        editorial.delete(0,END)
        ano_publicacion.delete(0,END)
        precio.delete(0,END)
        messagebox.showinfo("Libro eliminado")
    except Exception as e:
        print(e)
        mysqlC.rollback()
        mysqlC.close()


global idusuario
global nombre
global apellido
global contrasena
global usuario
global titulo
global autor 
global editorial 
global ano_publicacion
global precio
global rol 
global idlibro


ventana_login = tk.Tk()
ventana_login.title("Login")
ventana_login.geometry("400x300")

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




