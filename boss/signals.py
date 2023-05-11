from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import ReviewImage
import os

@receiver(pre_delete, sender=ReviewImage)
def auto_delete_image_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
