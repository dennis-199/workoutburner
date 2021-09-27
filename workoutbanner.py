from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
import kivy.utils
class WorkoutBanner(GridLayout):

    def __init__(self, **kwargs):
        self.rows = 1
        super(WorkoutBanner, self).__init__()

        left = FloatLayout()
        left_image = Image (source="icons/" + kwargs['workout_image'], size_hint=(1, 0.8), pos_hint = {"top":1,"right":1})
        left_label = Label(text=kwargs['description'], size_hint =(1, .2), pos_hint={"top":2, "left":1})
        left.add_widget(left_image)
        left.add_widget(left_label)


        middle = FloatLayout()
        middle_image = Image(source="icons/" + kwargs['type_image'], size_hint=(1, 0.8), pos_hint = {"top":1,"right":1})
        middle_label = Label(text = str(kwargs['number']) + " " + kwargs['units'], size_hint =(1, .2), pos_hint={"top":2, "right":1})
        middle.add_widget(middle_image)
        middle.add_widget(middle_label)

        self.add_widget(left)
        self.add_widget(middle)

