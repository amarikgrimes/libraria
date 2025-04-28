from tkinter import *
from tkinter import messagebox
import sqlite3

class AddMember(Toplevel):
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
        heading = Label(self.topFrame, text='Add Member', font=('Arial', 20), bg='white', fg='pink')
        heading.place(x=290, y=60)

        # Title
        self.lbl_name = Label(self.bottomFrame, text='Name', font=('Arial', 15), bg='white', fg='pink')
        self.lbl_name.place(x=40, y=40)
        self.entry_name = Entry(self.bottomFrame, width=30, bd=5, font=('Arial', 15))
        self.entry_name.place(x=150, y=45)

        # Year
        self.lbl_phone = Label(self.bottomFrame, text='Phone Number', font=('Arial', 15), bg='white', fg='pink')
        self.lbl_phone.place(x=40, y=100)
        self.entry_phone = Entry(self.bottomFrame, width=30, bd=5, font=('Arial', 15))
        self.entry_phone.place(x=150, y=100)

        # Language
        self.lbl_email = Label(self.bottomFrame, text='Email', font=('Arial', 15), bg='white', fg='pink')
        self.lbl_email.place(x=40, y=160)
        self.entry_email = Entry(self.bottomFrame, width=30, bd=5, font=('Arial', 15))
        self.entry_email.place(x=150, y=165)

        self.lbl_join_date = Label(self.bottomFrame, text='Join Date', font=('Arial', 15), bg='white', fg='pink')
        self.lbl_join_date.place(x=40, y=185)
        self.entry_join_date= Entry(self.bottomFrame, width=30, bd=5, font=('Arial', 15))
        self.entry_join_date.place(x=150, y=200)

        # Add Book Button
        self.button = Button(self.bottomFrame, text='Add Member', font=('Arial', 15),
                             command=self.add_member, bg='pink', fg='white')
        self.button.place(x=180, y=250)

    def add_member(self):
        name = self.entry_name.get().strip()
        phone = self.entry_phone.get().strip()
        email = self.entry_email.get().strip()
        join_date = self.entry_join_date.get().strip()

        if name == "" or phone == "" or email == "" or join_date == "":
            messagebox.showerror("Input Error", "Please fill all fields.")
            return

        try:
            conn = sqlite3.connect("libraria.db")
            cur = conn.cursor()
            cur.execute("INSERT INTO Members (name, phone, email, join_date) VALUES (?, ?, ?, ?)",
                        (name, phone, email, join_date))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Member '{name}' added successfully!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

