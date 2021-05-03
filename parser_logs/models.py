from django.db import models

class CommonInfo(models.Model):
	date_add = models.DateTimeField(verbose_name="Дата добавления", auto_now_add=True)
	date_change = models.DateTimeField(verbose_name="Дата изменения", auto_now=True)

	class Meta:
		abstract = True

class Logs(CommonInfo):
	ip_address = models.CharField(verbose_name="IPv4", max_length=15)
	date_log = models.DateTimeField(verbose_name="Дататайм лога")
	method = models.CharField(verbose_name="HTTP-метод", max_length=6)
	url_request = models.CharField(verbose_name="URL", max_length=500)
	code = models.IntegerField(verbose_name="Код ответа", default=200)

	def __str__(self):
		return '№{} {} {}'.format(self.id, self.method, self.ip_address)

	class Meta:
		verbose_name = "Лог"
		verbose_name_plural = "Логи"
