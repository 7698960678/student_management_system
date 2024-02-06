from django.db import models
from accounts.models import User


def image_upload_path(instance, filename):
    # Determine the user's role
    if instance.user.is_student:
        return "static/student/{0}/{1}".format(instance.user.email,filename)
    elif instance.user.is_teacher:
        return "static/teacher/{0}/{1}".format(instance.user.email,filename)
    elif instance.user.is_admin:
        return "static/admin/{0}/{1}".format(instance.user.email,filename)
    elif instance.user.is_superuser:
        return "static/super/{0}/{1}".format(instance.user.email,filename)

class Images(models.Model):
    id = models.AutoField("Image Id",primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    image = models.ImageField("Image Album", upload_to=image_upload_path, blank=False)
    class Meta:
        verbose_name_plural = "1. Images"
    def __str__(self) :
        return f'{self.user} : {self.image}'