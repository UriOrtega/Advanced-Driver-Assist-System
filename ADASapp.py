import threading
from functools import partial
from kivy.app import App
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.screenmanager import ScreenManager, Screen

from ADASCore import ADAS


class MainScreen(Screen):
    pass


class Manager(ScreenManager):
    pass


class Main(App):
    frames = ADAS.ADAS_sys()
    do_vid = True

    def build(self):

        # start the camera access code on a separate thread
        # if this was done on the main thread, GUI would stop
        # daemon=True means kill this thread when app stops
        threading.Thread(target=self.doit, daemon=True).start()

        sm = ScreenManager()
        self.main_screen = MainScreen()
        sm.add_widget(self.main_screen)
        return sm

    def doit(self):
        # this code is run in a separate thread
        self.do_vid = True  # flag to stop loop

        # start processing loop
        for frame in self.frames:
            if self.do_vid == True:
                Clock.schedule_once(partial(self.display_frame, frame))
            else:
                break

    def stop_vid(self):
        # stop the video capture loop
        self.do_vid = False
        self.main_screen.ids.list.size_hint = 1, 1
        self.main_screen.ids.l1.visible = True
        self.main_screen.ids.l2.visible = True
        self.main_screen.ids.lSlider.visible = True
        self.main_screen.ids.rSlider.visible = True

    def slide_change(self, widget):
        ADAS.set_lines(int(widget.value))

    def file_fire_select(self, *args):
        try:
            file_selected = args[1][0]
            print(file_selected)
            self.frames = ADAS.ADAS_sys(file_selected)
            self.main_screen.ids.list.size_hint = 0, 0
            self.main_screen.ids.l1.visible = False
            self.main_screen.ids.l2.visible = False
            self.main_screen.ids.lSlider.visible = False
            self.main_screen.ids.rSlider.visible = False

        except:
            print('No Video')

        threading.Thread(target=self.doit, daemon=True).start()

    def display_frame(self, frame, dt):
        # display the current video frame in the kivy Image widget

        # create a Texture the correct size and format for the frame
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')

        # copy the frame data into the texture
        texture.blit_buffer(frame.tobytes(order=None), colorfmt='bgr', bufferfmt='ubyte')

        # flip the texture (otherwise the video is upside down
        texture.flip_vertical()

        # actually put the texture in the kivy Image widget
        self.main_screen.ids.vid.texture = texture


if __name__ == '__main__':
    Main().run()
