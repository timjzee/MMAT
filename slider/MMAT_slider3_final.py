import time
import sys
import subprocess
import platform
if sys.version_info[0] == 2:
    import Tkinter as tk
else:
    import tkinter as tk


if platform.system() == "Linux":
    praat_path = "/usr/bin/praat"
    script_path = ""
    list_path = "./lists_final/"
elif platform.system() == "Darwin":
    praat_path = "/Applications/Praat.app/Contents/MacOS/Praat"
    script_path = ""
    list_path = "./lists/"
elif platform.system() == "Windows":
    praat_path = "C:\\Users\\User\\Desktop\\Praat6.exe"
    script_path = "D:\\Tim\\MMAT_slider\\"
    list_path = "D:\\Tim\MMAT_slider\\lists_final\\"
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
        self.configure(background="darkgray")
        self.bind("<Escape>", self.exitFullScreen)
        self.frames = {}
        for f in [StartPage, TrialPage, PracticeStart, PracticeEnd, PausePage]:
            frame = f(container, self)
            frame.config(bg="darkgray")
            self.frames[f] = frame
            frame.grid(row=1, column=1)
        self.showFrame(StartPage)

    def exitFullScreen(self, event):
        self.attributes("-fullscreen", False)

    def showFrame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.focus_set()

    def getFrame(self, f):
        return self.frames[f]

    def quitExperiment(self, event=None):
        self.destroy()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, minsize=1100)
        self.grid_rowconfigure(0, minsize=700)
        welcome_text = "Je gaat straks naar 3 verschillende versies van hetzelfde woord luisteren.\n\nHet is jouw taak om ervoor te zorgen dat het verschil tussen versie A en versie C twee keer zo groot wordt als het verschil tussen versie A en versie B.\n\nDit ga je doen door versie C aan te passen met een schuifknop. LET OP: het verschil tussen versie A en C is per woord anders. De uiteindelijke positie van de schuifknop kan dus per woord verschillen.\n\nAls je tevreden bent mag je zelf door klikken naar het volgende woord."
        msg = tk.Message(self, text=welcome_text, font=("Arial", 24), bg="darkgray", fg="white")
        msg.grid(row=0, column=0)
        self.bind("<Return>", lambda page: controller.showFrame(PracticeStart))


class PracticeStart(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, minsize=1100)
        self.grid_rowconfigure(0, minsize=650)
        self.grid_rowconfigure(1, minsize=50)
        practice_text = "Je gaat nu eerst een paar keer oefenen. Druk op 'Ok' om te beginnen."
        prac_msg = tk.Message(self, text=practice_text, font=("Arial", 24), width=800, bg="darkgray", fg="white")
        prac_msg.grid(row=0, column=0)
        button = tk.Button(self, text="Ok", bg="darkgray", command=lambda: self.toTrialPage(controller))
        button.grid(row=1, column=0)

    def toTrialPage(self, cont_class):
        tp = cont_class.getFrame(TrialPage)
        tp.current_stim_text.config(state="normal")
        tp.current_stim_text.delete(1.0, "end")
        cont_class.showFrame(TrialPage)
        cont_class.update()
        tp.autoPlay()


class PracticeEnd(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, minsize=1100)
        self.grid_rowconfigure(0, minsize=700)
        self.endprac_txt = tk.StringVar()
        # endprac_text = "Het experiment gaat nu beginnen."
        endprac_msg = tk.Message(self, textvariable=self.endprac_txt, font=("Arial", 24), width=800, bg="darkgray", fg="white")
        endprac_msg.grid(row=0, column=0)
        self.bind("<Return>", lambda cont: self.toTrialPage(controller))
        self.bind("q", controller.quitExperiment)

    def toTrialPage(self, cont_class):
        tp = cont_class.getFrame(TrialPage)
        tp.current_stim_text.config(state="normal")
        tp.current_stim_text.delete(1.0, "end")
        cont_class.showFrame(TrialPage)
        cont_class.update()
        tp.autoPlay()


class PausePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, minsize=1100)
        self.grid_rowconfigure(0, minsize=700)
        pause_msg = tk.Message(self, text="Pauze.", font=("Arial", 24), width=800, bg="darkgray", fg="white")
        pause_msg.grid(row=0, column=0)
        self.bind("<Return>", lambda cont: self.toTrialPage(controller))

    def toTrialPage(self, cont_class):
        tp = cont_class.getFrame(TrialPage)
        tp.current_stim_text.config(state="normal")
        tp.current_stim_text.delete(1.0, "end")
        cont_class.showFrame(TrialPage)
        cont_class.update()
        tp.autoPlay()


class TrialPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_rowconfigure(0, minsize=225)
        self.grid_rowconfigure(1, minsize=25)
        self.grid_rowconfigure(2, minsize=35)
        self.grid_rowconfigure(3, minsize=150)
        self.grid_rowconfigure(4, minsize=40)
        self.grid_rowconfigure(5, minsize=225)
        self.grid_columnconfigure(0, minsize=1100)
        self.current_stim = 0
        self.num_adjustments = 0
        self.prac_shifts = []
        # Stimulus name
        # self.current_stim_var = tk.StringVar()
        self.current_stim_text = tk.Text(self, height=2, wrap="word", font=("Arial", 18), bg="darkgray", fg="white", highlightthickness=0)
        self.current_stim_text.grid(row=0, column=0, sticky="n")
        # AB button
        self.ab_text = tk.Label(self, text="Versie A - Versie B", fg="white", bg="darkgray")
        self.ab_text.grid(row=1, column=0, sticky="s")
        self.ab_button = tk.Button(self, text="", bg="darkgray", width=65, command=self.sendVersionAB)
        self.ab_button.grid(row=2, column=0, sticky="n")
        # AC slider
        self.ac_text = tk.Label(self, text="Versie A - Versie C", fg="white", bg="darkgray")
        self.ac_text.grid(row=3, column=0, sticky="s")
        self.slider = tk.Scale(self, from_=0, to=slider_range, orient="horizontal", showvalue=False, length=600, width=30, highlightbackground="darkgray", bg="darkgray", troughcolor="lightgray")
        self.slider.bind("<ButtonRelease-1>", self.sendVersionAC)
        self.slider.grid(row=4, column=0, sticky="n")
        # Next Button
        self.next_button = tk.Button(self, text="Volgende", bg="darkgray", command=lambda: self.nextTrial(controller))
        self.next_button.grid(row=5, column=0, sticky="s")
        self.updateWidgets()

    def sendVersionAB(self, event=None):
        self.slider.unbind("<ButtonRelease-1>")
        self.slider.config(state="disabled")
        self.next_button.config(state="disabled")
        self.ab_button.config(state="disabled")
        subprocess.call([praat_path, "--run", script_path + "playStimuli.praat", stimulus_list[self.current_stim], "a_and_b", "0"])
        self.after(500, self.bindButtons)

    def sendVersionAC(self, event):
        self.slider.unbind("<ButtonRelease-1>")
        self.slider.config(state="disabled")
        self.next_button.config(state="disabled")
        self.ab_button.config(state="disabled")
        self.new_value = float(self.slider.get())
        self.min_erb = erb_shift_list[self.current_stim] - (erb_shift_range / 2)
        self.slider_prop = self.new_value / slider_range
        self.erb_shift = self.min_erb + (erb_shift_range * self.slider_prop)
        print("Slider pos: " + str(self.new_value) + "\nERB shift: " + str(self.erb_shift))
        subprocess.call([praat_path, "--run", script_path + "playStimuli.praat", stimulus_list[self.current_stim], "a_and_c", str(self.erb_shift)])
        self.num_adjustments += 1
        self.after(300, self.bindButtons)

    def bindButtons(self):
        self.slider.bind("<ButtonRelease-1>", self.sendVersionAC)
        self.slider.config(state="normal")
        self.next_button.config(state="normal")
        self.ab_button.config(state="normal")

    def updateWidgets(self):
        self.current_stim_text.config(state="normal")
        self.current_stim_text.delete(1.0, "end")
        self.current_stim_text.insert("end", "Versleep de schuif zo dat het verschil tussen versie A en versie C van " + stimulus_list[self.current_stim] + " 2x zo groot is als het verschil tussen versie A en versie B.")
        self.tag_end = "1." + str(71 + len(stimulus_list[self.current_stim]))
        self.current_stim_text.tag_add("red", "1.71", self.tag_end)
        self.current_stim_text.tag_configure("red", foreground="red")
        self.current_stim_text.tag_add("center", 1.0, "end")
        self.current_stim_text.tag_configure("center", justify='center')
        self.current_stim_text.config(state="disabled")
        # Slider
        self.slider.set(slider_start)

    def writeInput(self):
        g.write(str(self.current_stim + 1) + "," + stimulus_list[self.current_stim] + "," + str(self.erb_shift) + "," + str(self.num_adjustments) + "," + callbackPP.pp_age + "," + callbackPP.pp_gen + "\n")

    def autoPlay(self):
        "Autoplays and highlights stimuli at the start of each trial."
        self.ab_text.config(fg="red")
        self.ab_button.config(bg="red")
        self.update()
        self.sendVersionAB()
        self.ab_text.config(fg="white")
        self.ab_button.config(bg="darkgray")
        self.after(500, self.update())
        self.ac_text.config(fg="red")
        self.slider.config(bg="red")
        self.update()
        self.sendVersionAC("<ButtonRelease event state=Button1 num=1 x=300 y=13>")
        self.ac_text.config(fg="white")
        self.slider.config(bg="darkgray")
        self.updateWidgets()
        self.update()

    def nextTrial(self, cont_class, event=None):
        if self.num_adjustments > 1:
            self.slider.set(slider_start)
            self.writeInput()
            self.num_adjustments = 0
            if self.current_stim < 4:
                self.prac_shifts.append(self.erb_shift)
            if self.current_stim >= (len(stimulus_list) - 1):
                app.destroy()
            elif self.current_stim == 4:
                self.min_prac_erb = min(self.prac_shifts)
                pe = cont_class.getFrame(PracticeEnd)
                if self.min_prac_erb < 0.9:
                    pe.endprac_txt.set("Sluit experiment af (q) en geef nadere toelichting.")
                else:
                    pe.endprac_txt.set("Het experiment gaat nu beginnen. (Enter)")
                self.current_stim += 1
                self.updateWidgets()
                cont_class.showFrame(PracticeEnd)
            elif self.current_stim == 39:
                self.current_stim += 1
                self.updateWidgets()
                cont_class.showFrame(PausePage)
            else:
                self.current_stim += 1
                self.updateWidgets()
                self.current_stim_text.config(state="normal")
                self.current_stim_text.delete(1.0, "end")
                self.update()
                self.autoPlay()
                # self.current_stim_var.set(stimulus_list[self.current_stim])


def callbackPP():
    callbackPP.pp_num = int(getParticipantInfo.nument.get())
    callbackPP.pp_age = str(getParticipantInfo.ageent.get())
    callbackPP.pp_gen = str(getParticipantInfo.genent.get())
    infoLoop.window.destroy()


def getParticipantInfo():
    getParticipantInfo.numlbl = tk.Label(infoLoop.window, text="Participant number:")
    getParticipantInfo.numlbl.grid(row=0, column=0)
    getParticipantInfo.nument = tk.Entry(infoLoop.window)
    getParticipantInfo.nument.grid(row=0, column=1)
    getParticipantInfo.agelbl = tk.Label(infoLoop.window, text="Age:")
    getParticipantInfo.agelbl.grid(row=1, column=0)
    getParticipantInfo.ageent = tk.Entry(infoLoop.window)
    getParticipantInfo.ageent.grid(row=1, column=1)
    getParticipantInfo.genlbl = tk.Label(infoLoop.window, text="Gender (f/m):")
    getParticipantInfo.genlbl.grid(row=2, column=0)
    getParticipantInfo.genent = tk.Entry(infoLoop.window)
    getParticipantInfo.genent.grid(row=2, column=1)
    getParticipantInfo.btn = tk.Button(infoLoop.window, text="Ok", command=callbackPP)
    getParticipantInfo.btn.grid(row=3, column=1, sticky="e")


def infoLoop():
    infoLoop.window = tk.Tk()
    infoLoop.window.title("Enter Participant Info")
    getParticipantInfo()
    infoLoop.window.mainloop()


def loadLists():
    if callbackPP.pp_num < 10:
        list_name = "list0" + str(callbackPP.pp_num) + ".csv"
    else:
        list_name = "list" + str(callbackPP.pp_num) + ".csv"
    f = open(list_path + list_name, "r")
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
    prac_stimuli = ["staak", "fuik", "teug", "kaap", "schuit"]
    prac_shifts = [1.04, 1.52, 2.96, 2, 2.48]
    stim_list = prac_stimuli + stim_list
    shift_list = prac_shifts + shift_list
    return stim_list, shift_list, callbackPP.pp_num


infoLoop()
stimulus_list, erb_shift_list, pp = loadLists()
time_str = str(time.localtime()[3]) + "-" + str(time.localtime()[4]) + "-" + str(time.localtime()[5])
g = open("./logs/" + str(pp) + "_results_" + time_str + ".csv", "w")
g.write("trial,stimulus,erb_shift,num_adjustments,age,gender\n")

app = Experiment()
app.mainloop()
g.close()
