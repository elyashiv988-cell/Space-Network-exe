from space_network_lib import SpaceEntity,Packet,SpaceNetwork

class Satellite(SpaceEntity):
    def receive_signal(self, packet: Packet):
        print(f"{self.name} Received: {packet}")

network=SpaceNetwork(level=2)
sat1=Satellite("sat1",100)
sat2=Satellite("sat2",200)
message=Packet("Alert received",sat1,sat2)
network.send(message)