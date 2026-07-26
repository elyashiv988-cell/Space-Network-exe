from space_network_lib import *
import time
class Satellite(SpaceEntity):
    def receive_signal(self, packet: Packet):
        print(f"{self.name} Received: {packet}")
    

network=SpaceNetwork(level=3)
sat1=Satellite("sat1",100)
sat2=Satellite("sat2",200)
message=Packet("Alert received",sat1,sat2)

def attempt_transmission(paket):
    while True:
        try:
            network.send(message)
        except TemporalInterferenceError:
            print("Interference, waiting...")
            time.sleep(2)
        except DataCorruptedError:
            print("corrupted. ertrying...")
        break
    try:
        network.send(message)
    except OutOfRangeError:
        print("Target out of the range")
    except LinkTerminatedError:
        print("link lost")
attempt_transmission(message)