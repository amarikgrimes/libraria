from tkinter import *
from tkinter import messagebox
import sqlite3

class AddBook(Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.geometry("650x750+550+200")
        self.title('Add Book')
        self.resizable(False, False)

        # Top frame
        self.topFrame = Frame(self, height=150, bg='white')
        self.topFrame.pack(fill=X)

        # Bottom frame
        self.bottomFrame = Frame(self, height=600, bg='white')
        self.bottomFrame.pack(fill=X)

        # Heading
        heading = Label(self.topFrame, text='Add Book', font=('Arial', 20), bg='white', fg='pink')
        heading.place(x=290, y=60)

        # Title
        self.lbl_title = Label(self.bottomFrame, text='Title', font=('Arial', 15), bg='white', fg='pink')
        self.lbl_title.place(x=40, y=40)
        self.entry_title = Entry(self.bottomFrame, width=30, bd=5, font=('Arial', 15))
        self.entry_title.place(x=150, y=45)

        # Year
        self.lbl_year = Label(self.bottomFrame, text='Year', font=('Arial', 15), bg='white', fg='pink')
        self.lbl_year.place(x=40, y=100)
        self.entry_year = Entry(self.bottomFrame, width=30, bd=5, font=('Arial', 15))
        self.entry_year.place(x=150, y=100)

        # Language
        self.lbl_language = Label(self.bottomFrame, text='Language', font=('Arial', 15), bg='white', fg='pink')
        self.lbl_language.place(x=40, y=160)
        self.entry_language = Entry(self.bottomFrame, width=30, bd=5, font=('Arial', 15))
        self.entry_language.place(x=150, y=165)

        # Author Label
        self.lbl_authors = Label(self.bottomFrame, text='Select Author(s)', font=('Arial', 15), bg='white', fg='pink')
        self.lbl_authors.place(x=40, y=220)

        # Listbox for authors
        self.author_listbox = Listbox(self.bottomFrame, selectmode=MULTIPLE, width=30, height=5, bd=5, font=('Arial', 12))
        self.author_listbox.place(x=150, y=220)

        # Populate authors from DB
        self.populate_authors()

        # Add Book Button
        self.button = Button(self.bottomFrame, text='Add Book', font=('Arial', 15),
                             command=self.add_book, bg='pink', fg='white')
        self.button.place(x=180, y=350)

    def add_book(self):
        title = self.entry_title.get().strip()
        year = self.entry_year.get().strip()
        language = self.entry_language.get().strip()
        selected_indices = self.author_listbox.curselection()

        if title == "" or year == "" or language == "":
            messagebox.showerror("Input Error", "Please fill all fields.")
            return

        if not selected_indices:
            messagebox.showerror("Input Error", "Please select at least one author.")
            return

        try:
            conn = sqlite3.connect("libraria.db")
            cur = conn.cursor()

            # Insert book
            cur.execute("INSERT INTO Books (title, year, language) VALUES (?, ?, ?)", (title, year, language))
            book_id = cur.lastrowid

            # Insert into Book_Author
            for i in selected_indices:
                author_entry = self.author_listbox.get(i)
                author_id = author_entry.split("-")[0].strip()
                cur.execute("INSERT INTO Book_Author (book_id, author_id) VALUES (?, ?)", (book_id, author_id))

            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Book '{title}' added successfully with author(s)!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def populate_authors(self):
        try:
            conn = sqlite3.connect("libraria.db")
            cur = conn.cursor()
            cur.execute("SELECT id, name FROM Authors")
            authors = cur.fetchall()
            conn.close()

            for author in authors:
                self.author_listbox.insert(END, f"{author[0]} - {author[1]}")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

