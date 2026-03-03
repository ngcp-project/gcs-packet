from Command.CommandInterface import CommandInterface

import json
import struct

class EmergencyStop(CommandInterface):
    FORMAT_STRING = "BIB"
    COMMAND_ID = 2

    def __init__(self, stop_status: int):
        self.stop_status = stop_status
        self.packet_id = CommandInterface.generate_packet_id()

    def encode_packet(self) -> bytes:
        """Encode data packet

        Args:
            stop_status: Status for emergency stop: 0 = Enable Emergency Stop, 1 = Disable Emergency Stop

        Returns:
            Encoded data bytes
        """
        encoded_string = struct.pack(EmergencyStop.FORMAT_STRING, EmergencyStop.COMMAND_ID, self.packet_id, self.stop_status)

        return encoded_string

    @staticmethod
    def decode_packet(encoded_string) -> int:
        """Decodes data packet
        
        Args:
            encoded_string: Encoded data packet

        Returns:
            Data from encoded data packet
        """
        expected_size = 9

        if len(encoded_string) != expected_size:
            print("Invalid String Size")

        unpacked_data = struct.unpack(EmergencyStop.FORMAT_STRING, encoded_string)

        json_data = {
            "Command ID": unpacked_data[0],
            "Packet ID": unpacked_data[1],
            "Stop Status": unpacked_data[2]
        }

        return json.dumps(json_data)
