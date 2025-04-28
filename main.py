from tkinter import *
from tkinter import ttk
import sqlite3
import addbook, addmember, addauthor, addgenre, borrowbook, addreturn

class Main(object):
    def __init__(self, master):
        self.master = master

        # Database connection and setup
        self.conn = sqlite3.connect('libraria.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

        # Frame creation for main window
        mainFrame = Frame(self.master)
        mainFrame.pack()

        # Top frame
        topFrame = Frame(mainFrame, width=1350, height=70, bg='#F8F8F8', padx=20, relief=SUNKEN, borderwidth=2)
        topFrame.pack(side=TOP, fill=X)

        # Center frame
        centerFrame = Frame(mainFrame, width=1350, height=680, bg='#FFC0CB', relief=RIDGE, borderwidth=2)
        centerFrame.pack(side=TOP)

        # Left frame
        leftFrame = Frame(centerFrame, width=900, height=700, bg='#FF81C0', relief=SUNKEN, borderwidth=2)
        leftFrame.pack(side=LEFT)

        # Right frame
        rightFrame = Frame(centerFrame, width=450, height=700, bg='#FF69B4', relief=SUNKEN, borderwidth=2)
        rightFrame.pack(side=RIGHT)

        # Search bar
        search_bar = LabelFrame(rightFrame, text="Search Bar", bg='#FF69B4', width=440, height=75, font=('Arial', 12))
        search_bar.pack(fill=BOTH)
        self.lbn_search = Label(search_bar, text="Search Book", bg='#FF69B4', font=('Arial', 12))
        self.lbn_search.grid(row=0, column=0, padx=20, pady=10)
        self.entry_search = Entry(search_bar, width=30, bd=10, font=('Arial', 12))
        self.entry_search.grid(row=0, column=1, columnspan=3, padx=10, pady=10)
        self.btn_search = Button(search_bar, text="Search", font=('Arial', 12), command=self.searchBooks)
        self.btn_search.grid(row=0, column=4, padx=20, pady=10)

        # Book listbox area
        listbox = LabelFrame(rightFrame, text="List of Books", bg='#FF69B4', width=440, height=500, font=('Arial', 12))
        listbox.pack(fill=BOTH)
        lbn_list = Label(listbox, text="Sort By", bg='#FF69B4', font=('Arial', 12))
        lbn_list.grid(row=0, column=2)

        self.listChoice = IntVar()
        rb1 = Radiobutton(listbox, text="All Books", variable=self.listChoice, value=1, bg='#FF69B4', font=('Arial', 12))
        rb2 = Radiobutton(listbox, text="Currently Available", variable=self.listChoice, value=2, bg='#FF69B4', font=('Arial', 12))
        rb3 = Radiobutton(listbox, text="Borrowed", variable=self.listChoice, value=3, bg='#FF69B4', font=('Arial', 12))
        rb1.grid(row=1, column=0)
        rb2.grid(row=1, column=1)
        rb3.grid(row=1, column=2)

        btn_list = Button(listbox, text="Book List", font=('Arial', 12), command=self.listBooks)
        btn_list.grid(row=1, column=3, padx=40, pady=20)

        # Top Buttons
        self.btnab = Button(topFrame, text="Add Book", font=('Arial', 12), command=self.addBook)
        self.btnab.pack(side=LEFT, padx=3)
        self.btnam = Button(topFrame, text="Add Member", font=('Arial', 12), command=self.addMember)
        self.btnam.pack(side=LEFT, padx=5)
        self.btnaa = Button(topFrame, text="Add Author", font=('Arial', 12), command=self.addAuthor)
        self.btnaa.pack(side=LEFT, padx=7)
        self.btnag = Button(topFrame, text="Add Genre", font=('Arial', 12), command=self.addGenre)
        self.btnag.pack(side=LEFT, padx=9)
        self.btnbb = Button(topFrame, text="Book Borrow", font=('Arial', 12), command=self.addBorrow)  # We'll connect this later
        self.btnbb.pack(side=LEFT, padx=5)
        self.btnrb = Button(topFrame, text="Return Book", font=('Arial', 12), command=self.addReturn)
        self.btnrb.pack(side=LEFT, padx=7)


        # Tabs
        self.tabs = ttk.Notebook(leftFrame, width=900, height=600)
        self.tabs.pack()
        self.tab1 = ttk.Frame(self.tabs)
        self.tabs.add(self.tab1, text="Library System", compound=LEFT)

        # List of books and details
        self.booklist = Listbox(self.tab1, width=40, height=30, bd=5, bg='pink', font=('Arial', 12))
        self.sb = Scrollbar(self.tab1, orient=VERTICAL)
        self.booklist.grid(row=0, column=0, padx=(10, 0), pady=10, sticky=N)
        self.sb.config(command=self.booklist.yview)
        self.booklist.config(yscrollcommand=self.sb.set)
        self.sb.grid(row=0, column=1, sticky=N + S + E)

        self.details = Listbox(self.tab1, width=80, height=30, bd=5, bg='pink', font=('Arial', 12))
        self.details.grid(row=0, column=2, padx=(10, 0), pady=10, sticky=N)

        # Initial book list
        self.displayBooks()

    def addBook(self):
        addbook_window = addbook.AddBook(self.master)

    def addMember(self):
        addmember_window = addmember.AddMember(self.master)

    def addAuthor(self):
        addauthor_window = addauthor.AddAuthor(self.master)

    def addGenre(self):
        addgenre_window = addgenre.AddGenre(self.master)

    def addBorrow(self):
        try:
            value = self.booklist.get(self.booklist.curselection())
            book_id = int(value.split("-")[0].strip())
            borrow_window = borrowbook.addBorrow(self.master, book_id=book_id)
        except Exception as e:
            print("Error opening Borrow Book window:", e)
    def addReturn(self):
        try:
            value = self.booklist.get(self.booklist.curselection())
            book_id = int(value.split("-")[0].strip())
            return_window = addreturn.ReturnBook(self.master, book_id=book_id)
        except Exception as e:
            print("Error opening Return Book window:", e)



    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                year INTEGER,
                language TEXT,
                status INTEGER DEFAULT 0
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Authors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Book_Author (
                book_id INTEGER,
                author_id INTEGER,
                FOREIGN KEY (book_id) REFERENCES Books(id),
                FOREIGN KEY (author_id) REFERENCES Authors(id),
                PRIMARY KEY (book_id, author_id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Genres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                join_date TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Borrow_Records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER,
                member_id INTEGER,
                borrow_date TEXT,
                return_date TEXT,
                FOREIGN KEY (book_id) REFERENCES Books(id),
                FOREIGN KEY (member_id) REFERENCES Members(id)
            )
        ''')
        self.conn.commit()

    def displayBooks(self):
        self.booklist.delete(0, END)
        self.details.delete(0, END)

        books = self.cursor.execute("SELECT * FROM Books").fetchall()
        for count, book in enumerate(books):
            self.booklist.insert(count, f"{book[0]} - {book[1]}")

        self.booklist.bind('<<ListboxSelect>>', self.bookinfo)

    def bookinfo(self, evt):
        self.details.delete(0, END)
        try:
            value = self.booklist.get(self.booklist.curselection())
            book_id = value.split("-")[0].strip()

            book = self.cursor.execute("SELECT * FROM Books WHERE id=?", (book_id,)).fetchone()
            if book:
                self.details.insert(END, f"ID: {book[0]}")
                self.details.insert(END, f"Title: {book[1]}")
                self.details.insert(END, f"Year: {book[2]}")
                self.details.insert(END, f"Language: {book[4]}")
                self.details.insert(END, f"Status: {'Available' if book[3]==0 else 'Borrowed'}")
        except Exception as e:
            print("Error displaying book info:", e)

    def searchBooks(self):
        value = self.entry_search.get()
        search = self.cursor.execute("SELECT * FROM Books WHERE title LIKE ?", ('%' + value + '%',)).fetchall()
        self.booklist.delete(0, END)
        for count, book in enumerate(search):
            self.booklist.insert(count, f"{book[0]} - {book[1]}")

    def listBooks(self):
        value = self.listChoice.get()
        self.booklist.delete(0, END)

        if value == 1:
            books = self.cursor.execute("SELECT * FROM Books").fetchall()
        elif value == 2:
            books = self.cursor.execute("SELECT * FROM Books WHERE status=0").fetchall()
        elif value == 3:
            books = self.cursor.execute("SELECT * FROM Books WHERE status=1").fetchall()
        else:
            books = []

        for count, book in enumerate(books):
            self.booklist.insert(count, f"{book[0]} - {book[1]}")
        
        self.booklist.bind('<<ListboxSelect>>', self.bookinfo)








# Main runner
def main():
    root = Tk()
    app = Main(root)
    root.title("Libraria")
    root.geometry("1350x750+350+250")
    root.mainloop()

if __name__ == "__main__":
    main()
