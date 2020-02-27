import sqlite3
import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo


os.system("clear")

conn = sqlite3.connect("test.db")

c = conn.cursor()

sql = "frames3"
sql_tabel = "CREATE TABLE IF NOT EXISTS " + sql +" (Voornaam text, Achternaam text, geslacht text, mail text)"
sql_data_entry = "INSERT INTO "+ sql +" (Voornaam, Achternaam, geslacht, mail) VALUES (?,?,?,?)"
sql_update = "UPDATE "+ sql + " SET Voornaam = ?, Achternaam = ?, geslacht = ?, mail = ? WHERE rowid = ?"
sql_delete = "DELETE FROM "+ sql + " WHERE Achternaam = ?"

#=======================class InputFrame===============================
class App(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

		width = self.winfo_screenwidth()
		height = self.winfo_screenheight()

		self.geometry(f"{width}x{height}+0+0")

		container = tk.Frame(self)

		container.pack(side="top", fill="both", expand = True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_columnconfigure(0, weight=1)
		container.pack()
		#container.place(bordermode = OUTSIDE, relx = 0, rely = 0, relheight = 1, relwidth = 1)

		self.frames = {}

		for F in (StartPage, Aanwezigheden, Toevoegen, Vooruitgang, Opmerkingen,Aanbevelingen):

			frame = F(container, self)

			self.frames[F] = frame

			frame.grid(row=0, column=0, sticky="nsew")

		self.show_frame(Toevoegen)

	def show_frame(self, cont):
		frame = self.frames[cont]
		frame.tkraise()

class StartPage(tk.Frame):
	def __init__(self, window, controller):
		tk.Frame.__init__(self, window)
		self["bg"] = "white"

		fontsize = "Verdana 30"

		s = ttk.Style()
		s.configure('my.TButton', font=('Helvetica', 30))

		self.b1 = ttk.Button(self, text = "Toevoegen", command=lambda: controller.show_frame(Toevoegen), style="my.TButton")
		self.b2 = ttk.Button(self, text = "Aanwezigheden",command=lambda: controller.show_frame(Aanwezigheden), style='my.TButton')
		self.b3 = ttk.Button(self, text = "Vooruitgang",command=lambda: controller.show_frame(Vooruitgang), style='my.TButton')
		self.b4 = ttk.Button(self, text = "Opmerkingen",command=lambda: controller.show_frame(Opmerkingen), style='my.TButton')
		self.b5 = ttk.Button(self, text = "Aanbevelingen",command=lambda: controller.show_frame(Aanbevelingen), style='my.TButton')
		self.b6 = ttk.Button(self, text = "Afsluiten", command=lambda: self.quit(), style='my.TButton')

		self.b1.place( relx = 0.35, rely = 0.20, relheight = 0.1, relwidth = 0.3)
		self.b2.place( relx = 0.35, rely = 0.31, relheight = 0.1, relwidth = 0.3)
		self.b3.place( relx = 0.35, rely = 0.42, relheight = 0.1, relwidth = 0.3)
		self.b4.place( relx = 0.35, rely = 0.53, relheight = 0.1, relwidth = 0.3)
		self.b5.place( relx = 0.35, rely = 0.64, relheight = 0.1, relwidth = 0.3)
		self.b6.place( relx = 0.35, rely = 0.75, relheight = 0.1, relwidth = 0.3)
		
class Toevoegen(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent)
		
		#stijl instellen
		s = ttk.Style()
		s.configure('my.TButton', font=('Verdana', 30))
		s.configure('my.VButton', font=('Verdana', 30), bg = "red")
		s.configure('my.TCheckbutton', font=('Verdana', 30))
		s.configure('my.TOptionMenu', font=('Verdana', 30))

		#tekst font instellen
		fontsize = "Verdana 30"
		fontsizelijst = "Verdana 20"

		#variable
		self.Geslacht = tk.StringVar()
		self.lijst = tk.StringVar()

		#create labels
		self.l1 = tk.Label(self, text = "Voornaam", font = fontsize, anchor = "e")
		self.l2 = tk.Label(self, text = "Achternaam", font = fontsize, anchor = "e")
		self.l3 = tk.Label(self, text = "Geslacht", font = fontsize, anchor = "e")
		self.l4 = tk.Label(self, text = "E-mail", font = fontsize, anchor = "e")
		self.l5 = tk.Label(self, font = fontsize, textvariable = self.Geslacht, relief = "ridge")

		self.ls = tk.Label(self, textvariable = self.lijst, relief = "ridge", font = fontsizelijst, anchor = "nw", justify = "left", bg = "white")
	
		#create entry widgets
		self.Vnaam = ttk.Entry(self, style ='my.TButton', font = "Verdana 30")
		self.Anaam = ttk.Entry(self, style ='my.TButton', font = "Verdana 30")
		self.mail  = ttk.Entry(self, style ='my.TButton', font = "Verdana 30")

		#create checkbox's
		self.vrouwb = ttk.Button(self, text = "Vrouw", style='my.TButton', command = lambda: self.Select_Vrouw())
		self.manb = ttk.Button(self, text = "Man", style='my.TButton', command = lambda: self.Select_Man())
	
		#create buttons
		self.b1 = ttk.Button(self, text = "Opslaan", command = lambda: self.Opslaan(), style='my.TButton')
		self.b2 = ttk.Button(self, text = "Start pagina", command=lambda: controller.show_frame(StartPage), style='my.TButton')
		self.b3 = ttk.Button(self, text = "Update", command=lambda: Update_list_toe(self), style='my.TButton')
		self.b4 = ttk.Button(self, text = "Delete", command=lambda: Delete_list_toe(self), style='my.TButton')

		#plaats labels op scherm
		self.l1.place(relx = 0.02, rely = 0.04, relheight = 0.07, relwidth = 0.15)
		self.l2.place(relx = 0.02, rely = 0.12, relheight = 0.07, relwidth = 0.15)
		self.l3.place(relx = 0.02, rely = 0.2,  relheight = 0.07, relwidth = 0.15)
		self.l4.place(relx = 0.02, rely = 0.28, relheight = 0.07, relwidth = 0.15)
		self.l5.place(relx = 0.4,  rely = 0.2,  relheight = 0.07, relwidth = 0.08)

		self.ls.place(relx = 0.5, rely = 0.04, relheight = 0.92, relwidth = 0.45)

		#plaats entry widget op het scherm
		self.Vnaam.place(	relx = 0.18, rely = 0.04, relheight = 0.07, relwidth = 0.3)
		self.Anaam.place(	relx = 0.18, rely = 0.12, relheight = 0.07, relwidth = 0.3)
		self.mail.place(	relx = 0.18, rely = 0.28, relheight = 0.07, relwidth = 0.3)

		#plaats checkbox op het scherm
		#self.geslacht.place(relx = 0.18, rely = 0.2,  relheight = 0.07, relwidth = 0.3)
		self.vrouwb.place(	relx = 0.18, rely = 0.2, relheight = 0.07, relwidth = 0.1)
		self.manb.place(	relx = 0.29, rely = 0.2, relheight = 0.07, relwidth = 0.1)

		#plaats buttons op het scherm
		self.b1.place(relx = 0.18, rely = 0.36, relheight = 0.07, relwidth = 0.3)
		self.b2.place(relx = 0.18, rely = 0.68, relheight = 0.07, relwidth = 0.3)
		self.b3.place(relx = 0.18, rely = 0.44, relheight = 0.07, relwidth = 0.3)
		self.b4.place(relx = 0.18, rely = 0.52, relheight = 0.07, relwidth = 0.3)

		self.Vnaam.focus_set()
		Read_list_toe(self)

	def Opslaan(self):

		Data_entry_toe(self)

		self.Vnaam.delete(first = 0, last = tk.END)
		self.Anaam.delete(first = 0, last = tk.END)
		self.mail.delete( first = 0, last = tk.END)

		Read_list_toe(self)

	def Select_Vrouw(self):

		self.Geslacht.set("V")

	def Select_Man(self):

		self.Geslacht.set("M")		

class Aanwezigheden(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="Aanwezigheden")
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",font = 10,
                           command=lambda: controller.show_frame(StartPage))
        button.pack()

class Vooruitgang(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="Vooruitgang")
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",font = 10,
                           command=lambda: controller.show_frame(StartPage))
        button.pack()

class Opmerkingen(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="Opmerkingen")
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",font = 10,
                           command=lambda: controller.show_frame(StartPage))
        button.pack()

class Aanbevelingen(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="Training aanbevelingen")
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",font = 10,
                           command=lambda: controller.show_frame(StartPage))
        button.pack()

#=============functies=============================
def Create_tabel():
	c.execute(sql_tabel)

#===============================================================================================================================
def Data_entry_toe(frame):
	voornaam = frame.Vnaam.get()
	achternaam = frame.Anaam.get()
	geslacht = frame.Geslacht.get()
	mail = frame.mail.get()

	c.execute(sql_data_entry,(voornaam, achternaam, geslacht, mail))
	conn.commit()

#===============================================================================================================================
def Read_list_toe(frame):
	c.execute("SELECT * FROM " + sql)
	data = c.fetchall()
	naamlijst = ""
	

	c.execute("SELECT * FROM " + sql)
	for i in range(len(c.fetchall())):
		#t = c.execute("SELECT rowid FROM " + sql + " WHERE Voornaam = ?", [data[i][0]])
		naamlijst += str(i + 1) + "  " + data[i][0] + "\t" + data[i][1] + "\t" + data[i][2] + "\t" + data[i][3] + "\n"

	frame.lijst.set(naamlijst)

#===============================================================================================================================
def Delete_list_toe(frame):
	
	pos = askstring('ID', 'Voer ID nr. in van gegevens die je wilt Verwijderen')
	MsgBox = messagebox.askquestion ('Delete gegevens','Zeker dat je deze gegevens wilt verwijderen?',icon = 'warning')

	if MsgBox == 'yes':
		c.execute("DELETE FROM " + sql + " WHERE rowid = ?", pos)
		conn.commit()
		c.execute("VACUUM")

	frame.Vnaam.delete(first = 0, last = tk.END)
	frame.Anaam.delete(first = 0, last = tk.END)

	Read_list_toe(frame)

#===============================================================================================================================
def Update_list_toe(frame):
		
	voornaam 	= frame.Vnaam.get()
	achternaam 	= frame.Anaam.get()
	geslacht 	= frame.Geslacht.get()
	mail 		= frame.mail.get()

	if voornaam == "" and achternaam == "":
		print("niets ingevult")
		showinfo('Hello!', "Er zijn geen gegevens ingevult.")
		frame.Vnaam.focus_set()
	else:
		pos = askstring('ID', 'Voer ID nr. in van gegevens die je wilt update')
		MsgBox = messagebox.askquestion ('Update gegevens','Zeker dat je deze gegevens wilt Update?',icon = 'warning')
		
		if MsgBox == 'yes':
			c.execute(sql_update, (voornaam, achternaam, geslacht, mail, pos))
			conn.commit()

		frame.Vnaam.delete(first = 0, last = tk.END)
		frame.Anaam.delete(first = 0, last = tk.END)
		frame.geslacht = " "
		frame.mail.delete(first = 0, last = tk.END)

		Read_list_toe(frame)
	
#=============loop=========================
Create_tabel()
app = App()
app.mainloop()

