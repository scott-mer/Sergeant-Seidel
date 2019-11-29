### INTERNAL LIBRARIES ###
import tkinter as tk
import shelve
from random import seed
from random import randint
from datetime import datetime
from itertools import chain 

### EXTERNAL LIBRARIES ###
from PIL import ImageTk,Image
import numpy as np
import matplotlib.pyplot as plt

class Main:
    def __init__(self, master):
        """
        Runs when application is initialized
        """
        print("intializing...")
        ### INITIAL SETUP ###
        self.master = master
        master.title("Sergeant Seidel")
        self.frame = tk.Frame(self.master)

        ### GLOBAL VARIABLES ###
        self.level = 1
        self.score = 0
        self.coefs = [0,0,0,0,0,0,0]

        self.splash_widgets = []
        self.main_widgets = []
        self.score_widgets = []

        ### STARTING SPLASH SCREEN ###
        self.starting_splash()
        
        ### PACKS APP ON SCREEN ###
        self.frame.pack()

    #########################################################################################################################################################
    ### GUIS
    #########################################################################################################################################################

    def starting_splash(self, event=None):
        """
        Starting splash screen that runs first when opening the program
        Variable Name = "splash"
        """
        print("starting...")
        ### LABELS ###
        ## label_text_ref
        # 0: Text
        # 1: Font Size
        label_text_ref =    [["Welcome to", 36], 
                            ["SERGEANT SEIDEL", 48], 
                            ["Current High Score:", 18],
                            [str(self.get_high_score()), 12],
                            ["Choose difficulty", 18]]

        self.splash_labels = []
        for i in range(len(label_text_ref)):
            self.splash_labels.append(tk.Label(self.frame, text=label_text_ref[i][0], font=("Comic Sans MS", label_text_ref[i][1])))
            self.splash_labels[i].grid(row=i, column=0, sticky="we")

        current_row = i + 1
        
        ### RADIO BUTTONS ###
        game_modes_ref = ["Easy", "Normal", "Extreme"]

        self.game_mode = tk.StringVar()
        self.game_mode.set("Normal")

        self.splash_radios = []
        for i in range(len(game_modes_ref)):
            self.splash_radios.append(tk.Radiobutton(self.frame, text=game_modes_ref[i], variable=self.game_mode, value=game_modes_ref[i], font=("Comic Sans MS", 12)))
            self.splash_radios[i].grid(row=i + current_row, column=0, sticky="we")
        
        current_row = current_row + i + 1

        ### BUTTONS ###
        self.splash_button = tk.Button(self.frame, text="Play Game", font=("Comic Sans MS", 24), fg="white", bg="dark blue", width=25, command=self.load_game_from_splash)
        self.splash_button.grid(row=current_row, column=0, padx=5, pady=5, sticky="we")

        self.splash_widgets.append(self.splash_labels)
        self.splash_widgets.append(self.splash_radios)
        self.splash_widgets.append([self.splash_button])

    def main(self, event=None):
        """
        GUI for the main game
        Variable Name = "main"
        """
        print("   loading game ui...")

        ### TOP LABEL BAR ###
        top_labels_ref = ["Level: " + str(self.level), "Score: " + str(self.score), "High Score: " + str(self.get_high_score())]

        self.main_top_labels = []
        for i in range(len(top_labels_ref)):
            self.main_top_labels.append(tk.Label(self.frame, text=top_labels_ref[i],font=("Comic Sans MS", 24)))
            self.main_top_labels[i].grid(row=0, column=0 + i*2, columnspan=2, padx=10, pady=10, sticky="we")

        ### BOTTOM LABEL BAR AND SLIDERS ###

        coef_names = ["Tilt (x)", "Tilt (y)", "Defocus", "Astigmatism (y)", "Coma (y)", "Spherical (1st)"]
        
        self.main_bot_sliders = []
        self.main_bot_labels = []        
        for i in range(len(coef_names)):
            self.main_bot_sliders.append(tk.Scale(self.frame, from_=5, to=-5, font=("Comic Sans MS", 12)))
            self.main_bot_labels.append(tk.Label(self.frame, text=coef_names[i], width=12, font=("Comic Sans MS", 12), anchor="center"))
            self.main_bot_sliders[i].grid(row=3, column=0 + i, padx=10, pady=10, sticky="we")
            self.main_bot_labels[i].grid(row=2, column=0 + i, padx=5, pady=5, sticky="we")

        ### GUESS BUTTON ###
        self.main_button = tk.Button(self.frame,text="Make Guess",command=self.check_guess,fg="white",bg="dark blue",width=72)
        self.main_button.config(font=("Comic Sans MS", 18),anchor="center")
        self.main_button.grid(row=4,column=0,columnspan=6,padx=10,pady=10)

        self.main_widgets.append(self.main_top_labels)
        self.main_widgets.append(self.main_bot_sliders)
        self.main_widgets.append(self.main_bot_labels)
        self.main_widgets.append([self.main_button])
        
    def score_board(self, event=None):
        """
        Displays scores
        Variable name = "score"
        """
        print("displaying scoreboard...")

        ### TOP LABEL BAR ###
        top_labels_ref = ["Level: " + str(self.level), "Score: " + str(self.score), "High Score: " + str(self.get_high_score())]

        self.score_top_labels = []
        for i in range(len(top_labels_ref)):
            self.score_top_labels.append(tk.Label(self.frame, text=top_labels_ref[i],font=("Comic Sans MS", 24)))
            self.score_top_labels[i].grid(row=0, column=0 + i*2, columnspan=2, padx=10, pady=10, sticky="we")

        ### HEADING LABEL BAR ###
        heading_label_ref = ["Aberration", "Actual", "User", "Points", "%"]

        self.score_heading_labels = []
        for i in range(len(heading_label_ref)):
            self.score_heading_labels.append(tk.Label(self.frame, text=heading_label_ref[i], font=("Comic Sans MS bold", 20)))
            self.score_heading_labels[i].grid(row=1, column=i+1, columnspan=1, padx=10, pady=10, sticky="we")

        ### SCORE BREAK DOWN ###
        self.score_score_labels = []
        for i in range(len(self.main_bot_sliders)):
            # Aberration Name            
            self.score_score_labels.append([tk.Label(self.frame, text=self.main_bot_labels[i].cget("text"), font=("Comic Sans MS", 20), state=self.main_bot_labels[i].cget("state"))])
            self.score_score_labels[i][0].grid(row=i+2, column=1, columnspan=1, padx=10, pady=10, sticky="we")
            # Actual Value
            self.score_score_labels[i].append(tk.Label(self.frame, text=self.coefs[i+1], font=("Comic Sans MS", 20), state=self.main_bot_labels[i].cget("state")))
            self.score_score_labels[i][1].grid(row=i+2, column=2, columnspan=1, padx=10, pady=10, sticky="we")
            # User Entered Value
            self.score_score_labels[i].append(tk.Label(self.frame, text=self.main_bot_sliders[i].get(), font=("Comic Sans MS", 20), state=self.main_bot_labels[i].cget("state")))
            self.score_score_labels[i][2].grid(row=i+2, column=3, columnspan=1, padx=10, pady=10, sticky="we")
            # Score
            try:
                self.score_score_labels[i].append(tk.Label(self.frame, text=self.individual_scores[i], font=("Comic Sans MS", 20), state=self.main_bot_labels[i].cget("state")))
                self.score_score_labels[i][3].grid(row=i+2, column=4, columnspan=1, padx=10, pady=10, sticky="we")
            except:
                self.score_score_labels[i].append(tk.Label(self.frame, text="0", font=("Comic Sans MS", 20), state=self.main_bot_labels[i].cget("state")))
                self.score_score_labels[i][3].grid(row=i+2, column=4, columnspan=1, padx=10, pady=10, sticky="we") 
            # %
            try:
                percent = (float(self.individual_scores[i])/10)*100
                self.score_score_labels[i].append(tk.Label(self.frame, text="%.2f" % percent, font=("Comic Sans MS", 20), state=self.main_bot_labels[i].cget("state")))
                self.score_score_labels[i][4].grid(row=i+2, column=5, columnspan=1, padx=10, pady=10, sticky="we")
            except:
                self.score_score_labels[i].append(tk.Label(self.frame, text="NA", font=("Comic Sans MS", 20), state=self.main_bot_labels[i].cget("state")))
                self.score_score_labels[i][4].grid(row=i+2, column=5, columnspan=1, padx=10, pady=10, sticky="we") 
        
        current_row = i + 3

        ### TOTALS ###
        round_percent = (self.round_score/self.possible_score)*100
        score_totals_ref = ["Total", "", "", "", "%.2f" % round_percent]

        self.score_total_labels = []
        for i in range(len(score_totals_ref)):
            self.score_total_labels.append(tk.Label(self.frame, text=score_totals_ref[i], font=("Comic Sans MS bold", 20)))
            self.score_total_labels[i].grid(row=current_row, column=i+1, columnspan=1, padx=10, pady=10, sticky="we")

        ### BUTTON ###
        if self.level < 10:
            self.score_button = tk.Button(self.frame, text="Next Level", font=("Comic Sans MS", 24), fg="white", bg="dark blue", width=25, command=self.next_level)
            self.score_button.grid(row=current_row + 1, column=0, columnspan=6, padx=5, pady=5, sticky="we")
        else:
            self.score_button = tk.Button(self.frame, text="Finish Game", font=("Comic Sans MS", 24), fg="white", bg="dark blue", width=25, command=self.end_game)
            self.score_button.grid(row=current_row + 1, column=1, columnspan=6, padx=5, pady=5, sticky="we")

        self.score_widgets.append(self.score_top_labels)
        self.score_widgets.append(self.score_heading_labels)
        self.score_widgets.append(list(chain.from_iterable(self.score_score_labels)))
        self.score_widgets.append(self.score_total_labels)
        self.score_widgets.append([self.score_button])

    #########################################################################################################################################################
    ### GAME LOGIC
    #########################################################################################################################################################

    def game(self, event=None):
        """
        Where the main game architecture lives
        """
        print("   building game environment...")

        # Load the main ui
        self.main()

        print("Game UI loaded.")

        self.begin_level()

    def begin_level(self, event=None):
        """
        Used to set settings for the level, game logic
        """
        print("starting level " + str(self.level) + "...")
        
        ### GAME LOGIC ###

        game_mode_string = self.game_mode.get()

        if game_mode_string == "Easy":
            print("easy mode...")
            if self.level < 6:
                # Levels 1-5: Tilt
                for i in range(len(self.main_bot_sliders)):
                    if i < 2:
                        self.main_bot_sliders[i].config(state="normal")
                        self.main_bot_labels[i].config(state="normal")
                    else:
                        self.main_bot_sliders[i].config(state="disabled")
                        self.main_bot_labels[i].config(state="disabled")
            elif self.level >= 6 and self.level < 11:
                # Levels 6-10: Tilt, Defocus
                for i in range(len(self.main_bot_sliders)):
                    if i < 3:
                        self.main_bot_sliders[i].config(state="normal")
                        self.main_bot_labels[i].config(state="normal")
                    else:
                        self.main_bot_sliders[i].config(state="disabled")
                        self.main_bot_labels[i].config(state="disabled")
        elif game_mode_string == "Normal":
            print("normal mode...")
            if self.level < 3:
                #Levels 1-2: Tilt, Defocus
                for i in range(len(self.main_bot_sliders)):
                    if i < 3:
                        self.main_bot_sliders[i].config(state="normal")
                        self.main_bot_labels[i].config(state="normal")
                    else:
                        self.main_bot_sliders[i].config(state="disabled")
                        self.main_bot_labels[i].config(state="disabled")
            elif self.level >=3 and self.level < 5:
                #Levels 3-4: Tilt, Astig
                for i in range(len(self.main_bot_sliders)):
                    if i < 2 or i == 3:
                        self.main_bot_sliders[i].config(state="normal")
                        self.main_bot_labels[i].config(state="normal")
                    else:
                        self.main_bot_sliders[i].config(state="disabled")
                        self.main_bot_labels[i].config(state="disabled")
            elif self.level >=5 and self.level < 7:
                #Levels 6-7: Tilt, Coma
                for i in range(len(self.main_bot_sliders)):
                    if i < 2 or i == 4:
                        self.main_bot_sliders[i].config(state="normal")
                        self.main_bot_labels[i].config(state="normal")
                    else:
                        self.main_bot_sliders[i].config(state="disabled")
                        self.main_bot_labels[i].config(state="disabled")
            elif self.level >=7 and self.level < 9:
                #Levels 7-8: Tilt, Spherical
                for i in range(len(self.main_bot_sliders)):
                    if i < 2 or i == 5:
                        self.main_bot_sliders[i].config(state="normal")
                        self.main_bot_labels[i].config(state="normal")
                    else:
                        self.main_bot_sliders[i].config(state="disabled")
                        self.main_bot_labels[i].config(state="disabled")
            elif self.level == 9:
                #Level 9: Tilt, Defocus, Astig
                for i in range(len(self.main_bot_sliders)):
                    if i < 3 or i == 3:
                        self.main_bot_sliders[i].config(state="normal")
                        self.main_bot_labels[i].config(state="normal")
                    else:
                        self.main_bot_sliders[i].config(state="disabled")
                        self.main_bot_labels[i].config(state="disabled") 
            elif self.level == 10:
                #Level 10: Tilt, Defocus, Coma
                for i in range(len(self.main_bot_sliders)):
                    if i < 3 or i == 3:
                        self.main_bot_sliders[i].config(state="normal")
                        self.main_bot_labels[i].config(state="normal")
                    else:
                        self.main_bot_sliders[i].config(state="disabled")
                        self.main_bot_labels[i].config(state="disabled")            
        elif game_mode_string == "Extreme":
            print("extreme mode...")
            if self.level == 1:
                #Level 1: Tilt, Defocus
                for i in range(len(self.main_bot_sliders)):
                    if i < 3:
                        self.main_bot_sliders[i].config(state="normal")
                        self.main_bot_labels[i].config(state="normal")
                    else:
                        self.main_bot_sliders[i].config(state="disabled")
                        self.main_bot_labels[i].config(state="disabled") 
            elif self.level == 2:
                #Level 2: Tilt, Defocus, Astig
                for i in range(len(self.main_bot_sliders)):
                    if i < 3 or i == 3:
                        self.main_bot_sliders[i].config(state="normal")
                        self.main_bot_labels[i].config(state="normal")
                    else:
                        self.main_bot_sliders[i].config(state="disabled")
                        self.main_bot_labels[i].config(state="disabled") 
            elif self.level == 3:
                #Level 3: Tilt, Defocus, Coma
                for i in range(len(self.main_bot_sliders)):
                    if i < 3 or i == 4:
                        self.main_bot_sliders[i].config(state="normal")
                        self.main_bot_labels[i].config(state="normal")
                    else:
                        self.main_bot_sliders[i].config(state="disabled")
                        self.main_bot_labels[i].config(state="disabled")
            elif self.level == 4:
                #Level 4: Tilt, Defocus, Spherical
                for i in range(len(self.main_bot_sliders)):
                    if i < 3 or i == 5:
                        self.main_bot_sliders[i].config(state="normal")
                        self.main_bot_labels[i].config(state="normal")
                    else:
                        self.main_bot_sliders[i].config(state="disabled")
                        self.main_bot_labels[i].config(state="disabled")
            elif self.level == 5:
                #Level 5: Tilt, Astig, Coma
                for i in range(len(self.main_bot_sliders)):
                    if i < 2 or i == 3 or i == 4:
                        self.main_bot_sliders[i].config(state="normal")
                        self.main_bot_labels[i].config(state="normal")
                    else:
                        self.main_bot_sliders[i].config(state="disabled")
                        self.main_bot_labels[i].config(state="disabled")
            elif self.level == 6:
                #Level 6: Tilt, Astig, Spherical
                for i in range(len(self.main_bot_sliders)):
                    if i < 2 or i == 3 or i == 5:
                        self.main_bot_sliders[i].config(state="normal")
                        self.main_bot_labels[i].config(state="normal")
                    else:
                        self.main_bot_sliders[i].config(state="disabled")
                        self.main_bot_labels[i].config(state="disabled")
            elif self.level == 7:
                #Level 7: Tilt, Coma, Spherical
                for i in range(len(self.main_bot_sliders)):
                    if i < 2 or i == 4 or i == 5:
                        self.main_bot_sliders[i].config(state="normal")
                        self.main_bot_labels[i].config(state="normal")
                    else:
                        self.main_bot_sliders[i].config(state="disabled")
                        self.main_bot_labels[i].config(state="disabled")
            elif self.level == 8:
                #Level 8: Tilt, Astig, Coma, Spherical
                for i in range(len(self.main_bot_sliders)):
                    if i < 2 or i == 3 or i == 4 or i == 5:
                        self.main_bot_sliders[i].config(state="normal")
                        self.main_bot_labels[i].config(state="normal")
                    else:
                        self.main_bot_sliders[i].config(state="disabled")
                        self.main_bot_labels[i].config(state="disabled")
            elif self.level == 9:
                #Level 9: Tilt, Defocus, Astig, Coma, Spherical
                for i in range(len(self.main_bot_sliders)):
                    self.main_bot_sliders[i].config(state="normal")
                    self.main_bot_labels[i].config(state="normal")
            elif self.level == 10:
                #Level 10: Tilt, Defocus, Astig, Coma, Spherical
                for i in range(len(self.main_bot_sliders)):
                    self.main_bot_sliders[i].config(state="normal")
                    self.main_bot_labels[i].config(state="normal")
    
        self.random_coefs()
        self.interferogram(self.coefs[0],self.coefs[1],self.coefs[2],self.coefs[3],self.coefs[4],self.coefs[5],self.coefs[6])
        self.draw_image()

        self.main_widgets.append([self.img_canvas])

    def next_level(self, event=None):
        """
        Increments game to next level
        """
        print("leveling up...")
        self.level = self.level + 1
        self.load_game_from_score()

    def end_game(self, event=None):
        """
        Ends the game, sends it back to the splash screen
        """
        print("ending game...")

        self.check_high_score()
        
        self.level = 1
        self.score = 0
        self.coefs = [0,0,0,0,0,0,0]

        self.load_splash_from_score()

    #########################################################################################################################################################
    ### UTILITIES
    #########################################################################################################################################################

    def get_high_score(self, event=None):
        """
        Gets the high score
        """
        f = shelve.open("hs.txt")
        high_score = f['hs']

        return high_score

    def load_game_from_splash(self, event=None):
        """
        Loads the game when coming from the splash screen
        """
        print("loading game...")
        for i in range(len(self.splash_widgets)):
            for j in range(len(self.splash_widgets[i])):
                self.splash_widgets[i][j].grid_forget()
        
        # Loads the game
        self.game()

    def set_high_score(self, hs):
        """
        Sets the high score
        """
        f = shelve.open('hs.txt')  
        f['hs'] = hs             
        f.close()

    def random_coefs(self,event=None):
        """
        Makes random coeffecients for interferogram
        """
        seed(datetime.now())

        self.coefs = [0,0,0,0,0,0,0]

        for i in range(len(self.main_bot_sliders)):
            if self.main_bot_sliders[i].cget("state") == "normal":
                self.coefs[i+1] = randint(-5,5)
            else:
                self.coefs[i+1] = 0

    def makecircle(self, a, r, PR):
        """
        Makes the interferogram into a circle.
        """
        max = a.max()
        size = np.sqrt(a.size)
        for i in range(int(size)):
            for j in range(int(size)):
                if np.sqrt(r[i]**2+r[j]**2) > PR:
                    a[i,j] = max

    def interferogram(self, A, B, C, D, E, F, G, wl = 632*(1e-9), pr = 1):
        """
        Outputs Twyman Green Interferogram based on Seidel aberration as image
        
        user inputs:

        A: Constant(piston)term

        B: Tilt about the y axis

        C: Tilt about the x axis

        D: Reference sphere change, also called defocus

        E: Sagittal astigmatism along the y axis

        F: Sagittal coma along the y axis

        G: Primary spherical aberration

        default inputs:

        wl: wavelength in nanometer, default = 632nm

        pr: pupil radius, default = 1
        """
        print("   drawing interferogram...")

        r = np.linspace(-pr,pr,500)
        x,y = np.meshgrid(r,r)
        wavemap = lambda n: n*wl*2/pr 
        [A,B,C,D,E,F,G] = map(wavemap,[A,B,C,D,E,F,G])
        OPD = A + B*x + C*y + D*(x**2 + y**2) + E*(y**2) + F*y*(x**2 + y**2) + G*(x**2 + y**2)**2

        ph = np.pi/wl*OPD
        I1 = 1
        I2 = I1
        Ixy = I1 + I2 + 2 * np.sqrt(I1*I2) * np.cos(ph)
        self.makecircle(Ixy,r,pr)

        fig = plt.figure(figsize=(9, 9))
        plt.imshow(-Ixy, extent=[-pr,pr,-pr,pr])
        plt.set_cmap('Greys')

        plt.savefig('image.png')

        print("   Interferogram complete.")

    def draw_image(self,event=None):
        self.img_canvas = tk.Canvas(self.frame, width = 500, height = 500)  
        self.img_canvas.grid(row=1,column=0,columnspan=6,padx=10,pady=10)
        self.img = Image.open("image.png")
        self.img = self.img.resize((500, 500), Image.ANTIALIAS)
        self.display = ImageTk.PhotoImage(self.img)  
        self.img_canvas.create_image(0,0,anchor="nw",image=self.display)

    def check_guess(self, event=None):
        """
        Checks the user guess with the actual coefs
        """
        print("checking guess...")
        self.individual_scores = []
        self.round_score = 0
        self.possible_score = 0
        for i in range(len(self.main_bot_sliders)):
            if self.main_bot_sliders[i].cget("state") == "normal":
                score = 10 - np.abs(self.coefs[i + 1] - self.main_bot_sliders[i].get())
                self.individual_scores.append(score)
                self.round_score = self.round_score + score
                self.possible_score = self.possible_score + 10
                self.score = self.score + score
            else:
                self.individual_scores.append(0)
        
        self.load_score_from_game()
    
    def load_score_from_game(self, event=None):
        """
        Loads the scorecard when coming from the game
        """
        print("loading score card...")
        for i in range(len(self.main_widgets)):
            for j in range(len(self.main_widgets[i])):
                self.main_widgets[i][j].grid_forget()
        
        # Loads the score board
        self.score_board()

    def load_game_from_score(self, event=None):
        """
        Loads the game coming from the score card
        """
        print("loading game...")
        for i in range(len(self.score_widgets)):
            for j in range(len(self.score_widgets[i])):
                self.score_widgets[i][j].grid_forget()

        # Loads the game
        self.game()

    def check_high_score(self, event=None):
        """
        Checks if the user got a high score
        """
        if self.score > self.get_high_score():
            self.set_high_score(self.score)
    
    def load_splash_from_score(self, event=None):
        """
        Loads the splash screen from the scorecard
        """
        print("loading game...")
        for i in range(len(self.score_widgets)):
            for j in range(len(self.score_widgets[i])):
                self.score_widgets[i][j].grid_forget()

        # Loads the splash
        self.starting_splash()

def main(): 
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == '__main__':
    main()