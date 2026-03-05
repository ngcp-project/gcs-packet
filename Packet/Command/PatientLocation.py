from Command.CommandInterface import CommandInterface

import json
import struct
import warnings

class PatientLocation(CommandInterface):
    FORMAT_STRING = "=BIdd"
    COMMAND_ID = 5

    def __init__(self, coordinates: tuple[float, float]):
        self.coordinates = coordinates
        self.packet_id = CommandInterface.generate_packet_id()

    def encode_packet(self) -> bytes:
        """Encode data packet

        Args:
            coordinates: single (x, y) tuple to encode as doubles

        Returns:
            Encoded data bytes
        """

        # how struct.pack and its format characters (e.g. "BB" or "dd") are explained here https://docs.python.org/3/library/struct.html 
        # encodes the header
        encoded_string = struct.pack(self.FORMAT_STRING, PatientLocation.COMMAND_ID, self.packet_id, self.coordinates[0], self.coordinates[1])
    
        return encoded_string
    
    
    @staticmethod
    def decode_packet(encoded_string):
        """Decodes data packet
        
        Args:
            encoded_string: Encoded data packet
            format: "tuple" or "json". Defaults to "tuple" with a warning if not provided.

        Returns:
            (x, y) tuple or JSON string with x and y keys
        """
        #if format is None:
            #warnings.warn("Format not specified in decode_packet, defaulting to 'tuple'", UserWarning)

        expected_size = struct.calcsize(PatientLocation.FORMAT_STRING)

        if len(encoded_string) != expected_size:
            raise ValueError(f"Encoded string length {len(encoded_string)} does not match expected length {expected_size}")
        
        unpacked_data = struct.unpack(PatientLocation.FORMAT_STRING, encoded_string)

        # we are ignoring the "=BB" part here which is the header, "unpacked_data" would look like [1, 5, <some double value>, <some double value>]
        coordinates = (unpacked_data[2], unpacked_data[3])
        
        #if format == "json":
            #return json.dumps({"x": x, "y": y}, indent=2)

        json_data = {
            "Command ID": unpacked_data[0],
            "Packet ID": unpacked_data[1],
            "Coordinates": coordinates
        }
        
        return json.dumps(json_data)
        
    
