from Enum import *

@staticmethod
def GetVehicleFromMACAddress(MACAddress: str) -> Vehicle:
    match(MACAddress):
        case "1":
            return Vehicle.MRA
        case "2":
            return Vehicle.MEA
        case "3":
            return Vehicle.ERU
        case _:
            return Vehicle.UNKNOWN