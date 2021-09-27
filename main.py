from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label
from workoutbanner import WorkoutBanner
from functools import partial
from os import walk
from myfirebase import MyFirebase
import requests
import json


class HomeScreen(Screen):
    pass

class LoginScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class ChangeAvatarScreen(Screen):
    pass

class LabelButton(ButtonBehavior, Label):
    pass

class ImageButton(ButtonBehavior, Image):
    pass


GUI = Builder.load_file("main.kv")
class MainApp(App):
    my_friend_id = 1
    def build(self):
        self.my_firebase = MyFirebase()

        return GUI
    def on_start(self):


        # Get database data
        result = requests.get("https://public-transport-3f985-default-rtdb.firebaseio.com/" + str(self.my_friend_id)+ ".json")
        data = json.loads(result.content.decode())
        # Get and update avatar image
        avatar_image = self.root.ids['avatar_image']
        avatar_image.source = "icons/avatars/"+ data["avatar"]
        # populate avatar grid
        avatar_grid = self.root.ids['change_avatar_screen'].ids['avatar_grid']
        for root_dir, folder, files in walk("icons/avatars"):
            for f in files:
                img = ImageButton(source="icons/avatars/" + f, on_release=partial(self.change_avatar, f))
                avatar_grid.add_widget(img)


        #get and update streak label
        streak_label = self.root.ids['home_screen'].ids['streak_label']
        streak_label.text = data['streak']

        #Get and update friend id label

        friend_id_label = self.root.ids['settings_screen'].ids['friend_id_label']
        friend_id_label.text = "Friend ID: "+str(self.my_friend_id)

        banner_grid = self.root.ids['home_screen'].ids['banner_grid']
        workouts = data['workouts'][1:]
        for workout in workouts:
            w = WorkoutBanner(workout_image=workout['workout_image'],description=workout['description'],
                              type_image=workout['type_image'], number=workout['number'], units=workout['units'])
            banner_grid.add_widget(w)
        self.change_screen("home_screen")





    def change_avatar(self, image, widget_id):

        avatar_image = self.root.ids['avatar_image']
        avatar_image.source = "icons/avatars/"+ image
        my_data = '{"avatar": "%s"}' %image
        requests.patch("https://public-transport-3f985-default-rtdb.firebaseio.com/" + str(self.my_friend_id) + ".json",data =my_data)
        self.change_screen("settings_screen")

        pass


    def change_screen(self, screen_name):
        screen_manager=self.root.ids['screen_manager']
        screen_manager.current = screen_name
        #screen_manager = self.root.ids



MainApp().run()
