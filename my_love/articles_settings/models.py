from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from taggit.managers import TaggableManager
from django.conf import settings
from PIL import Image
import sys
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


# Model for store a users articles
class Gallery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gallery_set')
    description = models.TextField(max_length=1000)
    tags = TaggableManager()
    path = models.ImageField(upload_to='images/', default='images/default.png')
    name = models.CharField(max_length=200)
    main = models.BooleanField(default=False)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.user.username, self.name)

    # Check if there is an image on the server if not then return the path to the standard image
    def image(self):
        try:
            if not Image.open(self.path):
                return settings.MEDIA_URL + settings.DEFAULT_IMAGE
            else:
                return self.path.url
        except:
            return settings.MEDIA_URL + settings.DEFAULT_IMAGE

    @staticmethod
    # checks whether the field passed as an argument (user_pk) matches the field of the article owner, if so, it will be deleted
    def image_del(image_pk, user_pk):
        image = Gallery.objects.get(pk=image_pk)
        if image.user.pk == user_pk:
            image.delete()

    # before deleting the article from the database, the image was first deleted from the server
    def delete(self, *args, **kwargs):
        try:
            self.path.delete()
        except:
            pass
        super().delete(*args, **kwargs)

    # before saving the article to the database, the image will be compressed
    def save(self, *args, **kwargs):
        if not self.pk:
            self.path = self.compressImage(self.path)
        super().save(*args, **kwargs)

    # image compress logic
    def compressImage(self, uploadedImage):
        imageTemproary = Image.open(uploadedImage)
        outputIoStream = BytesIO()
        # imageTemproary = imageTemproary.resize((300, 350))
        imageTemproary.save(outputIoStream, format=imageTemproary.format, quality=60)
        outputIoStream.seek(0)
        uploadedImage = InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % uploadedImage.name.split('.')[0],
                                             'image/jpeg', sys.getsizeof(outputIoStream), None)
        return uploadedImage


@receiver(pre_save, sender=Gallery)
# logic to change the main article to the current one
def pre_save_main_image(sender, instance, **kwargs):
    try:
        if instance.main:
            Gallery.objects.filter(user=instance.user, main=True).update(main=False)
    except:
        pass