from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import random


class RockPaperScissor(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.spin_val = ["ROCK", "PAPER", "SCISSOR"]
        self.user_won, self.match_tie, self.comp_won = 0, 0, 0
        self.win_conditions = {"ROCK": "SCISSOR", "PAPER": "ROCK", "SCISSOR": "PAPER"}

    # change home screen -> user name screen function
    def change_screen(self):
        self.ids.screen_manager.current = "second_screen"
        self.ids.user_name_field.focus = True

    # check for valid user name function
    def validate_user_name(self):
        if len(self.ids.user_name_field.text) > 0:
            self.ids.screen_manager.current = "third_screen"
            self.ids.user_spinner.values = self.spin_val
            self.ids.display_user_name.text = f"Welcome {self.ids.user_name_field.text}"
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
        popup = Popup(title=title, content=layout, size_hint=(None, None), size=(300, 300))
        popup.open()
        popup_button.bind(on_press=popup.dismiss)

    # main function
    def play_game(self):
        user_selected = self.user_select()
        if user_selected == "SELECT":
            self.show_popup(title="Invalid Input", message="Invalid Input")
        else:
            comp_result = self.computer_select()
            if user_selected == comp_result:
                self.ids.game_status.text = "It's a tie!"
                self.match_tie += 1
                if self.user_won != 0:
                    self.user_won -= 1
                if self.comp_won != 0:
                    self.comp_won -= 1
            elif self.win_conditions[user_selected] == comp_result:
                self.ids.game_status.text = f"You Won!"
                self.user_won += 1
                if self.comp_won != 0:
                    self.comp_won -= 1
                if self.match_tie != 0:
                    self.match_tie -= 1
            else:
                self.ids.game_status.text = "Computer Has Won!"
                self.comp_won += 1
                if self.user_won != 0:
                    self.user_won -= 1
                if self.match_tie != 0:
                    self.match_tie -= 1
            self.ids.match_tie.text = f"Match Ties: {self.match_tie}"
            self.ids.user_won.text = f"Your Wins: {self.user_won}"
            self.ids.computer_won.text = f"Computer Wins: {self.comp_won}"

    # computer select function
    def computer_select(self):
        comp_selected = random.choice(self.spin_val)
        if comp_selected == "ROCK":
            self.ids.computer_image.source = "images/rock.jpg"
        elif comp_selected == "PAPER":
            self.ids.computer_image.source = "images/paper.jpg"
        elif comp_selected == "SCISSOR":
            self.ids.computer_image.source = "images/scissor.jpg"
        self.ids.computer_image_label.text = f'Computer Selected "{comp_selected}"'
        return comp_selected

    # user select function
    def user_select(self):
        user_selected = self.ids.user_spinner.text
        if user_selected == "ROCK":
            self.ids.user_image.source = "images/rock.jpg"
        elif user_selected == "PAPER":
            self.ids.user_image.source = "images/paper.jpg"
        elif user_selected == "SCISSOR":
            self.ids.user_image.source = "images/scissor.jpg"
        self.ids.user_image_label.text = f'You Selected "{user_selected}"'
        return user_selected


class RPSApp(App):
    def build(self):
        self.title = "Rock, Paper & Scissors Game"
        Config.set('kivy', 'window_icon', 'images/rock_paper_scissor.jpg')
        return RockPaperScissor()


if __name__ == "__main__":
    RPSApp().run()
