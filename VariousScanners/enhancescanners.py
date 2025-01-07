import nmap
import metasploit
import scapy.all as scapy

class NetworkScanner:
    def __init__(self, ip_range):
        self.ip_range = ip_range

    def vulnerability_scan(self):
        nm = nmap.PortScanner()
        nm.scan(self.ip_range, "22-443")
        vulnerabilities = []
        for host in nm.all_hosts():
            for proto in nm[host].all_protocols():
                for port in nm[host][proto].keys():
                    state = nm[host][proto][port]['state']
                    service = nm[host][proto][port]['name']
                    version = nm[host][proto][port]['version']
                    if state == "open" and service == "http":
                        vulnerabilities.append({"host": host, "port": port, "service": service, "version": version})
        return vulnerabilities

    def exploit_vulnerability(self, vulnerability):
        msf = metasploit.Metasploit()
        msf.connect()
        payload = msf.payloads("exploit/multi/handler")
        options = {"RHOST": vulnerability["host"], "RPORT": vulnerability["port"]}
        msf.execute(payload, options)
        print(msf.result)

    def config_scan(self):
        packet = scapy.IP(dst=self.ip_range) / scapy.TCP(flags="S", dport=22)
        response = scapy.srp(packet, timeout=1, verbose=False)[0]
        banners = []
        if response:
            for elem in response:
                banner = elem[1].payload
                banners.append({"ip": elem[1].src, "banner": banner})
        return banners

    def compliance_scan(self):
        nm = nmap.PortScanner()
        nm.scan(self.ip_range, "21-443")
        compliance_issues = []
        for host in nm.all_hosts():
            for proto in nm[host].all_protocols():
                for port in nm[host][proto].keys():
                    state = nm[host][proto][port]['state']
                    service = nm[host][proto][port]['name']
                    version = nm[host][proto][port]['version']
                    if state == "open" and service == "http":
                        compliance_issues.append({"host": host, "port": port, "service": service, "version": version})
        return compliance_issues

    def scan_network(self):
        print("Vulnerability Scan:")
        vulnerabilities = self.vulnerability_scan()
        for vulnerability in vulnerabilities:
            print(vulnerability)
            self.exploit_vulnerability(vulnerability)

        print("\nConfiguration Scan:")
        banners = self.config_scan()
        for banner in banners:
            print(banner)

        print("\nCompliance Scan:")
        compliance_issues = self.compliance_scan()
        for issue in compliance_issues:
            print(issue)


if __name__ == "__main__":
    scanner = NetworkScanner("192.168.1.0/24")
    scanner.scan_network()