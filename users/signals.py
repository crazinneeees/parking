from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from users.models import ParkingSpot

@receiver(post_save, sender=ParkingSpot)
@receiver(post_delete, sender=ParkingSpot)
def update_zone_spot_counts(sender, instance, **kwargs):
    if instance.zone:
        instance.zone.update_spot_counts()
