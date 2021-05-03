import os
import re
import requests
from datetime import datetime, date, timedelta
from apachelogs import LogParser

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand

from parser_logs.models import Logs

class Command(BaseCommand):
	help = 'Команда для парсинга лога'

	def handle(self, *args, **options):
		if options['url']:
			print(options['url'])
			val = URLValidator()
			try:
				val(options['url'])

				# скачивание файла фрагментами
				r = requests.get(options['url'], stream=True)
				if r.status_code == 200:
					stream = r.iter_content(chunk_size=1024)
					handle = open(os.path.basename(options['url']), 'wb')

					for i, x in enumerate(stream):
						try:
							handle.write(x)
							print(i, len(x))
						except StopIteration:
							handle.close()

					handle = open(os.path.basename(options['url']), 'r')
					content = handle.read()
					parts = [
						r'(?P<host>\S+)',                   # host %h
						r'\S+',                             # indent %l (unused)
						r'(?P<user>\S+)',                   # user %u
						r'\[(?P<time>.+)\]',                # time %t
						r'"(?P<request>.+)"',               # request "%r"
						r'(?P<status>[0-9]+)',              # status %>s
						r'(?P<size>\S+)',                   # size %b (careful, can be '-')
						r'"(?P<referer>.*)"',               # referer "%{Referer}i"
						r'"(?P<agent>.*)"',                 # user agent "%{User-agent}i"
					]
					pattern = re.compile(r'\s+'.join(parts)+r'\s*\Z')

					logs = []
					for line in content.split('\n'):
						if not line:
							continue

						# разбиваем строку на параметры
						m = pattern.match(line)
						res = m.groupdict()

						ip_address = res['host']
						date_log = datetime.strptime(res['time'], '%d/%b/%Y:%H:%M:%S %z')
						method, url_request, http_version = res['request'].split(' ')
						code = res['status']

						logs.append(Logs(
							ip_address=ip_address,
							date_log=date_log,
							method=method,
							url_request=url_request,
							code=code
						))

					# добавляем логи одним запросом
					Logs.objects.bulk_create(logs)
				else:
					print(r.status_code)
			except ValidationError:
				print('Неверный url')
		else:
			import this

	def add_arguments(self, parser):
		parser.add_argument(
		'-url',
		action='store',
		default=False
		)