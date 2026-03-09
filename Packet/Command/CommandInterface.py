# Can be used to implement the serial port manager for other radio modules

class CommandInterface:
    # FORMAT_STRING = # More information here: https://docs.python.org/3/library/struct.html
    PacketID = 0

    def encode_packet(self) -> bytes:
        """Encode data packet

        Args:
          data: Data passed into given command

        Returns:
          Encoded data string
        """
        pass

    @staticmethod
    def decode_data(encoded_string):
        """Decodes data packet
        
        Args:
          Encoded data packet

        Returns:
          Data from encoded data packet
        """
        pass
    
    @staticmethod
    def generate_packet_id():
        current_packet_id = CommandInterface.PacketID

        CommandInterface.PacketID += 1

        return current_packet_id