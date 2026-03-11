from Enum import *

class PacketLibrary:
    MRA_MAC_ADDRESS = ""
    MEA_MAC_ADDRESS = ""
    ERU_MAC_ADDRESS = ""

    @staticmethod
    def GetMACAddressFromVehicle(VehicleName: Vehicle) -> str | tuple:
        match (VehicleName):
            case Vehicle.MRA:
                return PacketLibrary.MRA_MAC_ADDRESS
            case Vehicle.MEA:
                return PacketLibrary.MEA_MAC_ADDRESS
            case Vehicle.ERU:
                return PacketLibrary.ERU_MAC_ADDRESS
            case Vehicle.ALL:
                return (Vehicle.MRA, Vehicle.MEA, Vehicle.ERU)
            case _:
                print("Vehicle specification unknown. MAC address cannot be provided")

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