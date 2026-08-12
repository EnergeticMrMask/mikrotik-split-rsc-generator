import yaml
import requests
from typing import List
from pathlib import Path
from .__init__ import BaseSource
from generator.secret_writer import write_adguardhome_domain_split_script

class DomainAdGuardHome(BaseSource):
    category_keyword = "CN"
    output_file = "domain-adguardhome.rsc"
    yaml_file: str = str(Path(__file__).parent / "force_domain.yaml")
    url = "https://raw.githubusercontent.com/felixonmars/dnsmasq-china-list/master/accelerated-domains.china.conf"

    def _load_yaml(self) -> dict:
        path = Path(self.yaml_file)
        if not path.exists():
            raise FileNotFoundError(f"File not exist: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def generate(self) -> int:
        data = self._load_yaml()
        entries: List[str] = []
        seen: set = set()
        for key, value in data.items():
            if self.category_keyword in key:
                if not isinstance(value, list):
                    raise TypeError(f"Type error: {key}")
                for x in value:
                    s = str(x).strip()
                    if s and s not in seen:
                        entries.append(s)
                        seen.add(s)
        if not entries:
            raise ValueError(f"No categories matching keyword: {self.category_keyword}")
        resp = requests.get(self.url)
        resp.raise_for_status()
        for raw_line in resp.text.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue
            parts = line.split("/")
            if len(parts) < 3:
                raise ValueError(f"Invalid server line: {line}")
            domain = parts[1]
            if not domain:
                raise ValueError(f"Empty domain in line: {line}")
            entries.append(domain)
        return write_adguardhome_domain_split_script(entries, self.output_file)