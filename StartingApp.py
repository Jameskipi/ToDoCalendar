import tkinter as tk
from datetime import date, timedelta, datetime
import json
import AppLogs


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
            AppLogs.error("StartingApp: No events found this month")
            current_json = []

        try:
            with open(next_json_path, mode='r', encoding='utf-8') as file:
                next_json = json.load(file)
        except FileNotFoundError:
            AppLogs.error("StartingApp: No events found in the next month")
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

        # Button options
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

        # Frame management
        if len(events) > 15:
            # Show right frame
            self.right_frame.grid(row=0, column=1)
            self.left_frame.configure(width=443)

        else:
            # Hide right frame
            self.right_frame.grid_forget()
            self.left_frame.configure(width=890)

        # Changing font depending on the number of events
        if len(events) < 15:
            for label in self.left_frame.winfo_children():
                label.configure(font=("Arial", 15, "bold"))
        else:
            for label in self.left_frame.winfo_children():
                label.configure(font=("Arial", 12, "bold"))

        # Update left frame
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

        # Update right frame
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

        self.window_width = 900
        self.window_height = 800
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.x_coordinate = int((self.screen_width / 2) - (self.window_width / 2))
        self.y_coordinate = int((self.screen_height / 2) - (self.window_height / 2))
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
        self.current_month_label.pack(side=tk.LEFT, padx=109, anchor=tk.CENTER)

        # Next 7 days button
        self.next_week_label = tk.Button(self.menu_frame, name="next_week_label", text="Najbliższe 7 dni",
                                    font=("Arial", 13, "bold"), bg="black", fg="white", width=14)
        self.next_week_label.configure(command=lambda: self.show_events(0))
        self.next_week_label.pack(side=tk.LEFT, anchor=tk.CENTER)

        # Next month
        self.next_month_label = tk.Button(self.menu_frame, name="next_month_label", text="Następny miesiąc",
                                    font=("Arial", 13, "bold"), bg="black", fg="white", width=14)
        self.next_month_label.configure(command=lambda: self.show_events(1))
        self.next_month_label.pack(side=tk.LEFT, padx=109, anchor=tk.CENTER)

        # Main frame
        self.main_frame = tk.Frame(self, name="main_frame", bg="gray",
                                   width=self.window_width - 10, height=self.window_height - 100)
        self.main_frame.config(highlightthickness=2, highlightbackground="black")
        self.main_frame.grid(row=1, column=0)
        self.main_frame.grid_propagate(False)

        # Left main frame
        self.left_frame = tk.Frame(self.main_frame, name="left_frame", bg="gray", width=443, height=696)
        self.left_frame.grid(row=0, column=0)
        self.left_frame.pack_propagate(False)

        # Right main frame
        self.right_frame = tk.Frame(self.main_frame, name="right_frame", bg="gray", width=443, height=696)
        self.right_frame.grid(row=0, column=1)
        self.right_frame.pack_propagate(False)

        # Dates label
        for i in range(15):
            self.date_label = tk.Label(self.left_frame, name=f"date{i}_label", font=("Arial", 12, "bold"),
                                         bg="dark slate gray", fg="white")
            self.date_label.config(highlightthickness=2, highlightbackground="black")
            self.date_label.pack(pady=7)

        for i in range(15, 30):
            self.date_label = tk.Label(self.right_frame, name=f"date{i}_label", font=("Arial", 12, "bold"),
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
