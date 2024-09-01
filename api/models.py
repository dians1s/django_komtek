from django.db import models


class Guide(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(verbose_name=(
        'Код справочника'), max_length=100, unique=True)
    name = models.CharField(verbose_name=(
        'Наименование справочника'), max_length=300)
    description = models.TextField(verbose_name=(
        'Описание справочника'), blank=True)

    class Meta:
        verbose_name = 'Справочник'
        verbose_name_plural = 'Справочники'

    def __str__(self):
        return str(self.id)


class GuideVersion(models.Model):
    id = models.AutoField(primary_key=True)
    codeGuide = models.ForeignKey(Guide, to_field='code', on_delete=models.CASCADE,
                                  verbose_name=('Код справочника и его наименование'))
    version = models.CharField(verbose_name=(
        'Версия справочника'), max_length=50)
    dateStart = models.DateField(verbose_name=(
        'Дата начала версии'), blank=True)

    class Meta:
        verbose_name = 'Версия справочника'
        verbose_name_plural = 'Версии справочников'
        constraints = [
            models.UniqueConstraint(
                fields=['codeGuide', 'version'], name='unique_codeGuide_version'),
            models.UniqueConstraint(
                fields=['codeGuide', 'dateStart'], name='unique_codeGuide_dateStart')
        ]

    def __str__(self):
        return str(self.id)


class GuideElement(models.Model):
    id = models.AutoField(primary_key=True)
    idVersion = models.ForeignKey(GuideVersion, on_delete=models.CASCADE, verbose_name=(
        'Код, наименование справочника и значение версии'))
    elementCode = models.CharField(verbose_name=(
        'Код элемента'), max_length=100)
    elementValue = models.CharField(verbose_name=(
        'Значение элемента'), max_length=300)

    class Meta:
        verbose_name = 'Элемент справочника'
        verbose_name_plural = 'Элементы справочников'
        constraints = [
            models.UniqueConstraint(
                fields=['idVersion', 'elementCode'], name='unique_idVersion_elementCode')
        ]

    def __str__(self):
        return str(self.id)
