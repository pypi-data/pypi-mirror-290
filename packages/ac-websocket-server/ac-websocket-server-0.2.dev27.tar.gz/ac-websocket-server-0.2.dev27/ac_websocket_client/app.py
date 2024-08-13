#!/usr/bin/env python

'''Assetto Corsa Websockets App'''

import asyncio
from concurrent.futures import TimeoutError as ConnectionTimeoutError
import json
import re
import sys
import tkinter as tk
from datetime import datetime

import websockets

from ac_websocket_client import DEBUG
from ac_websocket_client.connection import ConnectionUI
from ac_websocket_client.console import ConsoleUI
from ac_websocket_client.driver import DriverUI
from ac_websocket_client.objects import APP_TITLE
from ac_websocket_client.server import ServerUI
from ac_websocket_client.tracker import TrackerUI
from ac_websocket_server.protocol import Protocol


class App(tk.Tk):
    '''Wrapper class for Tk app'''

    UPDATE_INTERVAL = 1/120

    class States():
        '''Internal States of application'''
        is_connected: bool = False
        is_registered: bool = False
        is_started: bool = False
        is_tracking: bool = False

    def __init__(self, loop, url=None):
        super().__init__()

        self.loop = loop
        self.protocol("WM_DELETE_WINDOW", self.stop_ui)

        self.consumer_queue = asyncio.Queue()
        self.producer_queue = asyncio.Queue()

        self.states = App.States()

        self.drivers = {}
        self.entries = {}

        self.lobby = {}
        self.server = {}
        self.sessions = {}
        self.tracker = {}

        self.url = url
        self.websocket = None

        self.tasks = []

        self._create_ui()

    def _create_ui(self):
        '''Build the UI elements'''

        self.title(APP_TITLE)
        self.config(bg='lightgray')

        self.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=1)
        self.connection_ui = ConnectionUI(self)

        self.rowconfigure(1, weight=6)
        self.server_ui = ServerUI(self)

        self.rowconfigure(2, weight=1)
        self.tracker_ui = TrackerUI(self)

        self.rowconfigure(3, weight=4)
        self.driver_ui = DriverUI(self)

        self.rowconfigure(4, weight=4)
        self.console_ui = ConsoleUI(self)

        self.tasks.append(self.loop.create_task(self._monitor()))

        if DEBUG:
            self.update()
            self._debug_ui(self, 0)

    def _debug_ui(self, w, depth=0):
        '''Print debug information on UI'''
        print('  ' * depth + f'{w.winfo_class()} w={str(w.winfo_width())}/{str(w.winfo_reqwidth())} h={str(w.winfo_height())}/{str(w.winfo_reqheight())} x/y=+{str(w.winfo_x())}+{str(w.winfo_y())}')
        for i in w.winfo_children():
            self._debug_ui(i, depth+1)

    async def _handler(self, websocket):
        '''Handle websocket tasks'''
        consumer_task = asyncio.create_task(self._handler_consumer(websocket))
        producer_task = asyncio.create_task(self._handler_producer(websocket))
        _done, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()

        await self.consumer_queue.put(Protocol.success(data={'sent': {'websocket.cancel()': self.url}}))

    async def _handler_consumer(self, websocket):
        '''Handle messages received from websocket'''
        async for msg in websocket:
            await self.consumer_queue.put(msg)

    async def _handler_producer(self, websocket):
        '''Handle messages received to send on websocket'''
        while True:
            try:
                message = await self.producer_queue.get()
                await websocket.send(message)
                await self.consumer_queue.put(Protocol.success(data={'sent': message}))
            except Exception:
                print('\n> Connection Closing', file=sys.stderr)
                return

    async def _monitor(self):
        '''Monitor incoming messages and send to connection listbox'''
        while True:
            try:
                input_line = json.loads(await self.consumer_queue.get())

                output_timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                output_lines = ''

                if error_msg := input_line.get('error', None):

                    if error_msg['msg'] == 'ERROR,INVALID SERVER,CHECK YOUR PORT FORWARDING SETTINGS':
                        self.states.is_registered = False
                        self.server_ui.update_ui()

                    output_lines = json.dumps(error_msg, indent=4)
                    self.console_ui.output(
                        output_timestamp, output_lines, fg='Red')
                    continue

                if success_msg := input_line.get('data', None):

                    if success_msg.get('sent', None):

                        output_lines = json.dumps(success_msg, indent=4)
                        self.console_ui.output(
                            output_timestamp, output_lines, fg='Black')
                        continue

                    if driver_msg := success_msg.get('driver', None):
                        if guid := driver_msg.get('guid', None):
                            if driver_joining := driver_msg.get('msg', None):
                                slot = driver_msg['slot']
                                self.entries[slot]['guid'] = guid
                                self.entries[slot]['drivername'] = driver_msg['name']
                                if 'joining' in driver_joining:
                                    self.drivers[guid] = driver_msg
                                    self.entries[slot]['connected'] = 'Yes'
                                else:
                                    self.entries[slot]['connected'] = 'No'
                                    del self.drivers[guid]
                                self.driver_ui.update_ui()

                    if lobby := success_msg.get('lobby', None):
                        self.lobby = lobby
                        self.states.is_registered = self.lobby['connected']
                        self.server_ui.update_ui()

                    if server_msg := success_msg.get('server', None):
                        # Only process 'full' server objects
                        if server_msg.get('name', None):
                            self.server = server_msg
                            if not self.states.is_started:
                                self.states.is_started = server_msg.get(
                                    'running', False)
                            self.server_ui.update_ui()
                        if entries := server_msg.get('entries'):
                            _entries = {}
                            for entry in entries:
                                slot = int(re.sub(r'\D', '', entry))
                                _entries[slot] = entries[entry]
                                _entries[slot]['connected'] = 'No'
                        if lobby := server_msg.get('lobby', None):
                            self.lobby = lobby
                            self.states.is_registered = self.lobby['connected']
                        self.driver_ui.update_ui()

                    if generic_msg := success_msg.get('msg', None):
                        if generic_msg == 'Stracker started' or re.search(r'^.*stracker.*is running.*$', generic_msg):
                            self.states.is_tracking = True
                            self.tracker_ui.update_ui()
                        if generic_msg == 'Stracker server stopped':
                            self.states.is_tracking = False
                            self.tracker_ui.update_ui()
                        if generic_msg == 'Assetto Corsa server started':
                            self.states.is_started = True
                            self.server_ui.update_ui()
                        if generic_msg == 'Assetto Corsa server stopped':
                            self.states.is_started = False
                            self.server_ui.update_ui()

                    if tracker_msg := success_msg.get('stracker', None):
                        self.tracker = tracker_msg
                        self.states.is_tracking = self.tracker['running']
                        self.tracker_ui.update_ui()

                    if sessions_msg := success_msg.get('sessions', None):
                        self.sessions = sessions_msg
                        self.server_ui.update_ui()

                    output_lines = json.dumps(success_msg, indent=4)
                    self.console_ui.output(
                        output_timestamp, output_lines, fg='Green')

                else:
                    output_lines = json.dumps(input_line, indent=4)
                    self.console_ui.output(
                        output_timestamp, output_lines, fg='Purple')

            except Exception as err:
                print(
                    f'Exception: "{err}" caught when processing:\n{input_line}')

    async def send_command(self):
        '''Send command to ACWS server'''

        if self.states.is_connected:
            if command := self.console_ui.input():
                await self.consumer_queue.put(Protocol.success(data={'sent': command}))
                await self.producer_queue.put(command)
        else:
            await self.consumer_queue.put(Protocol.error(msg='Not connected to ACWS server'))

    async def start_ui(self, interval=UPDATE_INTERVAL):
        '''Start a the update of the UI'''
        while True:
            self.update()
            await asyncio.sleep(interval)

    def stop_ui(self):
        '''Cleanup all tasks'''
        for task in self.tasks:
            task.cancel()
        self.loop.stop()
        self.destroy()

    async def toggle_connection(self):
        '''Connect to the websocket server'''

        if self.states.is_connected:
            await self.websocket.close()
            return

        if not self.url:
            return

        try:
            await self.consumer_queue.put(Protocol.success(data={'sent': {'websocket.connect()': self.url}}))
            websocket = await asyncio.wait_for(websockets.connect(self.url), 10)
            self.title(f'{APP_TITLE} - Connected to {self.url}')
            self.states.is_connected = True
            self.connection_ui.update_ui()
            self.websocket = websocket
            await self.producer_queue.put('server info')
            await self.producer_queue.put('server sessions')
            await self.producer_queue.put('tracker status')
            await self._handler(websocket)
            await self.consumer_queue.put(Protocol.success(msg=f'Disconnecting from {self.url}'))
            self.websocket = None
            self.title(f'{APP_TITLE}')
            self.states.is_connected = False
            self.states.is_started = False
            self.states.is_tracking = False
            self._update_ui()
        except ConnectionTimeoutError as _error:
            await self.consumer_queue.put(Protocol.error(msg=str(f'Timeout connecting to {self.url}')))
        except OSError as error:
            await self.consumer_queue.put(Protocol.error(msg=str(error)))

    async def toggle_game(self):
        '''Start the game'''

        if self.states.is_connected:
            if not self.states.is_started:
                await self.producer_queue.put('server start')
                await self.producer_queue.put('server info')
            else:
                await self.producer_queue.put('server stop')
                await self.producer_queue.put('server info')
        else:
            await self.consumer_queue.put(Protocol.error(msg='Not connected to ACWS server'))

        self.server_ui.update_ui()

    async def toggle_registration(self):
        '''(Re)-register in lobby'''

        if self.states.is_connected:
            await self.producer_queue.put('lobby restart')
        else:
            await self.consumer_queue.put(Protocol.error(msg='Not connected to ACWS server'))

        self.server_ui.update_ui()

    async def toggle_tracker(self):
        '''Toggle tracker'''

        if self.states.is_connected:
            if not self.states.is_tracking:
                await self.producer_queue.put('tracker start')
            else:
                await self.producer_queue.put('tracker stop')
        else:
            await self.consumer_queue.put(Protocol.error(msg='Not connected to ACWS server'))

        self.tracker_ui.update_ui()

    async def update_grid(self,
                          by_finishing: bool = None,
                          by_reverse: bool = None, write: bool = None):
        '''Set the grid order'''

        if self.states.is_connected:
            if by_finishing:
                await self.producer_queue.put('grid finish')
                return
            if by_reverse:
                await self.producer_queue.put('grid reverse')
                return
            if write:
                await self.producer_queue.put('grid save')
                return
            await self.producer_queue.put('grid entries')
        else:
            await self.consumer_queue.put(Protocol.error(msg='Not connected to ACWS server'))

    def _update_ui(self):
        '''Update all UI elements'''

        self.connection_ui.update_ui()
        self.console_ui.update_ui()
        self.driver_ui.update_ui()
        self.server_ui.update_ui()
        self.tracker_ui.update_ui()
        self.tracker_ui.update_ui()
