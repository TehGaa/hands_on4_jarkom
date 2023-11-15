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

        default_gateway_koas = '192.168.12.1/26'
        default_gateway_internship = '192.168.12.65/27'
        default_gateway_spesialis = '192.168.12.97/28'
        default_gateway_residen = '192.168.12.113/29'

        #add 2 routers
        router_asrama = self.addNode('Router Asrama')
        router_rs = self.addNode('Router RS')

        ip_router_asrama_rs = '192.168.12.121/30'
        ip_router_rs_asrama = '192.168.12.122/30'

        #add 4 switch
        s1 = self.addSwitch('s1') #switch subnet koas
        s2 = self.addSwitch('s2') #switch subnet internship
        s3 = self.addSwitch('s3') #switch subnet spesialis
        s4 = self.addSwitch('s4') #switch subnet residen

        #add link for each switch
        self.addLink(s1, router_asrama, intfName2='Router Asrama-eth1', 
                     params2={'ip': default_gateway_koas})
        self.addLink(s2, router_asrama, intfName2='Router Asrama-eth2', 
                     params2={'ip':default_gateway_internship})
        self.addLink(s3, router_rs, intfName2='Router RS-eth1', 
                     params2={'ip':default_gateway_spesialis})
        self.addLink(s4, router_rs, intfName2='Router RS-eth2', 
                     params2={'ip':default_gateway_residen})

        #add link for router to router
        self.addLink(router_asrama, router_rs, 
                     intfName1='Router Asrama-Router RS',
                     intfName2='Router RS-Router Asrama',
                     params1={'ip':ip_router_asrama_rs},
                     params2={'ip':ip_router_rs_asrama})

        for i in range(num_switch):
            switch = 's%d'%(i+1)
            for j in range(number_host_per_switch[i]):
                host_name = 'h%d%d'%(i+1, j+1)
                if i == 0:
                    ip_addr = '192.168.12.%d/26'%(j+2)
                    self.addHost(host_name, ip=ip_addr, defaultRoute='via %s'%(default_gateway_koas[:-3]))
                elif i == 1:
                    ip_addr = '192.168.12.%d/27'%(64+j+2)
                    self.addHost(host_name, ip=ip_addr, defaultRoute='via %s'%(default_gateway_internship[:-3]))
                elif i == 2:
                    ip_addr = '192.168.12.%d/28'%(96+j+2)
                    self.addHost(host_name, ip=ip_addr, defaultRoute='via %s'%(default_gateway_spesialis[:-3]))
                else:
                    ip_addr = '192.168.12.%d/29'%(112+j+2)
                    self.addHost(host_name, ip=ip_addr, defaultRoute='via %s'%(default_gateway_residen[:-3]))
                self.addLink(host_name, switch)
        
topos = {'mytopo':(lambda:MyTopo())}
