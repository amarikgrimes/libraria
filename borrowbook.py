from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox

class addBorrow(Toplevel):
    def __init__(self, master=None, book_id=None):
        super().__init__(master)
        self.geometry("600x750+550+200")
        self.title("Borrow Book")
        self.resizable(False, False)

        # Database connection
        self.conn = sqlite3.connect('libraria.db')
        self.cursor = self.conn.cursor()

        self.book_id = book_id  # ✅ Now passed properly

        self.topFrame = Frame(self, height=150, bg="white")
        self.topFrame.pack(fill=X)

        self.bottomFrame = Frame(self, height=600, bg="pink")
        self.bottomFrame.pack(fill=X)

        heading = Label(self.topFrame, text="Borrow Book", font=("Arial", 20), bg="white")
        heading.place(x=220, y=60)

        # Book Label
        lbl_book = Label(self.bottomFrame, text="Selected Book", font=("Arial", 15), bg="pink")
        lbl_book.place(x=40, y=50)
        self.entry_book = Entry(self.bottomFrame, width=40, bd=5, font=("Arial", 15))
        self.entry_book.place(x=180, y=55)
        self.entry_book.config(state='readonly')

        # Fill in book title
        book = self.cursor.execute("SELECT title FROM Books WHERE id=?", (self.book_id,)).fetchone()
        if book:
            self.entry_book.config(state='normal')
            self.entry_book.insert(0, book[0])
            self.entry_book.config(state='readonly')

        # Member Label
        lbl_member = Label(self.bottomFrame, text="Select Member", font=("Arial", 15), bg="pink")
        lbl_member.place(x=40, y=150)

        self.member_combo = ttk.Combobox(self.bottomFrame, font=("Arial", 15))
        self.member_combo.place(x=180, y=155)
        self.load_members()

        # Borrow Button
        btn_borrow = Button(self.bottomFrame, text="Borrow", font=("Arial", 15), bg="white", command=self.borrow_book)
        btn_borrow.place(x=250, y=300)

    def load_members(self):
        members = self.cursor.execute("SELECT id, name FROM Members").fetchall()
        self.memberlist = []
        for member in members:
            self.memberlist.append(f"{member[0]} - {member[1]}")

        self.member_combo['values'] = self.memberlist

    def borrow_book(self):
        selected_member = self.member_combo.get()

        if not selected_member:
            messagebox.showerror("Input Error", "Please select a member.")
            return

        member_id = int(selected_member.split("-")[0].strip())

        try:
            # Insert into Borrow_Records
            self.cursor.execute(
                "INSERT INTO Borrow_Records (book_id, member_id, borrow_date) VALUES (?, ?, DATE('now'))",
                (self.book_id, member_id)
            )
            # Update Book status
            self.cursor.execute(
                "UPDATE Books SET status = 1 WHERE id = ?", (self.book_id,)
            )

            self.conn.commit()
            messagebox.showinfo("Success", "Book borrowed successfully!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
