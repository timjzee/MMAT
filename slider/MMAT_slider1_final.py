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
    list_path = "D:\\Tim\MMAT_slider\\lists\\"
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
        self.focus_var = tk.StringVar()
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
        self.focus_var.set(self.focus_get())

    def getFrame(self, f):
        return self.frames[f]

    def quitExperiment(self, event=None):
        self.focus_var.set("something different")
        self.destroy()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, minsize=1100)
        self.grid_rowconfigure(0, minsize=700)
        welcome_text = "Je krijgt straks 3 keer achter elkaar hetzelfde woord te horen.\n\nHet is jouw taak om ervoor te zorgen dat de 1e en 2e versie van het woord even veel van elkaar verschillen als de 2e en 3e versie.\n\nDit ga je doen door de 1e versie aan te passen met een schuifknop. LET OP: het verschil tussen de 1e en 2e versie is per woord anders. De uiteindelijke positie van de schuifknop kan dus per woord verschillen.\n\nAls je tevreden bent mag je zelf door klikken naar het volgende woord."
        msg = tk.Message(self, text=welcome_text, font=("Arial", 24), bg="darkgray", fg="white")
        msg.grid(row=0, column=0)
        self.bind("<Return>", lambda page: controller.showFrame(PracticeStart))


class PracticeStart(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, minsize=1100)
        self.grid_rowconfigure(0, minsize=650)
        practice_text = "Je gaat nu eerst een paar keer oefenen. Druk op 'Ok' om te beginnen."
        prac_msg = tk.Message(self, text=practice_text, font=("Arial", 24), bg="darkgray", fg="white")
        prac_msg.grid(row=0, column=0)
        button = tk.Button(self, text="Ok", bg="darkgray", command=lambda: self.toTrialPage(controller))
        button.grid(row=1, column=0)

    def toTrialPage(self, cont_class):
        tp = cont_class.getFrame(TrialPage)
        cont_class.showFrame(TrialPage)
        cont_class.update()
        tp.sendToPraat("<ButtonRelease event state=Button1 num=1 x=300 y=13>")


class PracticeEnd(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, minsize=1100)
        self.grid_rowconfigure(0, minsize=700)
        self.endprac_txt = tk.StringVar()
        # endprac_text = "Het experiment gaat nu beginnen."
        endprac_msg = tk.Message(self, textvariable=self.endprac_txt, font=("Arial", 24), bg="darkgray", fg="white")
        endprac_msg.grid(row=0, column=0)
        self.bind("<Return>", lambda page: controller.showFrame(TrialPage))
        self.bind("q", controller.quitExperiment)


class PausePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, minsize=1100)
        self.grid_rowconfigure(0, minsize=700)
        pause_msg = tk.Message(self, text="Pauze.", font=("Arial", 24), bg="darkgray", fg="white")
        pause_msg.grid(row=0, column=0)
        self.bind("<Return>", lambda page: controller.showFrame(TrialPage))


class TrialPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_rowconfigure(0, minsize=250)
        self.grid_rowconfigure(1, minsize=300)
        self.grid_rowconfigure(2, minsize=200)
        self.grid_columnconfigure(0, minsize=1100)
        self.current_stim = 0
        self.num_adjustments = 0
        self.cumul_prac_shift = 0
        # Stimulus name
        # self.current_stim_var = tk.StringVar()
        self.current_stim_text = tk.Text(self, height=2, wrap="word", font=("Arial", 18), bg="darkgray", fg="white", highlightthickness=0)
        self.current_stim_text.grid(row=0, column=0)
        # Slider
        self.slider = tk.Scale(self, from_=0, to=slider_range, orient="horizontal", showvalue=False, length=600, width=30, highlightbackground="darkgray", bg="darkgray", troughcolor="lightgray")
        self.slider.bind("<ButtonRelease-1>", self.sendToPraat)
        self.slider.grid(row=1, column=0)
        # Next Button
        self.next_button = tk.Button(self, text="Volgende", bg="darkgray", command=lambda: self.nextTrial(controller))
        self.next_button.grid(row=2, column=0)
        self.updateWidgets()

    def sendToPraat(self, event):
        self.slider.unbind("<ButtonRelease-1>")
        self.slider.config(state="disabled")
        self.next_button.config(state="disabled")
        self.new_value = float(self.slider.get())
        self.min_erb = erb_shift_list[self.current_stim] - (erb_shift_range / 2)
        self.slider_prop = self.new_value / slider_range
        self.erb_shift = self.min_erb + (erb_shift_range * self.slider_prop)
        print("Slider pos: " + str(self.new_value) + "\nERB shift: " + str(self.erb_shift))
        subprocess.call([praat_path, "--run", script_path + "playStimuli.praat", stimulus_list[self.current_stim], "c_b_a", str(self.erb_shift)])
        self.num_adjustments += 1
        self.after(500, self.bindSlider)

    def bindSlider(self):
        self.slider.bind("<ButtonRelease-1>", self.sendToPraat)
        self.slider.config(state="normal")
        self.next_button.config(state="normal")

    def updateWidgets(self):
        self.current_stim_text.config(state="normal")
        self.current_stim_text.delete(1.0, "end")
        self.current_stim_text.insert("end", "Versleep de schuif zodat het verschil tussen de eerste en tweede versie van " + stimulus_list[self.current_stim] + " even groot is als het verschil tussen de tweede en derde versie.")
        self.tag_end = "1." + str(76 + len(stimulus_list[self.current_stim]))
        self.current_stim_text.tag_add("red", "1.76", self.tag_end)
        self.current_stim_text.tag_configure("red", foreground="red")
        self.current_stim_text.tag_add("center", 1.0, "end")
        self.current_stim_text.tag_configure("center", justify='center')
        self.current_stim_text.config(state="disabled")
        # Slider
        self.slider.set(slider_start)

    def writeInput(self):
        g.write(str(self.current_stim + 1) + "," + stimulus_list[self.current_stim] + "," + str(self.erb_shift) + "," + str(self.num_adjustments) + "\n")

    def nextTrial(self, cont_class, event=None):
        if self.num_adjustments > 1:
            self.slider.set(slider_start)
            self.writeInput()
            self.num_adjustments = 0
            if self.current_stim < 4:
                self.cumul_prac_shift += self.erb_shift
            if self.current_stim >= (len(stimulus_list) - 1):
                app.destroy()
            elif self.current_stim == 4:
                self.mean_prac_erb = self.cumul_prac_shift / 5
                pe = cont_class.getFrame(PracticeEnd)
                if self.mean_prac_erb < 0.9:
                    pe.endprac_txt.set("Sluit experiment af (q) en geef nadere toelichting.")
                else:
                    pe.endprac_txt.set("Het experiment gaat nu beginnen. (Enter)")
                self.current_stim += 1
                self.updateWidgets()
                cont_class.showFrame(PracticeEnd)
                cont_class.wait_variable(cont_class.focus_var)
                cont_class.update()
                self.sendToPraat("<ButtonRelease event state=Button1 num=1 x=300 y=13>")
            elif self.current_stim == 39:
                self.current_stim += 1
                self.updateWidgets()
                cont_class.showFrame(PausePage)
                cont_class.wait_variable(cont_class.focus_var)
                cont_class.update()
                self.sendToPraat("<ButtonRelease event state=Button1 num=1 x=300 y=13>")
            else:
                self.current_stim += 1
                self.updateWidgets()
                self.update()
                self.sendToPraat("<ButtonRelease event state=Button1 num=1 x=300 y=13>")
                # self.current_stim_var.set(stimulus_list[self.current_stim])


def callbackPP():
    callbackPP.pp_num = int(getParticipantInfo.ent.get())
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
g = open("./logs/" + str(pp) + "_results.csv", "w")
g.write("trial,stimulus,erb_shift,num_adjustments\n")

app = Experiment()
app.mainloop()
g.close()
