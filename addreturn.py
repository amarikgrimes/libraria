from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox

class ReturnBook(Toplevel):
    def __init__(self, master=None, book_id=None):
        super().__init__(master)
        self.geometry("600x500+600+300")
        self.title("Return Book")
        self.resizable(False, False)

        # Database connection
        self.conn = sqlite3.connect('libraria.db')
        self.cursor = self.conn.cursor()

        self.book_id = book_id

        self.topFrame = Frame(self, height=100, bg="white")
        self.topFrame.pack(fill=X)

        self.bottomFrame = Frame(self, height=400, bg="pink")
        self.bottomFrame.pack(fill=X)

        heading = Label(self.topFrame, text="Return Book", font=("Arial", 20), bg="white")
        heading.place(x=220, y=30)

        # Book Title
        lbl_book = Label(self.bottomFrame, text="Book Title", font=("Arial", 15), bg="pink")
        lbl_book.place(x=40, y=50)
        self.entry_book = Entry(self.bottomFrame, width=40, bd=5, font=("Arial", 15))
        self.entry_book.place(x=180, y=55)
        self.entry_book.config(state='readonly')

        # Fill in Book Title
        book = self.cursor.execute("SELECT title FROM Books WHERE id=?", (self.book_id,)).fetchone()
        if book:
            self.entry_book.config(state='normal')
            self.entry_book.insert(0, book[0])
            self.entry_book.config(state='readonly')

        # Return Button
        btn_return = Button(self.bottomFrame, text="Return Book", font=("Arial", 15), bg="white", command=self.return_book)
        btn_return.place(x=220, y=150)

    def return_book(self):
        try:
            # Update Borrow_Records: set return_date to today
            self.cursor.execute(
                "UPDATE Borrow_Records SET return_date = DATE('now') WHERE book_id = ? AND return_date IS NULL",
                (self.book_id,)
            )
            # Update Book: set status back to available (0)
            self.cursor.execute(
                "UPDATE Books SET status = 0 WHERE id = ?",
                (self.book_id,)
            )

            self.conn.commit()
            messagebox.showinfo("Success", "Book returned successfully!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
