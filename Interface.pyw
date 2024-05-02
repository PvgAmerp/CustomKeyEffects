import tkinter as Tk
from tkinter import filedialog
import os
import shutil

window = Tk.Tk()

window.title("Custom Key Effects")
window.geometry("1200x800")
window.resizable(False,False)

script_dir = os.path.dirname(os.path.realpath(__file__))

def check_effects_folder():
    effects_folder = os.path.join(script_dir, 'Effects')
    if not os.path.exists(effects_folder):
        os.makedirs(effects_folder)
        EffectsFolderErrorWindow = Tk.Toplevel()
        EffectsFolderErrorWindow.geometry("700x200")
        EffectsFolderErrorWindow.title("Error")
        
        ErrorText1 = Tk.Label(EffectsFolderErrorWindow, text="""
        The Effects folder wasn't found so I created it.
        Please re-run the script so it can run correctly
        and create Effects.""", font=("Helvetica", 18))
        ErrorText1.place(x=50, y=30)
        
        return False
    else:
        return True

def Home():
    global NewEffect, LoadEffect

    NewEffect = Tk.Button(window, text="New Effect", font=("Helvetica", 20), command=NewEffect)
    NewEffect.place(x=335, y=100)

    LoadEffect = Tk.Button(window, text="Load Effect", font=("Helvetica", 20), command=LoadEffectF)
    LoadEffect.place(x=685, y=100)

    SetEffectToKeyButton = Tk.Button(window, text="Set Effect To Key", font=("Helvetica", 20), command=SETK)
    SetEffectToKeyButton.place(x=800, y=500)

    LoadEffectWarning = Tk.Label(window, text="WARNING: The selected folder will be moved to the 'Effects' folder.", font=("Helvetica", 12))
    LoadEffectWarning.place(x=550, y=165)

def SETK():
    def SETKdone():
        global SETKFolder, SETKKey

        SETKFolder = EffectFolderBox.get()
        SETKKey = KeyBox.get()

        existing_text = ""

        SETKCommandLine = Tk.Label(SETKwindow, text="Effect: " + SETKFolder + " will be played when " + SETKKey + " is pressed", font=("Helvetica", 16))
        SETKCommandLine.place(x=25, y=400)

        SETKFullPath = os.path.join(SETKFolder, "value.txt")

        if os.path.exists(SETKFullPath):
            with open(SETKFullPath, 'r') as file:
                existing_text = file.read()

        new_text = existing_text + "\n" + "key=" + SETKKey

        def UpdateValueKey():
            with open(SETKFullPath, 'w') as file:
                file.write(new_text)

        #its not my fault i aint no balls to make a tk object wait. Respect.

        UpdateValueKey()
        SETKwindow.destroy()
    
    SETKwindow = Tk.Tk()

    SETKwindow.title("Set Effect To Key:")
    SETKwindow.geometry("1200x450")
    SETKwindow.resizable(False,False)

    EffectFolderBox = Tk.Entry(SETKwindow, font=("Helvetica", 18), width=70)
    EffectFolderBox.place(x=150, y=80)
    EffectFolderBox.insert(0, script_dir + "/Effects/EffectNameHere")

    KeyBox = Tk.Entry(SETKwindow, font=("Helvetica", 18), width=70)
    KeyBox.place(x=150, y=200)
    KeyBox.insert(0, "Key Here. (Only 1 character)")

    TipSETK = Tk.Label(SETKwindow, text="Replace: EffectNameHere, with your effect name or change the path to your effect, if not on default location.", font=("Helvetica", 18))
    TipSETK.place(x=20, y=125)

    SETKdoneButton = Tk.Button(SETKwindow, text="Done", font=("Helvetica", 18), command=SETKdone)
    SETKdoneButton.place(x=550, y=300)

def NewEffect():
    def Next():
        global ValueTxtFullPath, NextWindow, SoundPathBox, URLBox
        
        NextWindow = Tk.Tk()

        NextWindow.title("Select type of effect:")
        NextWindow.geometry("600x400")
        NextWindow.resizable(False,False)

        NewEffectName = NewEffectNameBox.get()
        print("The name of the new effect is: " + NewEffectName)

        NewEffectNameBox.destroy()
        NextButton.destroy()

        os.makedirs(script_dir + "/Effects/" + NewEffectName)
        
        ValueTxtParentDir = script_dir + "/Effects/" + NewEffectName
        ValueTxtFullPath = os.path.join(ValueTxtParentDir, "value.txt")

        with open(ValueTxtFullPath, 'x'):
            pass

        SoundEffectButton = Tk.Button(NextWindow, text="Sound Effect", font=("Helvetica", 16), command=UpdateValueSound)
        SoundEffectButton.place(x=100, y=100)

        URLEffectButton = Tk.Button(NextWindow, text="URL Effect", font=("Helvetica", 16), command=UpdateValueURL)
        URLEffectButton.place(x=375, y=100)

        SoundPathBox = Tk.Entry(NextWindow, font=("Helvetica", 16), width=20)
        SoundPathBox.place(x=50, y=150)
        SoundPathBox.insert(0, "Sound Path Here")

        URLBox = Tk.Entry(NextWindow, font=("Helvetica", 16), width=20)
        URLBox.place(x=325, y=150)
        URLBox.insert(0, "https://")

    def UpdateValueSound():
        with open(ValueTxtFullPath, 'w') as file:
            file.write("type=sound\n" + "soundPath=" + SoundPathBox.get())

        SuccesfulEffectCreation()
        NextWindow.destroy()

    def UpdateValueURL():
        with open(ValueTxtFullPath, 'w') as file:
            file.write("type=URL\n" + "URL=" + URLBox.get())
            
        SuccesfulEffectCreation()
        NextWindow.destroy()

    def SuccesfulEffectCreation():
        SuccesfulEffectCreationText = Tk.Label(window, text="Succesful Effect Creation!", font=("Helvetica", 25))
        SuccesfulEffectCreationText.place(x=350, y=360)

        #I didnt quite have the balls to learn how to make a tk object wait. Respect.

        SuccesfulEffectCreationText.destroy()

    NewEffectNameBox = Tk.Entry(window, font=("Helvetica", 16), width=20)
    NewEffectNameBox.insert(0, "New Effect")
    NewEffectNameBox.place(x=300, y=170)

    NextButton = Tk.Button(window, text="Next", font=("Helvetica", 16), command=Next)
    NextButton.place(x=375, y=210)
    
def LoadEffectF():
    selected_folder = filedialog.askdirectory()
    if selected_folder:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        
        destination_directory = os.path.join(script_directory, 'effects')
        
        shutil.move(selected_folder, destination_directory)
        print("Moved selected folder to 'effects' directory.")
    else:
        print("No folder selected.")

if check_effects_folder():
    Home()

window.mainloop()