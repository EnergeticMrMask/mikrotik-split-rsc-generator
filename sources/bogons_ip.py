import requests
import ipaddress
from typing import List
from .__init__ import BaseSource
from generator.writer_rsc import write_ipv4_list

class BogonsIPsV4(BaseSource):
    output_file = "bogons-ips-v4.rsc"
    list_name = "bogons-ips"
    url = "https://team-cymru.org/Services/Bogons/fullbogons-ipv4.txt"

    def generate(self) -> int:
        resp = requests.get(self.url)
        resp.raise_for_status()

        entries: List[str] = []
        for raw_line in resp.text.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue
            try:
                network = ipaddress.IPv4Network(line, strict=False)
            except ValueError:
                raise ValueError(f"Invalid IP network: {line}")
            if network.prefixlen == 32:
                entries.append(str(network.network_address))
            else:
                entries.append(str(network))

        return write_ipv4_list(entries, self.list_name, self.output_file)