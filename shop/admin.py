from django.contrib import admin

from .models import Product,ProductGroup,Cart,Address,Order,OrderDetail,Category,CategoryParent


class OrderAdmin(admin.ModelAdmin):

    list_display    = ["dt","user","prefecture","city","address","paid","deliverd","session_id",]

class OrderDetailAdmin(admin.ModelAdmin):

    list_display    = ["order","user","product_price","product_name","amount",]



class CategoryAdmin(admin.ModelAdmin):

    list_display    = ["name","parent","dt"]

class CategoryParentAdmin(admin.ModelAdmin):

    list_display    = ["name","dt"]



admin.site.register(ProductGroup)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Address)

admin.site.register(Order,OrderAdmin)
admin.site.register(OrderDetail,OrderDetailAdmin)

admin.site.register(Category,CategoryAdmin)
admin.site.register(CategoryParent,CategoryParentAdmin)



