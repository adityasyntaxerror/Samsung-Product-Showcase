from django.db.utils import OperationalError, ProgrammingError

from .models import SiteImage


def site_images(request):
    """Expose every SiteImage slot to all templates as {{ site_images.<key> }}."""
    try:
        return {"site_images": {slot.key: slot for slot in SiteImage.objects.all()}}
    except (OperationalError, ProgrammingError):
        # Tables don't exist yet (before `migrate`): render placeholders instead of crashing.
        return {"site_images": {}}
