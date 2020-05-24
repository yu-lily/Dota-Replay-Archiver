from django.contrib import admin
from .models import Replay
from .models import ReplayPlayer

admin.site.register(Replay)
admin.site.register(ReplayPlayer)