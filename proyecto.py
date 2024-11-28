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

def registrar(listbox1):
    nombreAdd = nombre.get()
    apellidoAdd = apellido.get()
    usuarioAdd = usuarior.get()    
    contrasenaAdd = contrasenar.get()
    rolAdd = rol.get()
    
    mysqlC = mysql.connector.connect(host="localhost",user="root",password="",database="mysql")
    micursos=mysqlC.cursor()
    try:
        micursos.execute(f"INSERT INTO usuarios(nombre, apellido, usuario, contrasena, rol) VALUES('{nombreAdd}','{apellidoAdd}','{usuarioAdd}', '{contrasenaAdd}', '{rolAdd}')")
        mysqlC.commit()
        nombre.delete(0,END)
        apellido.delete(0,END)
        usuarior.delete(0,END)
        contrasenar.delete(0,END)
        rol.delete(0,END)
        messagebox.showinfo("informacion","usuario agregado")
        actualizarusuarios(listbox1)
        
    except Exception as e:
        print(e)
        mysqlC.rollback()
        mysqlC.close()

def delete(listbox1):
    idAdd = idusuario.get()
    mysqlC = mysql.connector.connect(host="localhost",user="root",password="",database="mysql")
    micursos=mysqlC.cursor()
    try:
        micursos.execute("DELETE FROM usuarios WHERE id = %s", (idAdd,))
        mysqlC.commit()

        nombre.delete(0,END)
        apellido.delete(0,END)
        usuarior.delete(0,END)
        contrasenar.delete(0,END)
        rol.delete(0,END)
        messagebox.showinfo("informacion","usuario eliminado")
        actualizarusuarios(listbox1)

    except Exception as e:
        print(e)
        mysqlC.rollback()
        mysqlC.close()

##ventana users

def segunda_ventana():
    ventana_login.withdraw()

    ventana_sec = tk.Toplevel(ventana_login)
    ventana_sec.title("Registrar Usuarios")
    ventana_sec.geometry("1200x600")
    
    def regresar_a_principal():
        ventana_sec.destroy()  
        ventana_login.deiconify()

    tk.Label(ventana_sec, text="ID:", font=("Arial", 12)).place(x=400, y=120)
    tk.Label(ventana_sec, text="Nombre:", font=("Arial", 12)).place(x=100, y=120)
    tk.Label(ventana_sec, text="Apellido:", font=("Arial", 12)).place(x=100, y=160)
    tk.Label(ventana_sec, text="Usuario:", font=("Arial", 12)).place(x=100, y=200)
    tk.Label(ventana_sec, text="Contrasena:", font=("Arial", 12)).place(x=100, y=240)
    tk.Label(ventana_sec, text="Rol: ", font=("Arial", 12)).place(x=100, y=280 )
    
    global idusuario, nombre, apellido, usuarior, contrasenar, rol
    idusuario = tk.Entry(ventana_sec)
    idusuario.place(x=450, y=120)
    nombre = tk.Entry(ventana_sec)
    nombre.place(x=200, y=120)
    apellido = tk.Entry(ventana_sec)
    apellido.place(x=200, y=160)
    usuarior = tk.Entry(ventana_sec)
    usuarior.place(x=200, y=200)
    contrasenar = tk.Entry(ventana_sec, show="*")
    contrasenar.place(x=200, y=240)
    rol = tk.Entry(ventana_sec)
    rol.place(x=200, y=280)
    
    
    tk.Button(ventana_sec, text="Registrar Usuario", command=lambda: registrar(listbox1)).place(x=160, y=340)
    tk.Button(ventana_sec, text="Regresar a la ventana principal", command=regresar_a_principal).place(x=800, y=200)
    tk.Button(ventana_sec, text="Delete", command=lambda: delete(listbox1)).place(x=460, y=160)

    columnas = ("Id","Nombre","Apellido","Usuario", "Contraseña", "Rol")
    listbox1 = ttk.Treeview(ventana_sec,columns=columnas,show="headings")
    for col in columnas:
        listbox1.heading(col, text=col)
        listbox1.grid(row=1, column=0, columnspan=1)
        listbox1.place(x=0, y=450)
    mostrarusuarios(listbox1)

def mostrarusuarios(listbox1):
        mysqlC = mysql.connector.connect(host="localhost",user="root",password="",database="mysql")
        micursos=mysqlC.cursor()
        micursos.execute("select * from usuarios")
        lista_usuarios = micursos.fetchall()
        listbox1.delete(*listbox1.get_children())

        for (id,nombre,apellido,usuario, contrasena,rol) in lista_usuarios:
            listbox1.insert("","end",values=(id,nombre,apellido,usuario,contrasena,rol))
            micursos.close()
            mysqlC.close()

def actualizarusuarios(listbox1):
    for i in listbox1.get_children():
        listbox1.delete(i)
        mostrarusuarios(listbox1)

def actualizar(listbox):
    for i in listbox.get_children():
        listbox.delete(i)
        mostrar_libros(listbox)


def mostrar_libros(listbox):
    mysqlC = mysql.connector.connect(host="localhost", user="root", password="", database="mysql")
    micursos = mysqlC.cursor()
    micursos.execute("SELECT * FROM libros")
    lista_libros = micursos.fetchall()
    listbox.delete(*listbox.get_children())

    for (id, titulo, autor, editorial, ano_publicacion, precio) in lista_libros:
        listbox.insert("", "end", values=(id, titulo, autor, editorial, ano_publicacion, precio))
    
    micursos.close()
    mysqlC.close()

def ventana_registro_libros(): 
    ventana_login.withdraw()

    ventana_libros = tk.Toplevel(ventana_login)
    ventana_libros.title("Registrar libros")
    ventana_libros.geometry("1200x600")

    def regresar_prin():
        ventana_libros.destroy()
        ventana_login.deiconify()

    global idlibro, titulo, autor, editorial, ano_publicacion, precio, editorialf
    idlibro = tk.Entry(ventana_libros)
    idlibro.place(x=450, y=120)
    titulo = tk.Entry(ventana_libros)
    titulo.place(x=200, y=120)
    autor = tk.Entry(ventana_libros)
    autor.place(x=200, y=160)
    editorial = tk.Entry(ventana_libros)
    editorial.place(x=200, y=200)
    ano_publicacion = tk.Entry(ventana_libros)
    ano_publicacion.place(x=200, y=240)
    precio = tk.Entry(ventana_libros)
    precio.place(x=200, y=280)
    editorialf = tk.Entry(ventana_libros)
    editorialf.place(x=450, y=240)
    
    
    tk.Label(ventana_libros, text="ID: ", font=("Arial",12)).place(x=400, y=120)
    tk.Label(ventana_libros, text="Titulo: ", font=("Arial",12)).place(x=100, y=120)
    tk.Label(ventana_libros, text="Autor: ", font=("Arial",12)).place(x=100, y=160)
    tk.Label(ventana_libros, text="Editorial: ", font=("Arial",12)).place(x=100, y=200)
    tk.Label(ventana_libros, text="Año: ", font=("Arial",12)).place(x=100, y=240)
    tk.Label(ventana_libros, text="Precio: ", font=("Arial",12)).place(x=100, y=280)
    tk.Label(ventana_libros, text="Filtrar x Editorial: ", font=("Arial",12)).place(x=400, y=200)

    
    tk.Button(ventana_libros, text="Registrar libro", command=lambda: registrar_libro(listbox)).place(x=160, y=340)
    tk.Button(ventana_libros, text="Eliminar libro", command=lambda: delete_libro(listbox)).place(x=460, y=160)
    tk.Button(ventana_libros, text="Filtrar", command=lambda: filtrar_libro(listbox)).place(x=460, y=270)
    tk.Button(ventana_libros, text="Regresar a ventana principal", command=regresar_prin).place(x=160, y=400)
    columnas = ("Id", "Titulo", "Autor", "Editorial", "Año de publicacion", "Precio")
    listbox = ttk.Treeview(ventana_libros, columns=columnas, show="headings")

    for col in columnas:
        listbox.heading(col, text=col)
        listbox.grid(row=1, column=0, columnspan=1)
        listbox.place(x=0, y=450)
    
    mostrar_libros(listbox)


def registrar_libro(listbox):
    titulo_add = titulo.get()
    autor_add = autor.get()
    editorial_add = editorial.get()
    ano_publicacion_add = ano_publicacion.get()
    precio_add = precio.get()
    
    mysqlC = mysql.connector.connect(host="localhost", user="root", password="", database="mysql")
    micursos = mysqlC.cursor()
    
    try:
        micursos.execute(f"INSERT INTO libros(titulo, autor, editorial, ano_publicacion, precio) VALUES('{titulo_add}', '{autor_add}', '{editorial_add}', '{ano_publicacion_add}', '{precio_add}')")
        mysqlC.commit()
        
        titulo.delete(0, END)
        autor.delete(0, END)
        editorial.delete(0, END)
        ano_publicacion.delete(0, END)
        precio.delete(0, END)
        messagebox.showinfo("Libro registrado correctamente")
        actualizar(listbox)
        
    except Exception as e:
        print(e)
        mysqlC.rollback()
        mysqlC.close()

def delete_libro(listbox):
    id_libro = idlibro.get()
    mysqlC = mysql.connector.connect(host="localhost", user="root", password="", database="mysql")
    micursos = mysqlC.cursor()
    
    try:
        micursos.execute(f"DELETE FROM libros WHERE id={id_libro}")
        mysqlC.commit()
        
        titulo.delete(0, END)
        autor.delete(0, END)
        editorial.delete(0, END)
        ano_publicacion.delete(0, END)
        precio.delete(0, END)
        messagebox.showinfo("Libro eliminado")
        actualizar(listbox)
        
    except Exception as e:
        print(e)
        mysqlC.rollback()
        mysqlC.close()


def filtrar_libro(listbox):
    editorial = editorialf.get()
    mysqlC = mysql.connector.connect(host="localhost", user="root", password="", database="mysql")
    micursos = mysqlC.cursor()
    micursos.execute(f"SELECT * FROM libros WHERE editorial ='{editorial}'")
    lista_libros = micursos.fetchall()
    listbox.delete(*listbox.get_children())

    for (id, titulo, autor, editorial, ano_publicacion, precio) in lista_libros:
        listbox.insert("", "end", values=(id, titulo, autor, editorial, ano_publicacion, precio))
    micursos.close()
    mysqlC.close()

ventana_login = tk.Tk()
ventana_login.title("Login")
ventana_login.geometry("500x300")

labelusuario = tk.Label(ventana_login, text="Usuario", font=("Arial", 12))
labelusuario.place(x=100, y=80)

labelcontrasena = tk.Label(ventana_login, text="Contrasena", font=("Arial", 12))
labelcontrasena.place(x=100, y=110)

usuario = tk.Entry(ventana_login)
usuario.place(x=270, y=80)

contrasena = tk.Entry(ventana_login)
contrasena.place(x=270, y=110)

tk.Button(ventana_login, text="Login", command=login, height=1, width=5, font=("Arial",12)).place(x=250, y=170)

ventana_login.mainloop()
