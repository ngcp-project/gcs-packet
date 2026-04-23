from Command.CommandInterface import CommandInterface
from Enum import *

import json
import struct
import warnings

class PatientLocation(CommandInterface):
    FORMAT_STRING = "=BIdd"
    COMMAND_ID = 5

    def __init__(self, Coordinates: tuple[float, float]):
        super().__init__()

        self.Coordinates = Coordinates

    def EncodePacket(self) -> bytes:
        """Encode data packet

        Args:
            coordinates: single (x, y) tuple to encode as doubles

        Returns:
            Encoded data bytes
        """

        # how struct.pack and its format characters (e.g. "BB" or "dd") are explained here https://docs.python.org/3/library/struct.html 
        # encodes the header
        EncodedString = struct.pack(self.FORMAT_STRING, PatientLocation.COMMAND_ID, self.PacketID, self.Coordinates[0], self.Coordinates[1])
    
        return EncodedString
    
    @staticmethod
    def DecodePacket(EncodedString: str, DecodeResult: DecodeFormat) -> CommandInterface | str:
        """Decodes data packet
        
        Args:
            encoded_string: Encoded data packet
            format: "tuple" or "json". Defaults to "tuple" with a warning if not provided.

        Returns:
            (x, y) tuple or JSON string with x and y keys
        """

        ExpectedSize = struct.calcsize(PatientLocation.FORMAT_STRING)

        if len(EncodedString) != ExpectedSize:
            raise ValueError(f"Encoded string length {len(EncodedString)} does not match expected length {ExpectedSize}")
        
        UnpackedData = struct.unpack(PatientLocation.FORMAT_STRING, EncodedString)

        Coordinates = (UnpackedData[2], UnpackedData[3])

        Data = None

        match (DecodeResult):
            case DecodeFormat.Class:
                Data = PatientLocation(Coordinates)

            case DecodeFormat.JSON:
                JSONData = {
                    "Command ID": UnpackedData[0],
                    "Packet ID": UnpackedData[1],
                    "Coordinates": Coordinates
                }

                Data = json.dumps(JSONData)

            case _:
                print("Decode Error")

                return

        return Data