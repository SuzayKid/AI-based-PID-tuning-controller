import serial
import serial.tools.list_ports
import time
import pandas as pd

class MotorInterface:
    def __init__(self, baud_rate=115200, timeout=2):
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.ser = None
        self.port = None

    def connect(self, port=None):
        """
        Connects to the Arduino. If port is None, tries to auto-detect.
        """
        if port:
            self.port = port
        else:
            self.port = self._find_arduino()
            if not self.port:
                raise Exception("Arduino not found. Please specify port manually.")
        
        print(f"Connecting to {self.port}...")
        self.ser = serial.Serial(self.port, self.baud_rate, timeout=self.timeout)
        time.sleep(2) # Wait for Arduino reset
        
        # Flush any startup garbage
        self.ser.reset_input_buffer()
        print("Connected.")

    def _find_arduino(self):
        """
        Auto-detects a likely Arduino port.
        """
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            # Common descriptions for Arduino/USB-Serial chips
            if "Arduino" in p.description or "CH340" in p.description or "CP210x" in p.description or "USB Serial" in p.description:
                return p.device
        
        # If we found nothing but there is only one port, try it
        if len(ports) == 1:
            return ports[0].device
            
        return None

    def send_command(self, kp, ki, kd, setpoint):
        """
        Sends the START command to the firmware.
        """
        if not self.ser or not self.ser.is_open:
            raise Exception("Not connected.")
            
        cmd = f"START:{kp},{ki},{kd},{setpoint}\n"
        self.ser.write(cmd.encode())
        print(f"Sent: {cmd.strip()}")

    def manual_drive(self, pwm):
        """
        Sends manual drive command (M:pwm).
        """
        if not self.ser or not self.ser.is_open:
            raise Exception("Not connected.")
            
        cmd = f"M:{pwm}\n"
        self.ser.write(cmd.encode())
        print(f"Sent: {cmd.strip()}")

    def stop(self):
        """
        Sends STOP command.
        """
        if self.ser and self.ser.is_open:
            self.ser.write(b"STOP\n")
            print("Sent: STOP")

    def read_response(self, timeout=None):
        """
        Reads the CSV stream from Arduino until 'DONE' is received.
        Returns a Pandas DataFrame with the data.
        """
        if not self.ser or not self.ser.is_open:
            raise Exception("Not connected.")

        data_list = []
        start_wait = time.time()
        
        print("Waiting for data stream...")
        
        while True:
            try:
                line = self.ser.readline().decode('utf-8').strip()
            except UnicodeDecodeError:
                continue # Ignore bad bytes
                
            if not line:
                if timeout and (time.time() - start_wait > timeout):
                    print("Timeout waiting for data.")
                    break
                continue

            # print(f"RX: {line}") # Debug print

            if line == "DONE":
                print("Test Complete.")
                break
            
            if line.startswith("ERROR"):
                print(f"Firmware Error: {line}")
                break

            # Parse CSV: TIME,POS,SETPOINT,OUTPUT
            parts = line.split(',')
            if len(parts) == 4:
                try:
                    record = {
                        'time': int(parts[0]),
                        'pos': int(parts[1]),
                        'setpoint': int(parts[2]),
                        'output': int(parts[3])
                    }
                    data_list.append(record)
                except ValueError:
                    continue # Skip partial lines

        return pd.DataFrame(data_list)

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Connection closed.")
