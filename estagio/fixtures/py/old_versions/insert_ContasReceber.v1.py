#-*- coding: UTF-8 -*-
from django.test import TestCase

import random, decimal
from datetime import datetime
import time
from pessoal.models import Cliente
from parametros_financeiros.models import FormaPagamento, GrupoEncargo
from contas_receber.models import ContasReceber, Recebimento
from caixa.models import Caixa, MovimentosCaixa

format_date = '%Y-%m-%d %I:%M:%S %p'

def strTimeProp(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.
    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.

    randomDate("2008/01/01 1:30:00 PM", "2009/01/01 4:50:00 AM", random.random())
    """
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(format, time.localtime(ptime))


def randomDate(start, end, prop):
    return strTimeProp(start, end, format_date, prop)


lista_clientes = Cliente.objects.filter(status=1)
lista_formas_pagamento = FormaPagamento.objects.filter(status=1)
lista_grupos_encargo = GrupoEncargo.objects.filter(status=1)
caixa_aberto = Caixa.objects.filter(status=1).values()[0]

if caixa_aberto["status"]:
    caixa_data_abertura = caixa_aberto["data_abertura"].strftime(format_date)
    data_atual = datetime.now().strftime(format_date)
    
    for i in range(1, 100):
        cliente = random.choice(lista_clientes)
        forma_pagamento = random.choice(lista_formas_pagamento)
        grupo_encargo = random.choice(lista_grupos_encargo)
        valor_total = decimal.Decimal(random.random() * 3000).quantize(decimal.Decimal('.01'))
        data = randomDate(caixa_data_abertura, data_atual, random.random())
        data = datetime.strptime(data, format_date).date()
        
        conta = ContasReceber(data=data, 
                              valor_total=valor_total, 
                              descricao=u'Criado à partir de procedimento de geração automática de registros.',
                              vendas=None, 
                              cliente=cliente, 
                              forma_pagamento=forma_pagamento, 
                              grupo_encargo=grupo_encargo, 
                              status=False
                              )
        conta.save()




# Atualiza as datas de recebimentos e movimentos de caixa
lista_recebimentos = Recebimento.objects.filter(parcelas_contas_receber__contas_receber__descricao__contains='Criado à partir de procedimento de geração automática de registros.', 
                                                parcelas_contas_receber__contas_receber__forma_pagamento__carencia=0,
                                                parcelas_contas_receber__num_parcelas=1
                                                ).values_list('pk', 'data', 'parcelas_contas_receber__contas_receber__data')
for l in lista_recebimentos:
    if l[1].date() != l[2]:
        r = Recebimento.objects.get(pk=l[0])
        r.data = l[2]
        r.save()
        m = MovimentosCaixa.objects.get(recebimento__pk=l[0])
        m.data = l[2]
        m.save()


