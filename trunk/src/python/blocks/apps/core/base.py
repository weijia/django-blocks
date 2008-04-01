from django.db import models
from django.utils.translation import ugettext_lazy as _

STATUS_CHOICES = (
	 ('D', _('disabled')),
	 ('E', _('enabled')),
)