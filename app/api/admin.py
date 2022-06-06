from django.contrib import admin

from .models import Dog
from .models import Key

admin.site.register(Key)
admin.site.register(Dog)
