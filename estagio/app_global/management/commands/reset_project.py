#-*- coding: UTF-8 -*-
from django.conf import settings
from django.db import connection, transaction
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
import os
import runpy


class Command(BaseCommand):
    """
        Uso:
        python manage.py reset_project              : Executa todos os trabalhos do procedimento 
        python manage.py reset_project --arquivos   : Executa somente o código que atualiza os arquivos estáticos do projeto
        python manage.py reset_project --dados      : Executa somente o código que elimina e recria todas as tabelas do projeto
    """

    help = u'Elimina todas as tabelas; Recria as tabelas; Atualiza os arquivos estáticos e reinsere os dados padrões de teste'

    def add_arguments(self, parser):

        # (optional) arguments
        parser.add_argument('--dados',
            action='store_true',
            dest='dados',
            default=False,
            help='Elimina e recria todas as tabelas do banco de dados do projeto.')
        parser.add_argument('--arquivos',
            action='store_true',
            dest='arquivos',
            default=False,
            help='Atualiza os arquivos estáticos do projeto e das bibliotecas utilizadas pelo mesmo.')


    def handle(self, *args, **options):
        if options['arquivos'] or (not options['arquivos'] and not options['dados']):
            
            # verbosity: especificca a quantidade de notifiação e depurações retornados no shell; interactive: Evita a confirmação da execução do procedimento pelo usuário
            # Instala os arquivos estáticos necessários para a geração dos gráficos | Python NVD3
            call_command('bower_install', verbosity=3, interactive=False)
            # Coleta os arquivos estáticos | Django
            call_command('collectstatic', verbosity=3, interactive=False)

        if options['dados'] or (not options['arquivos'] and not options['dados']):
            
            # Elimina todas as tabelas do banco de dados | Django Extensions
            call_command('reset_db', verbosity=3, interactive=False)
            # Recria as tabelas do banco de dados do projeto | Django
            call_command('migrate', verbosity=3)

            # Executa os scripts sql declarados na tupla FIXTURES do settings.py
            files = settings.FIXTURES
            cursor = connection.cursor()
            for file in files:
                f = open(file, encoding="utf8")
                response = cursor.execute(f.read())
                f.close()

            # Executa os scripts .py existentes no caminho declarado no atributo FIXTURES_PY do settings.py 
            files_py = settings.FIXTURES_PY
            for file in os.listdir(files_py):
                if file.endswith(".py"):
                    runpy.run_path(os.path.join(files_py, file))