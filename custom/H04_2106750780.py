from mininet.topo import Topo
from mininet.node import Node

class LinuxRouter(Node):
    "A Node with IP forwarding enabled"

    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        # Enable forwarding on the router
        self.cmd('sysctl net.ipv4.ip_forward=1')
    
    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

class MyTopo(Topo):
    def build(self):
        # number of router = 2
        num_switch = 4
        number_host_per_switch = [62, 30, 14, 6]
        number_host_s1 = 0
        number_host_s2 = 0
        number_host_s3 = 0
        number_host_s4 = 0