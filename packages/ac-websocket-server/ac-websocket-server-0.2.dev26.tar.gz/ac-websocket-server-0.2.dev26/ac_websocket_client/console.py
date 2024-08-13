#!/usr/bin/env python

'''Console UI'''

import tkinter as tk

from ac_websocket_client.objects import (
    GriddedButton, GriddedEntry, GriddedFrame,
    GriddedLabel, GriddedListbox, GriddedText, TrafficLight)

USE_TEXT = False


class ConsoleUI(GriddedFrame):
    '''Console UI'''

    def __init__(self, parent):

        super().__init__(grid_row=4, grid_col=0, height_by=3)

        self.parent = parent

        self.configure_columns(1, 1, 4, 1, 1)

        GriddedLabel(self, grid_row=0, grid_col=0, width=8, text="Console")
        GriddedLabel(self, grid_row=0, grid_col=1, width=8, text="command:")

        self._field = tk.StringVar()
        self.entry = GriddedEntry(self, grid_row=0, grid_col=2,
                                  textvariable=self._field)
        self.entry.bind('<Return>', self._async_send_command)

        self._button = tk.StringVar(value='Send')
        GriddedButton(self, grid_row=0, grid_col=3,
                      textvariable=self._button,
                      command=lambda: self.parent.loop.create_task(self.parent.send_command()))

        self._light = TrafficLight(self, row=0, column=4)
        self._light.gray()

        if USE_TEXT:
            self._text = GriddedText(
                self, grid_row=1, grid_col=0, grid_span=5)
        else:
            self._listbox = GriddedListbox(
                self, grid_row=1, grid_col=0, grid_span=5)

        self.update_ui()

    def _async_send_command(self, _event):
        '''Send command to ACWS server'''
        self.parent.loop.create_task(self.parent.send_command())

    def input(self):
        '''Return command input to be sent to ACWS server'''
        return self._field.get()

    def output(self, timestamp: str, lines: str, fg='Black'):
        '''Send command output to console.'''

        output_fmt = {'fg': fg}

        for line in lines.splitlines():
            if USE_TEXT:
                self._text.insert(tk.END, f'{timestamp}: {line}\n')
            else:
                self._listbox.insert(tk.END, f'{timestamp}: {line}\n')
                self._listbox.itemconfig(tk.END, output_fmt)

        self.update_ui()

    def update_ui(self):
        '''Update the UI'''

        if USE_TEXT:
            self._text.yview(tk.END)
        else:
            self._listbox.yview(tk.END)
