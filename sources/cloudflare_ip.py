import requests
import ipaddress
from typing import List
from .__init__ import BaseSource
from generator.writer_rsc import write_ipv4_list

class CloudflareIPsV4(BaseSource):
    output_file = "cloudflare-ips-v4.rsc"
    list_name = "cloudflare-ips"
    url = "https://www.cloudflare.com/ips-v4"

    def generate(self) -> int:
        resp = requests.get(self.url)
        resp.raise_for_status()
        entries: List[str] = []
        for raw_line in resp.text.splitlines():
            line = raw_line.strip()
            if not line:
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