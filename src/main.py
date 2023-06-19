from . import utils
from loguru import logger
import nmap
import json


def get_data(autogenerate: bool = False) -> tuple[tuple[str, ...], tuple[int, ...]]:
	if autogenerate:
		ip_list = utils.generate_ip_list()
		ports_list = utils.generate_ports_list()
		logger.info(
			f"There are {len(ip_list)} IP-addresses and {len(ports_list)} ports was automatically generated"
		)
	else:
		ip_list = utils.get_data_from_file(data_type="ip")
		ports_list = utils.get_data_from_file(data_type="ports")
		logger.info(
			f"There are {len(ip_list)} IP-addresses and {len(ports_list)} ports was readed from files"
		)

	return ip_list, ports_list


def make_response(ip_list: tuple[str, ...], ports_list: tuple[str, ...]):
	response = []
	for ip in ip_list:
		nm = nmap.PortScanner()
		logger.info(
			f"Started scanning for IP '{ip}'"
		)
		nm.scan(ip)
		host_dict = {
			"hostname": ip,
			"state": None,
			"open_ports": [],
			"closed_ports": []
		}
		host_dict = utils.get_host_info(nm, host_dict=host_dict, checking_ports=ports_list)
		response.append(host_dict)

	print(json.dumps(response))
