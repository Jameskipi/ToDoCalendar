import tkinter as tk


class StartingApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Initial
        self.title("To Do")
        self.resizable(False, False)
        self.lift()
        self.attributes("-topmost", True)
        self.protocol("WM_DELETE_WINDOW", exit)
        self.overrideredirect(True)
        self.wm_attributes("-transparentcolor", "green")

        self.window_width = 500
        self.window_height = 500
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (self.window_width / 2))
        y_coordinate = int((screen_height / 2) - (self.window_height / 2))
        self.geometry("{}x{}+{}+{}".format(self.window_width, self.window_height, x_coordinate, y_coordinate))

        # Menu frame
        self.menu_frame = tk.Frame(self, name="exit_frame", bg="green", width=500, height=30)
        self.menu_frame.config(highlightthickness=2, highlightbackground="black")
        self.menu_frame.grid(row=0, column=0)
        self.menu_frame.pack_propagate(False)

        self.exit_button = tk.Button(self.menu_frame, name="exit_button", text="X", font=("Arial", 13, "bold"),
                                     bg="black", fg="white")
        self.exit_button.config(command=self.destroy, width=2)
        self.exit_button.pack(side=tk.RIGHT)

        self.fullscreen_button = tk.Button(self.menu_frame, name="fullscreen_button", text="🗖", font=13,
                                           bg="black", fg="white")
        self.fullscreen_button.config(command=self.destroy, width=2)
        self.fullscreen_button.pack(side=tk.RIGHT, padx=(5, 5))


if __name__ == "__main__":
    startapp = StartingApp()
    startapp.mainloop()
