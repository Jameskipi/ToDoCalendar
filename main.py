import tkinter as tk
import os
import json


class StartingApp(tk.Tk):
    def fullscreen(self):
        if self.attributes("-fullscreen"):
            self.overrideredirect(True)
            self.attributes('-fullscreen', False)
            self.anchor_button['state'] = "normal"

            self.menu_frame.config(width=self.window_width, height=30, bg="green")
            self.main_frame.config(width=self.window_width, height=470)
            return

        self.overrideredirect(False)
        self.attributes('-fullscreen', True)
        self.anchor_button['state'] = "disabled"

        self.menu_frame.config(width=self.screen_width, height=30, bg="dark slate gray")
        self.main_frame.config(width=self.screen_width, height=self.screen_height)
        return

    def anchor(self):
        if self.overrideredirect():
            self.x_coordinate = self.winfo_x() - 8
            self.y_coordinate = self.winfo_y() - 32

            self.geometry(
                "{}x{}+{}+{}".format(self.window_width, self.window_height, self.x_coordinate, self.y_coordinate))

            self.overrideredirect(False)
            self.bind('<Leave>', self.lower_window)
            return

        self.overrideredirect(True)
        self.unbind('<Leave>')

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

    def lower_window(self, event):
        self.lower()

    def __init__(self):
        super().__init__()

        # Initial
        self.title("To Do")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", exit)
        self.overrideredirect(True)
        self.wm_attributes("-transparentcolor", "green")
        # self.bind('<Leave>', self.lower_window)

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

        self.exit_button = tk.Button(self.menu_frame, name="exit_button", text="X", font=("Arial", 13, "bold"),
                                     bg="black", fg="white")
        self.exit_button.config(command=self.destroy, width=2)
        self.exit_button.pack(side=tk.RIGHT, anchor=tk.NE)

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

        # Blank1 frame
        self.blank1_frame = tk.Frame(self.main_frame, name="blank1_frame", bg="green", width=self.window_width - 4,
                                     height=30)
        self.blank1_frame.grid(row=0, column=0)
        self.blank1_frame.pack_propagate(False)

        # Month frame
        self.month_frame = tk.Frame(self.main_frame, name="month_frame", bg="green", width=self.window_width - 4,
                                     height=50)
        self.month_frame.grid(row=1, column=0)
        self.month_frame.pack_propagate(False)

        self.back_button = tk.Button(self.month_frame, name="back_button", text="<",
                                     font=("Arial", 13, "bold"), bg="black", fg="white")
        self.back_button.config(command=lambda: self.destroy(), width=1, height=2)
        self.back_button.grid(row=0, column=0)

        self.month_label = tk.Label(self.month_frame, name="month_label", text="Styczeń", font=("Arial", 15, "bold"))
        self.month_label.config(bg="black", fg="white", width=15, height=2)
        self.month_label.config(highlightthickness=1, highlightbackground="gray")
        self.month_label.grid(row=0, column=1)

        self.year_label = tk.Label(self.month_frame, name="year_label", text="2025", font=("Arial", 15, "bold"))
        self.year_label.config(bg="black", fg="white", width=5, height=2)
        self.year_label.config(highlightthickness=1, highlightbackground="gray")
        self.year_label.grid(row=0, column=2)

        self.next_button = tk.Button(self.month_frame, name="next_button", text=">",
                                     font=("Arial", 13, "bold"), bg="black", fg="white")
        self.next_button.config(command=lambda: self.destroy(), width=1, height=2)
        self.next_button.grid(row=0, column=3)

        # Blank2 frame
        self.blank2_frame = tk.Frame(self.main_frame, name="blank2_frame", bg="green", width=self.window_width - 4,
                                     height=30)
        self.blank2_frame.grid(row=2, column=0)
        self.blank2_frame.pack_propagate(False)


if __name__ == "__main__":
    startapp = StartingApp()
    startapp.mainloop()
