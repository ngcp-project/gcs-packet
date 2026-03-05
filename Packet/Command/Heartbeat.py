from Command.CommandInterface import CommandInterface
from Enum.ConnectionStatus import ConnectionStatus

import json
import struct

class Heartbeat(CommandInterface):
    FORMAT_STRING = "BIH"
    COMMAND_ID = 1

    def __init__(self, connection_status: ConnectionStatus):
        self.connection_status = connection_status
        self.packet_id = CommandInterface.generate_packet_id()

    def encode_packet(self) -> bytes:
        """Encode data packet

        Args:
            connection_status: Status for emergency stop: 0 = Enable Emergency Stop, 1 = Disable Emergency Stop

        Returns:
            Encoded data bytes
        """
        encoded_string = struct.pack(Heartbeat.FORMAT_STRING, Heartbeat.COMMAND_ID, self.packet_id, self.connection_status.value)

        return encoded_string

    @staticmethod
    def decode_packet(encoded_string) -> int:
        """Decodes data packet
        
        Args:
            encoded_string: Encoded data packet

        Returns:
            Data from encoded data packet
        """
        expected_size = 10

        if len(encoded_string) != expected_size:

            print("Invalid String Size in hb")

        unpacked_data = struct.unpack(Heartbeat.FORMAT_STRING, encoded_string)

        json_data = {
            "Command ID": unpacked_data[0],
            "Packet ID": unpacked_data[1],
            "Connection Status": unpacked_data[2]
        }

        return json.dumps(json_data)
