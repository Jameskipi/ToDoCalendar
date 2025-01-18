import tkinter as tk
import os
import json


class StartingApp(tk.Tk):
    def fullscreen(self):
        if self.attributes("-fullscreen"):
            self.overrideredirect(True)
            self.attributes('-fullscreen', False)
            self.menu_frame.config(width=self.window_width, height=30, bg="green")
            self.main_frame.config(width=self.window_width, height=470)
            return

        self.overrideredirect(False)
        self.attributes('-fullscreen', True)
        self.menu_frame.config(width=self.screen_width, height=30, bg="dark slate gray")
        self.main_frame.config(width=self.screen_width, height=self.screen_height)
        return

    def anchor(self):
        if self.overrideredirect():
            self.overrideredirect(False)
            return

        self.overrideredirect(True)

        self.x_coordinate = self.winfo_x() + 8
        self.y_coordinate = self.winfo_y() + 32

        self.save_position()

        self.geometry(
            "{}x{}+{}+{}".format(self.window_width, self.window_height, self.x_coordinate, self.y_coordinate))
        return

    def save_position(self):
        # Save current position to json file

        config = {
            "x": self.x_coordinate,
            "y": self.y_coordinate
        }

        with open("config.json", mode="w", encoding="utf-8") as file:
            json.dump(config, file)

    def read_position(self):
        if not os.path.exists("config.json"):
            print("Creating new config file")

            config = {
                "x": self.x_coordinate,
                "y": self.y_coordinate
            }

            with open("config.json", mode="w", encoding="utf-8") as file:
                json.dump(config, file)

        # Read coordinates from json file
        with open("config.json", mode="r", encoding="utf-8") as file:
            config = json.load(file)

        print(config)
        self.x_coordinate = config["x"]
        self.y_coordinate = config["y"]
        self.geometry(
            "{}x{}+{}+{}".format(self.window_width, self.window_height, self.x_coordinate, self.y_coordinate))

    def __init__(self):
        super().__init__()

        # Initial
        self.title("To Do")
        self.resizable(False, False)
        self.lift()
        self.protocol("WM_DELETE_WINDOW", exit)
        self.overrideredirect(True)
        self.wm_attributes("-transparentcolor", "green")

        self.window_width = 500
        self.window_height = 500
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.x_coordinate = int((self.screen_width / 2) - (self.window_width / 2))
        self.y_coordinate = int((self.screen_height / 2) - (self.window_height / 2))

        self.read_position()

        # Menu frame
        self.menu_frame = tk.Frame(self, name="exit_frame", bg="green", width=self.window_width, height=30)
        self.menu_frame.config(highlightthickness=2, highlightbackground="black")
        self.menu_frame.grid(row=0, column=0)
        self.menu_frame.pack_propagate(False)

        self.anchor_button = tk.Button(self.menu_frame, name="exit_button", text="X", font=("Arial", 13, "bold"),
                                       bg="black", fg="white")
        self.anchor_button.config(command=self.destroy, width=2)
        self.anchor_button.pack(side=tk.RIGHT, anchor=tk.NE)

        self.fullscreen_button = tk.Button(self.menu_frame, name="fullscreen_button", text="🗖", font=13,
                                           bg="black", fg="white")
        self.fullscreen_button.config(command=self.fullscreen, width=2)
        self.fullscreen_button.pack(side=tk.RIGHT, anchor=tk.NE, padx=(5, 5))

        self.anchor_button = tk.Button(self.menu_frame, name="anchor_button", text="⇔", font=("Arial", 13, "bold"),
                                       bg="black", fg="white")
        self.anchor_button.config(command=self.anchor, width=2)
        self.anchor_button.pack(side=tk.RIGHT, anchor=tk.NE)

        # Main frame
        self.main_frame = tk.Frame(self, name="main_frame", bg="green", width=self.window_width, height=470)
        self.main_frame.config(highlightthickness=2, highlightbackground="black")
        self.main_frame.grid(row=1, column=0)
        self.main_frame.pack_propagate(False)


if __name__ == "__main__":
    startapp = StartingApp()
    startapp.mainloop()
