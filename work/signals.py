from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Company

@receiver(post_save, sender=Company)
@receiver(post_delete, sender=Company)
def update_companies_page(instance, **kwargs):
    group_name = 'companies'
    
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        group_name,
        {'type': 'restart.message', 'text': 'Restart it!'},
    )

    print('PING!')
