import time
import random

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from threading import Thread


class RockPaperScissor(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spin_val = ["ROCK", "PAPER", "SCISSOR"]
        self.user_won, self.comp_won = 0, 0
        self.win_conditions = {"ROCK": "SCISSOR", "PAPER": "ROCK", "SCISSOR": "PAPER"}
        self.time, self.score = 60, 30
        self.mode = None
        self.running_timer, self.running_score, self.time_selected, self.score_selected = False, False, False, False

    def start_timer_game(self):
        if self.ids.timer_game_spinner.text != "Select Mode":
            self.ids.screen_manager.current = "third_screen"
            if self.ids.set_timer_field.text != "":
                self.time = int(self.ids.set_timer_field.text)
            self.mode = self.ids.timer_game_spinner.text
            self.ids.left_label.text = f"Mode: {self.mode}"
            self.ids.right_label.text = f"Time Left: {self.time}"
            self.running_timer, self.time_selected = True, True
        else:
            self.show_popup(title="Invalid Game Mode", message="Please select game mode")

    def start_score_game(self):
        if self.ids.score_game_spinner.text != "Select Mode":
            self.ids.screen_manager.current = "third_screen"
            if self.ids.set_score_field.text != "":
                self.score = int(self.ids.set_score_field.text)
            self.mode = self.ids.score_game_spinner.text
            self.ids.left_label.text = f"Mode: {self.mode}"
            self.ids.right_label.text = f"Set Score: {self.score}"
            self.running_score, self.score_selected = True, True
        else:
            self.show_popup(title="Invalid Game Mode", message="Please select game mode")

    def select_timer_spinner(self):
        self.ids.timer_game_spinner.values = ["Easy", "Medium", "Hard"]
        self.ids.set_timer_field.disabled = False
        self.ids.timer_game_spinner.disabled = False
        self.ids.timer_game_button.disabled = False
        self.ids.score_game_spinner.text = "Select Mode"
        self.ids.set_score_field.disabled = True
        self.ids.set_score_field.text = ""
        self.ids.score_game_spinner.disabled = True
        self.ids.score_game_button.disabled = True

    def select_score_spinner(self):
        self.ids.score_game_spinner.values = ["Easy", "Medium", "Hard"]
        self.ids.set_score_field.disabled = False
        self.ids.score_game_spinner.disabled = False
        self.ids.score_game_button.disabled = False
        self.ids.timer_game_spinner.text = "Select Mode"
        self.ids.set_timer_field.disabled = True
        self.ids.set_timer_field.text = ""
        self.ids.timer_game_spinner.disabled = True
        self.ids.timer_game_button.disabled = True

    def game_continuous_function(self):
        while True:
            if self.running_timer:
                time.sleep(1)
                time_left = int(self.ids.right_label.text.split(":")[1])
                if time_left == 0:
                    self.ids.right_label.text = "Time Left: 60"
                    self.running_timer = False
                    self.decision_popup(title="Game Over", message=f"{self.check_game_winner()}")
                else:
                    time_left -= 1
                    self.ids.right_label.text = f"Time Left: {time_left}"
            elif self.running_score:
                if (self.user_won == self.score) or (self.comp_won == self.score):
                    self.running_score = False
                    self.decision_popup(title="Game Over", message=f"{self.check_game_winner()}")

    def check_game_winner(self):
        if self.user_won > self.comp_won:
            message = f"""Congratulations You Won!\nYour Score: {self.user_won}\nComputer Score: {self.comp_won}"""
        elif self.comp_won > self.user_won:
            message = f"""Computer Has Won!\nYour Score: {self.user_won}\nComputer Score: {self.comp_won}"""
        else:
            message = f"""It's a tie.\nYour Score: {self.user_won}\nComputer Score: {self.comp_won}"""
        self.user_won, self.comp_won = 0, 0
        return message

    # change home screen -> user name screen function
    def change_screen(self):
        self.ids.screen_manager.current = "second_screen"
        self.ids.user_name_field.focus = True

    # check for valid user name function
    def validate_user_name(self):
        if len(self.ids.user_name_field.text) > 0:
            self.ids.screen_manager.current = "selection_screen"
            self.ids.user_spinner.values = self.spin_val
            self.ids.display_user_name.text = f"Welcome {self.ids.user_name_field.text}"
            thread1 = Thread(target=self.game_continuous_function)
            thread1.daemon = True
            thread1.start()
        else:
            self.show_popup(title="Invalid Username", message="Please provide a valid user name")

    # show popup function
    def show_popup(self, title, message):
        layout = GridLayout(cols=1, padding=10, spacing=10, size=self.size, pos=self.pos)
        popup_label = Label(text=message, font_size=20, bold=True, pos_hint={"center_x": .5, "center_y": .5})
        popup_button = Button(text="OK", size_hint_y=None, height=50, bold=True, font_size=20, background_normal="",
                              background_color=(.06, .47, .47, 1))
        layout.add_widget(popup_label)
        layout.add_widget(popup_button)
        popup = Popup(title=title, content=layout, size_hint=(None, None), size=(300, 300), auto_dismiss=False)
        popup.open()
        popup_button.bind(on_press=popup.dismiss)

    def decision_popup(self, title, message, flag=False):
        if flag and self.time_selected:
            self.running_timer = False
        layout = GridLayout(cols=1, padding=10, spacing=10, size=self.size, pos=self.pos)
        popup_label = Label(text=message, font_size=20, bold=True, pos_hint={"center_x": .5, "center_y": .5})
        boxlayout = BoxLayout(orientation="horizontal", pos=self.pos, size=self.size, spacing=10)
        if flag:
            play_again_button = Button(text="Resume", size_hint_y=None, height=50, bold=True, font_size=20,
                                       background_normal="", background_color=(.06, .47, .47, 1))
        else:
            play_again_button = Button(text="Play Again", size_hint_y=None, height=50, bold=True, font_size=20,
                                       background_normal="", background_color=(.06, .47, .47, 1))
        go_back_button = Button(text="Go Back", size_hint_y=None, height=50, bold=True, font_size=20,
                                background_normal="", background_color=(.06, .47, .47, 1))
        boxlayout.add_widget(play_again_button)
        boxlayout.add_widget(go_back_button)
        layout.add_widget(popup_label)
        layout.add_widget(boxlayout)
        popup = Popup(title=title, content=layout, size_hint=(None, None), size=(300, 300), auto_dismiss=False)
        popup.open()
        if flag:
            play_again_button.bind(on_press=self.resume)
        else:
            play_again_button.bind(on_press=self.play_again)
        play_again_button.bind(on_press=popup.dismiss)
        go_back_button.bind(on_press=self.go_back_function)
        go_back_button.bind(on_press=popup.dismiss)

    def resume(self, *args):
        if self.time_selected:
            self.running_timer = True
        else:
            self.running_score = True

    def play_again(self, *args):
        if self.time_selected:
            self.ids.right_label.text = f"Time Left: {self.time}"
            self.running_timer = True
        elif self.score_selected:
            self.ids.right_label.text = f"Set Score: {self.score}"
            self.running_score = True
        self.clear_data()

    def clear_data(self):
        self.ids.user_image.source = "images/bg.jpg"
        self.ids.user_spinner.text = "SELECT"
        self.ids.user_image_label.text = ""
        self.ids.computer_image.source = "images/bg.jpg"
        self.ids.game_status.text = ""
        self.ids.computer_image_label.text = ""
        self.ids.user_won.text = "Your Wins: 0"
        self.ids.computer_won.text = "Computer Wins: 0"
        self.ids.match_tie.text = "Game Status"
        self.time_selected, self.score_selected = False, False
        self.user_won, self.comp_won = 0, 0

    def go_back_function(self, *args):
        self.ids.screen_manager.current = "selection_screen"
        if self.time_selected:
            self.ids.timer_game_spinner.text = "Select Mode"
            self.ids.set_timer_field.disabled = True
            self.ids.set_timer_field.text = ""
            self.ids.timer_game_spinner.disabled = True
            self.ids.timer_game_button.disabled = True
        elif self.score_selected:
            self.ids.score_game_spinner.text = "Select Mode"
            self.ids.set_score_field.disabled = True
            self.ids.set_score_field.text = ""
            self.ids.score_game_spinner.disabled = True
            self.ids.score_game_button.disabled = True
        self.clear_data()

    # main function
    def play_game(self):
        user_selected = self.user_select()
        if user_selected == "SELECT":
            self.show_popup(title="Invalid Input", message="Invalid Input")
        else:
            comp_result = self.computer_select()
            if user_selected == comp_result:
                self.game_algorithm(message="Tie")
            elif self.win_conditions[user_selected] == comp_result:
                self.game_algorithm(message="User")
            else:
                self.game_algorithm(message="Computer")
            self.ids.user_won.text = f"Your Wins: {self.user_won}"
            self.ids.computer_won.text = f"Computer Wins: {self.comp_won}"

    def game_algorithm(self, message):
        if self.mode == "Easy":
            if message == "User":
                self.user_won += 1
                self.ids.match_tie.text = "You Won!"
            elif message == "Computer":
                self.comp_won += 1
                self.ids.match_tie.text = "Computer Has Won!"
            else:
                self.ids.match_tie.text = "It's a tie!"
        elif self.mode == "Medium":
            if message == "User":
                self.user_won += 1
                if self.comp_won != 0:
                    self.comp_won -= 1
                self.ids.match_tie.text = "You Won!"
            elif message == "Computer":
                self.comp_won += 1
                if self.user_won != 0:
                    self.user_won -= 1
                self.ids.match_tie.text = "Computer Has Won!"
            else:
                self.ids.match_tie.text = "It's a tie!"
        else:
            if message == "Tie":
                if self.comp_won != 0:
                    self.comp_won -= 1
                if self.user_won != 0:
                    self.user_won -= 1
                self.ids.match_tie.text = "It's a tie!"
            elif message == "User":
                self.user_won += 1
                if self.comp_won != 0:
                    self.comp_won -= 1
                self.ids.match_tie.text = "You Won!"
            else:
                self.comp_won += 1
                if self.user_won != 0:
                    self.user_won -= 1
                self.ids.match_tie.text = "Computer Has Won!"

    # computer select function
    def computer_select(self):
        comp_selected = random.choice(self.spin_val)
        if comp_selected == "ROCK":
            self.ids.computer_image.source = "images/rock.png"
        elif comp_selected == "PAPER":
            self.ids.computer_image.source = "images/paper.png"
        elif comp_selected == "SCISSOR":
            self.ids.computer_image.source = "images/scissor.png"
        self.ids.computer_image_label.text = f'Computer Selected "{comp_selected}"'
        self.ids.game_status.text = comp_selected
        return comp_selected

    # user select function
    def user_select(self):
        user_selected = self.ids.user_spinner.text
        if user_selected == "ROCK":
            self.ids.user_image.source = "images/flip_rock.png"
        elif user_selected == "PAPER":
            self.ids.user_image.source = "images/flip_paper.png"
        elif user_selected == "SCISSOR":
            self.ids.user_image.source = "images/flip_scissor.png"
        self.ids.user_image_label.text = f'You Selected "{user_selected}"'
        return user_selected


class RPSApp(App):
    def build(self):
        self.title = "Rock, Paper & Scissors Game"
        Config.set('kivy', 'window_icon', 'images/rock_paper_scissor.jpg')
        return RockPaperScissor()


if __name__ == "__main__":
    RPSApp().run()
