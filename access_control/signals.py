from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import AccessLog
import subprocess
from datetime import datetime

@receiver(post_save, sender=AccessLog)
def log_access_creation(sender, instance, created, **kwargs):
    if created:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "GRANTED" if instance.access_granted else "DENIED"
        log_message = f"[{timestamp}] - CREATE: Access log created for card {instance.card_id}. Status: {status}.\n"
        
        # Using subprocess to append to system_events.log
        try:
            subprocess.run(
                ['bash', '-c', f'echo "{log_message}" >> system_events.log'],
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"Error writing to log file: {e}")

@receiver(post_delete, sender=AccessLog)
def log_access_deletion(sender, instance, **kwargs):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] - DELETE: Access log (ID: {instance.id}) for card {instance.card_id} was deleted.\n"
    
    # Using subprocess to append to system_events.log
    try:
        subprocess.run(
            ['bash', '-c', f'echo "{log_message}" >> system_events.log'],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error writing to log file: {e}")