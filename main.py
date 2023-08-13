import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
from collections import Counter
from PIL import Image, ImageTk
import pygame as pg




# Gérer les transitions entre fenêtres
# Gérer la succession de plusieurs questions
# tester sur windows
# écrire requirements.txt


activated = -1

 
image_folder = os.path.join("images","AGE")# A changer pour aussi accomoder windows
images = os.listdir(image_folder)


keyboard = [["1","2","3","4","5","6","7","8","9","0"],
    ["A","Z","E","R","T","Y","U","Y","I","O","P"],
            ["Q","S","D","F","G","H","J","K","L","M"],
            ["W","X","C","V","B","N"]]


def analyse_frequency(string):
    freq = Counter(string)
    
    n_alpha = 0
    n_num = 0
    n_special = 0
    for k,v in freq.items():
        if k.isalpha():
            n_alpha += 1
        else:
            if k.isnumeric():
                n_num += 1
            else:
                n_special += 1
                
    return n_alpha,n_num,n_special



class ChoiceManager(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        self.fr = tk.Frame(self)        
        self.fr.place(x=0,y=0,relwidth=0.3,relheight=4/5)
        
        tk.Label(self.fr,text="Quel est le modèle de base?").pack()
 
        self.canvas = tk.Canvas(self.fr,background="white")
        self.canvas.pack(expand=True,fill="both")       
        
        
        image_file = os.path.join(image_folder,os.listdir(image_folder)[0])
        self.image_original = Image.open(image_file)
        self.image_tk = ImageTk.PhotoImage(image=self.image_original)
        
        self.aspect_ratio = self.image_original.width / self.image_original.height
        
        
        self.canvas.bind("<Configure>",self.stretch_image)
        

        self.choiceFrame = ChoiceFrame(self)
        self.choiceFrame.place(relx=0.3,y=0,relwidth=0.7,relheight=4/5)
        
        self.confirmButton = ttk.Button(self,text="Confirmer",command=self.gameOpen)

        self.confirmButton.place(relx=0.875,rely=0.875)
    
        self.pack(expand=True,fill="both")
    def gameOpen(self):
        if activated != -1:
            self.master.switch_to_game()
            
        
    def stretch_image(self,event):
        orig_width = event.width
        orig_height = event.height
        
        
        if self.aspect_ratio > 1: #width > height
            height = int(orig_width / self.aspect_ratio)
            width = orig_width
        else: # height > width
            width = int(orig_height * self.aspect_ratio)
            height = orig_height
            if width > orig_width:
                width = orig_width
                height = int(width / self.aspect_ratio)
            
                    

        resized_image = self.image_original.resize((width,height))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        
        self.canvas.create_image(orig_width/2,orig_height/2,image=self.image_tk,anchor="center")
        

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        pg.mixer.init()
        self.title("GunPendu")
        
        self.geometry('1400x800')
        self.minsize(1200,800)
        
             
        self.choice_mgr = ChoiceManager(self)
        
        
        self.mainloop()
    
    def switch_to_game(self):
        self.choice_mgr.pack_forget()
        
        self.new_window = GamePendu(self)
        
        

class PresentingFrame(tk.Frame):
    def __init__(self,master):
        super().__init__(master=master)
        
        
        self.pack(expand=True,fill='both')
        image_file = os.path.join(image_folder,os.listdir(image_folder)[0])
        image_original = Image.open(image_file)
        image_tk = ImageTk.PhotoImage(image=image_original)
        
        
        self.canvas = tk.Canvas(self,background="black",highlightthickness=0,bd=0)
        self.canvas.create_image(0,0,image = image_tk,anchor='nw')
        
        self.canvas.pack(expand=True,fill="both") 
        
        
        
            
        
class ChoiceFrame(ttk.Frame):
    def __init__(self,master):
        super().__init__(master)
        
        #ttk.Label(self, background='yellow').pack(expand=True,fill='both')
        self.rowconfigure([0,1],weight=1,uniform='a')
        self.columnconfigure((0,1),weight=1,uniform='a')
        
        
        self.possibilies = []
        for i in range(2):
            for j in range(2):
                p = ChoicePossibility(self,id=len(self.possibilies),label_name=f"label {len(self.possibilies)}")
                p.grid(row=i,column=j,sticky="nsew")
                self.possibilies.append(p)
        
    def activate(self,id):
        global activated
        for p in self.possibilies:
            p.deactivate_button()
        activated = id
        
        self.possibilies[id].activate_button()
           
           
class ChoicePossibility(ttk.Frame):
    
    def __init__(self,master,id,label_name,img_file=None):
        super().__init__(master)
        
        image_file = os.path.join(image_folder,os.listdir(image_folder)[id+1])
        
        self.label_name = os.listdir(image_folder)[id+1].split(".")[0]
        self.image_original = Image.open(image_file)
        self.image_tk = ImageTk.PhotoImage(image=self.image_original)
        self.aspect_ratio = self.image_original.width / self.image_original.height
        
        
        self.canvas = tk.Canvas(master=self,background="white")
      
        self.id = id
        
        
        self.rowconfigure((0,1,2,3),weight=1,uniform='a')
        self.columnconfigure((0,1),weight=1,uniform='a')        
        
        self.canvas.grid(row=0,column=0,rowspan=3,columnspan=2,sticky="nsew")
        self.nameLabel = ttk.Label(self,text=f"{self.label_name}",background='lightgray',font="Calibri 9")
        self.nameLabel.grid(row=3,column=0,sticky="nsew")
        
        self.modelButton = tk.Button(self,text="Celui-ci!",command=lambda: master.activate(self.id),background="white")
        self.modelButton.grid(row=3,column=1,sticky="nsew")
        
        self.canvas.bind("<Configure>",self.stretch_image)
        
        
    def stretch_image(self,event):
        orig_width = event.width
        orig_height = event.height
        
        
        if self.aspect_ratio > 1: #width > height
            height = int(orig_width / self.aspect_ratio)
            width = orig_width
        else: # height > width
            width = int(orig_height * self.aspect_ratio)
            height = orig_height
                    

        resized_image = self.image_original.resize((width,height))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        
        self.canvas.create_image(orig_width/2,orig_height/2,image=self.image_tk,anchor="center")
        
    def deactivate_button(self):
        self.modelButton.config(background="lightgray")
        
    def activate_button(self):
        self.modelButton.config(background="red")
        self.modelButton.config(highlightcolor="red")
        
    

  

class FrequencyCounter(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        
        self.char_count = 0
        self.num_count = 0
        self.spec_count = 0
        self.char_count_var = tk.StringVar()
        self.num_count_var = tk.StringVar()
        self.special_count_var = tk.StringVar()
        
        
        self.rowconfigure((0,1,2),weight=1,uniform='a')
        self.columnconfigure((0,1),weight=1,uniform='a')
        
        tk.Label(self,text="Caractères:").grid(row=0,column=0)
        tk.Label(self,textvariable=self.char_count_var).grid(row=0,column=1)
        
        tk.Label(self,text="Chiffres:").grid(row=1,column=0)
        tk.Label(self,textvariable=self.num_count_var).grid(row=1,column=1)
        
        tk.Label(self,text="Special:").grid(row=2,column=0)
        tk.Label(self,textvariable=self.special_count_var).grid(row=2,column=1)
        
        
        self.pack()
        
    def fit(self,string):
        self.char_count,self.num_count,self.spec_count = analyse_frequency(string)
        self.refresh()
    
    def refresh(self):
        self.char_count_var.set(f'{self.char_count}')
        self.num_count_var.set(f'{self.num_count}')
        self.special_count_var.set(f'{self.spec_count}')
    
        

class GamePendu(tk.Frame):
    def __init__(self,master):
        super().__init__(master=master)
        
        
        
        self.life_counter = LifeCounter(self,10)
        self.frame = tk.Frame(self,bg="white")
        
        self.frame.pack(expand=True,fill="both")
        
        
        label_activated = os.listdir(image_folder)[activated + 1].split('.')[0].upper()
    
        self.canvas = tk.Canvas(self.frame ,background="white",highlightthickness=0)
        self.canvas.pack()       
        
        
    
        image_file = os.path.join(image_folder,os.listdir(image_folder)[0])
        self.image_original = Image.open(image_file)
        self.image_tk = ImageTk.PhotoImage(image=self.image_original)
        
        
        self.secret = os.listdir(image_folder)[0].split(".")[0]
        self.aspect_ratio = self.image_original.width / self.image_original.height
        
        
        self.hidden_field = PenduHidden(self,self.secret)
        remainder = self.hidden_field.reveal_compare(label_activated)
        
        
    
        
        self.keyboard = Keyboard(self,self.hidden_field)
        
        self.canvas.bind("<Configure>",self.stretch_image)
        
        self.freq_counter = FrequencyCounter(self)
        self.freq_counter.fit(remainder)
        
        self.pack(expand=True,fill="both")
        
    def stretch_image(self,event):
        orig_width = event.width
        orig_height = event.height
        
        
        if self.aspect_ratio > 1: #width > height
            height = int(orig_width / self.aspect_ratio)
            width = orig_width
        else: # height > width
            width = int(orig_height * self.aspect_ratio)
            height = orig_height
            if width > orig_width:
                width = orig_width
                height = int(width / self.aspect_ratio)
            
                    
        resized_image = self.image_original.resize((width,height))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        
        self.canvas.create_image(orig_width/2,orig_height/2,image=self.image_tk,anchor="center")
        
    def deduce_one_life(self):
        self.life_counter.decrement()
        if self.life_counter.life == 0:
            pg.mixer.music.load("sound/wawawa.wav")
            pg.mixer.music.play()
            for i in range(len(self.secret)):
                if self.hidden_field.hidden[i] == "*":
                    self.hidden_field.highlight(i,False)
                    self.hidden_field.textvariables[i].set(self.secret[i].upper())
           
            result = messagebox.showinfo("Résultat",f"Votre score: {self.life_counter.life}")
            if result:
                self.pack_forget()
                self.master.destroy()

    def acknowledge_letter(self,letter):
        if letter.isalpha():
            self.freq_counter.char_count -= 1
        elif letter.isnumeric():
            self.freq_counter.num_count -= 1
        else:
            self.freq_counter.spec_count -= 1
        
        self.freq_counter.refresh()
    def check_win(self):
        if self.hidden_field.won():
            pg.mixer.music.load("sound/Victory.wav")
            pg.mixer.music.play()
            result = messagebox.showinfo("Résultat",f"Votre score: {self.life_counter.life}")
            if result:
                self.pack_forget()
                self.master.destroy()
            
class PenduHidden(tk.Frame):
    def __init__(self,master,secret):
        super().__init__(master)
        self.hidden = "*" * len(secret)
        self.secret = secret.upper()
        
        self.letters = []
        self.textvariables = []
        
        for i in range(len(self.secret)):
            vartext = tk.StringVar()
            vartext.set("*")
            h_letter = tk.Label(self,textvariable=vartext)
            h_letter.pack(side="left",expand=True,fill="x")
            self.letters.append(h_letter) 
            self.textvariables.append(vartext)
    
               
        self.pack()
        

        
    def won(self):
        if self.hidden == self.secret:
            return True
        return False
    
    def reveal_one_letter(self,letter):
        new_hidden = ""
        inside = False
        
        for i in range(len(self.secret)):
            if self.secret[i] == letter and self.hidden[i] == "*":
                inside = True
                new_hidden += letter
                self.textvariables[i].set(letter)
                self.highlight(i)
            else:
                new_hidden += self.hidden[i]
        
        self.hidden = new_hidden

        
        return inside

    def reveal_compare(self,string):
        new_hidden = ""
        words = string.split("-")
        char_table = ['*'] * len(self.hidden)
        
        for i in range(len(self.hidden)):
            if self.secret[i] == '-':
                char_table[i] = '-'
                self.textvariables[i].set('-')
                self.highlight(i)
        
        for word in words:
            for i in range(len(self.hidden) - len(word)+1):
                
                if word[0] == self.secret[i]:
                    if word == self.secret[i:i+len(word)]:
                        for j in range(i,i+len(word)):
                            char_table[j] = word[j-i]
                            self.textvariables[j].set(word[j-i])
                            self.highlight(j)
                        break
        
        
        
        new_hidden = "".join(char_table)
        
        remainder = ""
        
        for i in range(len(new_hidden)):
            if new_hidden[i] == "*":
                remainder += self.secret[i]
                
        self.hidden = new_hidden                        
        
        return remainder
   
    def highlight(self,i,victory=True):
        self.letters[i].config(background="green" if victory else "red")
        
class Keyboard(tk.Frame):
    
    def __init__(self,master,pendu): 
        super().__init__(master)
        
        self.pack()
        self.rows = []
        self.pendu = pendu
        
        for row in range(len(keyboard)):
            row = LineKbd(self,row)
            row.pack()
            self.rows.append(row)
            
    def issueLetter(self,row,i):
        result = self.pendu.reveal_one_letter(keyboard[row][i])
        
        if not result:

            pg.mixer.music.load("sound/Wrong.wav")
            pg.mixer.music.play()
            self.master.deduce_one_life()
            
        else:
            
            pg.mixer.music.load("sound/success.mp3")
            pg.mixer.music.play()
            self.master.acknowledge_letter(keyboard[row][i])
            self.master.check_win()
           
        self.rows[row].disable(i)
        
        
    
class LineKbd(tk.Frame):
    def __init__(self,master,row):
        super().__init__(master)
        self.buttons = []
        for i in range(len(keyboard[row])):
            button = tk.Button(self,text=f"{keyboard[row][i]}",font="Calibri 12",command=lambda i=i,row=row : master.issueLetter(row,i))
            button.pack(side="left")
            self.buttons.append(button)
            
        
    def disable(self,i):
        self.buttons[i].config(state="disabled")
 
 
class LifeCounter(tk.Frame):
    def __init__(self,master,starting_life=10):
        super().__init__(master)
        self.life = starting_life
        self.rowconfigure(0,weight=1,uniform='a')
        self.columnconfigure((0,1),weight=1,uniform='a')
        
        self.life_stringvar = tk.StringVar()
        self.life_stringvar.set(f"{self.life}")
        
        tk.Label(self,text="Vie:").grid(row=0,column=0)
        tk.Label(self,textvariable=self.life_stringvar).grid(row=0,column=1)
        
        self.pack()    
    
    def decrement(self):
        self.life -= 1
        self.life_stringvar.set(f"{self.life}")
            
                      

App()        