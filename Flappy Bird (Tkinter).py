import tkinter as tk
import random as rnd

class Gameplay:
    def __init__(self, root):
        self.root = root
        self.root.title("Flappy Bird")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=1400, height=700, bg="#43a1db", highlightthickness=0)
        self.canvas.pack()

        self.root.bind("<space>", self.fly_space)

        self.sky = None
        self.ground = None
        self.bird = None
        self.bird_y = 300
        self.bird_velocity = 0
        self.pipes = []
        self.score = 0
        self.game_running = False
        self.game_over_flag = False

        self.menu_screen()

    def fly_space(self, event):
        if self.game_over_flag:
            self.start_game()
        elif not self.game_running:
            self.start_game()
        else:
            self.bird_velocity = -7.5

    def menu_screen(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 700 - 50, 1400, 700, fill="lightblue", tags="ground")
        self.canvas.create_text(1400 // 2, 700 // 4, text="FLAPPY BIRD", font=("Arial", 30, "bold"), fill="black")
        self.canvas.create_text(1400 // 2, 700 // 3, text="by Izzy", font=("Arial", 24, "bold"), fill="black")
        self.canvas.create_text(1400 // 2, 700 // 2, text="Press SPACE to Start", font=("Arial", 14), fill="black")

    def start_game(self):
        self.canvas.delete("all")
        self.score = 0
        self.bird_y = 300
        self.bird_velocity = 0
        self.pipes = []
        self.game_running = True
        self.game_over_flag = False

        self.sky = self.canvas.create_rectangle(0, 0, 1400, 600, fill="#43a1db", tags="ground", outline="")
        self.ground = self.canvas.create_rectangle(0, 600, 1400, 700, fill="darkgreen", tags="ground", outline="")
        self.bird = self.canvas.create_oval(300, self.bird_y, 350, self.bird_y + 50, fill="yellow", outline="black", width=2)
        self.score_text = self.canvas.create_text(1400 // 2, 50, text="0", font=("Arial", 28, "bold"), fill="white")

        self.update_game()
        self.spawn_pipes()

    def spawn_pipes(self):
        if not self.game_running:
            return

        height = rnd.randint(100, 500)
        pillar_up = self.canvas.create_rectangle (1400, 0, 1400+100, height, fill="#2CA52C", outline="black", width=2)
        pillar_down = self.canvas.create_rectangle(1400, height+150, 1400+100, 700, fill="#2CA52C", outline="black", width=2)

        self.pipes.append({"top": pillar_up, "bottom": pillar_down, "passed": False})
        self.root.after(2500, self.spawn_pipes)

    def update_game(self):
        if not self.game_running:
            return
        self.bird_velocity += 0.5
        self.bird_y += self.bird_velocity

        self.canvas.moveto(self.bird, 300, int(self.bird_y))

        bird_loc = self.canvas.coords(self.bird)
        #x1 y1 x2 y2
        # 0  1  2  3

        remove_pipes = []
        for pipe in self.pipes:
            self.canvas.move(pipe["top"], -3, 0)
            self.canvas.move(pipe["bottom"], -3, 0)

            pipe_loc = self.canvas.coords(pipe["top"])
            #x1 y1 x2 y2
            # 0  1  2  3

            if not pipe["passed"] and pipe_loc[2] < bird_loc[0]:
                pipe["passed"] = True
                self.score += 1
                self.canvas.itemconfig(self.score_text, text=str(self.score))

            if pipe_loc[2] < 0:
                remove_pipes.append(pipe)

        for pipe in remove_pipes:
            self.canvas.delete(pipe["top"])
            self.canvas.delete(pipe["bottom"])
            self.pipes.remove(pipe)

        if self.collisions(bird_loc):
            self.gameover()
            return

        self.root.after(16, self.update_game)

    def collisions(self, bird_loc):
        if bird_loc[1] > 700 or bird_loc[1] < 0:
            return True

        overlapping = self.canvas.find_overlapping(bird_loc[0], bird_loc[1], bird_loc[2], bird_loc[3])

        for check in overlapping:
            if check not in (self.bird, self.sky, self.ground):
                return True

        return False

    def gameover(self):
        self.game_running = False
        self.game_over_flag = True
        self.canvas.delete("all")
        self.canvas.create_rectangle(0, 700 - 50, 1400, 700, fill="#ded895", tags="ground")
        self.canvas.create_text(1400 // 2, 700 // 4, text="GAME OVER", font=("Arial", 30, "bold"), fill="red")
        self.canvas.create_text(1400 // 2, 700 // 3, text=f"Final Score: {self.score}", font=("Arial", 18), fill="white")
        self.canvas.create_text(1400 // 2, 700 // 2, text="Press SPACE to Play Again", font=("Arial", 12), fill="white")

if __name__ == "__main__":
    mainmenu = tk.Tk()
    game = Gameplay(mainmenu)
    mainmenu.mainloop()
