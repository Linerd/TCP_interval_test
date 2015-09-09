#!/usr/bin/python

from argparse import ArgumentParser
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import OVSController
from mininet.cli import CLI

class SingleSwitchTopoWithLossAndDelay(Topo):
    "Single switch connected to n hosts."
    def build(self,n,delay,loss):
        switch = self.addSwitch('s1')
        for h in range(n):
            host = self.addHost('h%s' % (h + 1))
            self.addLink(host, switch, delay=delay, loss=loss, use_htb=True)
#class SingleSwitchTopo(Topo):
#    "Single switch connected to n hosts."
#    def build(self,n=2):
#        switch = self.addSwitch('s1')
       #for h in range(n):
       #    host = self.addHost('h%s' %(h+1))
       #     self.addLink(host,switch,use_htb=True)
            
def perfTest(n,delay,loss,c):
    "Create network and run simple performance test"
    #topo= SingleSwitchTopo()
    topo = SingleSwitchTopoWithLossAndDelay()
    topo.build(n=n,delay=delay,loss=loss)
    #topoLAD.build()
    net = Mininet(topo=topo,link=TCLink,controller=OVSController)
    net.start()
    print "Dumping host connections"
    dumpNodeConnections(net.hosts)
    print "Testing network connectivity"
    net.pingAll()
    print "Testing bandwidth between h1 and h2"
    h1, h2 ,s1 = net.get('h1', 'h2', 's1')
    #h1.sendCmd('sudo tcpdump -s 68 -ttt -w h1-normal.pcap -i h1-eth0 &')
    #h2.sendCmd('sudo tcpdump -s 68 -ttt -w h2-normal.pcap -i h2-eth0 &')
    cmd = 'sudo tcpdump -s 68 -ttt -w s1-%d-%s-%d.pcap -i s1-eth1 &'%(c,delay if delay else '0ms',loss)
    s1.sendCmd(cmd)
    net.iperf((h1, h2))
    net.stop()

    #cleanup()
    #net = Mininet(topo=topoLAD,link=TCLink,controller=OVSController)
    #net.start()
    #print "Dumping host connections"
    #dumpNodeConnections(net.hosts)
    #print "Testing network connectivity"
    #net.pingAll()
    #print "Testing bandwidth between h1 and h2"
    #h1, h2 = net.get('h1', 'h2')
    #h1.sendCmd('sudo tcpdump -s 68 -ttt -w h1-abnormal.pcap -i h1-eth0')
    #h2.sendCmd('sudo tcpdump -s 68 -ttt -w h2-abnormal.pcap -i h2-eth0')
    #s1.sendCmd('sudo tcpdump -s 68 -ttt -w s1-abnormal.pcap -i s1-eth0')
    #net.iperf((h1, h2))
    #CLI(net)
    #net.stop()
if __name__ == '__main__':
    setLogLevel('info')
    description = 'boo'
    parser = ArgumentParser(description=description)
    parser.add_argument("-d", dest="delay",default='',help="delay")
    parser.add_argument("-l", dest="loss",type=int,default=0,help="loss rate")
    parser.add_argument("-n",dest="n",type=int,default=2,help="num of hosts")
    parser.add_argument("-c",dest="c",type=int,default=1,help="num of loops")
    args = parser.parse_args()
    perfTest(args.n,args.delay,args.loss,args.c)
