from tkinter import *
from random import shuffle
import pprint

class quizGUI:
    def __init__(self, window, *args, **kwargs):
        self.window = window
        self.window.title("What Don't you know?")
        self.terms = []
        self.definitions = []
        self.questcounter = 0
        self.score = 0
        self.num_terms = 0
        self.wronganswers = {}
        self.messages = ['', 'correct', 'wrong']
        
        self.canvas = Canvas(self.window, width=800, height=200, bg='black') #for surface: w = 800, for pc: w = 600
        self.canvas.pack()
        
        #question label
        self.questionvar = StringVar()
        self.questionLabel = Label (self.window, textvariable = self.questionvar, font="Arial 11", fg='white', bg = 'black',wraplength=500)
        self.canvas.create_window(300, 50,window = self.questionLabel, tag='question')
        
        #score label
        self.canvas.create_text(725, 30, text="Score: "+str(self.score), font="Arial 11", fill="white", tag="score")
        

        #Answer box
        self.AppEntry = StringVar()
        self.AppEntryBox = Entry(self.canvas, textvariable=self.AppEntry, width=40)
        self.canvas.create_window(300,150,window=self.AppEntryBox)
        self.AppEntryBox.bind('<Return>',self.checkanswer)
        self.AppEntryBox.config(state='disabled')
        
        #start button
        self.startbutton = Button(self.canvas, text = "start", width=10, fg='white', bg='green', command=self.loadData)
        self.canvas.create_window(600, 150, window=self.startbutton, tag='start') #surf: x= 600, pc: x =500
        
        
    
    def loadData(self):
        with open("hist151_test1_dates.txt") as file:
            lines = file.readlines()
            shuffle(lines)
            
            #load data into various lists
            for eachline in lines:
                splittedlines = eachline.strip().split('\t')
                
                if (splittedlines[1] == "to be found out***"):
                    continue
                    
                self.terms.append(splittedlines[0].lower())                
                self.definitions.append(splittedlines[1].lower())
        
        self.startbutton.config(state='disabled')
        self.AppEntryBox.config(state='normal')
        self.AppEntryBox.focus()
        self.num_terms = len(self.terms)
        
        self.canvas.create_text(725, 50, text="Ques left: "+ str(self.num_terms), font="Arial 11", fill="white", tag="questcount")
        self.beginlearning()
        
        
    def beginlearning(self):
        self.AppEntryBox.delete(0, END)   #clearing the entry box
        
        if self.questcounter == len(self.definitions):
            self.questionvar.set("Completed Learning: Score is:" + str(self.score) + "/" + str(len(self.terms)))
            self.canvas.delete('score')
            self.write_wrong_answersToTextFile()
            self.canvas.create_text(300, 75, text="Check for answered wrong in textfile", font="Arial 11 bold", fill="red")
            self.AppEntryBox.config(state='disabled')
        else:
            self.questionvar.set(self.definitions[self.questcounter])
            
            
    
    def checkanswer(self,event):
       
        if self.AppEntry.get() == self.terms[self.questcounter]:
            self.score+=1
            self.canvas.delete("score")
            self.canvas.create_text(725, 30, text="Score: "+ str(self.score), font="Arial 11", fill="white", tag="score")
            self.canvas.create_text(625, 30, text=self.messages[1], font="Arial 11 bold", fill="green", tag="message")
        else:
           self.canvas.create_text(625, 30, text=self.messages[2], font="Arial 11 bold", fill="red", tag="message")
           self.canvas.create_text(250, 100, text=self.terms[self.questcounter], font="Arial 11 bold", fill="yellow", tag="message")
           self.wronganswers[self.terms[self.questcounter]] = self.definitions[self.questcounter] 
        
        self.questcounter+=1 #change to the next question in the list
        self.num_terms -=1 #reduce question count left
        self.canvas.delete("questcount")
        self.canvas.create_text(725, 50, text="Ques left: "+ str(self.num_terms), font="Arial 11", fill="white", tag="questcount")
        self.canvas.after(1500, self.deletemessage)
        self.beginlearning()
        
    def deletemessage(self):
        self.canvas.delete("message")
    
    def write_wrong_answersToTextFile(self):
        with open ("answered_wrong.txt", "w") as wrongfile:
            for term, definition in self.wronganswers.items() :
                wrongfile.write(term + "-->" + definition +"\n")
            
        
window = Tk()
program = quizGUI(window)
window.resizable(0, 0) 
window.mainloop()