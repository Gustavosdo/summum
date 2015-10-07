#-*- coding: UTF-8 -*-
from django.forms import ModelForm, CheckboxInput
from suit.widgets import NumberInput, SuitSplitDateTimeWidget
from django.forms import forms
from contas_receber.models import *
from parametros_financeiros.models import GrupoEncargo


class ContasReceberForm(ModelForm):
    u""" 
    Classe ContasReceberForm. 
    Criada para customizar as propriedades dos campos da model ContasReceber
    
    Criada em 04/10/2014. 
    """

    def __init__(self, *args, **kwargs):
        super(ContasReceberForm, self).__init__(*args, **kwargs)
        try:
            grupo_encargo_padrao = GrupoEncargo.objects.get(padrao=1)
            self.fields['grupo_encargo'].initial = grupo_encargo_padrao.pk
        except GrupoEncargo.DoesNotExist and KeyError:
            pass

    class Meta:
        widgets = {
            'data': SuitSplitDateTimeWidget,
        }

        

class RecebimentoForm(ModelForm):
    u""" 
    Classe RecebimentoForm. 
    Criada para customizar as propriedades dos campos da model Recebimento
    
    Criada em 06/10/2014. 
    Última alteração em --.
    """

    class Meta:
        widgets = {
            'valor': NumberInput(attrs={'class': 'input-small text-right', 'placeholder': '0,00', 'step': '0.01'}),
            'juros': NumberInput(attrs={'readonly': 'readonly', 'class': 'input-small text-right', 'placeholder': '0,00', 'step': '0.01'}),
            'multa': NumberInput(attrs={'readonly': 'readonly', 'class': 'input-small text-right', 'placeholder': '0,00', 'step': '0.01'}),
            'desconto': NumberInput(attrs={'class': 'input-small text-right', 'placeholder': '0,00', 'step': '0.01'}),
            'parcelas_contas_receber': NumberInput(attrs={'readonly': 'readonly', 'class': 'input-small'}),
        }



class ParcelasContasReceberForm(ModelForm):

    class Media:
        js = (
            '/static/js/formata_campos_contas_receber.js',
            '/static/js/formata_parcelas_contas_receber.js',
        )

    class Meta:
        widgets = {
            'status': CheckboxInput(attrs={'class': 'status-parcela'}),
        }