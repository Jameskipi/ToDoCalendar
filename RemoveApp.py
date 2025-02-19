import tkinter as tk
import json
import os
import AppLogs


class RemoveApp(tk.Toplevel):
    def exit(self):
        self.data_button.configure(bg="black", fg="white")
        self.master.update_days()
        self.destroy()

    def event_changed(self, *args):
        selected = self.selected_event.get()

        if selected == "Remove All":
            self.event_menu.configure(bg="red")
        else:
            self.event_menu.configure(bg="gray")

    def confirm(self, e):
        if self.selected_event.get() == "Select":
            # Nothing was selected
            return

        elif self.selected_event.get() == "Remove All":
            # Remove everything 5 times because of weird bug
            for i in range(5):
                for event in self.jsonfile:
                    if event['date'] == self.date:
                        AppLogs.warning(f'Removed event: {event}')
                        self.jsonfile.remove(event)

        else:
            # One event was selected
            text = self.selected_event.get().split(".")[1][1:]

            for event in self.jsonfile:
                if event['text'] == text:
                    AppLogs.warning(f'Removed event: {event}')
                    self.jsonfile.remove(event)

        # Save updated jsonfile
        with open(self.jsonpath, mode="w", encoding="utf-8") as file:
            json.dump(self.jsonfile, file)

        # Remove file if empty
        if not self.jsonfile:
            os.remove(self.jsonpath)

        self.exit()

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
        self.input_frame = tk.Frame(self, name="input_frame", bg="#353935", width=500, height=self.window_height)
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

        self.info_label = tk.Label(self.input_frame, name="info_label", bg="#160D08", fg="white", width=10,
                                   text=eu_date, font=("Arial", 10, "bold"))
        self.info_label.config(highlightthickness=2, highlightbackground="black")
        self.info_label.pack(pady=5, padx=10, side=tk.LEFT)

        # Events menu
        self.selected_event = tk.StringVar(self, value="Select")
        self.selected_event.trace("w", self.event_changed)

        year_month = self.date.split("-")
        year_month = f"{year_month[0]}-{year_month[1]}"
        self.jsonpath = f"data/{year_month}.json"

        with open(self.jsonpath, mode='r', encoding='utf-8') as jsonfile:
            self.jsonfile = json.load(jsonfile)

        self.options_list = []
        i = 1
        for event in self.jsonfile:
            if event['date'] == f"{year_month}-{self.data_button['text']}":
                self.options_list.append(f"{i}. {event['text']}")
                i = i + 1
        self.options_list.append("Remove All")

        self.event_menu = tk.OptionMenu(self.input_frame, self.selected_event, *self.options_list)
        self.event_menu.configure(font=("Arial", 8, "bold"), bg="gray", highlightbackground="black")
        self.event_menu.pack(pady=5, padx=10, side=tk.RIGHT, expand=True)

        # Confirm button
        self.confirm_frame = tk.Frame(self, name="confirm_frame", bg="green", width=50, height=self.window_height)
        self.confirm_frame.config(highlightthickness=2, highlightbackground="black")
        self.confirm_frame.grid(row=0, column=2)
        self.confirm_frame.pack_propagate(False)
        self.confirm_button = tk.Button(self.confirm_frame, name="exit_button", text="-", font=("Arial", 20, "bold"),
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
