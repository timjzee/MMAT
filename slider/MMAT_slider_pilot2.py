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
    list_path = "./lists/"
elif platform.system() == "Darwin":
    praat_path = "/Applications/Praat.app/Contents/MacOS/Praat"
    script_path = ""
    list_path = "./lists2/"
elif platform.system() == "Windows":
    praat_path = "C:\\Users\\User\\Desktop\\Praat6.exe"
    script_path = "D:\\Tim\\MMAT_slider\\"
    list_path = "D:\\Tim\MMAT_slider\\lists2\\"
else:
    print("Incompatible operating system detected.")
    sys.exit()
# Slider resolution in ticks per ERB
slider_resolution = 50
slider_start = 0


class Experiment(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(expand=True)
        self.attributes("-fullscreen", True)
        self.configure(background="darkgray")
        self.bind("<Escape>", self.exitFullScreen)
        self.frames = {}
        for f in [StartPage, TrialPage]:
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


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_columnconfigure(0, minsize=1100)
        self.grid_rowconfigure(0, minsize=700)
        welcome_text = "Welkom bij dit luister experiment. In dit experiment krijg je steeds 3 keer achter elkaar hetzelfde woord te horen.\n\nHet verschil tussen de eerste en tweede versie moet even groot worden als het verschil tussen de tweede en derde versie.\n\nHet is jouw taak om dit voor elkaar te krijgen door de eerste versie aan te passen. Dit doe je door de knop die op het scherm verschijnt te verschuiven. LET OP: het verschilt per woord hoe gevoelig de schuifknop voor jouw veranderingen is.\n\nElke keer dat je de knop verschuift krijg je de drie versies te horen. Je mag de knop zo vaak verschuiven als je wilt. Als je tevreden bent mag je zelf door klikken naar het volgende woord."
        msg = tk.Message(self, text=welcome_text, font=("Arial", 24), bg="darkgray", fg="white")
        msg.grid(row=0, column=0)
        button = tk.Button(self, text="Ok", bg="darkgray", command=lambda: controller.showFrame(TrialPage))
        button.grid(row=1, column=0)


class TrialPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.grid_rowconfigure(0, minsize=250)
        self.grid_rowconfigure(1, minsize=300)
        self.grid_rowconfigure(2, minsize=200)
        self.grid_columnconfigure(0, minsize=1100)
        self.current_stim = 0
        self.num_adjustments = 0
        # Stimulus name
        # self.current_stim_var = tk.StringVar()
        self.current_stim_text = tk.Text(self, height=2, wrap="word", font=("Arial", 18), bg="darkgray", fg="white", highlightthickness=0)
        self.current_stim_text.grid(row=0, column=0)
        # Slider
        self.slider = tk.Scale(self, from_=0, orient="horizontal", showvalue=False, length=600, width=30, highlightbackground="darkgray", bg="darkgray", troughcolor="lightgray")
        self.slider.set(slider_start)
        self.slider.bind("<ButtonRelease-1>", self.sendToPraat)
        self.slider.grid(row=1, column=0)
        self.updateWidgets()
        # Next Button
        self.next_button = tk.Button(self, text="Volgende", bg="darkgray", command=self.nextTrial)
        self.next_button.grid(row=2, column=0)

    def sendToPraat(self, event):
        self.slider.unbind("<ButtonRelease-1>")
        self.slider.config(state="disabled")
        self.next_button.config(state="disabled")
        self.new_value = float(self.slider.get())
        self.slider_prop = self.new_value / self.slider_range
        self.erb_shift = self.min_erb + (self.erb_shift_range * self.slider_prop)
        print("Slider pos: " + str(self.new_value) + "\nERB shift: " + str(self.erb_shift))
        subprocess.call([praat_path, "--run", script_path + "playStimuli.praat", stimulus_list[self.current_stim], "c_b_a", str(self.erb_shift)])
        self.num_adjustments += 1
        self.after(500, self.bindSlider)

    def bindSlider(self):
        self.slider.bind("<ButtonRelease-1>", self.sendToPraat)
        self.slider.config(state="normal")
        self.next_button.config(state="normal")

    def updateWidgets(self):
        # Update text
        self.current_stim_text.config(state="normal")
        self.current_stim_text.delete(1.0, "end")
        self.current_stim_text.insert("end", "Versleep de schuif zodat het verschil tussen de eerste en tweede versie van " + stimulus_list[self.current_stim] + " even groot is als het verschil tussen de tweede en derde versie.")
        self.tag_end = "1." + str(76 + len(stimulus_list[self.current_stim]))
        self.current_stim_text.tag_add("red", "1.76", self.tag_end)
        self.current_stim_text.tag_configure("red", foreground="red")
        self.current_stim_text.tag_add("center", 1.0, "end")
        self.current_stim_text.tag_configure("center", justify='center')
        self.current_stim_text.config(state="disabled")
        # Update slider range
        self.max_erb = max_shift_list[self.current_stim]
        self.min_erb = 0.8
        self.erb_shift_range = self.max_erb - self.min_erb
        self.slider_range = self.erb_shift_range * slider_resolution
        self.slider.config(to=self.slider_range)

    def writeInput(self):
        g.write(str(self.current_stim + 1) + "," + stimulus_list[self.current_stim] + "," + str(self.erb_shift) + "," + str(self.num_adjustments) + "\n")

    def nextTrial(self, event=None):
        self.slider.set(slider_start)
        self.writeInput()
        self.num_adjustments = 0
        if self.current_stim >= (len(stimulus_list) - 1):
            app.destroy()
        else:
            self.current_stim += 1
            self.updateWidgets()
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
    max_erb_list = []
    counter = 0
    for line in f:
        counter += 1
        if counter == 1:
            continue
        else:
            line_list = line[:-1].split(",")
            stim_list.append(line_list[0])
            max_erb_list.append(float(line_list[1]))
    f.close()
    return stim_list, max_erb_list, callbackPP.pp_num


infoLoop()
stimulus_list, max_shift_list, pp = loadLists()
g = open("./logs/" + str(pp) + "_results.csv", "w")
g.write("trial,stimulus,erb_shift,num_adjustments\n")

app = Experiment()
app.mainloop()
g.close()
