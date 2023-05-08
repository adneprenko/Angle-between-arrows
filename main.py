import collections
import math

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.graphics import Color, Line
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty

Builder.load_string('''

<MyClockWidget>:
    on_pos: self.update_clock()
    on_size: self.update_clock()
    FloatLayout
        id: face
        size_hint: None, None
        pos_hint: {"center_x":0.5, "center_y":0.5}
        size: 0.9*min(root.size), 0.9*min(root.size)
        canvas:
            Color:
                rgb: 0.1, 0.1, 0.1
            Ellipse:
                size: self.size
                pos: self.pos
    FloatLayout
        id: hands
        size_hint: None, None
        pos_hint: {"center_x":0.5, "center_y":0.5}
        size: 0.9*min(root.size), 0.9*min(root.size)

    FloatLayout
        id: angle
        size_hint: None, None
        pos_hint: {"center_x":0.4, "center_y":0.5}
        size: 0.9*min(root.size), 0.9*min(root.size)

    FloatLayout
        id: btn
        size_hint: .2, .1
        pos_hint: {"center_x":0.1, "center_y":0}
        size: 0.1*min(root.size), 0.1*min(root.size)
        
    FloatLayout
        id: btn_ex
        size_hint: .2, .1
        pos_hint: {"center_x":0.7, "center_y":0}
        size: 0.1*min(root.size), 0.1*min(root.size)
''')

Position = collections.namedtuple('Position', 'x y')


class MyClockWidget(FloatLayout):
    def on_parent(self, myclock, parent):
        """
        Add number labels when added in widget hierarchy
        """
        for i in range(1, 13):
            number = Label(
                text=str(i),
                pos_hint={
                    # pos_hint is a fraction in range (0, 1)
                    "center_x": 0.5 + 0.45 * math.sin(2 * math.pi * i / 12),
                    "center_y": 0.5 + 0.45 * math.cos(2 * math.pi * i / 12),
                }
            )
            self.ids["face"].add_widget(number)
        angle_h = 30 * h + (m / 60) * 30
        angle_m = 6 * m
        main_result = abs(angle_h - angle_m)
        if main_result > 180: main_result = 360 - main_result
        angle = Label(
            text="Angle is: " + str(abs(main_result)),
            pos_hint={
                "center_x": 1,
                "center_y": 1,
            }
        )
        self.ids["angle"].add_widget(angle)
        btn = Button(
            text="Again?",
            pos_hint={
                "center_x": 1,
                "center_y": 1,
            }
        )
        btn.bind(on_press=on_pr_btn)
        self.ids["btn"].add_widget(btn)
        btn_ex = Button(
            text="Exit",
            pos_hint={
                "center_x": 1,
                "center_y": 1,
            }
        )
        btn_ex.bind(on_press=on_pr_ex)
        self.ids["btn_ex"].add_widget(btn_ex)

    def position_on_clock(self, fraction, length):
        """
        Calculate position in the clock using trigonometric functions
        """
        center_x = self.size[0] / 2
        center_y = self.size[1] / 2
        return Position(
            center_x + length * math.sin(2 * math.pi * fraction),
            center_y + length * math.cos(2 * math.pi * fraction),
        )

    def update_clock(self, *args):
        """
        Redraw clock hands
        """
        # time = datetime.datetime.now()
        time_hour = h
        time_minute = m
        hands = self.ids["hands"]
        # seconds_hand = self.position_on_clock(time.second/60, length=0.45*hands.size[0])
        minutes_hand = self.position_on_clock(time_minute / 60, length=0.40 * hands.size[0])
        hours_hand = self.position_on_clock(time_hour / 12 + time_minute / 720, length=0.25 * hands.size[0])

        hands.canvas.clear()
        with hands.canvas:
            # Color(0.2, 0.5, 0.2)
            # Line(points=[hands.center_x, hands.center_y, seconds_hand.x, seconds_hand.y], width=1, cap="round")
            Color(0.3, 0.6, 0.3)
            Line(points=[hands.center_x, hands.center_y, minutes_hand.x, minutes_hand.y], width=2, cap="round")
            Color(0.4, 0.7, 0.4)
            Line(points=[hands.center_x, hands.center_y, hours_hand.x, hours_hand.y], width=3, cap="round")
def on_pr_btn(instance):
    global h
    h = 25
    App.get_running_app().stop()

def on_pr_ex(instance):
    global h
    h = 35
    App.get_running_app().stop()



class MyApp(App):
    def build(self):
        self.title = 'AD Company'
        clock_widget = MyClockWidget()
        Clock.schedule_once(clock_widget.update_clock, 0)
        return clock_widget


class text_widget(FloatLayout):
    hello_label = ObjectProperty()
    name_input = ObjectProperty()

    def get_h_m(self):
        global h, m
        # check correct input
        try:
            h = int(self.name_input.text.split(":")[0])
            m = int(self.name_input.text.split(":")[1])
            if h > 24 or h < 0: raise IndexError
            if m > 60 or m < 0: raise IndexError
        except:
            show_popup()
        else:
            App.get_running_app().stop()


class FirstApp(App):
    kv = Builder.load_file("kv.kv")

    def build(self):
        self.title = 'AD Company'
        return text_widget()


class P(FloatLayout):
    pass


def show_popup():
    show = P()
    popupWindow = Popup(title="Error", content=show, size_hint=(None, None), size=(700, 140), auto_dismiss=True)
    popupWindow.open()


if __name__ == '__main__':

    h = 25
    while h == 25:
        FirstApp().run()
        MyApp().run()

