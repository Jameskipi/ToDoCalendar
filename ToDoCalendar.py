import time
import tkinter as tk
import os
import json
import logging
from datetime import date, timedelta, datetime
from calendar import monthcalendar, monthrange
from threading import Thread


class StartingApp(tk.Toplevel):
    def get_events(self):
        raw_date = str(date.today()).split("-")
        year = int(raw_date[0])
        month = int(raw_date[1])
        day = int(raw_date[2])

        # Paths
        current_json_path = f"data/{year}-{month}.json"

        if month + 1 > 12:
            next_json_path = f"data/{year+1}-1.json"
        else:
            next_json_path = f"data/{year}-{month + 1}.json"

        # Json files
        try:
            with open(current_json_path, mode='r', encoding='utf-8') as file:
                current_json = json.load(file)
        except FileNotFoundError:
            logging.error("StartingApp: No events found this month")
            current_json = []

        try:
            with open(next_json_path, mode='r', encoding='utf-8') as file:
                next_json = json.load(file)
        except FileNotFoundError:
            logging.error("StartingApp: No events found in the next month")
            next_json = []

        # Every event left in this month
        for event in current_json:
            date_fixed = event['date'].split("-")
            date_fixed = date(int(date_fixed[0]), int(date_fixed[1]), int(date_fixed[2]))

            if date_fixed > date.today():
                self.current_month_events.append(event)

        # Every event in the next month
        for event in next_json:
            self.next_month_events.append(event)

        # Every event in the next 7 days
        start_date = date.today()
        end_date = date.today() + timedelta(days=8)

        next_week = []
        while start_date != end_date:
            next_week.append(start_date)
            start_date = start_date + timedelta(days=1)

        this_month = []
        next_month = []
        for event_day in next_week:
            if event_day.month == date.today().month:
                this_month.append(f"{event_day.year}-{event_day.month}-{event_day.day}")
            else:
                next_month.append(f"{event_day.year}-{event_day.month}-{event_day.day}")

        # Update next week events
        for event in current_json:
            for event_day in this_month:
                if str(event_day) == event['date']:
                    self.next_week_events.append(event)

        for event in next_json:
            for event_day in next_month:
                if str(event_day) == event['date']:
                    self.next_week_events.append(event)

    def show_events(self, option):
        events = []

        # Clear all events
        for label in self.left_frame.winfo_children():
            label.configure(text="", bg="gray", fg="white")
            label.configure(highlightbackground="gray")

        for label in self.right_frame.winfo_children():
            label.configure(text="", bg="gray", fg="white")
            label.configure(highlightbackground="gray")

        match option:
            case -1:
                events = self.current_month_events

                self.current_month_label.configure(fg="white")
                self.next_week_label.configure(fg="gray")
                self.next_month_label.configure(fg="gray")
            case 0:
                events = self.next_week_events

                self.current_month_label.configure(fg="gray")
                self.next_week_label.configure(fg="white")
                self.next_month_label.configure(fg="gray")
            case 1:
                events = self.next_month_events

                self.current_month_label.configure(fg="gray")
                self.next_week_label.configure(fg="gray")
                self.next_month_label.configure(fg="white")

        # Sort events
        events.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))

        if len(events) > 15:
            # Show right frame
            self.right_frame.grid(row=0, column=1)
            self.left_frame.configure(width=343)
        else:
            # Hide right frame
            self.right_frame.grid_forget()
            self.left_frame.configure(width=680)

        for i, label in enumerate(self.left_frame.winfo_children()):
            try:
                eu_date = events[i]['date'].split("-")
                if int(eu_date[1]) < 10:
                    eu_date[1] = "0" + eu_date[1]
                if int(eu_date[2]) < 10:
                    eu_date[2] = "0" + eu_date[2]

                eu_date = f"{eu_date[2]}.{eu_date[1]}.{eu_date[0]}"

                text = f"{eu_date}   -   {events[i]['text']}"
                label.configure(text=text, bg="dark slate gray")
                label.configure(highlightbackground="black")

                if events[i]['priority'] == "RED":
                    label.configure(fg="red")

            except IndexError:
                continue

        if len(events) > 15:
            i = 15
            for label in self.right_frame.winfo_children():
                try:
                    eu_date = events[i]['date'].split("-")
                    if int(eu_date[1]) < 10:
                        eu_date[1] = "0" + eu_date[1]
                    if int(eu_date[2]) < 10:
                        eu_date[2] = "0" + eu_date[2]

                    eu_date = f"{eu_date[2]}.{eu_date[1]}.{eu_date[0]}"

                    text = f"{eu_date}   -   {events[i]['text']}"
                    label.configure(text=text, bg="dark slate gray")
                    label.configure(highlightbackground="black")

                    if events[i]['priority'] == "RED":
                        label.configure(fg="red")

                    i = i + 1

                except IndexError:
                    continue

    def __init__(self):
        super().__init__()
        self.current_month_events = []
        self.next_month_events = []
        self.next_week_events = []

        # Initial
        self.title("Important dates")
        self.resizable(False, False)
        self.wm_attributes("-transparentcolor", "green")
        self.overrideredirect(True)
        self.configure(bg='gray')
        self.config(highlightthickness=5, highlightbackground="black")
        self.lift()
        self.attributes("-topmost", True)

        self.window_width = 700
        self.window_height = 700
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.x_coordinate = int((self.screen_width / 2) - (self.window_width / 2))
        self.y_coordinate = int((self.screen_height / 2) - (self.window_height / 2))
        self.geometry("{}x{}+{}+{}".format(self.window_width, self.window_height, self.x_coordinate, self.y_coordinate))
        self.geometry(
            "{}x{}+{}+{}".format(self.window_width, self.window_height, self.x_coordinate, self.y_coordinate))

        # Update events
        self.get_events()

        # Menu frame
        self.menu_frame = tk.Frame(self, name="menu_frame", bg="dark slate gray", width=self.window_width - 10, height=50)
        self.menu_frame.config(highlightthickness=2, highlightbackground="black")
        self.menu_frame.grid(row=0, column=0)
        self.menu_frame.pack_propagate(False)

        # Current month
        self.current_month_label = tk.Button(self.menu_frame, name="current_month_label", text="Ten miesiąc",
                                          font=("Arial", 13, "bold"), bg="black", fg="white", width=14)
        self.current_month_label.configure(command=lambda: self.show_events(-1))
        self.current_month_label.pack(side=tk.LEFT, padx=58, anchor=tk.CENTER)

        # Next 7 days button
        self.next_week_label = tk.Button(self.menu_frame, name="next_week_label", text="Najbliższe 7 dni",
                                    font=("Arial", 13, "bold"), bg="black", fg="white", width=14)
        self.next_week_label.configure(command=lambda: self.show_events(0))
        self.next_week_label.pack(side=tk.LEFT, anchor=tk.CENTER)

        # Next month
        self.next_month_label = tk.Button(self.menu_frame, name="next_month_label", text="Następny miesiąc",
                                    font=("Arial", 13, "bold"), bg="black", fg="white", width=14)
        self.next_month_label.configure(command=lambda: self.show_events(1))
        self.next_month_label.pack(side=tk.LEFT, padx=58, anchor=tk.CENTER)

        # Main frame
        self.main_frame = tk.Frame(self, name="main_frame", bg="gray", width=self.window_width - 10, height=600)
        self.main_frame.config(highlightthickness=2, highlightbackground="black")
        self.main_frame.grid(row=1, column=0)
        self.main_frame.grid_propagate(False)

        # Left main frame
        self.left_frame = tk.Frame(self.main_frame, name="left_frame", bg="gray", width=343, height=596)
        self.left_frame.grid(row=0, column=0)
        self.left_frame.pack_propagate(False)

        # Right main frame
        self.right_frame = tk.Frame(self.main_frame, name="right_frame", bg="gray", width=343, height=596)
        self.right_frame.grid(row=0, column=1)
        self.right_frame.pack_propagate(False)

        # Dates label
        for i in range(15):
            self.date_label = tk.Label(self.left_frame, name=f"date{i}_label", font=("Arial", 8, "bold"),
                                         bg="dark slate gray", fg="white")
            self.date_label.config(highlightthickness=2, highlightbackground="black")
            self.date_label.pack(pady=7)

        for i in range(15, 30):
            self.date_label = tk.Label(self.right_frame, name=f"date{i}_label", font=("Arial", 8, "bold"),
                                         bg="dark slate gray", fg="white")
            self.date_label.config(highlightthickness=2, highlightbackground="black")
            self.date_label.pack(pady=7)

        # Confirmation frame
        self.exit_frame = tk.Frame(self, name="exit_frame", bg="dark slate gray", width=self.window_width - 10, height=40)
        self.exit_frame.config(highlightthickness=2, highlightbackground="black")
        self.exit_frame.grid(row=2, column=0)
        self.exit_frame.pack_propagate(False)

        # Confirm button
        self.exit_button = tk.Button(self.exit_frame, name="exit_button", text="OK", font=("Arial", 13, "bold"),
                                     bg="black", fg="white")
        self.exit_button.config(command=self.destroy, width=5)
        self.exit_button.pack(side=tk.TOP, anchor=tk.CENTER, pady=1)

        # Start at next 7 days
        self.show_events(0)


class AddApp(tk.Tk):
    def exit(self):
        self.data_button.configure(bg="black", fg="white")
        app.update_days()
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

        logging.warning(f'Added new event: {data}')

        self.exit()


class RemoveApp(tk.Tk):
    def exit(self):
        self.data_button.configure(bg="black", fg="white")
        app.update_days()
        self.destroy()

    def event_changed(self, *args):
        selected = self.selected_event.get()

        if selected == "Remove All":
            self.event_menu.configure(bg="red")
        else:
            self.event_menu.configure(bg="gray")

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

    def confirm(self, e):
        if self.selected_event.get() == "Select":
            # Nothing was selected
            return

        elif self.selected_event.get() == "Remove All":
            # Remove everything 5 times because of weird bug
            for i in range(5):
                for event in self.jsonfile:
                    if event['date'] == self.date:
                        logging.warning(f'Removed event: {event}')
                        self.jsonfile.remove(event)

        else:
            # One event was selected
            text = self.selected_event.get().split(".")[1][1:]

            for event in self.jsonfile:
                if event['text'] == text:
                    logging.warning(f'Removed event: {event}')
                    self.jsonfile.remove(event)

        # Save updated jsonfile
        with open(self.jsonpath, mode="w", encoding="utf-8") as file:
            json.dump(self.jsonfile, file)

        # Remove file if empty
        if not self.jsonfile:
            os.remove(self.jsonpath)

        self.exit()


class App(tk.Tk):
    def update_midnight(self):
        # Update date on midnight
        while True:
            try:
                self.state()

                if datetime.now().hour == 0 and datetime.now().minute == 0:
                    logging.warning("MIDNIGHT DATE UPDATE")
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
        def translate_month(number):
            match number:
                case 1:
                    return "Styczeń"
                case 2:
                    return "Luty"
                case 3:
                    return "Marzec"
                case 4:
                    return "Kwiecień"
                case 5:
                    return "Maj"
                case 6:
                    return "Czerwiec"
                case 7:
                    return "Lipiec"
                case 8:
                    return "Sierpień"
                case 9:
                    return "Wrzesień"
                case 10:
                    return "Październik"
                case 11:
                    return "Listopad"
                case 12:
                    return "Grudzień"

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

        self.month_label.config(text=translate_month(self.month))
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
            self.detail_date_label.configure(bg="green")
            self.detail_label.configure(bg="green")

            return

        self.overrideredirect(False)
        self.attributes('-fullscreen', True)
        self.anchor_button['state'] = "disabled"

        self.menu_frame.config(width=self.screen_width, height=30, bg="dark slate gray")
        self.main_frame.config(width=self.screen_width, height=self.screen_height)
        self.main_frame.grid(pady=int((self.screen_height / 2) - (self.window_height / 2) - 100))

        self.main_frame.configure(bg="dark slate gray")
        for widget in self.main_frame.winfo_children():
            widget.configure(bg="dark slate gray")

        # Show more details
        self.details_frame.config(height=200)
        self.detail_date_label.configure(bg="dark slate gray")
        self.detail_label.configure(bg="dark slate gray")

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

        with open("data/config.json", mode="w", encoding="utf-8") as file:
            json.dump(config, file)

        logging.warning(f"New coordinates for startup: {config}")

    def read_position(self):
        # Create config file
        if not os.path.exists("data/config.json"):
            logging.warning("Creating new config file")

            config = {
                "x": self.x_coordinate,
                "y": self.y_coordinate
            }

            with open("data/config.json", mode="w", encoding="utf-8") as file:
                json.dump(config, file)

        # Read coordinates from json file
        with open("data/config.json", mode="r", encoding="utf-8") as file:
            config = json.load(file)

        logging.warning(f"Main App started at coordinates: {config}")
        self.x_coordinate = config["x"]
        self.y_coordinate = config["y"]
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
            self.detail_date_label.configure(text="", bg="dark slate gray")
            self.detail_label.configure(text="", bg="dark slate gray")
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

        logging.warning('Main App shutdown')
        self.destroy()

    def __init__(self):
        super().__init__()
        self.add_app = None
        self.remove_app = None
        self.popup = None

        # Logger setup
        if not os.path.isdir("data"):
            os.makedirs("data")
        logging.basicConfig(
            filename="data/app.log",
            encoding="utf-8",
            filemode="a",
            format="{asctime} - {levelname} - {message}",
            style="{",
            datefmt="%Y-%m-%d %H:%M",)
        logging.warning('Main App start')

        # Popup window with important dates
        self.popup = StartingApp()

        # Initial
        self.title("To Do")
        self.resizable(False, False)
        self.overrideredirect(True)
        self.wm_attributes("-transparentcolor", "green")
        self.configure(bg='gray')
        self.lower_window(self.event_generate("<<Foo>>"))

        self.window_width = 500
        self.window_height = 500
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.x_coordinate = int((self.screen_width / 2) - (self.window_width / 2))
        self.y_coordinate = int((self.screen_height / 2) - (self.window_height / 2))

        # Read saved position from config
        self.read_position()

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
