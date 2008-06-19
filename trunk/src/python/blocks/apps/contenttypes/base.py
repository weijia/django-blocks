from django.utils.translation import ugettext_lazy as _

STATUS_CHOICES = (
	('N', _('new')),
	('P', _('published')),
	('D', _('disabled')),
)

WEIGHT_CHOICES = (
	( 0,  0),
	( 1,  1),
	( 2,  2),
	( 3,  3),
	( 4,  4),
	( 5,  5),
	( 6,  6),
	( 7,  7),
	( 8,  8),
	( 9,  9),
	(10, 10),
)

LEVEL_CHOICES = (
	('P', _('primary')),
	('S', _('secondary')),
)