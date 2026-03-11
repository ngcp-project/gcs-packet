from Enum import *

class PacketLibrary:
    MRA_MAC_ADDRESS = ""
    MEA_MAC_ADDRESS = ""
    ERU_MAC_ADDRESS = ""

    @staticmethod
    def GetVehicleFromMACAddress(MACAddress: str) -> Vehicle:
        MACAddress = MACAddress.upper()
        
        if (MACAddress == PacketLibrary.MRA_MAC_ADDRESS):
            return Vehicle.MRA
        elif (MACAddress == PacketLibrary.MEA_MAC_ADDRESS):
            return Vehicle.MEA
        elif (MACAddress == PacketLibrary.ERU_MAC_ADDRESS):
            return Vehicle.ERU
        else:
            return Vehicle.UNKNOWN
    
    @staticmethod
    def SetVehicleMACAddress(VehicleName: Vehicle, MACAddress: str):
        match (VehicleName):
            case Vehicle.MRA:
                PacketLibrary.MRA_MAC_ADDRESS = MACAddress
            case Vehicle.MEA:
                PacketLibrary.MEA_MAC_ADDRESS = MACAddress
            case Vehicle.ERU:
                PacketLibrary.ERU_MAC_ADDRESS = MACAddress
            case _:
                print("Vehicle specification unknown. MAC address assignment ignored")