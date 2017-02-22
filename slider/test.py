import tkinter


def callbackPP():
    pp_num = getParticipantInfo.ent.get()
    getParticipantInfo.ent.pack_forget()
    getParticipantInfo.lbl.pack_forget()
    getParticipantInfo.btn.pack_forget()
    print(pp_num)
    showInstructions()


def getParticipantInfo():
    getParticipantInfo.lbl = tkinter.Label(window, text="Participant number:")
    getParticipantInfo.ent = tkinter.Entry(window)
    getParticipantInfo.btn = tkinter.Button(window, text="Ok", command=callbackPP)
    getParticipantInfo.lbl.pack()
    getParticipantInfo.ent.pack()
    getParticipantInfo.btn.pack()


def callbackInstr():
    showInstructions.txt.pack_forget()
    showInstructions.btn.pack_forget()
    runTrials()


def showInstructions():
    """Show instructions"""
    text = "Welkom bij dit luister experiment. In dit experiment krijg je telkens 3 versies van hetzelfde woord te horen. De eerste versie die je hoort is de oorspronkelijke opname van het woord. De tweede en derde versie zijn gamanipuleerd.\n\nHet is jouw taak om de derde versie van het woord aan te passen zodat het verschil tussen versie 1 en versie 2 even groot is als het verschil tussen versie 2 en versie 3. Dit doe je door de knop die op het scherm verschijnt de verschuiven. Elke keer dat je de knop verschuift krijg je de drie versies te horen. Je mag de knop zo vaak verschuiven als je wilt.\n\nAls je tevreden bent met je manipulatie mag je zelf door klikken naar het volgende woord."
    showInstructions.txt = tkinter.Message(window, text=text, anchor="center")
    showInstructions.btn = tkinter.Button(window, text="Ok", command=callbackInstr)
    showInstructions.txt.pack()
    showInstructions.btn.pack()


def runTrials():
    for i in range(10):
        num = tkinter.Label(window, text=str(i), anchor="center")
        btn = tkinter.Button(window, text="Ok", command=lambda: num.pack_forget())
        num.pack()
        btn.pack()


window = tkinter.Tk()
window.title("experiment")
window.geometry("800x600")

getParticipantInfo()

window.mainloop()
