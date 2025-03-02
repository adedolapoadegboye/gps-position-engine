import scipy
import serial
from collections import deque
from utils import DEBUG

class GPSReceiver:
    def __init__(self, serial_port=None, baudrate=115200, file_input=None):
        """
        Handles GPS input from a live serial receiver or a recorded file.

        Args:
            serial_port (str): Serial port for live GPS receiver.
            baudrate (int): Baud rate for serial communication.
            file_input (str): File path for recorded RTCM data.
        """
        self.serial_port = serial_port
        self.file_input = file_input
        self.data_queue = deque()

        if serial_port:
            try:
                self.ser = serial.Serial(serial_port, baudrate, timeout=1)
                self.serial_reader = self.ser.read(2056)  # Initialize serial reader
                print(f"✅ Successfully connected to GPS receiver on {serial_port} at {baudrate} baud.") if DEBUG else None
            except serial.SerialException as e:
                print(f"❌ Failed to connect to GPS receiver on {serial_port}: {e}") if DEBUG else None
                self.ser = None  # Prevent further issues

        elif file_input:
            try:
                self.load_file_data()
                print(f"✅ Successfully loaded RTCM data from file: {file_input}") if DEBUG else None
            except Exception as e:
                print(f"❌ Failed to load RTCM file {file_input}: {e}") if DEBUG else None
                self.data_queue = deque()  # Reset data queue

    def load_file_data(self):
        """Load RTCM messages from a pre-recorded file."""
        data = scipy.io.loadmat(self.file_input)
        self.data_queue.extend(data['data'][0])

    def get_next_message(self):
        """
        Retrieve the next raw RTCM message from serial or file.
        - If serial input, reads binary RTCM and logs output.
        - If file input, dequeues preloaded RTCM messages.

        Returns:
            Raw RTCM message or None if no data is available.
        """
        if self.serial_port:
            try:
                # Read binary RTCM message
                raw_msg = self.serial_reader  # pyrtcm automatically reads binary
                if raw_msg:
                    return raw_msg  # Pass parsed RTCM object to next step
            except StopIteration:
                return None

        elif self.file_input and self.data_queue:
            return self.data_queue.popleft()

        return None
