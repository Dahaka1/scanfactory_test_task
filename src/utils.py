import os
import re
from typing import Any
import requests
import random
from . import settings
import nmap


def generate_ip_list() -> tuple[str]:
	string_template = "%s.%s.%s.%s"
	ip_addresses = []

	for _ in range(settings.IP_ADDRESSES_AMOUNT):
		ip_address = string_template % tuple(random.randint(0, 255) for _ in range(4))
		ip_addresses.append(ip_address)

	return tuple(ip_addresses)


def generate_ports_list() -> tuple[int, ...]:
	available_ports = requests.get(
		os.environ.get("PORTS_URL")
	)
	ports = re.findall(r"<td>\d+</td>", available_ports.text)
	ports_list = (random.choice(ports) for _ in range(settings.PORTS_AMOUNT))
	return tuple([int(port[4:-5]) for port in ports_list])


def get_data_from_file(data_type: str) -> tuple[str | int, ...]:
	"""
	:param data_type: ip/ports
	"""
	files = {
		"ip": settings.IP_LIST_FILENAME,
		"ports": settings.PORTS_LIST_FILENAME
	}

	with open(files.get(data_type)) as file:
		if data_type == "ip":
			return tuple([line.rstrip() for line in file.readlines()])
		else:
			return tuple([int(line.rstrip()) for line in file.readlines()])


def get_host_info(nm: nmap.PortScanner, host_dict: dict[str, None | list | str],
				  checking_ports: tuple[str, ...]) -> dict[str, Any]:
	for host in nm.all_hosts():
		host_dict["state"] = nm[host].state()
		for proto in nm[host].all_protocols():
			lport = list(nm[host][proto].keys())
			lport.sort()
			for port in lport:
				port_state = nm[host][proto][port]['state']
				if port_state == "open":
					host_dict["open_ports"].append(port)
		for port in checking_ports:
			if port not in host_dict["open_ports"]:
				host_dict["closed_ports"].append(port)
	return host_dict
