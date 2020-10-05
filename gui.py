#-----------------------------------Type-O--------------------------------------

#                           -------Project by------
#                           Montserrat Ulloa Barrón
#                           Sofía Carrión Cervantes
#                           Esteban Padilla Cerdio
#
#



#-----------------------------Imported Libraries--------------------------------

#For the interface
from tkinter import *
from PIL import Image,ImageTk
from pygame import mixer

#Pynput for the keyboard and mouse
from pynput.keyboard import Key,KeyCode
from pynput.keyboard import Listener as keyboardListener
from pynput.mouse import Button
from pynput.mouse import Listener as mouseListener

#The project's own modules
from fingers import fingers #A library that stores the finger used per key
from lessons import lessons #Loads the lessons
from gloves import Gloves   #A controller for the external gloves

#Some extra functions
from math import floor
from time import sleep

#-----------------------------Interface Elements--------------------------------

#Images to be used
title = Image.open("Resources/title.jpg")
menu = Image.open("Resources/menu.jpg")
level = Image.open("Resources/level.jpg")
result = Image.open("Resources/result.jpg")

#Master application
global master
master = Tk()
master.title("Type-O")
master.geometry(str(title.size[0])+"x"+str(title.size[1]))
mixer.init()

#Title window
title_frame = Frame(master,bg="white")
title_frame.pack(expand=YES,fill=BOTH)
title_image_to_canvas = ImageTk.PhotoImage(title)
title_canvas = Canvas(title_frame,bg="white",width=title.size[0],height=title.size[1])
title_canvas.create_image(0,0,anchor=NW,image=title_image_to_canvas)
title_canvas.grid(row=0,column=0,sticky=E+W)

#Menu window
menu_frame = Frame(master,bg="white")
menu_image_to_canvas = ImageTk.PhotoImage(menu)
menu_canvas = Canvas(menu_frame,bg="white",width=title.size[0],height=title.size[1])
menu_canvas.create_image(0,0,anchor=NW,image=menu_image_to_canvas)
menu_canvas.grid(row=0,column=0,sticky=E+W,rowspan = 50,columnspan = 5)

#Automatically create the menu items and the different levels
menu_items = ["tutorial"]
level_titles = ["Tutorial"]

for x in range(1,7):
    exec("""level{0} = Label(menu_frame,text='Level {0}',
        font=('Helvetica',20),bg='white',fg='#9b9b9b')\nlevel{0}.grid(row={1},
        column=2,sticky=E+W)""".format(str(x),str(x+29)))
    menu_items.append("level"+str(x))
    level_titles.append("Level "+str(x))

for x in range(7,13):
    exec("""level{0} = Label(menu_frame,text='Level {0}',
        font=('Helvetica',20),bg='white',fg='#9b9b9b')\nlevel{0}.grid(row={1},
        column=3,sticky=E+W)""".format(str(x),str(x+23)))
    menu_items.append("level"+str(x))
    level_titles.append("Level "+str(x))

#Level window
level_frame = Frame(master,bg="white")
level_image_to_canvas = ImageTk.PhotoImage(level)
level_canvas = Canvas(level_frame,bg="white",width=title.size[0],
height=title.size[1])
level_canvas.create_image(0,0,anchor=NW,image=level_image_to_canvas)
level_canvas.grid(row=0,column=0,sticky=E+W,rowspan = 10,columnspan = 10)
level_title = Label(level_frame,font=("Helvetica",70),bg ="white",fg="#2aada9")
level_title.grid(row=1,column=3,sticky=E+W,columnspan = 4)
level_press = Label(level_frame,font=("Helvetica",40),bg ="white",fg="#9b9b9b",
text="Press 'F' and 'J' keys to begin")
level_press.grid(row=4,column=2,sticky=E+W,columnspan = 6)
level_key = Label(level_frame,font=("Helvetica",280),bg ="white",fg="#9b9b9b")

#Results window
result_frame = Frame(master,bg="white")
result_image_to_canvas = ImageTk.PhotoImage(result)
result_canvas = Canvas(result_frame,bg="white",width=result.size[0],
height=result.size[1])
result_canvas.create_image(0,0,anchor=NW,image=result_image_to_canvas)
result_canvas.grid(row=0,column=0,sticky=E+W,rowspan = 10,columnspan = 20)
result_label = Label(result_frame,font=("Helvetica",200),bg ="white",
fg="#2aada9")
result_label.grid(row=3,column=11,sticky=E+W,columnspan = 8)
result_highscore = Label(result_frame,font=("Helvetica",50),bg ="white",
fg="#2aada9",text="Highscore: ")
result_highscore.grid(row=5,column=1,sticky=E+W,columnspan = 8)

#Tutorial Window
tutorial = Label(menu_frame,text="Tutorial",font=("Helvetica",20),
bg="#2aada9",fg="white")
tutorial.grid(row=25,column=2,sticky=E+W,columnspan = 2)

#-------------------------------Global Variables--------------------------------
global state
state = "title"         #Saves the current window

global item
item = 0                #Saves the level/item number

global double
double = ""             #Allows detection of full words from pynput

global onkey
onkey = 0               #Saves the current target key


global currentLesson    #Saves the current lesson

global presses,correct  #Allow the calculation of the effectiveness percentage

global gloves
gloves = Gloves()
gloves.start()

#-------------------------------Main Functions----------------------------------

#Turn raw key name to readable text. Display key. Play audio.
def formatKey(level_key,key):
    try:
        level_key.config(font=("Helvetica",280),
        text=key.upper().split("'")[1])
        try:
            queue("keys/"+key.upper().split("'")[1])
        except:
            try:
                queue("keys/"+key.upper().split('"')[1])
            except:
                print("{} File not found".format(key))
    except IndexError:
        level_key.config(font=("Helvetica",110),
        text=key.upper().split(".")[1].replace("_"," ").title())
        try:
            queue("keys/"+key.upper().split(".")[1].replace("_"," ").title())
        except:
            print("File not found")


#Move from one window to another
def transition(previous,next,state_):
    global state
    previous.forget()
    next.pack(expand=1,fill=BOTH)
    state=state_

def play(file):
    mixer.music.load('Audio/{}.mp3'.format(file))
    mixer.music.play()

def queue(file):
    while True:
        pos = mixer.music.get_pos()
        if int(pos) == -1:
            return play(file)

#Whenever a key is pressed
def on_press(key):

    global state,presses,correct,item               #Load global variables

    #Press any key to continue
    if(state=="title"):
        transition(title_frame,menu_frame,"menu")
        play("screens/menu")

    #When on the level menu
    elif(state=="menu"):

    #If the pressed key is escape close window,
    #any other key opens selected level
        if(key==Key.esc):
            master.destroy()
        else:
            transition(menu_frame,level_frame,"level_waiting")
            level_title.config(text=level_titles[item])
            play("screens/selected")
            queue("levels/"+level_titles[item])
            if(item==0):
                queue("screens/tutorial exp")
            else:
                queue("screens/F and J")


    #When waiting for the user to click f and j to begin the lesson
    elif(state=="level_waiting"):

        #Escape returns to menu
        if(key==Key.esc):
            transition(level_frame,menu_frame,"menu")
            play("screens/menu")
        else:

            #Begin simultaneous key press detection
            global double
            if(len(double)==0):
                double = str(key)
            else:
                double+=str(key)

                #If j and f are pressed simultaneously, begin lesson

                if(double=="'f''j'" or double=="'j''f'"):
                    if(item>0):
                        global currentLesson
                        currentLesson = lessons[level_titles[item]]

                        #Vibrate glove on corresponding finger
                        gloves.vibrate(fingers[currentLesson[0]]+"\n")

                        level_press.forget()
                        level_key.grid(row=2,column=2,sticky=E+W,
                        columnspan = 6,rowspan=6)
                        play("effects/start")

                        formatKey(level_key,currentLesson[0])
                        correct = 0
                        presses = 0
                        state="level_playing"
                    else:
                        level_press.config(text="Wait for the Tutorial to end...")
                        play("effects/start")
                        queue("screens/tutorial exp 2")
                        while True:
                            pos = mixer.music.get_pos()
                            if int(pos) == -1:
                                gloves.vibrate("5\n")
                                break
                        queue("screens/tutorial exp 3")
                        queue("screens/continue")
                        state="tutorial_waiting"

                else:
                    double=""

    #When the level is active
    elif(state=="level_playing"):
        global onkey

        #During the lesson
        try:

            presses+=1                          #Add one to total attempts

            #If pressed key is target key
            if(str(key)==currentLesson[onkey]):
                correct+=1                      #Add one to total correct
                onkey+=1                        #Move to the next key

                #Turn green and change
                play("effects/correct")
                level_key.config(fg="green")
                sleep(0.3)
                level_key.config(fg="#9b9b9b")

                #Vibrate glove on corresponding finger
                gloves.vibrate(fingers[currentLesson[onkey]]+"\n")

                formatKey(level_key,currentLesson[onkey])


            #If pressed key is not target key
            else:

                #Turn red and return
                level_key.config(fg="red")
                formatKey(level_key,str(key))
                sleep(0.3)
                level_key.config(fg="#9b9b9b")
                queue("effects/incorrect")

                formatKey(level_key,currentLesson[onkey])

                #Vibrate glove on corresponding finger
                gloves.vibrate(fingers[currentLesson[onkey]]+"\n")



        #When the lesson is over
        except IndexError as e:

            sleep(1)
            #Calculate success rate
            avg = floor(correct/presses*100)

            #Make font smaller if result is 100
            if(avg == 100):
                result_label.config(font=("Helvetica",155))
            else:
                result_label.config(font=("Helvetica",200))
            result_label.config(text=str(avg)+"%")

            #Get highscore from file
            with open("Resources/highscores.txt","r") as file:
                highscores = file.readlines()
            highscore = int(highscores[item-1].split(": ")[1])

            #Write new highscore if necessary
            if(highscore<avg):
                highscore = avg
                with open("Resources/highscores.txt","w") as file:
                    highscores[item-1] = level_titles[item]+": "+str(highscore)+"\n"
                    file.writelines(highscores)
                    print(highscore)
            result_highscore.config(text="Highscore: "+str(highscore)+"%")

            transition(level_frame,result_frame,"result")
            gloves.vibrate(str(0))


            play("effects/complete")
            queue("screens/complete")

            #Transform score percentage to audio
            if(avg<20):
                queue("numbers/"+str(avg))
            elif (avg>=20 and avg<100):
                queue("numbers/{}0".format(str(avg)[0]))
                if(int(str(avg)[1])>0):
                    queue("numbers/{}".format(str(avg)[1]))
            else:
                queue("numbers/100")
            queue("screens/percent")

            queue("screens/highscore")

            #Transform highscore percentage to audio
            if(highscore<20):
                queue("numbers/"+str(highscore))
            elif (highscore>=20 and highscore<100):
                queue("numbers/{}0".format(str(highscore)[0]))
                if(int(str(highscore)[1])>0):
                    queue("numbers/{}".format(str(highscore)[1]))
            else:
                queue("numbers/100")

            queue("screens/percent")
            queue("screens/next")
            queue("screens/return")

    elif(state=="tutorial_waiting"):
        transition(level_frame,menu_frame,"menu")

    #When on the result window
    elif(state=="result"):

        #Key goes to next level
        level_key.forget()
        formatKey(level_key,"")
        transition(result_frame,level_frame,"level_waiting")
        item+=1
        onkey = 0
        level_title.config(text=level_titles[item])
        level_press.grid(row=4,column=2,sticky=E+W,columnspan = 6)
        play("levels/Level "+str(item))
        queue("screens/F and J")


#Whenever the mouse is clicked
def on_click(x, y, button, pressed):
    global state,item,double                          #Load global variables

    #If the menu is open
    if(state=="menu"):

        #Right click goes down the menu and left click goes up
        if(pressed):
            exec(menu_items[item]+".config(bg='white',fg='#9b9b9b')")
            if button == Button.left:
                if(item == 0):
                    item = 12
                else:
                    item-=1

            elif button == Button.right:
                if(item == 12):
                    item = 0
                else:
                    item+=1
            exec(menu_items[item]+".config(bg='#2aada9',fg='white')")

            if(item == 0):
                play("levels/tutorial")
            else:
                play("levels/Level "+str(item))

    #When on the result window
    elif(state=="result"):
        level_key.forget()
        formatKey(level_key,"")
        double=""
        onkey = 0
        transition(result_frame,menu_frame,"menu")
        level_press.grid(row=4,column=2,sticky=E+W,columnspan = 6)
        play("screens/menu")

#Main loop embeded inside listeners for mouse click and key press

with mouseListener(on_click = on_click) as listener:
    with keyboardListener(on_press = on_press) as listener:
        play("screens/welcome")
        gloves.vibrate(str(0))
        master.mainloop()
        listener.join()
