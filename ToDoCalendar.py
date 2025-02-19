import time
import tkinter as tk
import os
import json
from datetime import date, datetime
from calendar import monthcalendar, monthrange
from threading import Thread
import AppLogs
from StartingApp import StartingApp
from AddApp import AddApp
from RemoveApp import RemoveApp
from Translator import translate_month


class App(tk.Tk):
    def update_midnight(self):
        # Update date on midnight
        while True:
            try:
                self.state()

                if datetime.now().hour == 0 and datetime.now().minute == 0:
                    AppLogs.warning("MIDNIGHT DATE UPDATE")
                    self.update_days()
                    time.sleep(60)
                else:
                    time.sleep(1)

            except RuntimeError:
                break
            except tk.TclError:
                break

    def update_days(self):
        days_raw = monthcalendar(self.year, self.month)
        days = []
        for weeks in days_raw:
            for day in weeks:
                days.append(day)

        # Clear all buttons
        for day_button in self.days_frame.winfo_children():
            day_button.configure(text="")
            day_button['state'] = "normal"
            day_button.configure(bg="black")
            day_button.unbind("<Enter>")
            day_button.unbind("<Leave>")
            day_button.unbind("<Button-3>")

        # Write days to buttons
        empty_days = {}
        for i, day_button in enumerate(self.days_frame.winfo_children()):
            try:
                if days[i] == 0:
                    empty_days.update({i: day_button})
                    day_button['state'] = "disabled"
                    day_button.configure(bg="#28231D")
                    continue
                day_button.configure(text=days[i])
            except IndexError:
                empty_days.update({i: day_button})
                day_button['state'] = "disabled"
                day_button.configure(bg="#28231D")
                continue

        # Write days before current month
        if self.month == 1:
            range_before = monthrange(self.year, 12)
        else:
            range_before = monthrange(self.year, self.month - 1)
        days_before = range_before[1]

        added_days = []
        for i in range(21):
            if i in empty_days.keys():
                added_days.append(days_before - i)
        added_days = added_days[::-1]

        for i in range(len(added_days)):
            empty_days[i].configure(text=added_days[i])

        # Write days after current month
        days_after = 1
        for i in range(21, 42):
            if i in empty_days.keys():
                empty_days[i].configure(text=days_after)
                days_after = days_after + 1

        # Write events
        jsonpath = f"data/{self.year}-{self.month}.json"

        if os.path.isfile(jsonpath):
            with open(jsonpath, mode='r', encoding='utf-8') as file:
                jsonfile = json.load(file)

            for event in jsonfile:
                for button in self.days_frame.winfo_children():
                    if button.winfo_name() == event['button']:
                        button.bind("<Enter>", self.show_events)
                        button.bind("<Leave>", self.hide_events)
                        button.bind("<Button-3>", self.remove_events)

                        if button.cget('bg') != "RED":
                            button.configure(bg=event['priority'])

        # Show current day
        raw_date = str(date.today()).split("-")
        year = int(raw_date[0])
        month = int(raw_date[1])
        day = int(raw_date[2])

        for day_button in self.days_frame.winfo_children():
            if all([int(day_button['text']) == day, self.month == month, self.year == year,
                    day_button['state'] == "normal"]):
                day_button.configure(bg="#007FFF")

    def change_month(self, add_number):
        if add_number == 0:
            raw_date = str(date.today()).split("-")
            year = int(raw_date[0])
            month = int(raw_date[1])
            day = int(raw_date[2])

            self.month = month
            self.year = year
            self.day = day

        elif self.month + add_number < 1:
            self.month = 12
            self.year = self.year - 1

        elif self.month + add_number > 12:
            self.month = 1
            self.year = self.year + 1

        else:
            self.month = self.month + add_number

        self.month_label.config(text=translate_month(self.month, self.language))
        self.year_label.config(text=self.year)

        self.update_days()

    def fullscreen(self):
        if self.attributes("-fullscreen"):
            self.overrideredirect(True)
            self.attributes('-fullscreen', False)
            self.anchor_button['state'] = "normal"

            self.menu_frame.config(width=self.window_width, height=30, bg="green")
            self.main_frame.config(width=self.window_width, height=470)
            self.main_frame.grid(pady=0)

            self.main_frame.configure(bg="green")
            for widget in self.main_frame.winfo_children():
                widget.configure(bg="green")

            # Show less details
            self.details_frame.config(height=94)
            self.detail_date_label.configure(bg="green", font=("Arial", 12, "bold"))
            self.detail_label.configure(bg="green", font=("Arial", 9, "bold"))

            return

        self.overrideredirect(False)
        self.attributes('-fullscreen', True)
        self.anchor_button['state'] = "disabled"

        self.menu_frame.config(width=self.screen_width, height=30, bg="black")
        self.main_frame.config(width=self.screen_width, height=self.screen_height)
        self.main_frame.grid(pady=int((self.screen_height / 2) - (self.window_height / 2) - 100))

        self.main_frame.configure(bg="#28231D")
        for widget in self.main_frame.winfo_children():
            widget.configure(bg="#28231D")

        # Show more details
        self.details_frame.config(height=300)
        self.detail_date_label.configure(bg="#28231D", font=("Arial", 15, "bold"))
        self.detail_label.configure(bg="#28231D", font=("Arial", 12, "bold"))

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

        self.save_config()

        self.geometry(
            "{}x{}+{}+{}".format(self.window_width, self.window_height, self.x_coordinate, self.y_coordinate))
        return

    def save_config(self):
        # Save current position to json file

        config = {
            "x": self.x_coordinate,
            "y": self.y_coordinate,
            "language": self.language
        }

        with open("data/config.json", mode="w", encoding="utf-8") as file:
            json.dump(config, file)

        AppLogs.warning(f"New coordinates for startup: {config}")

    def read_config(self):
        # Create config file
        if not os.path.exists("data/config.json"):
            AppLogs.warning("Creating new config file")

            config = {
                "x": self.x_coordinate,
                "y": self.y_coordinate,
                "language": "ENG"
            }

            with open("data/config.json", mode="w", encoding="utf-8") as file:
                json.dump(config, file)

        # Read coordinates from json file
        with open("data/config.json", mode="r", encoding="utf-8") as file:
            config = json.load(file)

        AppLogs.warning(f"Main App started at coordinates: {config}")
        self.x_coordinate = config["x"]
        self.y_coordinate = config["y"]
        self.language = config["language"]

        self.geometry(
            "{}x{}+{}+{}".format(self.window_width, self.window_height, self.x_coordinate, self.y_coordinate))

    def lower_window(self, event):
        self.lower()

    def add_event(self, button):
        self.day = button.cget('text')

        selected_date = f"{self.year}-{self.month}-{self.day}"
        data = [selected_date, button]

        self.add_app = AddApp(data)
        self.add_app.mainloop()

    def show_events(self, event):
        widget_name = str(event.widget).split(".")[-1]
        jsonpath = f"data/{self.year}-{self.month}.json"

        for button in self.days_frame.winfo_children():
            if button.winfo_name() == widget_name:
                day = button.cget('text')
                selected_date = f"{self.year}-{self.month}-{day}"

                if os.path.isfile(jsonpath):
                    with open(jsonpath, mode='r', encoding='utf-8') as file:
                        jsonfile = json.load(file)

                    texts = []
                    for event in jsonfile:
                        if event['date'] == selected_date:
                            texts.append(event['text'])

                    ready_text = ""
                    for i, text in enumerate(texts):
                        if i == 3:
                            ready_text += "...\n"

                        ready_text = ready_text + f"{i+1}. {text}\n"

                    ready_text = ready_text[:-1]

                    eu_date = selected_date.split("-")
                    if int(eu_date[1]) < 10:
                        eu_date[1] = "0" + eu_date[1]
                    if int(eu_date[2]) < 10:
                        eu_date[2] = "0" + eu_date[2]

                    eu_date = f"{eu_date[2]}.{eu_date[1]}.{eu_date[0]}"

                    self.detail_date_label.configure(text=eu_date, bg="black", fg=button.cget("bg"))
                    self.detail_label.configure(text=ready_text, bg="black", fg=button.cget("bg"))

    def hide_events(self, event):
        if self.attributes("-fullscreen"):
            self.detail_date_label.configure(text="", bg="#28231D")
            self.detail_label.configure(text="", bg="#28231D")
            return

        self.detail_date_label.configure(text="", bg="green")
        self.detail_label.configure(text="", bg="green")
        return

    def remove_events(self, event):
        button = event.widget
        self.day = button.cget('text')

        selected_date = f"{self.year}-{self.month}-{self.day}"
        data = [selected_date, button]

        self.remove_app = RemoveApp(data)
        self.remove_app.mainloop()

    def exit(self):
        try:
            self.add_app.destroy()
        except AttributeError:
            pass
        except tk.TclError:
            pass

        try:
            self.remove_app.destroy()
        except AttributeError:
            pass
        except tk.TclError:
            pass

        AppLogs.warning('Main App shutdown')
        self.destroy()

    def __init__(self):
        super().__init__()
        self.add_app = None
        self.remove_app = None
        self.popup = None

        # Logger setup
        AppLogs.start()

        # Initial
        self.title("To Do")
        self.resizable(False, False)
        self.overrideredirect(True)
        self.wm_attributes("-transparentcolor", "green")
        self.configure(bg='#353935')
        self.lower_window(self.event_generate("<<Foo>>"))

        self.window_width = 500
        self.window_height = 500
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.x_coordinate = int((self.screen_width / 2) - (self.window_width / 2))
        self.y_coordinate = int((self.screen_height / 2) - (self.window_height / 2))

        # Read saved position from config
        self.language = "ENG"
        self.read_config()

        # Popup window with important dates
        self.popup = StartingApp()

        # Menu frame
        self.menu_frame = tk.Frame(self, name="exit_frame", bg="green", width=self.window_width, height=30)
        self.menu_frame.config(highlightthickness=2, highlightbackground="black")
        self.menu_frame.grid(row=0, column=0)
        self.menu_frame.pack_propagate(False)

        self.exit_button = tk.Button(self.menu_frame, name="exit_button", text="X", font=("Arial", 13, "bold"),
                                     bg="black", fg="white")
        self.exit_button.config(command=self.exit, width=2)
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
                                     height=20)
        self.blank1_frame.grid(row=0, column=0)
        self.blank1_frame.pack_propagate(False)

        # Month frame
        self.month_frame = tk.Frame(self.main_frame, name="month_frame", bg="green", width=self.window_width - 4,
                                     height=50)
        self.month_frame.grid(row=1, column=0)
        self.month_frame.pack_propagate(False)

        self.back_button = tk.Button(self.month_frame, name="back_button", text="<",
                                     font=("Arial", 13, "bold"), bg="black", fg="white")
        self.back_button.config(command=lambda: self.change_month(-1), width=1, height=2)
        self.back_button.grid(row=0, column=0)

        self.month_label = tk.Label(self.month_frame, name="month_label", text="", font=("Arial", 15, "bold"))
        self.month_label.config(bg="black", fg="white", width=15, height=2)
        self.month_label.config(highlightthickness=1, highlightbackground="gray")
        self.month_label.grid(row=0, column=1)

        self.year_label = tk.Label(self.month_frame, name="year_label", text="2000", font=("Arial", 15, "bold"))
        self.year_label.config(bg="black", fg="white", width=5, height=2)
        self.year_label.config(highlightthickness=1, highlightbackground="gray")
        self.year_label.grid(row=0, column=2)

        self.next_button = tk.Button(self.month_frame, name="next_button", text=">",
                                     font=("Arial", 13, "bold"), bg="black", fg="white")
        self.next_button.config(command=lambda: self.change_month(1), width=1, height=2)
        self.next_button.grid(row=0, column=3)

        # Blank2 frame
        self.blank2_frame = tk.Frame(self.main_frame, name="blank2_frame", bg="green", width=self.window_width - 4,
                                     height=20)
        self.blank2_frame.grid(row=2, column=0)
        self.blank2_frame.pack_propagate(False)

        # Weekdays frame
        self.weekdays_frame = tk.Frame(self.main_frame, name="weekdays_frame", bg="black")
        self.weekdays_frame.grid(row=3, column=0)

        self.weekdays = ['pon', 'wto', 'śro', 'czw', 'pią', 'sob', 'nie']
        for i, weekday in enumerate(self.weekdays):
            self.weekday_label = tk.Label(self.weekdays_frame, name=f"weekday{i}_label", width=7, height=1,
                                          font=("Arial", 8, "bold"), bg="#28231D", fg="gray", text=weekday)
            self.weekday_label.config(highlightthickness=2, highlightbackground="black")
            self.weekday_label.grid(row=0, column=i)

        # Days frame
        self.days_frame = tk.Frame(self.main_frame, name="days_frame", bg="green")
        self.days_frame.grid(row=4, column=0)

        for i in range(42):
            self.day_button = tk.Button(self.days_frame, name=f"day{i}_button", width=7, height=2,
                                        font=("Arial", 8, "bold"), bg="black", fg="white")
            self.day_button.config(highlightthickness=1, highlightbackground="gray")
            self.day_button.config(command=lambda day=self.day_button: self.add_event(day))
            self.day_button.grid(row=int(i / 7), column=int(i % 7))

        # Blank3 frame
        self.blank3_frame = tk.Frame(self.main_frame, name="blank3_frame", bg="green", width=self.window_width - 4,
                                     height=20)
        self.blank3_frame.grid(row=5, column=0)
        self.blank3_frame.pack_propagate(False)

        # Details frame
        self.details_frame = tk.Frame(self.main_frame, name="details_frame", bg="green", width=self.window_width - 4,
                                     height=94)
        self.details_frame.config(highlightthickness=2, highlightbackground="black")
        self.details_frame.grid(row=6, column=0)
        self.details_frame.pack_propagate(False)

        self.detail_date_label = tk.Label(self.details_frame, name="detail_date_label",
                                     font=("Arial", 12, "bold"), bg="green", fg="white")
        self.detail_date_label.pack(pady=3)

        self.detail_label = tk.Label(self.details_frame, name="detail1_label", anchor="n", justify="left",
                                     font=("Arial", 9, "bold"), bg="green", fg="white")
        self.detail_label.pack()

        # Get current date
        self.year = 0
        self.month = 0
        self.day = 0
        self.change_month(0)

        # Date update on midnight
        Thread(target=self.update_midnight).start()


if __name__ == "__main__":
    app = App()
    app.mainloop()
