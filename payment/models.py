from django.db import models

# Create your models here.
class Snippet(models.Model):
    
    title = models.CharField(max_length=180)
    
    class Meta:
        verbose_name = 'Snippet'
        verbose_name_plural = 'Snippets'

    
    def __str__(self):
        return self.title
    