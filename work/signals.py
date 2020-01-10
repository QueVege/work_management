from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import (
    Company, Worker, WorkPlace, WorkTime)


def retrieve(group_name):
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        group_name,
        {'type': 'restart.message', 'text': 'Restart it!'},
    )


@receiver(post_save, sender=Company)
@receiver(post_delete, sender=Company)
def update_companies_page(instance, **kwargs):
    group_name = 'visitors_companies'
    retrieve(group_name)


@receiver(post_save, sender=Worker)
@receiver(post_delete, sender=Worker)
def update_workers_page(instance, **kwargs):
    group_name = 'visitors_workers'
    retrieve(group_name)


@receiver(post_save, sender=WorkPlace)
@receiver(post_delete, sender=WorkPlace)
def wp_worker_detail_page(instance, **kwargs):
    group_name = f'visitors_workers_{instance.worker.id}'
    retrieve(group_name)


@receiver(post_save, sender=WorkTime)
@receiver(post_delete, sender=WorkTime)
def wt_worker_detail_page(instance, **kwargs):
    group_name = f'visitors_workers_{instance.workplace.worker.id}'
    retrieve(group_name)