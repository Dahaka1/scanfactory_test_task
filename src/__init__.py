import os
from . import settings
from . import main
from loguru import logger


def check_files_exists() -> None:
	searched_files = (settings.IP_LIST_FILENAME, settings.PORTS_LIST_FILENAME)
	if not all(file in os.listdir() for file in searched_files):
		raise RuntimeError(f"Files not found ({searched_files} are required).\nCreate files or just start script with "
						f"'{settings.AUTOGENERATE_COMMAND}' command-line argument for automatically generating data.\n\n"
						   f"Write to CMD: 'python main.py {settings.AUTOGENERATE_COMMAND}'")


def execute_from_command_line(args: list[str]):
	if len(args) > 2:
		raise Exception("Got an non-supportable amount of command line args")
	cmd = args[-1]
	if cmd == settings.AUTOGENERATE_COMMAND:
		data = main.get_data(autogenerate=True)
		return data
	raise ValueError("Got an non-supportable command")


def logger_init() -> None:
	for level in settings.LOGGING_LEVELS:
		logger.add(
			settings.ERRORS_OUTPUT_FILE,
			level=level,
			format=settings.LOGGING_FORMAT,
			rotation="1 MB",
			compression="zip"
		)
