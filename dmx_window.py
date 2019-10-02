#
# DMX Emulator Window - for testing AtHomeDMX
# Copyright © 2019  Dave Hocker (email: AtHomeX10@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the LICENSE file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program (the LICENSE file).  If not, see <http://www.gnu.org/licenses/>.
#

# Python 2/3
import sys
if sys.version_info.major is 3:
    import tkinter as Tk, tkinter.font as tkFont
    from tkinter import ttk
else:
    import Tkinter as Tk, tkFont
from dmx_connection_handler import DMXConnectionHandler

class DMXTestFrame(Tk.Tk):
    def __init__(self, num_channels, polling_interval_ms=30, frame_size=0):
        """
        Constructor
        :param num_channels: Number of pixels in LED string
        :param polling_interval: Polling time in ms.
        """
        # TODO Rework for DMX-512
        super(DMXTestFrame, self).__init__()
        self.title("DMX Emulator")
        self._num_channels = num_channels

        # This is the polling time converted to seconds (e.g. 0.030 = 30ms)
        self._polling_interval = float(polling_interval_ms) / 1000.0
        # How many polling intervals to wait to clear change marker
        self._clear_changes_after = 10.0
        self._reset_changed_count = 0

        # Largest row size, max 32 LEDs per line
        if self._num_channels < 32:
            max_row_size = self._num_channels
        else:
            max_row_size = 32

        # Determine width of a channel for 32 channels per line
        sw = self.winfo_screenwidth()
        # Use 60% of screen width for 32 channels wide
        w = int((sw * 0.6) / 32)
        # Diameter of a channel (aka height of a channel)
        # h = 30
        h = w + 3

        # Fixed pitch font
        self._fixed_font = tkFont.Font(family="Courier New", size=14, weight=tkFont.NORMAL)
        self._small_font = tkFont.Font(family="Helvetica", size=10, weight=tkFont.NORMAL)

        # main frame grid row tracker
        main_gr = 0

        # How many rows of max row size channels do we need?
        nrows = int((self._num_channels - 1) / max_row_size) + 1

        # Height of canvas accounts for border of 1 px
        self._canvas = Tk.Canvas(self, height=(h * nrows) + 4, width=(max_row_size * w) + 4, bd=1, relief="solid")
        self._canvas.grid(row=main_gr, column=0)

        self._channels = []
        self._channel_values = []

        # Top and bottom
        # Top is offset from border
        y0 = 6
        y1 = y0 + h - 8
        nchannels = self._num_channels
        channel_tag_value = 1
        while nchannels > 0:
            if nchannels >= 32:
                row_size = 32
            else:
                row_size = nchannels
            for i in range(row_size):
                # n circles across
                # oval(x0, y0, x1, y1)
                # Left and right
                x0 = (w * i) + 6
                x1 = x0 + w - 3
                # http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/create_oval.html
                # self.channels.append(self.canvas.create_oval(x0, y0, x1, y1))
                # The channel box
                self._channels.append(self._canvas.create_rectangle(x0, y0, x1, y1))

                # The channel box label
                tx = int((x0 + x1) / 2)
                ty = y0 + int(h / 5)
                c = self._canvas.create_text(tx, ty, text=str(channel_tag_value), font=self._small_font)

                # The current channel value
                tx = int((x0 + x1) / 2)
                ty = int((y0 + y1) / 2) + int(h / 4)
                c = self._canvas.create_text(tx, ty, text="---")
                self._canvas.itemconfig(c, tags=(str(channel_tag_value)))
                self._channel_values.append(c)

                channel_tag_value += 1

            # Set up for next row
            y0 += h
            y1 += h
            nchannels -= 32

        main_gr += 1

        # Metrics frame
        self._metrics_frame = Tk.Frame(self, height=h + w + 5, width=(self._num_channels * w))
        self._metrics_frame.grid(row=main_gr, column=0)

        # Metrics frame grid row tracker
        metrics_gr = 0

        # Metrics

        # Polling interval in seconds
        self._speed_wait = Tk.Label(self._metrics_frame, font=self._fixed_font)
        self._speed_wait.grid(row=metrics_gr, column=0)
        self._speed_wait["text"] = "Polling Interval: " + str(self._polling_interval) + "sec"

        # Number of configured channels
        self._frame_pixels = Tk.Label(self._metrics_frame, font=self._fixed_font)
        self._frame_pixels.grid(row=metrics_gr, column=1)
        self._frame_pixels["text"] = "Number channels: " + str(self._num_channels)

        # Number of received DMX data frames
        self._frame_count = 0
        self._frame_count_w = Tk.Label(self._metrics_frame, font=self._fixed_font)
        self._frame_count_w.grid(row=metrics_gr, column=2)
        self._frame_count_w["text"] = "DMX frame count: " + str(self._frame_count)

        main_gr += 1

        # Quit button
        # For some reason, on macOS Mojave, the button text does not show
        # This is a work around using the ttk button and styling
        style = ttk.Style()
        style.map("C.TButton",
                  foreground=[('pressed', 'white'), ('active', 'green')],
                  background=[('pressed', 'blue'), ('active', 'red')]
                  )
        self._q = ttk.Button(self, text="Quit", width=6, command=self.destroy, style="C.TButton")
        self._q.grid(row=main_gr, column=0)

        main_gr += 1

        buffer = Tk.Label(self, text=" ")
        buffer.grid(row=main_gr, column=0)

        # Prime the color and timer event
        self._next_frame()

    def _next_frame(self):
        """
        Process all queued DMX data frames
        :return:
        """
        # Here's where we need to get the next data frame
        frame = DMXConnectionHandler.get_frame()
        while frame:
            # Each frame contains up to 512 channel values
            self._frame_count += 1
            self._frame_count_w["text"] = "Frame count: " + str(self._frame_count)
            for i in range(len(frame)):
                channel_value = int(frame[i])
                self._canvas.itemconfigure(self._channels[i], fill="green")
                self._canvas.itemconfigure(self._channel_values[i], text=str(channel_value))
            # Reset unchanged channels
            for i in range(len(frame), self._num_channels):
                self._canvas.itemconfigure(self._channels[i], fill="")

            # How many poll intervals until it's time to clear change markers
            self._reset_changed_count = int(self._clear_changes_after / self._polling_interval)

            # Check for another DMX data frame
            frame = DMXConnectionHandler.get_frame()

        # Reset changed markers after n polls with no changes
        if self._reset_changed_count > 0:
            self._reset_changed_count -= 1
        elif self._reset_changed_count == 0:
            for i in range(self._num_channels):
                self._canvas.itemconfigure(self._channels[i], fill="")
            self._reset_changed_count = -1

        # Scehdule next polling cycle
        self.after(int(self._polling_interval * 1000.0), self._next_frame)

def run_dmx_window(num_channels, polling_interval):
    test_frame = DMXTestFrame(num_channels, polling_interval_ms=polling_interval)
    test_frame.mainloop()
    print("DMX window closed")