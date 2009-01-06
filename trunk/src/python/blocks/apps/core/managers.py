from django.db.models import Manager, Q
from django.utils.translation import ugettext_lazy as _

from datetime import datetime

STATUS_DRAFT     = 'N'
STATUS_PUBLISHED = 'P'
STATUS_DISABLED  = 'D'

STATUS_CHOICES = (
	(STATUS_DRAFT,     _('Draft')),
	(STATUS_PUBLISHED, _('Published')),
	(STATUS_DISABLED,  _('Disabled')),
)

class BaseManager(Manager):

    def published(self):
        return self.filter(
            Q(unpublish_date__gte=datetime.now()) | Q(unpublish_date__isnull=True),
            publish_date__lte=datetime.now(),
            status=STATUS_PUBLISHED
        )

    def promoted(self):
        return self.published().filter(promoted=True)
