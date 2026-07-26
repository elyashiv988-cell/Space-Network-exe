from space_network_lib import *
import time
class Satellite(SpaceEntity):
    def receive_signal(self, packet: Packet):
        print(f"{self.name} Received: {packet}")

class BrokenConnectionError(CommsError):
    pass  

network=SpaceNetwork(level=3)
sat1=Satellite("sat1",100)
sat2=Satellite("sat2",200)
message=Packet("Alert received",sat1,sat2)

def attempt_transmission(paket):
    while True:
        try:
            network.send(message)
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
    attempt_transmission(message)
except BrokenConnectionError:
    print("Transmission failed")