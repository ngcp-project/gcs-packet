from Command.CommandInterface import CommandInterface
from Enum import *

import json
import struct

class AddZone(CommandInterface):
    FORMAT_STRING = "=BIHB"
    COMMAND_ID = 3
    ZONE_ID = 0

    def __init__(self, Zone: ZoneType, Coordinates: list):
        super().__init__()

        self.Coordinates = Coordinates
        self.Zone = Zone
        self.ZoneID = AddZone.ZONE_ID

        if ((len(self.Coordinates) < 3) or (len(self.Coordinates) > 6)):
            raise Exception("Invalid Coordinate Count")
        
        AddZone.ZONE_ID += 1

    def EncodePacket(self) -> bytes:
        """Encode data packet

        Args:
            coordinates: List of (x, y) tuples to encode as doubles

        Returns:
            Encoded data bytes
        """
        # Start with Command ID and Packet IDs
        Header = struct.pack(self.FORMAT_STRING, AddZone.COMMAND_ID, self.PacketID, self.Zone.value, self.ZoneID)

        # Flatten the list of tuples into a single list of floats
        FlattenedCoordinates = [Item for Coordinate in self.Coordinates for Item in Coordinate]

        # Build the format string: two bytes for header, then 2 doubles per coordinate
        FormatString = f"{len(FlattenedCoordinates)}d"

        if FlattenedCoordinates:
            CoordinateBytes = struct.pack(FormatString, *FlattenedCoordinates)
            EncodedString = Header + CoordinateBytes
        else:
            EncodedString = Header

        return EncodedString

    @staticmethod
    def DecodePacket(EncodedString: str, DecodeResult: DecodeFormat) -> CommandInterface | str:
        """Decodes data packet
        
        Args:
            encoded_string: Encoded data packet

        Returns:
            Data from encoded data packet
        """
        CoordinateCount = (len(EncodedString) - 2) // 16

        if CoordinateCount > 6:
            print("Too many coordinates")

        FormatString = AddZone.FORMAT_STRING + "dd" * int(CoordinateCount)

        ExpectedLength = struct.calcsize(FormatString)

        if len(EncodedString) != ExpectedLength:
            raise ValueError(f"Encoded string length {len(EncodedString)} does not match expected {ExpectedLength} for format '{FormatString}'")

        UnpackedData = struct.unpack(FormatString, EncodedString)

        Coordinates = []

        for i in range(0, (CoordinateCount * 2), 2):
            Coordinates.append((UnpackedData[(i + 2)], UnpackedData[(i + 3)]))
        
        Data = None

        match (DecodeResult):
            case DecodeFormat.Class:
                Data = AddZone(UnpackedData[2], Coordinates)

            case DecodeFormat.JSON:
                JSONData = {
                    "Command ID": UnpackedData[0],
                    "Packet ID": UnpackedData[1],
                    "Zone": UnpackedData[2],
                    "Zone ID": UnpackedData[3],
                    "Coordinates": Coordinates
                }

                Data = json.dumps(JSONData)

            case _:
                print("Decode Error")

                return

        return Data
    
    def __str__(self):
        return f"Add Zone:\nCommand ID: {self.COMMAND_ID}\nPacket ID: {self.PacketID}\nZone Type: {self.Zone.value} => {self.Zone.name}\nZone ID: {self.ZoneID}\nCoordinates: {self.Coordinates}"