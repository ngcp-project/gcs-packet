from Command.CommandInterface import CommandInterface

import json
import struct

class SearchArea(CommandInterface):
    FORMAT_STRING = "=BI"
    COMMAND_ID = 6

    def __init__(self, coordinates: list):
        self.coordinates = coordinates
        self.packet_id = CommandInterface.generate_packet_id()

    def encode_packet(self) -> bytes:
        """Encode data packet

        Args:
            coordinates: List of (x, y) tuples to encode as doubles

        Returns:
            Encoded data bytes
        """
        # Start with payload and command IDs
        header = struct.pack(self.FORMAT_STRING, SearchArea.COMMAND_ID, self.packet_id)

        # Flatten the list of tuples into a single list of floats
        flat_coords = [item for coord in self.coordinates for item in coord]

        # Build the format string: two bytes for header, then 2 doubles per coordinate
        format_string = f"{len(flat_coords)}d"

        if flat_coords:
            coords_bytes = struct.pack(format_string, *flat_coords)
            encoded_string = header + coords_bytes
        else:
            encoded_string = header

        return encoded_string

    @staticmethod
    def decode_packet(encoded_string) -> int:
        """Decodes data packet
        
        Args:
            encoded_string: Encoded data packet

        Returns:
            Data from encoded data packet
        """
        num_coordinates = (len(encoded_string) - 2) // 16

        if num_coordinates > 6:
            print("Too many coordinates")

        format_string = SearchArea.FORMAT_STRING + "dd" * int(num_coordinates)

        expected_length = struct.calcsize(format_string)

        if len(encoded_string) != expected_length:
            raise ValueError(f"Encoded string length {len(encoded_string)} does not match expected {expected_length} for format '{format_string}'")

        unpacked_data = struct.unpack(format_string, encoded_string)

        coordinates = []

        for i in range(0, (num_coordinates * 2), 2):
            coordinates.append((unpacked_data[(i + 2)], unpacked_data[(i + 3)]))

        json_data = {
            "Command ID": unpacked_data[0],
            "Packet ID": unpacked_data[1],
            "Coordinates": coordinates
        }

        return json.dumps(json_data)