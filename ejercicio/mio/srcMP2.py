'''
Created on 2 oct 2024

@author: alvaro
'''
import csv
from tkinter import *
from tkinter import messagebox
import sqlite3


def ventana_principal():
    raiz = Tk()

    menu = Menu(raiz)

    # DATOS
    menudatos = Menu(menu, tearoff=0)
    menudatos.add_command(label="Cargar", command=cargar)
    menudatos.add_command(label="Salir", command=raiz.quit)
    menu.add_cascade(label="Datos", menu=menudatos)
    
    # LISTAR
    menulistar = Menu(menu, tearoff=0)
    menulistar.add_command(label="Completo", command=listar_libros_completo)
    menulistar.add_command(label="Ordenado", command=listar_libros_ordenado)
    menu.add_cascade(label="Listar", menu=menulistar)
    
    # BUSCAR
    menubuscar = Menu(menu, tearoff=0)
    menubuscar.add_command(label="Título", command=buscar_titulo)
    menubuscar.add_command(label="Editorial", command=buscar_editorial)
    menu.add_cascade(label="Buscar", menu=menubuscar)

    raiz.config(menu=menu)

    raiz.mainloop()

    
def extraer_datos(fichero):
    try:
        with open(fichero) as f:
            l = [row for row in csv.reader(f, delimiter=';', quotechar='"')] 
        return l[1:]  # elimina la linea de la cabecera
    except:
        messagebox.showerror("Error", "Error en la apertura del fichero de libros")
        return None


def almacenar_bd(libros):

    conn = sqlite3.connect('libros.db')
    conn.text_factory = str
    conn.execute("DROP TABLE IF EXISTS LIBROS")
    conn.execute('''CREATE TABLE LIBROS
       (ISBN            TEXT NOT NULL,
        TITULO    TEXT,
        AUTOR      TEXT,
        AÑO            INTEGER,          
        EDITORIAL         TEXT);''')
    
    for libro in libros:
        isbn = libro[0]
        titulo = libro[1]
        autor = libro[2]
        editorial = libro[4]
        año = libro[3]
        if(libro[3] == 'Unknown'):
            año = 0
        
        conn.execute("""INSERT INTO LIBROS (ISBN, TITULO, AUTOR, EDITORIAL, AÑO) VALUES (?,?,?,?,?)""",
                     (isbn, titulo, autor, editorial, año))
    conn.commit()

    cursor = conn.execute("SELECT COUNT(*) FROM LIBROS")
    messagebox.showinfo("Base Datos",
                        "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " libros")
    conn.close()

    
def cargar():
    respuesta = messagebox.askyesno(title="Confirmar", message="Esta seguro que quiere recargar los datos?")
    if respuesta:
        libros = extraer_datos("books.csv")
        if libros:
            almacenar_bd(libros)
            

def listar_libros_completo():
            conn = sqlite3.connect('libros.db')
            conn.text_factory = str
            cursor = conn.execute("SELECT ISBN, TITULO, AUTOR, AÑO FROM LIBROS")
            conn.close
            formato_libros(cursor)
            
            
def formato_libros(cursor): 
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for row in cursor:
        s = 'TÍTULO: ' + row[1]
        lb.insert(END, s)
        lb.insert(END, "------------------------------------------------------------------------")
        s = "     ISBN: " + str(row[0]) + ' | AUTOR: ' + row[2] + ' | AÑO: ' + str(row[3])
        lb.insert(END, s)
        lb.insert(END, "\n\n")
    lb.pack(side=LEFT, fill=BOTH)
    sc.config(command=lb.yview)

    
def listar_libros_ordenado():

    def lista():
            conn = sqlite3.connect('libros.db')
            conn.text_factory = str
            if control.get() == 1:
                cursor = conn.execute("SELECT ISBN, TITULO, AUTOR, AÑO FROM LIBROS ORDER BY ISBN")
            else:
                cursor = conn.execute("SELECT ISBN, TITULO, AUTOR, AÑO FROM LIBROS ORDER BY AÑO")
            conn.close
            formato_libros(cursor)

    ventana = Toplevel()
    control = IntVar()
    rb1 = Radiobutton(ventana, text="Ordenado por Año", variable=control, value=0)
    rb2 = Radiobutton(ventana, text="Ordenado por ISBN", variable=control, value=1)
    b = Button(ventana, text="Listar", command=lista)
    rb1.pack()
    rb2.pack()
    b.pack()


def buscar_editorial():

    def lista(event):
            conn = sqlite3.connect('libros.db')
            conn.text_factory = str
            cursor = conn.execute("SELECT TITULO, AUTOR, EDITORIAL, AÑO FROM LIBROS WHERE EDITORIAL = '" + sb.get() + "'")
            conn.close
            formato_libros(cursor)
    
    conn = sqlite3.connect('libros.db')
    conn.text_factory = str
    cursor = conn.execute("SELECT DISTINCT EDITORIAL FROM LIBROS")
    
    editoriales = [i[0] for i in cursor]
        
    v = Toplevel()
    sb = Spinbox(v, values=editoriales)
    sb.bind("<Return>", lista)
    sb.pack()
    
    conn.close()
    

def buscar_titulo():

    def lista(event):
            conn = sqlite3.connect('libros.db')
            conn.text_factory = str
            cursor = conn.execute("SELECT ISBN, TITULO, AUTOR, AÑO FROM LIBROS WHERE TITULO LIKE  '%" + en.get() + "%'")
            conn.close
            formato_libros(cursor)
    
    conn = sqlite3.connect('libros.db')
    conn.text_factory = str
        
    v = Toplevel()
    lb = Label(v, text="Introduzca la palabra a buscar")
    en = Entry(v)
    en.bind("<Return>", lista)
    lb.pack(side=LEFT)
    en.pack(side=LEFT)
    
    conn.close()


if __name__ == '__main__':
    ventana_principal()
    
