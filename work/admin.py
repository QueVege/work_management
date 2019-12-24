from django.contrib import admin
from .models import Company
from .models import Manager
from .models import Work, WorkPlace, WorkTime
from .models import Worker


admin.site.register(Company)
admin.site.register(Manager)
admin.site.register(Work)
admin.site.register(WorkPlace)
admin.site.register(WorkTime)
admin.site.register(Worker)
