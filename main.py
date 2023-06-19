import src
import sys
from dotenv import load_dotenv

# TODO: Сделать асинхронное сканирование хостов в main.make_response


def main():
	load_dotenv()
	src.logger_init()
	if len(sys.argv) == 1:
		src.check_files_exists()
		data = src.main.get_data()
	else:
		data = src.execute_from_command_line(sys.argv)
	src.main.make_response(*data)


if __name__ == '__main__':
	main()

