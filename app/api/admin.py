from django.contrib import admin

from .models import Dog
from .models import Key
from .models import ModifiedDog

admin.site.register(Key)
admin.site.register(Dog)
admin.site.register(ModifiedDog)
