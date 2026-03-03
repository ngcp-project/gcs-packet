import struct

class Telemetry:
    """Handles telemetry data encoding and decoding for UAV/UGV communication."""

    format_string = "=BI6fQ2d2B2dB"
    PacketID = 0
    
    def __init__(self, payloadId=0, packetId = PacketID, speed=0, pitch=0, yaw=0, roll=0, altitude=0, battery_life=0, last_updated=0,
             current_position = (0, 0), vehicle_status=0,
             message_flag=0, message_lat=0.0, message_lon=0.0, patient_status=0):
        self.payloadId = payloadId # Payload ID for telemetry data is always 2
        self.packetId = Telemetry.PacketID
        self.speed = speed
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll
        self.altitude = altitude
        self.battery_life = battery_life
        self.last_updated = last_updated
        self.current_long = current_position[0]
        self.current_lat = current_position[1]
        self.vehicle_status = vehicle_status  # 1 byte (Status flag 0-255)

        # Message attributes (default: no message)
        self.message_flag = message_flag  # 0 = No Message, 1 = Package, 2 = Patient
        self.message_lat = message_lat
        self.message_lon = message_lon
        self.patient_status = patient_status

    def encode(self):
        """Encode the current Telemetry instance into binary format."""

        #Telemetry.PacketID += 1

        return struct.pack(self.format_string, self.payloadId, self.packetId,
                        self.speed, self.pitch, self.yaw, self.roll,
                        self.altitude, self.battery_life, self.last_updated,
                        self.current_lat, self.current_long,
                        self.vehicle_status,
                        self.message_flag,
                        self.message_lat, self.message_lon, self.patient_status
                        )

    @staticmethod
    def decode(binary_data):
        """Decode binary telemetry data into a Telemetry object."""
        expected_size = 72  # Total size of the telemetry packet (in bytes)
        if len(binary_data) != expected_size:
            print(f"Invalid telemetry packet size. Expected {expected_size}, got {len(binary_data)}")
            return None
        


        unpacked_data = struct.unpack(Telemetry.format_string, binary_data)

        list_data = list(unpacked_data)

        current_location = (unpacked_data[9], unpacked_data[10])

        list_data.pop(10)
        list_data[9] = current_location

        unpacked_data = tuple(list_data)

        return Telemetry(*unpacked_data)

    def __str__(self):
        return (f"Telemetry(Speed={self.speed}, Pitch={self.pitch}, Yaw={self.yaw}, Roll={self.roll}, "
            f"Altitude={self.altitude}, Battery Life={self.battery_life}, Last Updated={self.last_updated}, "
            f"Current Position=({self.current_long}, {self.current_lat}), "
            f"Vehicle Status={self.vehicle_status}, "
            f"Message Flag={self.message_flag}, "
            f"Message Location=({self.message_lat}, {self.message_lon}), "
            f"Patient Status={self.patient_status}"
            )
