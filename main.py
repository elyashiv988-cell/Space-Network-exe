from space_network_lib import *
import time
class Satellite(SpaceEntity):
    def receive_signal(self, packet: Packet):
        if isinstance(packet,RelayPacket):
            inner_packet=packet.data
            print("Unwrapping and forwarding to {inner_packet.receiver}")
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
   
earth=SpaceEarth("earth",0)
network=SpaceNetwork(level=3)
sat1=Satellite("sat1",100)
sat2=Satellite("sat2",200)
p_final=Packet("Hello from Earth",sat1,sat2)
p_earth_to_sat1=RelayPacket(p_final,earth,sat1)

def attempt_transmission(paket):
    while True:
        try:
            network.send(p_earth_to_sat1)
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

