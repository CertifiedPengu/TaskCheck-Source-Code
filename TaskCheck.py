from tkinter import *
from tkinter import font
import os

class TaskEnterGui:
    def __init__(self, existing=None):
        taskfont = font.Font(size=14, family="Segoe Print")
        Label(text="Enter tasks, one per line, max 8", font=taskfont).pack()
        self.text = Text(height=10, width=60)
        if existing != None:
            self.text.insert(END, existing)
        self.text.pack()
        Button(text="Generate To-Do List", font=taskfont, command=self.button).pack()

    def setroot(self,root):
        self.root = root
        
    def button(self):
        textlist = self.text.get("1.0", "end-1c").split("\n")
        if textlist != [""] and len(textlist) <= 8:
            textstr = str()
            with open("tasks.txt","w") as f:
                for i in textlist:
                    textstr += i + "\n"
                textstr += "generate"
                f.write(textstr)
        self.root.destroy()
        run()

class ChecklistGui():
    def __init__(self, taskin:list):
        if taskin[-1] == "generate":
            taskin.pop()
            self.tasklist = taskin
            self.taskvals = self.gentaskvals(taskin)
        else:
            self.tasklist = list()
            for i in taskin:
                self.tasklist.append(i[0])
            self.taskvals = taskin

        titlefont = font.Font(size=36, family="Segoe Script")
        taskfont = font.Font(size=14, family="Segoe Print")
        self.boxes = list()

        Label(text="To-do List", font=titlefont).grid(row=0, column=1, pady=10)
        Button(text="Generate New List", font=taskfont, command=self.newlist).grid(row=2,column=1)
        Button(text="Modify List", font=taskfont, command=self.modlist).grid(row=3, column=1, pady=(10,20))

        frame = Frame()
        daylist = ("Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday")
        for i in range(7):
            Label(frame, font=taskfont, text=daylist[i]).grid(row=i+1, column=0, pady=(0,8))
        self.cbvars = []
        for i in range(len(self.tasklist)):
            Label(frame, wraplength=200, font=taskfont, text=self.tasklist[i]).grid(row=0, column=i+1)
            boxlist = []
            vars = []
            for j in range(1,8):
                iv = BooleanVar()
                iv.set(self.taskvals[i][j])
                c = Checkbutton(frame, variable=iv)
                vars.append(iv)
                boxlist.append(c)
                c.grid(row=j, column=i+1, padx=60, pady=15)
            self.boxes.append(boxlist)
            self.cbvars.append(vars)
        frame.grid(row=1, column=1, padx=30)
        
    def gentaskvals(self, tasklist:list):
        tdict = list()
        for i in range(len(tasklist)):
            tdict.append([tasklist[i],False,False,False,False,False,False,False])
        return tdict
    
    def setroot(self,root):
        self.root = root
    
    def endprotocol(self):
        self.valstotxt()
        self.root.destroy()

    def valstotxt(self):
        val = str()
        for i in range(len(self.taskvals)):
            val += self.taskvals[i][0]
            for j in range(len(self.cbvars[i])):
                val += "," + str(bool(self.cbvars[i][j].get()))
            val += "\n"
        with open("tasks.txt","w") as f:
            f.write(val)
    
    def newlist(self):
        with open("tasks.txt","w") as f:
            f.write("")
        self.root.destroy()
        run()
    
    def modlist(self):
        temp = str()
        for i in self.tasklist:
            temp += i + "\n"
        self.endprotocol()
        root = Tk()
        tgui = TaskEnterGui(temp)
        tgui.setroot(root)
        root.mainloop()

def run():
    for l in [1]:
        try:
            f = open("tasks.txt","r")
        except FileNotFoundError:
            guitype = 0
            break
        fread = f.read()
        f.close()
        if len(fread) == 0:
            guitype = 0
            break
        tasklist = fread.split("\n")
        for i in tasklist:
            if i == "":
                tasklist.remove(i)
        templist = list()
        for i in tasklist:
            if len(i.split(",")) > 1:  
                templist.append(i.split(","))
            else:
                templist.append(i)
        tasklist = templist
        for i in tasklist:
            if i == "":
                tasklist.remove(i)
        guitype = 1
    root = Tk()
    root.title("To-Do List")
    if guitype == 1:
        gui = ChecklistGui(tasklist)
        gui.valstotxt()
        root.protocol("WM_DELETE_WINDOW", gui.endprotocol)
        gui.setroot(root)
    else:
        tgui = TaskEnterGui()
        tgui.setroot(root)

    #Comment this line to make it work without compiling
    #Remember to uncomment before committing
    root.iconbitmap(os.getcwd() + "\icon\pencil.ico")

    root.mainloop()

run()