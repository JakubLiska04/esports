import sqlite3
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.switch import Switch
from subprocess import Popen, PIPE

# Connect to the database
conn = sqlite3.connect('esports.db')
c = conn.cursor()


class BotControlApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bot_process = None
        self.monthly_rankings = False  # Flag to toggle between total and monthly rankings

    def start_bot(self, instance):
        if self.bot_process is None or self.bot_process.poll() is not None:
            print("Starting bot...")
            self.bot_process = Popen(["python3", "main.py"], stdout=PIPE, stderr=PIPE)
            self.start_button.disabled = True
            self.stop_button.disabled = False
        else:
            print("Bot is already running.")

    def stop_bot(self, instance):
        if self.bot_process is not None and self.bot_process.poll() is None:
            print("Stopping bot...")
            self.bot_process.terminate()
            self.bot_process.wait()
            print("Bot stopped.")
            self.start_button.disabled = False
            self.stop_button.disabled = True
        else:
            print("Bot is not running.")

    def toggle_rankings(self, instance, value):
        self.monthly_rankings = value
        self.update_leaderboard()

    def register_team(self, instance):
        team_name = self.team_name_input.text
        # Insert the team into the database
        c.execute("INSERT INTO teams (team_name) VALUES (?)", (team_name,))
        conn.commit()
        print(f"Team '{team_name}' registered successfully!")
        # Update the team leaderboard
        self.update_leaderboard()

    def delete_team(self, instance, team_id):
        try:
            c.execute("DELETE FROM teams WHERE team_id = ?", (team_id,))
            conn.commit()
            self.update_leaderboard()  # Refresh the leaderboard after deletion
        except Exception as e:
            print(f"Error deleting team: {e}")

    def update_leaderboard(self):
        # Fetch teams from the database
        if self.monthly_rankings:
            c.execute("SELECT team_id, team_name, monthly_rating FROM teams")
        else:
            c.execute("SELECT team_id, team_name, rating FROM teams")
        teams = c.fetchall()

        # Clear the leaderboard layout
        self.leaderboard_layout.clear_widgets()

        if not teams:
            empty_label = Label(text="Leaderboard is empty")
            self.leaderboard_layout.add_widget(empty_label)
        else:
            # Add teams, ratings, IDs, and delete buttons to the leaderboard layout
            for team in teams:
                team_id, team_name, rating = team
                team_row = GridLayout(cols=4, size_hint_y=None, height=40)
                team_row.add_widget(Label(text=str(team_id)))
                team_row.add_widget(Label(text=team_name))
                rating_input = TextInput(text=str(rating), multiline=False, input_filter='float')
                rating_input.bind(text=lambda instance, value, team_id=team_id: self.update_rating(value, team_id))
                team_row.add_widget(rating_input)
                delete_button = Button(text="Delete", size_hint_x=None, width=100)
                delete_button.bind(on_press=lambda instance, team_id=team_id: self.delete_team(instance, team_id))
                team_row.add_widget(delete_button)
                self.leaderboard_layout.add_widget(team_row)

    def update_rating(self, value, team_id):
        try:
            new_rating = float(value)
            if self.monthly_rankings:
                c.execute("UPDATE teams SET monthly_rating = ? WHERE team_id = ?", (new_rating, team_id))
            else:
                c.execute("UPDATE teams SET rating = ? WHERE team_id = ?", (new_rating, team_id))
            conn.commit()
        except ValueError:
            print("Invalid rating format. Rating must be a number.")

    def build(self):
        root_layout = GridLayout(cols=1, spacing=10, padding=[50, 50])

        # Start and Stop Buttons
        start_stop_layout = GridLayout(cols=2, spacing=10)
        start_button = Button(text="Start Bot")
        start_button.bind(on_press=self.start_bot)
        self.start_button = start_button
        start_stop_layout.add_widget(start_button)

        stop_button = Button(text="Stop Bot")
        stop_button.bind(on_press=self.stop_bot)
        stop_button.disabled = True
        self.stop_button = stop_button
        start_stop_layout.add_widget(stop_button)

        root_layout.add_widget(start_stop_layout)

        # Monthly Rankings Switch
        rankings_layout = GridLayout(cols=2, spacing=10)
        rankings_label = Label(text="Total Rankings")
        rankings_layout.add_widget(rankings_label)
        self.rankings_switch = Switch(active=False)
        self.rankings_switch.bind(active=self.toggle_rankings)
        rankings_layout.add_widget(self.rankings_switch)
        root_layout.add_widget(rankings_layout)

        # Leaderboard
        leaderboard_label = Label(text="Leaderboard", size_hint_y=None, height=40)
        root_layout.add_widget(leaderboard_label)

        leaderboard_scroll = ScrollView(size_hint=(1, None), size=(400, 200))
        self.leaderboard_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.leaderboard_layout.bind(minimum_height=self.leaderboard_layout.setter('height'))
        leaderboard_scroll.add_widget(self.leaderboard_layout)
        root_layout.add_widget(leaderboard_scroll)

        # Add Team
        add_team_layout = GridLayout(cols=2, spacing=10)
        self.team_name_input = TextInput(hint_text="Enter team name")
        add_team_layout.add_widget(self.team_name_input)
        add_team_button = Button(text="Add Team")
        add_team_button.bind(on_press=self.register_team)
        add_team_layout.add_widget(add_team_button)

        root_layout.add_widget(add_team_layout)

        # Populate the leaderboard initially
        self.update_leaderboard()

        return root_layout


if __name__ == "__main__":
    BotControlApp().run()
