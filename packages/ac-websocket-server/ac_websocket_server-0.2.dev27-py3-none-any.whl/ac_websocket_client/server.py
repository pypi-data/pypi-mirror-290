#!/usr/bin/env python

'''Server UI'''

import tkinter as tk

from ac_websocket_client.objects import (
    GriddedButton, GriddedEntry, GriddedFrame, GriddedLabel, TrafficLight)


class ServerUI(GriddedFrame):
    '''Server UI'''

    def __init__(self, parent):

        super().__init__(grid_row=1, grid_col=0, height_by=3)

        self.parent = parent

        self.configure_columns(1, 1, 4, 1, 1)

        self._buttons = {}
        self._fields = {}
        self._lights = {}

        GriddedLabel(self, grid_row=0, grid_col=0, width=8, text="Game")
        GriddedLabel(self, grid_row=0, grid_col=1, width=8, text="started:")

        self._fields['started'] = tk.StringVar()
        GriddedEntry(self, grid_row=0, grid_col=2,
                     textvariable=self._fields['started'], state=tk.DISABLED)

        self._fields['registered'] = tk.StringVar()
        GriddedLabel(self, grid_row=1, grid_col=1,
                     width=8, text="registered:")
        GriddedEntry(self, grid_row=1, grid_col=2,
                     textvariable=self._fields['registered'], state=tk.DISABLED)

        self._fields['name'] = tk.StringVar()
        GriddedLabel(self, grid_row=2, grid_col=1, width=8, text="name:")
        GriddedEntry(self, grid_row=2, grid_col=2,
                     textvariable=self._fields['name'], state=tk.DISABLED)

        self._fields['track'] = tk.StringVar()
        GriddedLabel(self, grid_row=3, grid_col=1, width=8, text="track:")
        GriddedEntry(self, grid_row=3, grid_col=2,
                     textvariable=self._fields['track'], state=tk.DISABLED)

        self._fields['cars'] = tk.StringVar()
        GriddedLabel(self, grid_row=4, grid_col=1, width=8, text="cars:")
        GriddedEntry(self, grid_row=4, grid_col=2,
                     textvariable=self._fields['cars'], state=tk.DISABLED)

        self._fields['sessions'] = {}
        self._lights['sessions'] = {}

        self._fields['sessions']['Practice'] = tk.StringVar()
        GriddedLabel(self, grid_row=5, grid_col=1,
                     width=8, text="practice session:")
        GriddedEntry(self, grid_row=5, grid_col=2,
                     textvariable=self._fields['sessions']['Practice'], state=tk.DISABLED)
        self._lights['sessions']['Practice'] = TrafficLight(
            self, row=5, column=4)
        self._lights['sessions']['Practice'].gray()

        self._fields['sessions']['Qualify'] = tk.StringVar()
        GriddedLabel(self, grid_row=6, grid_col=1,
                     width=8, text="qualify session:")
        GriddedEntry(self, grid_row=6, grid_col=2,
                     textvariable=self._fields['sessions']['Qualify'], state=tk.DISABLED)
        self._lights['sessions']['Qualify'] = TrafficLight(
            self, row=6, column=4)
        self._lights['sessions']['Qualify'].gray()

        self._fields['sessions']['Race'] = tk.StringVar()
        GriddedLabel(self, grid_row=7, grid_col=1,
                     width=8, text="race session:")
        GriddedEntry(self, grid_row=7, grid_col=2,
                     textvariable=self._fields['sessions']['Race'], state=tk.DISABLED)
        self._lights['sessions']['Race'] = TrafficLight(self, row=7, column=4)
        self._lights['sessions']['Race'].gray()

        self._buttons['game'] = tk.StringVar(value='Start Game')
        GriddedButton(self, grid_row=0, grid_col=3,
                      textvariable=self._buttons['game'],
                      command=lambda: self.parent.loop.create_task(self.parent.toggle_game()))
        self._lights['game'] = TrafficLight(self, row=0, column=4)

        self._buttons['lobby'] = tk.StringVar(value='(Re)register')
        GriddedButton(self, grid_row=1, grid_col=3,
                      textvariable=self._buttons['lobby'],
                      command=lambda: self.parent.loop.create_task(self.parent.toggle_registration()))
        self._lights['lobby'] = TrafficLight(self, row=1, column=4)

        self.update_ui()

    def update_ui(self):
        '''Update the UI with the contents of the parent.server'''

        if self.parent.states.is_started:
            self._fields['started'].set(
                self.parent.server.get('timestamp', None))
            self._buttons['game'].set('Stop Game')
            self._lights['game'].green()
            self._fields['name'].set(self.parent.server.get('name', ''))
            self._fields['track'].set(self.parent.server.get('track', ''))
            self._fields['cars'].set(self.parent.server.get('cars', ''))
        else:
            self._fields['started'].set('Not started')
            self._buttons['game'].set('Start Game')
            self._lights['game'].red()
            self._fields['name'].set('')
            self._fields['track'].set('')
            self._fields['cars'].set('')

        if self.parent.states.is_registered and self.parent.states.is_started:
            self._fields['registered'].set(
                self.parent.lobby.get('since', 'unknown'))
            self._buttons['lobby'].set('Re-register')
            self._lights['lobby'].green()
        else:
            self._fields['registered'].set('Not registered')
            self._buttons['lobby'].set('Register')
            self._lights['lobby'].red()

        if sessions := self.parent.sessions:
            for session_type in sessions:
                if session_type not in ('Practice', 'Qualify', 'Race'):
                    return
                session_active = sessions[session_type]['active']
                if session_active:
                    self._lights['sessions'][session_type].green()
                else:
                    self._lights['sessions'][session_type].gray()
                session_description = str(
                    sessions[session_type]['time'])
                if sessions[session_type]['laps'] == 0:
                    session_description += ' minutes'
                else:
                    session_description += ' laps'
                self._fields['sessions'][session_type].set(session_description)
