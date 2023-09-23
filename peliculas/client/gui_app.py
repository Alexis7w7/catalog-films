import tkinter as tk
from tkinter import ttk, messagebox
from model.pelicula_dao import crear_tabla, borrar_tabla
from model.pelicula_dao import Pelicula, guardar, listar, editar, eliminar


def barra_menu(root):
    barra_menu = tk.Menu(root)
    root.config(menu=barra_menu, width=300, height=300)

    menu_inicio = tk.Menu(barra_menu, tearoff=0)
    barra_menu.add_cascade(label="Inicio", menu=menu_inicio)

    menu_inicio.add_command(label="Crear Registro BD", command=crear_tabla)
    menu_inicio.add_command(label="Eliminar Registro BD", command=borrar_tabla)
    menu_inicio.add_command(label="Salir", command=root.destroy)

    barra_menu.add_cascade(label="Consultas")
    barra_menu.add_cascade(label="Configuracion")
    barra_menu.add_cascade(label="Ayuda")


class Frame(tk.Frame):
    def __init__(self, root=None):
        super().__init__(root, width=480, height=320)
        self.root = root
        self.pack()
        self.config(bg="grey")
        self.id_pelicula = None

        self.campos_peliculas()
        self.deshabilitar_campos()
        self.tabla_peliculas()

    def campos_peliculas(self):
        # labels de campo
        self.label_nombre = tk.Label(self, text="Nombre: ")
        self.label_nombre.config(font=("Arial", 12, "bold"))
        self.label_nombre.grid(row=0, column=0, padx=10, pady=10)

        self.label_duracion = tk.Label(self, text="Duracion: ")
        self.label_duracion.config(font=("Arial", 12, "bold"))
        self.label_duracion.grid(row=1, column=0, padx=10, pady=10)

        self.label_genero = tk.Label(self, text="Genero: ")
        self.label_genero.config(font=("Arial", 12, "bold"))
        self.label_genero.grid(row=2, column=0, padx=10, pady=10)

        # entrys de cada campo
        self.my_name = tk.StringVar()
        self.entry_nombre = tk.Entry(self, textvariable=self.my_name)
        self.entry_nombre.config(
            width=50,
            font=("Arial", 12))
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=10, columnspan=2)

        self.my_duracion = tk.StringVar()
        self.entry_duracion = tk.Entry(self, textvariable=self.my_duracion)
        self.entry_duracion.config(
            width=50,
            font=("Arial", 12))
        self.entry_duracion.grid(
            row=1,
            column=1,
            padx=10,
            pady=10,
            columnspan=2)

        self.my_genero = tk.StringVar()
        self.entry_genero = tk.Entry(self, textvariable=self.my_genero)
        self.entry_genero.config(
            width=50,
            font=("Arial", 12))
        self.entry_genero.grid(
            row=2,
            column=1,
            padx=10,
            pady=10,
            columnspan=2)

        # Buttoms
        self.new_buttom = tk.Button(
            self,
            text="New",
            command=self.habilitar_campos
            )
        self.new_buttom.config(
            width=20,
            font=("Arial", 12, "bold"),
            fg="#DAD5D6",
            bg="#158645",
            cursor="hand2",
            activebackground="#35BD6F",
        )
        self.new_buttom.grid(row=3, column=0, padx=10, pady=10)

        self.save_buttom = tk.Button(
            self,
            text="Save",
            command=self.guardar_datos
            )
        self.save_buttom.config(
            width=20,
            font=("Arial", 12, "bold"),
            fg="#DAD5D6",
            bg="#1658A2",
            cursor="hand2",
            activebackground="#3586DF",
        )
        self.save_buttom.grid(row=3, column=1, padx=10, pady=10)

        self.cancel_buttom = tk.Button(
            self,
            text="Cancel",
            command=self.deshabilitar_campos
            )
        self.cancel_buttom.config(
            width=20,
            font=("Arial", 12, "bold"),
            fg="#DAD5D6",
            bg="#BD152E",
            cursor="hand2",
            activebackground="#E15370",
        )
        self.cancel_buttom.grid(row=3, column=2, padx=10, pady=10)

    # metodos para habilitar
    def habilitar_campos(self):
        self.my_name.set('')
        self.my_duracion.set(' ')
        self.my_genero.set('')

        self.entry_nombre.config(state='normal')
        self.entry_duracion.config(state='normal')
        self.entry_genero.config(state='normal')

        self.save_buttom.config(state='normal')
        self.cancel_buttom.config(state='normal')

    def deshabilitar_campos(self):
        self.id_pelicula = None
        self.my_name.set('')
        self.my_duracion.set(' ')
        self.my_genero.set('')

        self.entry_nombre.config(state='disabled')
        self.entry_duracion.config(state='disabled')
        self.entry_genero.config(state='disabled')

        self.save_buttom.config(state='disabled')
        self.cancel_buttom.config(state='disabled')

    def guardar_datos(self):

        pelicula = Pelicula(
            self.my_name.get(),
            self.my_duracion.get(),
            self.my_genero.get()
        )

        if self.id_pelicula == None:
            guardar(pelicula)
        else:
            editar(pelicula, self.id_pelicula)

        self.tabla_peliculas()

        self.deshabilitar_campos()

    def tabla_peliculas(self):
        self.lista_peliculas = listar()
        self.lista_peliculas.reverse()
        self.tabla = ttk.Treeview(
            self,
            columns=('Nombre', 'Duracion', 'Genero')
        )
        self.tabla.grid(
            row=4,
            column=0,
            columnspan=4,
            sticky='nse'
        )

        # Scroll bar
        self.scroll = ttk.Scrollbar(
            self,
            orient='vertical',
            command=self.tabla.yview)
        self.scroll.grid(row=4, column=4, sticky='nse')
        self.tabla.configure(yscrollcommand=self.scroll.set)

        self.tabla.heading('#0', text='ID')
        self.tabla.heading('#1', text='NOMBRE')
        self.tabla.heading('#2', text='DURACION')
        self.tabla.heading('#3', text='GENERO')

        # Iterar lista de peliculas
        for p in self.lista_peliculas:
            self.tabla.insert('', 0, text=p[0], values=(p[1], p[2], p[3]))

        # Boton de Editar
        self.edit_buttom = tk.Button(
            self,
            text="Edit",
            command=self.editar_datos
            # command=self.habilitar_campos
            )
        self.edit_buttom.config(
            width=20,
            font=("Arial", 12, "bold"),
            fg="#DAD5D6",
            bg="#158645",
            cursor="hand2",
            activebackground="#35BD6F",
        )
        self.edit_buttom.grid(row=5, column=0, padx=10, pady=10)

        # Boton de Eliminar
        self.delete_buttom = tk.Button(
            self,
            text="Eliminar",
            command=self.eliminar_datos
            # command=self.deshabilitar_campos
            )
        self.delete_buttom.config(
            width=20,
            font=("Arial", 12, "bold"),
            fg="#DAD5D6",
            bg="#BD152E",
            cursor="hand2",
            activebackground="#E15370",
        )
        self.delete_buttom.grid(row=5, column=1, padx=10, pady=10)

    def editar_datos(self):
        try:
            self.id_pelicula = self.tabla.item(self.tabla.selection())['text']
            self.nombre_pelicula = self.tabla.item(
                self.tabla.selection())['values'][0]
            self.duracion_pelicula = self.tabla.item(
                self.tabla.selection())['values'][1]
            self.genero_pelicula = self.tabla.item(
                self.tabla.selection())['values'][2]

            self.habilitar_campos()

            self.entry_nombre.insert(0, self.nombre_pelicula)
            self.entry_duracion.insert(0, self.duracion_pelicula)
            self.entry_genero.insert(0, self.genero_pelicula)

        except:
            titulo = 'Edicion de datos'
            mensaje = 'No ha seleccionado ningun registro'
            messagebox.showerror(titulo, mensaje)

    def eliminar_datos(self):
        try:
            self.id_pelicula = self.tabla.item(self.tabla.selection())['text']
            eliminar(self.id_pelicula)
            self.tabla_peliculas()
            self.id_pelicula = None
        except:
            titulo = 'Eliminar un registro'
            mensaje = 'No se ha seleccionado ningun registro'
            messagebox.showerror(titulo, mensaje)
