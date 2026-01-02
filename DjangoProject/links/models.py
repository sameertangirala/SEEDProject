from django.db import models

class AppLink(models.Model):
    name = models.CharField(max_length=100)
    icon_url = models.URLField()
    link_url = models.URLField()
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name
