from django.contrib import admin

# Register your models here.
from bayke.models import article, product, order, system, user

admin.site.register(product.BaykeProductCategory)
admin.site.register(product.BaykeProductSPU)
admin.site.register(product.BaykeProductSKU)
admin.site.register(product.BaykeProductSpec)