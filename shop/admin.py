from django.contrib import admin
from .models import *
from django.utils.translation import ugettext_lazy as _


class GoodStatusListFilter(admin.SimpleListFilter):
    title = _(u'状态')
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('0', _(u'0 未上架')),
            ('1', _(u'1 已上架')),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(status=0)
        if self.value() == '1':
            return queryset.filter(status=1)


class GoodPriceListFilter(admin.SimpleListFilter):
    title = _(u'价格')
    parameter_name = 'price'

    def lookups(self, request, model_admin):
        return (
            ('1', _(u'0--50')),
            ('2', _(u'50--100')),
            ('3', _(u'100--150')),
            ('4', _(u'150--200')),
            ('5', _(u'200--250')),
            ('6', _(u'250--300')),
            ('7', _(u'350--400')),
            ('8', _(u'450--500')),

        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(price__gte=0, price__lte=50)
        if self.value() == '2':
            return queryset.filter(price__gte=50, price__lte=100)
        if self.value() == '3':
            return queryset.filter(price__gte=100, price__lte=150)
        if self.value() == '4':
            return queryset.filter(price__gte=150, price__lte=200)
        if self.value() == '5':
            return queryset.filter(price__gte=200, price__lte=250)
        if self.value() == '6':
            return queryset.filter(price__gte=250, price__lte=300)


class UserStatusListFilter(admin.SimpleListFilter):
    title = _(u'用户类型')
    parameter_name = 'type'

    def lookups(self, request, model_admin):
        return (
            ('1', _(u'1 买家')),
            ('2', _(u'2 卖家')),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(type=1)
        if self.value() == '2':
            return queryset.filter(type=2)


class ListStatusListFilter(admin.SimpleListFilter):
    title = _(u'状态')
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('0', _(u'0 未付款')),
            ('1', _(u'1 未完成')),
            ('2', _(u'2 未评论')),
            ('3', _(u'3 已评论')),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(status=0)
        if self.value() == '1':
            return queryset.filter(status=1)
        if self.value() == '2':
            return queryset.filter(status=2)
        if self.value() == '3':
            return queryset.filter(status=3)


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'fund')
    search_fields = ('name',)
    list_per_page = 50
    list_filter = (UserStatusListFilter,)


class GoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'seller', 'price', 'amount', 'turnover', 'put_on_time', 'number')
    search_fields = ('name',)
    list_per_page = 50
    list_filter = (GoodStatusListFilter, GoodPriceListFilter)


class OldGoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'seller', 'price', 'put_off_time', 'number')
    search_fields = ('name',)
    list_per_page = 50
    list_filter = (GoodPriceListFilter,)


class DetailListAdmin(admin.ModelAdmin):
    list_display = ('number', 'buyer', 'seller', 'goods_number', 'goods_version', 'status')
    list_per_page = 50
    list_filter = (ListStatusListFilter,)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'goods', 'time')
    search_fields = ('name',)
    list_per_page = 50


admin.site.register(User, UserAdmin)
admin.site.register(Goods, GoodAdmin)
admin.site.register(OldGoods, OldGoodAdmin)
admin.site.register(DetailList, DetailListAdmin)
admin.site.register(Comment, CommentAdmin)

