import tkinter as tk 
from tkinter import ttk
import sqlite3

# Класс нового окна

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    # Инициализируем виджеты для главного окна
    def init_main(self):
        toolbar = tk.Frame(bg="#d7d7e0", bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # Кнопка добавления
        self.img_add = tk.PhotoImage(file="./add.png")
        btn_add = tk.Button(toolbar, text="Добавить", bg="#d7d7e0",
                            bd = 0, image=self.img_add,
                            command=self.open_child)
        btn_add.pack(side=tk.LEFT)

        # Кнопка изменения
        self.img_upd = tk.PhotoImage(file="./change.png")
        btn_upd = tk.Button(toolbar, bg="#d7d7d7",
                            bd = 0, image=self.img_upd,
                            command=self.open_update_child)
        btn_upd.pack(side=tk.LEFT)

        # Кнопка поиска
        self.img_search = tk.PhotoImage(file="./search.png")
        btn_search = tk.Button(toolbar, bg="#d7d7e0", 
                               bd = 0, image=self.img_search,
                               command=self.open_searc)
        btn_search.pack(side=tk.LEFT)

        # Кнопка обновления
        self.img_refresh = tk.PhotoImage(file="./refresh.png")
        btn_refresh = tk.Button(toolbar, bg="#d7d7e0",
                                bd = 0, image=self.img_refresh,
                                command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        # Таблица
        self.tree = ttk.Treeview(root,
                                 columns=("id","joke"),
                                 height=45,
                                 show="headings")
        
        self.tree.column("id", width=45, anchor=tk.CENTER)
        self.tree.column("joke", width=600, anchor=tk.CENTER)

        self.tree.heading("id", text="id")
        self.tree.heading("joke", text="анекдот")

        self.tree.pack(side=tk.LEFT)

        # добавление скроллбара
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    # Метод добавления данных
    def records(self, joke):
        self.db.insert_data(joke)
        self.view_records()

    # Отображение данных в treeview
    def view_records(self):
        self.db.cur.execute("SELECT * FROM db")
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=i) for i in self.db.cur.fetchall()]

    # Метод поиска данных
    def search_records(self, joke):
        self.db.cur.execute("SELECT * FROM db WHERE joke LIKE ?",
                            ("%" + joke + "%", ))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=i) for i in self.db.cur.fetchall()]

    # Метод изменения данных
    def update_record(self, joke):
        id = self.tree.set(self.tree.selection()[0], "#1")
        self.db.cur.execute("""UPDATE db SET joke WHERE id = ?""", (joke, id))
        self.db.conn.commit()
        self.view_records()

    # Метод удаления строк
    def delete_records(self):
        for row in self.tree.selection():
            self.db.cur.execute("DELETE FROM db WHERE id = ?",
                                (self.tree.set(row, "#1"), ))
            
            self.db.conn.commit()
            self.view_records()

    # Метод вызывающий дочернее окно
    def open_child(self):
        Child()

    # Метод вызывающий дочернее окно для редактирования
    def open_update_child(self):
        Update()

    # Метод вызывающий дочернее окно для поиска данных
    def open_searc(self):
        Search()


# Класс дочернего окна

class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    # Инициализируем виджеты для дочернего окна
    def init_child(self):
        self.title("Добавление анекдота")
        self.geometry("400x200")
        self.resizable(False, False)

        # Перехватываем все события
        self.grab_set()

        # Перехватываем фокус
        self.focus_set()

        label_joke = tk.Label(self, text="Шутка")
        label_joke.place(x=50, y=50)

        self.entry_joke = tk.Entry(self)
        self.entry_joke.place(x=200, y=50)

        btn_cancel = tk.Button(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=200, y=150)

        self.btn_add = tk.Button(self, text="Добавить")
        self.btn_add.bind("<Button-1>", lambda ev: self.view.records(self.entry_joke.get()))
        self.btn_add.place(x=265, y=150)

        # класс дочернего окна для изменения данных

class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_update()
        self.db = db
        self.default_data()

    def init_update(self):
        self.title("Изменение Шутки")
        self.btn_add.destroy()
        self.btn_upd = tk.Button(self, text="Изменить")
        self.btn_upd.bind("<Button-1>",
                     lambda ev: self.view.update_record(self.entry_joke.get()))
        self.btn_upd.bind("<Button-1>", lambda ev: self.destroy(), add="+")
        self.btn_upd.place(x=265, y=150)

    def default_data(self):
        id = self.view.tree.set(self.view.tree.selection()[0], "#1")
        self.db.cur.execute("SELECT * from db WHERE id = ?", (id, ))
        row = self.db.cur.fetchone()
        self.entry_joke.insert(0, row[1])

class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    # инициализация виджетов дочернего окна
    def init_child(self):
        self.title("Поиск Шутки")
        self.geometry("300x100")
        self.resizable(False, False)

        self.grab_set()

        self.focus_set()

        label_joke = tk.Label(self, text="Шутка")
        label_joke.place(x=30, y=30)

        self.entry_joke = tk.Entry(self)
        self.entry_joke.place(x=130, y=30)

        btn_cancel = tk.Button(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=150, y=70)

        self.btn_add = tk.Button(self, text="Найти")
        self.btn_add.bind("<Button-1>",
                          lambda ev: self.view.search_records(self.entry_joke.get()))
        self.btn_add.bind("<Button-1>", lambda ev: self.destroy(), add = "+")
        self.btn_add.place(x=225, y=70)
            

# Класс БД
class Db:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("db.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS db (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         joke TEXT
        )""")
        self.conn.commit()

    def insert_data(self, joke):
        self.cur.execute("""
                         INSERT INTO db (joke)
                         Values (?)""", [joke])
        self.conn.commit()

# При запуске программы
if __name__ == "__main__":
    root = tk.Tk()
    db = Db()
    app = Main(root)
    root.title("Анекдоты")
    root.geometry("665x450")
    root.resizable(False, False)
    root.mainloop()
