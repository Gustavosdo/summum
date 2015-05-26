#-*- coding: UTF-8 -*-
from django.contrib import admin
from import_export.admin import ExportMixin
from movimento.export import ProdutosResource
from app_global.admin import GlobalAdmin
from django.contrib.admin.views.main import IS_POPUP_VAR
from sorl.thumbnail.admin import AdminImageMixin
from salmonella.admin import SalmonellaMixin
from movimento.models import *
from django.utils.translation import ugettext_lazy as _
from selectable_filter.filter import SelectableFilter
from configuracoes.models import OrdemModelos


class MarcaAdmin(AdminImageMixin, admin.ModelAdmin):
    model = Marca
    fields = ('nome', 'logo', 'descricao')


class CategoriaAdmin(admin.ModelAdmin):
    model = Categoria
    fields = ('nome', 'descricao')


class ProdutosAdmin(ExportMixin, SalmonellaMixin, AdminImageMixin, GlobalAdmin):
    resource_class = ProdutosResource
    model = Produtos
    filter_horizontal = ('categorias',)
    salmonella_fields = ('marca',)
    popup_list_display = ('nome', 'marca', 'quantidade', 'descricao')

    lista = list(OrdemModelos.objects.filter(classe='Produtos', exibe_listagem_principal=True).values_list('campo', flat=True).order_by('ordem'))
    print (lista)
    list_display = lista
    # list_display = ('nome', 'quantidade', 'descricao', 'status')
    list_filter = (('categorias', SelectableFilter), ('marca', SelectableFilter), 'status')
    search_fields = ['nome',]
    readonly_fields = ('quantidade',)

    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-geral',),
            'fields': ('nome', 'preco', 'preco_venda', 'quantidade', 'status')
        }),
        (None, {
            'classes': ('suit-tab suit-tab-geral',),
            'fields': ('imagem',)
        }),
        (None, {
            'classes': ('suit-tab suit-tab-detalhes',),
            'fields': ('descricao', 'marca', 'categorias')
        }),
    )

    suit_form_tabs = (
        ('geral', _(u"Geral")),
        ('detalhes', _(u"Detalhes")),
    )

    def suit_row_attributes(self, obj, request):
        rowclass = ''
        if not obj.status:
            rowclass = 'error'

        return {'class': rowclass}


    def get_queryset(self, request):
        qs = super(ProdutosAdmin, self).get_queryset(request)
        if IS_POPUP_VAR in request.GET:  
            return qs.filter(status=True)
        return qs



admin.site.register(Produtos, ProdutosAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Marca, MarcaAdmin)