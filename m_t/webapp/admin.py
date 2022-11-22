from django.contrib import admin
from webapp.models import Todo, Status, Type

admin.site.register(Todo)
admin.site.register(Status)
admin.site.register(Type)