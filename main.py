import psycopg2
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import hashlib

global results
salt = "123rot0r13"

con = psycopg2.connect(
    host="localhost",
    database="kursovaya",
    user="postgres",
    password="1",
    port=5432
)


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()

    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        btn_open_dialog = tk.Button(toolbar, text='Авторизация', command=self.open_dialog, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP)
        btn_open_dialog.pack(side=tk.LEFT)
        btn_open_dialog2 = tk.Button(toolbar, text='Запросы', command=self.open_dialog2, bg='#d7d8e0', bd=0)
        btn_open_dialog2.pack(side=tk.LEFT)




    def open_dialog2(self):
       Zapros()

    def open_dialog(self):
        Authorization()


class Zapros(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.zapros2()
        self.view = app
    def zapros2(self):
        def testclick():
            try:
                e = edit.get()
                if('DROP' in e):
                    tk.messagebox.showerror(title="ERROR", message="DROP is not allowed in this area")
                    exit()
                if(accessFlag==False and e[0]!="S"):
                    tk.messagebox.showerror(title="Ошибка", message="Отказано в доступе")
                    exit()
                if(accessFlag == False and 'UNION' in e[7::]):
                    tk.messagebox.showerror(title='Ошибка', message='Замечена попытка SQL-инъекции')
                    exit()

                con.commit()
                cur.execute(e)
                if (e[0]=="S"):
                    results = cur.fetchall()
                    print(*results, sep='\n')
            except:
                print("")
        cur = con.cursor()
        self.geometry("800x100")

        t1 = tk.Label(self, text='Введите запрос')
        #t2 = tk.Label(self, text='Введите запрос')
        #t2.pack()

        edit = ttk.Entry(self, width=50, font='Arial 14')
        edit.insert(0, "SELECT * FROM addresses")

        but = ttk.Button(self, text="Click", command=testclick)

        t1.pack()
        but.pack()
        edit.pack()


class Authorization(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.auth()
        self.view = app

    def auth(self):
        def enterButtonOnClick():
            global accessFlag
            authFlag = False
            password = entry_password.get()
            password = hashlib.md5((password + salt).encode())
            password = password.hexdigest()
            for row in rows:
                if (entry_login.get() == row[0]) and (password == row[1]):
                    authFlag = True
            if authFlag:
                if entry_login.get() == 'root':
                    accessFlag = True
                else:
                    accessFlag = False
                self.destroy()
            else:
                tk.messagebox.showerror(title="Ошибка", message="Неверный логин или пароль")
            print(accessFlag)

        cur = con.cursor()
        cur.execute("SELECT login, password from users")

        rows = cur.fetchall()
        '''
        for row in rows:
            print("LOGIN =", row[0])
            print("PASSWORD =", row[1], "\n")
        '''

        self.title('Авторизация')
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        label_description = tk.Label(self, text='Логин:')
        label_description.place(x=50, y=50)
        label_sum = tk.Label(self, text='Пароль:')
        label_sum.place(x=50, y=110)

        entry_login = ttk.Entry(self)
        entry_login.place(x=200, y=50)

        entry_password = ttk.Entry(self, show="*")
        entry_password.place(x=200, y=110)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        btn_ok = ttk.Button(self, text='Войти', command=enterButtonOnClick)
        btn_ok.place(x=220, y=170)




if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.pack()
    root.title("Курсовая работа")
    root.geometry("165x50")
    root.resizable(False, False)
    root.mainloop()