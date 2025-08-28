from django.db import models

HTTP_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "CONNECT", "TRACE"]

class EndPointsURLs(models.Model):
  name = models.TextField()
  url = models.TextField(unique=True)
  method = models.CharField(max_length=10, choices=[(m, m) for m in HTTP_METHODS ])
  class Meta:
    db_table = "EndPointsURLs"
  def __str__(self):
    return f"{self.name} EndPoint with url {self.url}"
