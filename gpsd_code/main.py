#!/usr/bin/env python3

import os
import threading
import json
import time
from uuid import getnode as gma

from robotStateCode import RobotState
import gui
import buttons
import _gps
import ws

from logging import basicConfig, INFO
basicConfig(level=INFO)


class MainApp():

    def __init__(self, gps_rate=None):
        # initialize objects
        self.stop_blink = threading.Event()
        self._gui = gui.GUI(
            on_green=self.green_callback,
            on_blue=self.blue_callback,
            on_red=self.red_callback
        )
        self._buttons = buttons.Buttons(
            on_green=self.green_callback, 
            on_blue=self.blue_callback, 
            on_red=self.red_callback
        )

        self.rs = RobotState()
        print("The first state in the state machine is: %s" % self.rs.state)
        # print("Mac Address: " + str(gma()))
        self._gps = _gps.GPS()

    def set(self, all=None, r=None, g=None, b=None):
        if all is not None:
            r, g, b = all, all, all
        if r is not None:
            self._buttons.setRedLed(r)
            self._gui.setRedButton(r)
        if g is not None:
            self._buttons.setGreenLed(g)
            self._gui.setGreenButton(g)
        if b is not None:
            self._buttons.setBlueLed(b)
            self._gui.setBlueButton(b)

    def set_text(self, desc):
        print(desc)
        self._gui.setDescription(desc)

    def get_text(self):
        print(desc)
        self._gui.getDescription()

    def start(self, gps_rate=None):
        # User login
        # self.user_name = self._gui.waitForLogin() # < blocking
        if os.getenv('USERNAME', None):
            self.user_name = os.getenv('USERNAME')
        else:
            temp_user = '%012x' % gma()
            self.user_name = "picker_"+temp_user.replace(':', '')
            print("User: "+self.user_name)

        # init websocket
        address = os.getenv('WEBSERVER_ADDRESS')
        self._ws = ws.WS(address=address,
                         user_name=self.user_name,
                         update_orders_cb=self.update_orders_cb)

        # setup the main gui window
        self._gui.setupMainWindow()

        self._gui.setUser("User: " + self.user_name)
        self.set_text("Welcome to Call A Robot.")

        # start gps thread
        self._gps.start()

        # start ws thread
        self._ws.start()

        print("Initialization complete")
        if gps_rate is None:
            # we want gps readings as soon as they arrive
            self._gps.set_callback(self._ws.send_gps)

            # start gui thread (tkinter only runs on the main thread :-( )
            self._gui.loopMainWindow()  # < blocking
        else:
            # we want gps readings at a certain rate
            seconds = 1./float(gps_rate)

            while self._gps.has_more_data():
                lat, lon, epx, epy, ts  = self._gps.get_latest_data()

                self._ws.send_gps(lat, lon, epx, epy, ts)

                time.sleep(seconds)

    def stop(self):
        self._gps.stop()
        self._ws.stop()
        self._buttons.cleanup()

    # this receives updated state for the current user
    def update_orders_cb(self, new_state):
        old_state = self.rs.state

        # CONNECTED sent from the coordintor on agent init
        if new_state in ["CONNECTED"]:
            self.set_text("Connected to Server.")
            self.set(True)

        # REGISTERED sent once human_base_init completes, at this point the picker is able to respond
        # car_INIT sent after completion or cancellation
        elif new_state in ["REGISTERED", "car_INIT"]:
            self.set_text("Ready to Call")
            self.set(False)

        # car_ACCEPT sent once robot is assigned by coordinator in response to BEGUN
        elif new_state in ["car_ACCEPT"]:
            self.set_text("A Robot is on the way")
            self.set(g=False, r=True, b=False)
            self.rs.accepted_robot()

        # car_ARRIVED sent once robot has reached the picker
        elif new_state in ["car_ARRIVED"]:
            self.set_text("Load trays on robot then press blue button.")
            self.set(False)
            self.blink_thr = threading.Thread(target=self.blue_blink)
            self.blink_thr.start()
            self.rs.robot_arrived()

        # car_LOADED sent by picker once trays have been loaded
        # elif new_state == "car_LOADED" and old_state == "car_LOADED":
        #     self.stop_blink.set()

        # car_COMPLETE sent by ???
        elif new_state in ["car_COMPLETE"]:
            self.stop_blink.set()

        # Task cancellation from coordinator
        elif new_state in ["car_CANCEL"]:
            self.set_text("Task Has Been Cancelled. \nClick any to Reset")
            self.set(g=False, r=True, b=False)
            self.rs.cancel()


    def green_callback(self, _):
        print("Green button pressed")
        if self.rs.state in ["REGISTERED", "car_INIT"]:
            self.set_text("Calling Robot.")
            self.set(g=True)
            self._ws.call_robot()
            self.rs.call_robot()
            self.stop_blink.clear()
        else:
            txt = self.get_text()
            self.set_text("Cannot call a robot right now.")
            time.sleep(2)
            self.set_text(txt)

    def red_callback(self, _):
        print("Red button pressed")
        if self.rs.state in ["car_CALLED", "car_ACCEPT", "car_ARRIVED"]:
            self.set_text("Cancelling...")
            self.set(r=True)
            self._ws.cancel_robot()
            self.rs.cancel()
            # time.sleep(1)
            # self.set_text("Robot Sucessfully Cancelled.")
            # self.set(g=False, r=False)
            # time.sleep(1)
            # self.set_text("Welcome to Call A Robot.")
        else:
            txt = self.get_text()
            self.set_text("Cannot cancel any robot right now.")
            time.sleep(2)
            self.set_text(txt)

    def blue_callback(self, _):
        if self.rs.state in ["car_ARRIVED"]:
            self.set_text("Thank you the robot will now drive away.")
            self._ws.set_loaded()
            self.rs.robot_loaded()
            # time.sleep(2)
            # self.rs.user_reset()
            # self._ws.set_init()
            # self.set_text("Welcome to Call A Robot.")
        elif self.rs.state in ["car_COMPLETE"]:
            self.set_text("Thank you the robot will now drive away.")
            self._ws.set_init()
            self.rs.reset_session()
        else:
            txt = self.get_text()
            self.set_text("Cannot load a robot right now.")
            time.sleep(2)
            self.set_text(txt)



    def blue_blink(self):        
        while not (self.stop_blink.is_set()):
            self.set(b=True)
            time.sleep(0.5)
            self.set(b=False)
            time.sleep(0.5)


if __name__ == "__main__":
    # pub gps rate
    rate = 2 # hz
    app = MainApp(rate)

    try:
        app.start()
    except KeyboardInterrupt: 
        print ("Exiting")
        app.stop()
