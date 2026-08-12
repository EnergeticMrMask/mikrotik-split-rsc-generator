import os
from typing import List

def _generate_file(
        output_file: str,
        lines: List[str],
) -> None:
    output_file = os.path.join("rsc", output_file)
    os.makedirs(os.path.dirname(output_file) or "rsc", exist_ok=True)
    tmp = output_file + ".tmp"
    if os.path.exists(tmp):
        os.remove(tmp)
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        os.replace(tmp, output_file)
    except OSError as e:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise OSError(f"Failed to write to {output_file}: {e}")

def write_ipv4_list(
    entries: List[str],
    list_name: str,
    output_file: str,
) -> int:
    if len(entries) < 1:
        raise ValueError(f"0 entries for {list_name}, refusing to write {output_file}")
    lines: List[str] = []
    lines.append(":local entriesList {")
    for entry in entries:
        lines.append(f"    \"{entry}\";")
    lines.append("}")
    lines.append("")
    lines.append(f":local listName \"{list_name}\"")
    lines.append("")
    lines.append(":foreach id in=[/ip firewall address-list find list=$listName !dynamic] do={")
    lines.append("    :local addr [/ip firewall address-list get $id address]")
    lines.append("    :if ([:len [:find $entriesList $addr]] = 0) do={")
    lines.append("        :do {/ip firewall address-list remove $id} on-error={}")
    lines.append("    }")
    lines.append("}")
    lines.append("")
    lines.append(":foreach entry in=$entriesList do={")
    lines.append("    :do {/ip firewall address-list add list=$listName address=$entry} on-error={}")
    lines.append("}")
    _generate_file(output_file, lines)
    return len(entries)

def write_domain_list(
    entries: List[str],
    list_name: str,
    dns_server: str,
    output_file: str,
) -> int:
    if len(entries) < 1:
        raise ValueError(f"0 entries for {list_name}, refusing to write {output_file}")
    lines: List[str] = []
    lines.append(":local entriesList {")
    for entry in entries:
        lines.append(f"    \"{entry}\";")
    lines.append("}")
    lines.append("")
    lines.append(f":local listName \"{list_name}\"")
    if dns_server:
        lines.append(f":local dnsServer \"{dns_server}\"")
    else:
        lines.append(":local dnsServer [/ip dns get servers]")
        lines.append(":set $dnsServer [:pick $dnsServer 0 [:find $dnsServer \";\"]]")
    lines.append("")
    lines.append(":foreach id in=[/ip dns static find address-list=$listName] do={")
    lines.append("    :local addr [/ip dns static get $id name]")
    lines.append("    :local currentDns [/ip dns static get $id forward-to]")
    lines.append("    :if ([:len [:find $entriesList $addr]] = 0 || $currentDns != $dnsServer) do={")
    lines.append("        :do {/ip dns static remove $id} on-error={}")
    lines.append("    }")
    lines.append("}")
    lines.append("")
    lines.append(":foreach entry in=$entriesList do={")
    lines.append("    :do {/ip dns static add forward-to=$dnsServer name=$entry address-list=$listName type=FWD match-subdomain=yes} on-error={}")
    lines.append("}")
    _generate_file(output_file, lines)
    return len(entries)

def write_domain_and_ipv4_list(
    entries: List[str],
    list_name: str,
    dns_server: str,
    output_file: str,
) -> int:
    if len(entries) < 1:
        raise ValueError(f"0 entries for {list_name}, refusing to write {output_file}")
    lines: List[str] = []
    lines.append(":local entriesList {")
    for entry in entries:
        lines.append(f"    \"{entry}\";")
    lines.append("}")
    lines.append("")
    lines.append(f":local listName \"{list_name}\"")
    if dns_server:
        lines.append(f":local dnsServer \"{dns_server}\"")
    else:
        lines.append(":local dnsServer [/ip dns get servers]")
        lines.append(":set $dnsServer [:pick $dnsServer 0 [:find $dnsServer \";\"]]")
    lines.append("")
    lines.append(":foreach id in=[/ip dns static find address-list=$listName] do={")
    lines.append("    :local addr [/ip dns static get $id name]")
    lines.append("    :local currentDns [/ip dns static get $id forward-to]")
    lines.append("    :if ([:len [:find $entriesList $addr]] = 0 || $currentDns != $dnsServer) do={")
    lines.append("        :do {/ip dns static remove $id} on-error={}")
    lines.append("    }")
    lines.append("}")
    lines.append("")
    lines.append(":foreach id in=[/ip firewall address-list find list=$listName !dynamic] do={")
    lines.append("    :local addr [/ip firewall address-list get $id address]")
    lines.append("    :if ([:len [:find $entriesList $addr]] = 0) do={")
    lines.append("        :do {/ip firewall address-list remove $id} on-error={}")
    lines.append("    }")
    lines.append("}")
    lines.append("")
    lines.append(":foreach entry in=$entriesList do={")
    lines.append("    :do {/ip dns static add forward-to=$dnsServer name=$entry address-list=$listName type=FWD match-subdomain=yes} on-error={}")
    lines.append("    :do {/ip firewall address-list add list=$listName address=$entry} on-error={}")
    lines.append("}")
    _generate_file(output_file, lines)
    return len(entries)