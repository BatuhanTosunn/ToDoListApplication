import tkinter.messagebox
from tkinter import *
from tkinter import Frame
from tkinter.ttk import *

# Global değişkenlerin tanımlanması
frames = []  # Görev çerçevelerini içeren liste
b = 58  # İlk yatay konum değeri
tasks = []  # Görev metinlerini içeren liste
label = []  # Etiketleri içeren liste
global count  # Görev sayısını takip etmek için global değişken

# Görev çerçevesini kaldıran fonksiyon
def remove(taskframe):
    global tasks
    global count
    global b
    task_text = taskframe.task_text
    ycord = taskframe.winfo_y()

    # Kullanıcıya kaldırma işlemini onaylamasını sor
    msg_box = tkinter.messagebox.askquestion('Remove Tasks', 'Are you sure about removing?')
    if msg_box == 'yes':
        count -= 1
        taskframe.destroy()  # Çerçeveyi GUI'dan kaldır
        frames.remove(taskframe)  # Çerçeveyi listeden kaldır

        # Silinen çerçevenin altındaki çerçeveleri kontrol et
        for frame in frames:
            if frame.winfo_y() > ycord:
                frame.place(y=frame.winfo_y() - 28)

        try:
            # Dosyadan görevi kaldır
            tasksfileremoving = open("unfinishedtasks.txt", "r")
            rows2 = tasksfileremoving.readlines()
            tasksfileremoving.close()
            file = open("unfinishedtasks.txt", "w")
            for removingtask in rows2:
                if removingtask.rstrip().capitalize() != task_text:
                    file.write(removingtask)
            tkinter.messagebox.showinfo("To-Do List Application", "Tasks removed")
            file.close()
        except FileNotFoundError:
            tkinter.messagebox.showerror("To-Do List Application", "File doesnt exist!")
        except IOError:
            tkinter.messagebox.showerror("To-Do List", "IO Error")
    else:
        tkinter.messagebox.showinfo("To-Do List Application", "Task remove cancelled")

# Yeni görev ekleyen fonksiyon
def addtask():
    global count
    last = 58
    for frame in frames:
        last = frame.winfo_y() + 28
    if addEntry.get() == "" or addEntry.get().isspace():
        tkinter.messagebox.showwarning(title="ERROR", message="Please enter a valid!")
    else:
        # Kullanıcıdan yeni görevi eklemeyi onaylamasını sor
        msg_box = tkinter.messagebox.askquestion('To-Do List Application',
                                                 'Are you sure you want to add the task?',
                                                 icon='warning')
        if msg_box == 'yes':
            if count == 11:
                tkinter.messagebox.showinfo("To Do List Application", "Maximum task count is 11")
            else:
                count += 1
                tkinter.messagebox.showinfo('Return', 'This task has been added to the list!')
                try:
                    # Dosyaya yeni görevi ekle
                    taskfile = open("unfinishedtasks.txt", "a")
                    taskfile.write(f"{addEntry.get().capitalize()}\n")
                except FileNotFoundError:
                    tkinter.messagebox.showerror("To-Do List Application", "File doesnt exist!")
                except IOError:
                    tkinter.messagebox.showerror("To-Do List Application", "IO Exception")
                task_button = create_task_frame(addEntry.get())
                task_button.place(x=10, y=last)
        else:
            tkinter.messagebox.showinfo('Return', 'This task has been cancelled!')
        addEntry.delete(0, END)

# Tamamlanan görevleri gösteren fonksiyon
def showfinished():
    try:
        c = 35
        file = open("completedtasks.txt", "r")
        rows2 = file.readlines()

        finishedtasks = []
        for row2 in rows2:
            finishedtasks.append(row2.rstrip().capitalize())

        # Yeni pencere oluştur
        app2 = Tk()
        app2.title("Finished Tasks")
        app2.geometry("400x300")

        # Tamamlanan görevleri temizleme düğmesi
        clear_button = Button(app2, text="Clear Finished Tasks", command=clear)
        clear_button.place(x=10, y=5)

        counter = 1
        # Tamamlanan görevleri listele
        for finishedtask in finishedtasks:
            finishedlabel = Label(app2, text=str(counter) + '-)' + finishedtask)
            finishedlabel.place(x=10, y=c)
            label.append(finishedlabel)
            c += 20
            counter += 1
    except FileNotFoundError:
        tkinter.messagebox.showwarning(title='Error', message='File does not exist!')
    except IOError:
        tkinter.messagebox.showwarning(title='Error', message='IO Exception')

    app2.mainloop()

# Tamamlanan görevleri temizleyen fonksiyon
def clear():
    try:
        file = open("completedtasks.txt", "r")
        read = file.read()
        file.close()
        finishedfile = open("completedtasks.txt", "w")
        if read == "":
            tkinter.messagebox.showwarning(title='Error', message='There is no finished task exist!')
        else:
            # Kullanıcıya tamamlanan görevleri temizleme işlemini onaylamasını sor
            msg_box = tkinter.messagebox.askquestion('To-Do List Application',
                                                     'Are you sure about clearing the completed tasks?',
                                                     icon='warning')
            if msg_box == 'yes':
                finishedfile.write("")
                for lb in label:
                    lb.destroy()
                tkinter.messagebox.showinfo('To-Do List Application',
                                            'Completed tasks deleted succesfully')
            else:
                finishedfile.write(read)
        finishedfile.close()
    except FileNotFoundError:
        tkinter.messagebox.showwarning(title='Error', message='File can not be found!')
    except IOError:
        tkinter.messagebox.showwarning(title='Error', message='IO Exception')

# Görevi tamamlandı olarak işaretleyen fonksiyon
def finish(finished_task_frame):
    global tasks
    try:
        finishfile = open("completedtasks.txt", "a")
        finishfile.write(finished_task_frame.task_text + '\n')
    except FileNotFoundError:
        tkinter.messagebox.showerror("To-Do List Application", "File doesnt exist!")
    except IOError:
        tkinter.messagebox.showerror("Error", "IO Exception")

    ycord = finished_task_frame.winfo_y()
    finished_task_frame.destroy()
    frames.remove(finished_task_frame)

    # Silinen görevin altındaki görevleri kontrol et
    for frame in frames:
        if frame.winfo_y() > ycord:
            frame.place(y=frame.winfo_y() - 28)

    # Dosyadan ve listeden silinen görevi çıkart
    finishedtasksfile = open("unfinishedtasks.txt", "r")
    rows3 = finishedtasksfile.readlines()
    finishedtasksfile.close()

    # Dosyayı güncelle
    file = open("unfinishedtasks.txt", "w")
    for finishedtask in rows3:
        if finishedtask.rstrip().capitalize() != finished_task_frame.task_text:
            file.write(finishedtask)
    file.close()

# Görev çerçevesi oluşturan fonksiyon
def create_task_frame(task_text):
    created_task_frame = Frame(app)
    created_task_frame.task_text = task_text
    task_str = Checkbutton(created_task_frame, text=task_text.lower().capitalize())
    task_str.pack(side=LEFT)

    remove_button = Button(created_task_frame, text='Remove', width=7, command=lambda: remove(created_task_frame))
    remove_button.pack(side=LEFT)

    finish_button = Button(created_task_frame, text='Finished', width=7, command=lambda: finish(created_task_frame))
    finish_button.pack(side=LEFT, padx=3)

    frames.append(created_task_frame)

    return created_task_frame

# Ana Tkinter uygulaması
app = Tk()
app.title('To-Do List')
app.geometry('450x400')

# Stil konfigürasyonu
style = Style()
style.configure('TButton', font='Calibri 10 bold', borderwidth=2)
style.map('TButton', foreground=[('active', 'blue'), ('disabled', 'black')])

# Giriş çerçevesi
entry_frame = Frame(app)
entry_frame.place(x=10, y=10)

addEntry = Entry(entry_frame, width=37)
addEntry.pack(side=LEFT)

addButton = Button(entry_frame, text='Add', width=7, command=addtask)
addButton.pack(side=LEFT, padx=3)

FinishedButton = Button(entry_frame, text='Show Finished Tasks', command=showfinished)
FinishedButton.pack(side=LEFT, padx=3)

TasksLabel = Label(app, text='Unfinished Tasks : ', font='Arial 9 bold')
TasksLabel.place(x=10, y=40)

# Dosyadan görevleri oku ve görev çerçevelerini oluştur
try:
    tasksfile = open("unfinishedtasks.txt", "r")
    rows1 = tasksfile.readlines()

    for row in rows1:
        tasks.append(row.rstrip().capitalize())
except FileNotFoundError:
    tkinter.messagebox.showerror('To-Do List Application', 'File not found!')

count = 0
# Her bir görev için bir çerçeve oluştur ve GUI'da konumlandır
for task in tasks:
    if task == "" or task.isspace():
        continue
    else:
        task_frame = create_task_frame(task)
        task_frame.place(x=10, y=b)
        b += 28
        count += 1

# Tkinter uygulamasını çalıştır
app.mainloop()
