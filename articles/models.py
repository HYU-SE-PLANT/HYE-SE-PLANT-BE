from django.db import models


class Article(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    article_title = models.CharField(max_length=255, null=False, blank=False)
    article_content_url = models.CharField(max_length=255, null=False, blank=False)
    article_thumbnail_url = models.CharField(max_length=255, null=False, blank=False)
    
    def __str__(self):
        return self.article_title