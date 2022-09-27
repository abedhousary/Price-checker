import json 
from tkinter import * 
from tkinter.messagebox import * 
import mysql.connector
class pricechecker :
    def __init__(self):
            self.checkconfig()
            self.get_connection()
            self.widgets()

    def get_connection (self):
        with open("app.json","r") as config :
                self.configfile = json.load(config)
        try : 
            self.cn = mysql.connector.connect(
                user = "root",
                password = "",
                database = self.configfile["database"]
            )
            self.cr = self.cn.cursor()
        except:
            showerror("Connection","Failed to connect to database")
    def widgets (self):
        root = Tk()
        width = 500 
        height = 200 
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        x = (sw / 2) - (width / 2)
        y = (sh / 2) - (height / 2)
        root.geometry("%dx%d+%d+%d"%(width,height,x,y))
        title = Label(root,text = "Price Checker",font=15).pack()
        self.barcodeentry = Entry(root,font=15)
        self.barcodeentry.bind("<Return>",self.lookupprice)
        self.barcodeentry.pack(pady=20)
        self.price = Label(root,text = "",font=15)
        self.price.pack()
        root.mainloop()
    def lookupprice (self,event) :


        self.cr.execute(f"select pricesell from {self.configfile['table']} where code = {self.barcodeentry.get()}")
        self.price.config(text = f"{self.cr.fetchall()[0][0]} L.L",fg = "green")
    def configwindows(self):
        def save ():
            with open("app.json","r") as f :
                olddata = json.load(f)
                olddata['database'] = Databaseentry.get()
                olddata['table'] = tableeentry.get()
            with open("app.json","w") as n :
                newdata =  json.dumps(olddata)
                n.write(newdata)
        win2 = Tk()
        width = 500 
        height = 200 
        sw = win2.winfo_screenwidth()
        sh = win2.winfo_screenheight()
        x = (sw / 2) - (width / 2)
        y = (sh / 2) - (height / 2)
        win2.geometry("%dx%d+%d+%d"%(width,height,x,y))

        DatabaseName = Label(win2,text = "Database Name here").grid(row =0 ,column=0,padx=20,pady=30)
        TableName = Label(win2,text = "Table Name here").grid(row =1 ,column=0,padx=20,pady=30)

        Databaseentry = Entry(win2)
        tableeentry = Entry(win2)

        savebutton = Button(win2,text = "Save",width=9,command=save)

        Databaseentry.grid(row =0,column=1,padx=20,pady=30)
        tableeentry.grid(row =1 ,column=1,padx=20,pady=30)

        savebutton.grid(row =0 ,column=2,padx=20,pady=30)


        win2.mainloop()
    def checkconfig(self):   
        with open("app.json","r") as file :
            data  = json.load(file)
            if len(data) < 2:
                self.configwindows()
                return False
            else:
                return True
app = pricechecker()