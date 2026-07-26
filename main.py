from space_network_lib import *
import time
class Satellite(SpaceEntity):
    def receive_signal(self, packet: Packet):
        if isinstance(packet,RelayPacket):
            inner_packet=packet.data
            print(f"Unwrapping and forwarding to {inner_packet.receiver}")
            attempt_transmission(inner_packet)
        else:
            print(f"Final destination reached: {packet.data}")

class SpaceEarth(SpaceEntity):
    def __init__(self, name, distance_from_earth):
        super().__init__(name, distance_from_earth)
    def receive_signal(self, packet):
        pass        
    

class BrokenConnectionError(CommsError):
    pass  

class RelayPacket(Packet):
    def __init__(self,pacdet_to_relay, sender, proxy):
        super().__init__(pacdet_to_relay,sender,proxy)
        
    def __repr__(self):
        return f"RelayPacket(Relaying [{self.data}] to {self.receiver} from {self.sender})"    
network=SpaceNetwork(level=3)   
earth=SpaceEarth("earth",0)
sat1=Satellite("sat1",100)
sat2=Satellite("sat2",200)
sat3=Satellite("sat3",300)
sat4=Satellite("sat4",400)
p_final=Packet("Hello from Earth",sat3,sat4)
p_sat2_to_3=RelayPacket(p_final,sat2,sat3)
p_sat1_to_2=RelayPacket(p_sat2_to_3,sat1,sat2)
p_earth_to_sat1=RelayPacket(p_sat1_to_2,earth,sat1)


def attempt_transmission(paket):
    while True:
        try:
            network.send(paket)
            break
        except TemporalInterferenceError:
            print("Interference, waiting...")
            time.sleep(2)
        except DataCorruptedError:
            print("corrupted. ertrying...")
            
        except OutOfRangeError:
            print("Target out of range")
            raise BrokenConnectionError("broken conection")
        except LinkTerminatedError:
            print("link lost")
            raise BrokenConnectionError("broken conection")

try:
    attempt_transmission(p_earth_to_sat1)
except BrokenConnectionError:
    print("Transmission failed")

