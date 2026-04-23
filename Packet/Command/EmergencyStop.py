from Command.CommandInterface import CommandInterface
from Enum import *

import json
import struct

class EmergencyStop(CommandInterface):
    FORMAT_STRING = "BIB"
    COMMAND_ID = 2

    def __init__(self, StopStatus: int):
        super().__init__()

        self.StopStatus = StopStatus

    def EncodePacket(self) -> bytes:
        """Encode data packet

        Args:
            stop_status: Status for emergency stop: 0 = Enable Emergency Stop, 1 = Disable Emergency Stop

        Returns:
            Encoded data bytes
        """
        EncodedString = struct.pack(EmergencyStop.FORMAT_STRING, EmergencyStop.COMMAND_ID, self.PacketID, self.StopStatus)

        return EncodedString

    @staticmethod
    def DecodePacket(EncodedString: str, DecodeResult: DecodeFormat) -> CommandInterface | str:
        """Decodes data packet
        
        Args:
            encoded_string: Encoded data packet

        Returns:
            Data from encoded data packet
        """
        ExpectedSize = 9

        if len(EncodedString) != ExpectedSize:
            print("Invalid String Size")

        UnpackedData = struct.unpack(EmergencyStop.FORMAT_STRING, EncodedString)

        Data = None

        match (DecodeResult):
            case DecodeFormat.Class:
                Data = EmergencyStop(UnpackedData[2])

            case DecodeFormat.JSON:
                JSONData = {
                    "Command ID": UnpackedData[0],
                    "Packet ID": UnpackedData[1],
                    "Stop Status": UnpackedData[2]
                }

                Data = json.dumps(JSONData)
                
            case _:
                print("Decode Error")

                return

        return Data