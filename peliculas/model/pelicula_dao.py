from .conexion_db import ConexionDB
from tkinter import messagebox


def crear_tabla():
    conexion = ConexionDB()

    sql = """
    CREATE TABLE peliculas(
        id_pelicula INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre VARCHAR(100),
        duracion VARCHAR(10),
        genero VARCHAR(100)
    )
"""
    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()
        titulo = 'Crear Registro'
        mensaje = 'Se ha creado la tabla de Películas correctamente.'
        messagebox.showinfo(titulo, mensaje)
    except:
        titulo = 'Registro Ya Existente'
        mensaje = 'La tabla ya existe.'
        messagebox.showwarning(titulo, mensaje)


def borrar_tabla():
    conexion = ConexionDB()

    sql = """DROP TABLE peliculas"""

    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()
        titulo = 'Borrar Registro'
        mensaje = 'La tabla ha sido borrada con exito.'
        messagebox.showinfo(titulo, mensaje)
    except:
        titulo = 'Registro Ya Borrado'
        mensaje = 'La tabla ya ha sido borrada.'
        messagebox.showerror(titulo, mensaje)


class Pelicula:
    def __init__(self, nombre, duracion, genero):
        self.id_pelicula = None
        self.nombre = nombre
        self.duracion = duracion
        self.genero = genero

    def __str__(self):
        return f'Pelicula[{self.nombre}, {self.duracion}, {self.genero}]'


def guardar(pelicula):
    conexion = ConexionDB()

    sql = f"""INSERT INTO peliculas(nombre, duracion, genero)
    VALUES('{pelicula.nombre}',
    '{pelicula.duracion}',
    '{pelicula.genero}')"""

    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()
    except:
        titulo = 'Conexion al Registro'
        mensaje = 'La taabla pelicula no esta creada en la DB.'
        messagebox.showerror(titulo, mensaje)


def listar():
    conexion = ConexionDB()

    lista_peliculas = []

    sql = """SELECT * FROM peliculas"""

    try:
        conexion.cursor.execute(sql)
        lista_peliculas = conexion.cursor.fetchall()
        conexion.cerrar()
    except:
        titulo = 'Conexion al registro'
        mensaje = 'Crea la tabla en la base de datos'
        messagebox.showwarning(titulo, mensaje)

    return lista_peliculas


def editar(pelicula, id_pelicula):
    conexion = ConexionDB()

    sql = f"""UPDATE peliculas
    SET nombre = '{pelicula.nombre}',
    duracion = '{pelicula.duracion}',
    genero = '{pelicula.genero}'
    WHERE id_pelicula = '{id_pelicula}'
    """

    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()
    except:
        titulo = 'Edicion de datos'
        mensaje = 'No se ha podido editar este registro'
        messagebox.showerror(titulo, mensaje)


def eliminar(id_pelicula):
    conexion = ConexionDB()
    sql = f"""DELETE FROM peliculas WHERE id_pelicula = '{id_pelicula}'"""

    try:
        conexion.cursor.execute(sql)
        conexion.cerrar()
    except:
        titulo = 'Eliminar datos'
        mensaje = 'No se pudo eliminar el registro'
        messagebox.showerror(titulo, mensaje)
