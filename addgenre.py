from tkinter import *
from tkinter import messagebox
import sqlite3

class AddGenre(Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.geometry("650x750+550+200")
        self.title('Add Member')
        self.resizable(False, False)

        # Top frame
        self.topFrame = Frame(self, height=150, bg='white')
        self.topFrame.pack(fill=X)

        # Bottom frame
        self.bottomFrame = Frame(self, height=600, bg='white')
        self.bottomFrame.pack(fill=X)

        # Heading
        heading = Label(self.topFrame, text='Add Genre', font=('Arial', 20), bg='white', fg='pink')
        heading.place(x=290, y=60)

        # Title
        self.lbl_name = Label(self.bottomFrame, text='Name', font=('Arial', 15), bg='white', fg='pink')
        self.lbl_name.place(x=40, y=40)
        self.entry_name = Entry(self.bottomFrame, width=30, bd=5, font=('Arial', 15))
        self.entry_name.place(x=150, y=45)

        # Add Book Button
        self.button = Button(self.bottomFrame, text='Add Genre', font=('Arial', 15),
                             command=self.add_genre, bg='pink', fg='white')
        self.button.place(x=180, y=250)

    def add_genre(self):
        name = self.entry_name.get().strip()

        if name == "":
            messagebox.showerror("Input Error", "Please fill all fields.")
            return

        try:
            conn = sqlite3.connect("libraria.db")
            cur = conn.cursor()
            cur.execute("INSERT INTO Genres (name) VALUES (?)",
                        (name,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Genre '{name}' added successfully!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

