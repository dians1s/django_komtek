from django.db import models


class Guide(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=300)
    description = models.TextField(blank=True)

    def __str__(self):
        return str(self.id)


class GuideVersion(models.Model):
    id = models.AutoField(primary_key=True)
    idGuide = models.ForeignKey(Guide, on_delete=models.CASCADE)
    version = models.CharField(max_length=50)
    dateStart = models.DateField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['idGuide', 'version'], name='unique_idGuide_version'),
            models.UniqueConstraint(
                fields=['idGuide', 'dateStart'], name='unique_idGuide_dateStart')
        ]

    def __str__(self):
        return str(self.id)


class GuideElement(models.Model):
    id = models.AutoField(primary_key=True)
    idVersion = models.ForeignKey(GuideVersion, on_delete=models.CASCADE)
    elementCode = models.CharField(max_length=100)
    elementValue = models.CharField(max_length=300)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['idVersion', 'elementCode'], name='unique_idVersion_elementCode')
        ]

    def __str__(self):
        return str(self.id)
