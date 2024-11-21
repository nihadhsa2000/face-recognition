from tkinter.constants import BOTH
from numpy.core.fromnumeric import size
from numpy.lib.polynomial import roots
from Detector import main_app
from create_classifier import train_classifer
from create_dataset import start_capture
import tkinter as tk
from tkinter import  Canvas, Grid, Label, font as tkfont
from tkinter import messagebox,PhotoImage
from PIL import Image,ImageTk
import tkinter.font as font


#from gender_prediction import emotion,ageAndgender
names = set()


class MainUI(tk.Tk):
       
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global names
        # Create a window
        
        with open("nameslist.txt", "r") as f:
            x = f.read()
            z = x.rstrip().split(" ")
            for i in z:
                names.add(i)
        self.title_font = tkfont.Font(family='Helvetica', size=25, weight="bold")
        self.title("Face Recognizer")
        self.resizable(False, False)
        self.geometry("1000x500")
        #self.configure(bg='steelblue')
        self.fontImage= PhotoImage(file= "future-of-AI.png")
        self.container= Canvas(self, width= 1920, height= 1080)
        self.container.place(relx=-0.001, rely=-0.001)
        self.container.create_image(400,290, image= self.fontImage)  
     
        
        #filename=PhotoImage(file="")
        #background_label=Label(self,image=filename)
        #background_label.place(x=0,y=0,relwidth=1,relheight=1)
        
       
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None
        container = tk.Frame(self)
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
      
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
               
      
        self.show_frame("StartPage")

    def show_frame(self, page_name):
            frame = self.frames[page_name]
       
            frame.tkraise()

    def on_closing(self):

        if messagebox.askokcancel("Quit", "Are you sure?"):
            global names
            f =  open("nameslist.txt", "a+")
            for i in names:
                    f.write(i+" ")
            self.destroy()

   
class StartPage(tk.Frame):

        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            self.fontImage= PhotoImage(file= "future-of-AI.png")
            self.container= Canvas(self, width= 1000, height= 1080)
            self.container.place(relx=-0.001, rely=-0.001)
            self.container.create_image(400,290, image= self.fontImage)  
            
            #load = Image.open("homepagepic.png")
            #load = load.resize((250, 250), Image.ANTIALIAS)
           
            label = tk.Label(self, text="        FACE DETECTION AND RECOGNITION                 ", font=self.controller.title_font, background="white")
            label.grid(row=0)
            myFont = font.Font(family='Helvetica', size=20, weight='bold')
            button1 = tk.Button(self, text="   Add a User  ", fg="#ffffff",cursor='hand2', bg="#263942",command=lambda: self.controller.show_frame("PageOne"))
            button1.place(relx=0.37, rely=0.40)
            button1['font'] = myFont

            button2 = tk.Button(self, text="   Check a User  ", fg="#ffffff",cursor='hand2', bg="#263942",command=lambda: self.controller.show_frame("PageTwo"))
            button2['font'] = myFont

            button3 = tk.Button(self, text="Quit", fg="#263942", bg="#ffffff",cursor='hand2', command=self.on_closing)
            button3['font'] = myFont

            button1.grid(row=1, column=0, pady=40, padx=6)
            button2.grid(row=4, column=0, pady=40, padx=6)
            button3.grid(row=6, column=0, pady=40, padx=6)


        def on_closing(self):
            if messagebox.askokcancel("Quit", "Are you sure?"):
                global names
                with open("nameslist.txt", "w") as f:
                    for i in names:
                        f.write(i + " ")
                self.controller.destroy()
            

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.fontImage= PhotoImage(file= "face.png")
        self.container= Canvas(self, width= 4428, height= 2087)
        self.container.place(relx=-0.008, rely=-0.007)
        self.container.create_image(10,10, image= self.fontImage)  

        self.configure(bg="#B1D0E0")
        tk.Label(self, text="Enter the name",bg="#B1D0E0" ,fg="white", font='Helvetica 12 bold').grid(row=0, column=0, pady=10, padx=5)
        self.user_name = tk.Entry(self, borderwidth=3, bg="white", font='Helvetica 11')
        self.user_name.grid(row=0, column=1, pady=30, padx=50)
        myFont = font.Font(family='Helvetica', size=14, weight='bold')
        self.buttoncanc = tk.Button(self, text="Cancel", bg="#406882", fg="#ffffff", command=lambda: controller.show_frame("StartPage"))
        self.buttoncanc['font'] = myFont
        self.buttonext = tk.Button(self, text="Next", fg="#ffffff", bg="#406882", command=self.start_training)
        self.buttonext['font'] = myFont
        self.buttoncanc.grid(row=1, column=0, pady=10, ipadx=20, ipady=4)
        self.buttonext.grid(row=1, column=1, pady=10, ipadx=20, ipady=4)
    def start_training(self):
        global names
        if self.user_name.get() == "None":
            messagebox.showerror("Error", "Name cannot be 'None'")
            return
        elif self.user_name.get() in names:
            messagebox.showerror("Error", "User already exists!")
            return
        elif len(self.user_name.get()) == 0:
            messagebox.showerror("Error", "Name cannot be empty!")
            return
        name = self.user_name.get()
        names.add(name)
        self.controller.active_name = name
        self.controller.frames["PageTwo"].refresh_names()
        self.controller.show_frame("PageThree")


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global names
        self.controller = controller
        self.fontImage= PhotoImage(file= "face.png")
        self.container= Canvas(self, width= 4428, height= 2087)
        self.container.place(relx=-0.008, rely=-0.007)
        self.container.create_image(10,10, image= self.fontImage) 
        myFont = font.Font(family='Helvetica', size=14, weight='bold')
        tk.Label(self, text="Select user", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=0, padx=10, pady=10)
        self.buttoncanc = tk.Button(self, text="Cancel", command=lambda: controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        self.buttoncanc['font'] = myFont
        self.menuvar = tk.StringVar(self)
        self.dropdown = tk.OptionMenu(self, self.menuvar, *names)
        self.dropdown.config(bg="lightgrey")
        self.dropdown["menu"].config(bg="lightgrey")
        self.buttonext = tk.Button(self, text="Next", command=self.nextfoo, fg="#ffffff", bg="#263942")
        self.buttonext['font'] = myFont
        self.dropdown.grid(row=0, column=1, ipadx=8, padx=10, pady=10)
        self.buttoncanc.grid(row=1, ipadx=5, ipady=4, column=0, pady=10)
        self.buttonext.grid(row=1, ipadx=5, ipady=4, column=1, pady=10)

    def nextfoo(self):
        if self.menuvar.get() == "None":
            messagebox.showerror("ERROR", "Name cannot be 'None'")
            return
        self.controller.active_name = self.menuvar.get()
        self.controller.show_frame("PageFour")

    def refresh_names(self):
        global names
        self.menuvar.set('')
        self.dropdown['menu'].delete(0, 'end')
        for name in names:
            self.dropdown['menu'].add_command(label=name, command=tk._setit(self.menuvar, name))

class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.fontImage= PhotoImage(file= "face.png")
        self.container= Canvas(self, width= 4428, height= 2087)
        self.container.place(relx=-0.008, rely=-0.007)
        self.container.create_image(10,10, image= self.fontImage) 
         
        self.numimglabel = tk.Label(self, text="Number of images captured = 0", font='Helvetica 12 bold', fg="#263942")
        self.numimglabel.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
        myFont = font.Font(family='Helvetica', size=14, weight='bold')
        self.capturebutton = tk.Button(self, text="Capture Data Set", fg="#ffffff", bg="#263942", command=self.capimg)
        self.capturebutton['font'] = myFont
        self.trainbutton = tk.Button(self, text="Train The Model", fg="#ffffff", bg="#263942",command=self.trainmodel)
        self.trainbutton['font'] = myFont
        self.capturebutton.grid(row=1, column=0, ipadx=5, ipady=4, padx=10, pady=20)
        self.trainbutton.grid(row=1, column=1, ipadx=5, ipady=4, padx=10, pady=20)

    def capimg(self):
        self.numimglabel.config(text=str("Captured Images = 0 "))
        messagebox.showinfo("INSTRUCTIONS", "We will Capture 300 pic of your Face.")
        x = start_capture(self.controller.active_name)
        self.controller.num_of_images = x
        self.numimglabel.config(text=str("Number of images captured = "+str(x)))

    def trainmodel(self):
        if self.controller.num_of_images < 300:
            messagebox.showerror("ERROR", "No enough Data, Capture at least 300 images!")
            return
        train_classifer(self.controller.active_name)
        messagebox.showinfo("SUCCESS", "The modele has been successfully trained!")
        self.controller.show_frame("PageFour")


class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.fontImage= PhotoImage(file= "face.png")
        self.container= Canvas(self, width= 4428, height= 2087)
        self.container.place(relx=-0.008, rely=-0.007)
        self.container.create_image(10,10, image= self.fontImage)

        label = tk.Label(self, text="Face Recognition", font='Helvetica 16 bold')
        label.grid(row=0,column=0, sticky="ew")
        myFont = font.Font(family='Helvetica', size=14, weight='bold')
        button1 = tk.Button(self, text="Face Recognition", command=self.openwebcam, fg="#ffffff", bg="#263942")
        button1['font'] = myFont
        #button2 = tk.Button(self, text="Emotion Detection", command=self.emot, fg="#ffffff", bg="#263942")
        #button3 = tk.Button(self, text="Gender and Age Prediction", command=self.gender_age_pred, fg="#ffffff", bg="#263942")

        button4 = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        button4['font'] = myFont
        button1.grid(row=1,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        #button2.grid(row=1,column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        #button3.grid(row=2,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        button4.grid(row=1,column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)

    def openwebcam(self):
        main_app(self.controller.active_name)
    #def gender_age_pred(self):
     #  ageAndgender()
    #def emot(self):
     #   emotion()



app = MainUI()
app.iconphoto(False, tk.PhotoImage(file='icon.ico'))
app.mainloop()

