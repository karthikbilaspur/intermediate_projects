import scapy.all as scapy

class NetworkScanner:
    def __init__(self, ip_range):
        self.ip_range = ip_range

    def host_discovery(self):
        arp_request = scapy.ARP(pdst=self.ip_range)
        broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
        arp_broadcast = broadcast / arp_request
        clients = scapy.srp(arp_broadcast, timeout=1, verbose=False)[0]
        hosts = []
        for element in clients:
            hosts.append({"ip": element[1].psrc, "mac": element[1].hwsrc})
        return hosts

    def tcp_port_scan(self, ip, ports):
        open_ports = []
        for port in ports:
            packet = scapy.IP(dst=ip) / scapy.TCP(dport=port)
            response = scapy.srp(packet, timeout=1, verbose=False)[0]
            if response:
                open_ports.append(port)
        return open_ports

    def udp_port_scan(self, ip, ports):
        open_ports = []
        for port in ports:
            packet = scapy.IP(dst=ip) / scapy.UDP(dport=port)
            response = scapy.srp(packet, timeout=1, verbose=False)[0]
            if response:
                open_ports.append(port)
        return open_ports

    def os_detection(self, ip):
        packet = scapy.IP(dst=ip) / scapy.TCP(flags="S")
        response = scapy.srp(packet, timeout=1, verbose=False)[0]
        if response:
            ttl = response[0][1].ttl
            if ttl <= 64:
                return "Linux/Unix-based OS"
            elif ttl >= 128:
                return "Windows-based OS"
            else:
                return "Unknown OS"

    def scan_network(self):
        hosts = self.host_discovery()
        print("Hosts discovered:")
        for host in hosts:
            print(f"IP: {host['ip']}    MAC: {host['mac']}")
            
            # TCP port scan
            tcp_ports = [22, 80, 443]
            open_tcp_ports = self.tcp_port_scan(host['ip'], tcp_ports)
            print(f"Open TCP ports on {host['ip']}: {open_tcp_ports}")
            
            # UDP port scan
            udp_ports = [53, 161]
            open_udp_ports = self.udp_port_scan(host['ip'], udp_ports)
            print(f"Open UDP ports on {host['ip']}: {open_udp_ports}")
            
            # OS detection
            os = self.os_detection(host['ip'])
            print(f"Operating System: {os}")
            print("-" * 50)


if __name__ == "__main__":
    scanner = NetworkScanner("192.168.1.0/24")
    scanner.scan_network()