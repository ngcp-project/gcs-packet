import struct

class Telemetry:
    """Handles telemetry data encoding and decoding for UAV/UGV communication."""

    FORMAT_STRING = "=BI6fQ2d2B2dB"
    
    def __init__(self, CommandID = 0, PacketID = 0, Speed = 0, Pitch = 0, Yaw = 0, Roll = 0, Altitude = 0, BatteryLife = 0, LastUpdated = 0,
             CurrentPosition = (0, 0), VehicleStatus = 0,
             MessageFlag = 0, MessageLat = 0.0, MessageLon = 0.0, PatientStatus = 0):
        self.CommandID = CommandID
        self.PacketID = PacketID
        self.Speed = Speed
        self.Pitch = Pitch
        self.Yaw = Yaw
        self.Roll = Roll
        self.Altitude = Altitude
        self.BatteryLife = BatteryLife
        self.LastUpdated = LastUpdated
        self.CurrentPositionX = CurrentPosition[0]
        self.CurrentPositionY = CurrentPosition[1]
        self.VehicleStatus = VehicleStatus  # 1 byte (Status flag 0-255)

        # Message attributes (default: no message)
        self.MessageFlag = MessageFlag  # 0 = No Message, 1 = Package, 2 = Patient
        self.MessageLat = MessageLat
        self.MessageLon = MessageLon
        self.PatientStatus = PatientStatus

    def Encode(self):
        """Encode the current Telemetry instance into binary format."""

        return struct.pack(self.FORMAT_STRING, self.CommandID, self.PacketID,
                        self.Speed, self.Pitch, self.Yaw, self.Roll,
                        self.Altitude, self.BatteryLife, self.LastUpdated,
                        self.CurrentPositionX, self.CurrentPositionY,
                        self.VehicleStatus,
                        self.MessageFlag,
                        self.MessageLat, self.MessageLon, self.PatientStatus
                        )

    @staticmethod
    def Decode(BinaryData):
        """Decode binary telemetry data into a Telemetry object."""

        ExpectedSize = 72  # Total size of the telemetry packet (in bytes)

        if len(BinaryData) != ExpectedSize:
            print(f"Invalid telemetry packet size. Expected {ExpectedSize}, got {len(BinaryData)}")
            return None
        


        UnpackedData = struct.unpack(Telemetry.FORMAT_STRING, BinaryData)

        ListData = list(UnpackedData)

        CurrentLocation = (UnpackedData[9], UnpackedData[10])

        ListData.pop(10)
        ListData[9] = CurrentLocation

        UnpackedData = tuple(ListData)

        return Telemetry(*UnpackedData)

    def __str__(self):
        return (f"Telemetry: Command ID: {self.CommandID}, Packet ID: {self.PacketID}, Speed: {self.Speed}, Pitch: {self.Pitch}, Yaw: {self.Yaw}, Roll: {self.Roll}, "
            f"Altitude: {self.Altitude}, Battery Life: {self.BatteryLife:.2f}, Last Updated: {self.LastUpdated}, "
            f"Current Position: ({self.CurrentPositionX}, {self.CurrentPositionY}), "
            f"Vehicle Status: {self.VehicleStatus}, "
            f"Message Flag: {self.MessageFlag}, "
            f"Message Location: ({self.MessageLat}, {self.MessageLon}), "
            f"Patient Status: {self.PatientStatus}"
            )
