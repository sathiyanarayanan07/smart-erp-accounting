from django.contrib import admin
from .models import role1,accountent,product,QA,Admin,schedule,product_details,plan_product,product_material
from .models import product_options,account_page,schedule_process

# Register your models here.

admin.site.register(role1)

admin.site.register(accountent)

admin.site.register(product)

admin.site.register(QA)

admin.site.register(Admin)
admin.site.register(schedule)
admin.site.register(product_details)
admin.site.register(plan_product)
admin.site.register(product_material)
admin.site.register(product_options)
admin.site.register(account_page)
admin.site.register(schedule_process)
