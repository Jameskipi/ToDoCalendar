import tkinter as tk
import os
import json
import AppLogs


class AddApp(tk.Toplevel):
    def exit(self):
        self.data_button.configure(bg="black", fg="white")
        self.master.update_days()
        self.destroy()

    def priority_changed(self, *args):
        selected = self.priority.get()

        if selected == "RED":
            self.priority_menu.configure(bg="red")
        elif selected == "GRAY":
            self.priority_menu.configure(bg="gray")

    def __init__(self, data):
        super().__init__()

        self.data = data
        self.date = data[0]
        self.data_button = data[1]
        self.data_button.configure(bg="light gray", fg="black")

        # Initial
        self.title("To Do")
        self.resizable(False, False)
        self.overrideredirect(True)
        self.wm_attributes("-transparentcolor", "green")
        self.lift()
        self.attributes("-topmost", True)

        self.window_width = 600
        self.window_height = 50
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_coordinate = int((screen_width / 2) - (self.window_width / 2))
        y_coordinate = int((screen_height / 2) - (self.window_height / 2))
        self.geometry("{}x{}+{}+{}".format(self.window_width, self.window_height, x_coordinate, y_coordinate))

        # Input text frame
        self.input_frame = tk.Frame(self, name="input_frame", bg="#a4dade", width=500, height=self.window_height)
        self.input_frame.grid(row=0, column=1)
        self.input_frame.pack_propagate(False)
        self.input_frame.configure(highlightthickness=3, highlightbackground="black")

        # Info label
        eu_date = self.date.split("-")
        if int(eu_date[1]) < 10:
            eu_date[1] = "0" + eu_date[1]
        if int(eu_date[2]) < 10:
            eu_date[2] = "0" + eu_date[2]

        eu_date = f"{eu_date[2]}.{eu_date[1]}.{eu_date[0]}"

        self.info_label = tk.Label(self.input_frame, name="info_label", bg="#4fb7bf", width=10, text=eu_date,
                                   font=("Arial", 10, "bold"))
        self.info_label.config(highlightthickness=2, highlightbackground="black")
        self.info_label.pack(pady=5, padx=10, side=tk.LEFT)

        # Input text
        self.input_entry = tk.Entry(self.input_frame, font=("Arial", 10, "bold"))
        self.input_entry.configure(width=40)
        self.input_entry.pack(pady=5, side=tk.LEFT)
        self.input_entry.focus_force()
        self.input_entry.bind("<Return>", self.confirm)

        # Priority menu
        self.priority = tk.StringVar(self, value="GRAY")
        self.priority.trace("w", self.priority_changed)

        self.priority_menu = tk.OptionMenu(self.input_frame, self.priority, "RED", "GRAY")
        self.priority_menu.configure(font=("Arial", 8, "bold"), bg="gray", highlightbackground="black")
        self.priority_menu.pack(pady=5, padx=10, side=tk.LEFT)

        # Confirm button
        self.confirm_frame = tk.Frame(self, name="confirm_frame", bg="green", width=50, height=self.window_height)
        self.confirm_frame.config(highlightthickness=2, highlightbackground="black")
        self.confirm_frame.grid(row=0, column=2)
        self.confirm_frame.pack_propagate(False)
        self.confirm_button = tk.Button(self.confirm_frame, name="exit_button", text="+", font=("Arial", 13, "bold"),
                                        bg="black", fg="white")
        self.confirm_button.config(command=lambda: self.confirm(self.event_generate("<<Foo>>")), width=50,
                                   height=self.window_height)
        self.confirm_button.pack()

        # Exit button
        self.exit_frame = tk.Frame(self, name="exit_frame", bg="green", width=50, height=self.window_height)
        self.exit_frame.config(highlightthickness=2, highlightbackground="black")
        self.exit_frame.grid(row=0, column=3)
        self.exit_frame.pack_propagate(False)
        self.exit_button = tk.Button(self.exit_frame, name="exit_button", text="X", font=("Arial", 13, "bold"),
                                     bg="black", fg="white")
        self.exit_button.config(command=self.exit, width=50, height=self.window_height)
        self.exit_button.pack()

    def confirm(self, e):
        text = self.input_entry.get()

        if text == "":
            return

        data = {
            "date": self.date,
            "button": self.data_button.winfo_name(),
            "text": text,
            "priority": self.priority.get()
        }

        year_month = self.date.split("-")
        year_month = f"{year_month[0]}-{year_month[1]}"

        path = f"data/{year_month}.json"

        if not os.path.isfile(path):
            with open(path, mode="w", encoding="utf-8") as file:
                json.dump([], file)

        with open(path, mode='r', encoding='utf-8') as feedsjson:
            feeds = json.load(feedsjson)

        with open(path, mode="w", encoding="utf-8") as file:
            feeds.append(data)
            json.dump(feeds, file)

        AppLogs.warning(f'Added new event: {data}')

        self.exit()