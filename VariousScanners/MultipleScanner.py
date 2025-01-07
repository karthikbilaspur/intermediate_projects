import scapy.all as scapy
import nmap
import virus_total_api
import ssl
import socket
import psutil
import dns.resolver
import pysnmp.hlapi as hlapi
import ldap3

class NetworkScanner:
    def __init__(self, ip_range):
        self.ip_range = ip_range

    # Intrusion Detection Scanner
    def intrusion_detection(self):
        packet = scapy.IP(dst=self.ip_range) / scapy.TCP(flags="S")
        responses = scapy.srp(packet, timeout=1, verbose=False)[0]
        for response in responses:
            if response[1].haslayer(scapy.TCP) and response[1].getlayer(scapy.TCP).flags == 0x12:
                print("Potential SYN flood attack detected")

    # Malware Scanner
    def malware_scan(self):
        packet = scapy.IP(dst=self.ip_range) / scapy.DNS(qd=scapy.DNSQR(qname="example.com"))
        responses = scapy.srp(packet, timeout=1, verbose=False)[0]
        for response in responses:
            domain = response[1].getlayer(scapy.DNS).an.rdata
            api = virus_total_api.VirusTotalAPI()
            report = api.get_domain_report(domain)
            if report.positives > 0:
                print(f"Malware detected: {domain}")

    # Firewall Scanner
    def firewall_scan(self):
        nm = nmap.PortScanner()
        nm.scan(self.ip_range, "22-443")
        for host in nm.all_hosts():
            for proto in nm[host].all_protocols():
                for port in nm[host][proto].keys():
                    state = nm[host][proto][port]['state']
                    if state == "filtered":
                        print(f"Firewall blocking port {port}")

    # Encryption Scanner
    def encryption_scan(self, host, port):
        context = ssl.create_default_context()
        with socket.create_connection((host, port)) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                print(ssock.cipher())

    # Network Traffic Monitor
    def network_traffic_monitor(self):
        net_io = psutil.net_io_counters()
        bytes_sent = net_io.bytes_sent
        bytes_recv = net_io.bytes_recv
        print(f"Bytes sent: {bytes_sent}, Bytes received: {bytes_recv}")

    # System Monitor
    def system_monitor(self):
        cpu_percent = psutil.cpu_percent()
        mem_percent = psutil.virtual_memory().percent
        print(f"CPU usage: {cpu_percent}%, Memory usage: {mem_percent}%")

    # Application Monitor
    def application_monitor(self, pid):
        process = psutil.Process(pid)
        cpu_percent = process.cpu_percent()
        mem_percent = process.memory_percent()
        print(f"CPU usage: {cpu_percent}%, Memory usage: {mem_percent}%")

    # User Activity Monitor
    def user_activity_monitor(self, username):
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == "bash" and proc.uids().real == username:
                print(f"User {username} is active")

    # DNS Scanner
    def dns_scan(self, domain):
        resolver = dns.resolver.Resolver()
        answers = resolver.query(domain, 'NS')
        for rdata in answers:
            print(rdata)

    # DHCP Scanner
    def dhcp_scan(self):
        packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") / scapy.IP(dst="255.255.255.255") / scapy.UDP(dport=68) / scapy.BOOTP(chaddr=scapy.RandMAC())
        scapy.sendp(packet)
        responses = scapy.srp(packet, timeout=1, verbose=False)[0]
        for response in responses:
            print(response[1].summary())

    # SNMP Scanner
    def snmp_scan(self, ip, community):
        for (error_indication, error_status, error_index, var_binds) in hlapi.nextCmd(
            hlapi.SnmpEngine(),
            hlapi.CommunityData(community),
            hlapi.UdpTransportTarget((ip, 161)),
            hlapi.ContextData(),
            hlapi.ObjectType(hlapi.ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)),
            hlapi.ObjectType(hlapi.ObjectIdentity('SNMPv2-MIB', 'sysLocation', 0)),
        ):
            if error_indication:
                print(error_indication)
            elif error_status:
                print('%s at %s' % (error_status.prettyPrint(), error_index and error_index.prettyPrint() or '?'))
            else:
                for var_bind in var_binds:
                    print(' = '.join([x.prettyPrint() for x in var_bind]))

    # LDAP Scanner
    def ldap_scan(self, server, username, password):
        server = ldap3.Server(server)
        connection = ldap3.Connection(server, user=username, password=password, auto_bind=True)
        connection.search(search_base='dc=example,dc=com', search_filter='(objectClass=*)', search_scope=ldap3.SUBTREE)
        for entry in connection.entries:
            print(entry)

    def scan_network(self):
        print("Intrusion Detection Scan:")
        self.intrusion_detection()

        print("\nMalware Scan:")
        self.malware_scan()

        print("\nFirewall Scan:")
        self.firewall_scan()

        print("\nEncryption Scan:")
        self.encryption_scan("www.example.com", 443)

        print("\nNetwork Traffic Monitor:")
        self.network_traffic_monitor()

        print("\nSystem Monitor:")
        self.system_monitor()

        print("\nApplication Monitor:")
        self.application_monitor(1234)

        print("\nUser Activity Monitor:")
        self.user_activity_monitor(1000)

        print("\nDNS Scan:")
        self.dns_scan("example.com")

        print("\nDHCP Scan:")
        self.dhcp_scan()

        print("\nSNMP Scan:")
        self.snmp_scan("192.168.1.100", "public")

        print("\nLDAP Scan:")
        self.ldap_scan("ldap://ldap.example.com", "cn=admin,dc=example,dc=com", "password")


if __name__ == "__main__":
    scanner = NetworkScanner("192.168.1.0/24")
    scanner.scan_network()
    
#Note :- 
#Features
#Intrusion detection scanning
#Malware scanning
#Firewall configuration analysis
#Encryption implementation evaluation
#Network traffic monitoring
#System performance and security tracking
#Application performance supervision
#User activity monitoring
#DNS configuration evaluation
#DHCP setting analysis
#SNMP-based network device monitoring
#LDAP directory service evaluation
#Tools and Resources
#Scapy: 
#Nmap: 
#PySNMP: 
#LDAP: 
#Virus Total API:
    