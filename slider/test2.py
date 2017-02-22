import sys
import subprocess
import platform
if sys.version_info[0] == 2:
    import Tkinter as tk
else:
    import tkinter as tk


if platform.system() == "Linux":
    praat_path = "/usr/bin/praat"
elif platform.system() == "Darwin":
    praat_path = "/Applications/Praat.app/Contents/MacOS/Praat"
elif platform.system() == "Windows":
    praat_path = "C:\Program Files\Praat.exe"
else:
    print("Incompatible operating system detected.")
    sys.exit()
slider_range = 100
slider_start = slider_range / 2
erb_shift_range = 4


class Experiment(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(expand=True)
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", self.exitFullScreen)
        self.frames = {}
        for f in [StartPage, TrialPage]:
            frame = f(container, self)
            self.frames[f] = frame
            frame.grid(row=1, column=1)
        self.showFrame(StartPage)

    def exitFullScreen(self, event):
        self.attributes("-fullscreen", False)

    def showFrame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def quitExperiment():
        app.destroy()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, minsize=800)
        # self.grid_rowconfigure(0, minsize=600)
        welcome_text = "Welkom bij dit luister experiment. In dit experiment krijg je telkens 3 versies van hetzelfde woord te horen. De eerste versie die je hoort is de oorspronkelijke opname van het woord. De tweede en derde versie zijn gamanipuleerd.\n\nHet is jouw taak om de derde versie van het woord aan te passen zodat het verschil tussen versie A en versie B even groot is als het verschil tussen versie B en versie C. Dit doe je door de knop die op het scherm verschijnt de verschuiven. Elke keer dat je de knop verschuift krijg je de drie versies te horen. Je mag de knop zo vaak verschuiven als je wilt.\n\nAls je tevreden bent met je manipulatie mag je zelf door klikken naar het volgende woord."
        msg = tk.Message(self, text=welcome_text, font=("Arial", 24))
        msg.grid(row=0, column=0)
        button = tk.Button(self, text="Ok", command=lambda: controller.showFrame(TrialPage))
        button.grid(row=1, column=0)


class TrialPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_rowconfigure(0, minsize=150)
        self.grid_rowconfigure(1, minsize=100)
        self.grid_rowconfigure(3, minsize=250)
        self.current_stim = 0
        # Stimulus name
        # self.current_stim_var = tk.StringVar()
        # self.current_stim_name = tk.Label(self, textvariable=self.current_stim_var)
        # self.current_stim_name.pack()
        # self.current_stim_var.set(stimulus_list[self.current_stim])
        # AB button
        self.ab_button = tk.Button(self, text="Versie A - Versie B", command=self.sendVersionAB)
        self.ab_button.grid(row=0, column=0)
        # BC button
        self.bc_button = tk.Button(self, text="Versie B - Versie C", command=self.sendVersionBC)
        self.bc_button.grid(row=0, column=2)
        # Slider
        slider_text = tk.Label(self, text="Versie C:")
        slider_text.grid(row=1, column=1, sticky="s")
        self.slider = tk.Scale(self, from_=0, to=slider_range, orient="horizontal", showvalue=False, length=400)
        self.slider.set(slider_start)
        self.slider.bind("<ButtonRelease-1>", self.sendVersionC)
        self.slider.grid(row=2, column=1)
        # Next Button
        self.next_button = tk.Button(self, text="Volgende", command=self.nextTrial)
        self.next_button.grid(row=3, column=1)

    def sendVersionAB(self, event=None):
        subprocess.call([praat_path, "--run", "playStimuli.praat", stimulus_list[self.current_stim], "a_and_b", "0"])

    def sendVersionBC(self, event=None):
        self.c_value = self.slider.get()
        self.min_erb = erb_shift_list[self.current_stim] - (erb_shift_range / 2)
        self.slider_prop = self.c_value / slider_range
        self.erb_shift = self.min_erb + (erb_shift_range * self.slider_prop)
        subprocess.call([praat_path, "--run", "playStimuli.praat", stimulus_list[self.current_stim], "b_and_c", str(self.erb_shift)])

    def sendVersionC(self, event):
        self.new_value = self.slider.get()
        self.min_erb = erb_shift_list[self.current_stim] - (erb_shift_range / 2)
        self.slider_prop = self.new_value / slider_range
        self.erb_shift = self.min_erb + (erb_shift_range * self.slider_prop)
        print("Slider pos: {}\nERB shift: {}".format(self.new_value, self.erb_shift))
        subprocess.call([praat_path, "--run", "playStimuli.praat", stimulus_list[self.current_stim], "c", str(self.erb_shift)])

    def nextTrial(self, event=None):
        self.slider.set(slider_start)
        if self.current_stim >= (len(stimulus_list) - 1):
            Experiment.quitExperiment()
        else:
            self.current_stim += 1
            # self.current_stim_var.set(stimulus_list[self.current_stim])


def callbackPP():
    callbackPP.pp_num = getParticipantInfo.ent.get()
    infoLoop.window.destroy()


def getParticipantInfo():
    getParticipantInfo.lbl = tk.Label(infoLoop.window, text="Participant number:")
    getParticipantInfo.ent = tk.Entry(infoLoop.window)
    getParticipantInfo.btn = tk.Button(infoLoop.window, text="Ok", command=callbackPP)
    getParticipantInfo.lbl.grid(row=0)
    getParticipantInfo.ent.grid(row=0, column=1)
    getParticipantInfo.btn.grid(row=1, column=1, sticky="e")


def infoLoop():
    infoLoop.window = tk.Tk()
    infoLoop.window.title("Enter Participant Info")
    getParticipantInfo()
    infoLoop.window.mainloop()


def loadLists():
    list_name = "list0" + str(callbackPP.pp_num) + ".csv"
    f = open(list_name, "r")
    stim_list = []
    shift_list = []
    counter = 0
    for line in f:
        counter += 1
        if counter == 1:
            continue
        else:
            line_list = line[:-1].split(",")
            stim_list.append(line_list[0])
            shift_list.append(float(line_list[1]))
    f.close()
    return stim_list, shift_list


infoLoop()
stimulus_list, erb_shift_list = loadLists()

app = Experiment()
app.mainloop()
