"""
# **Biblioteca de ferramentas LBX S/A**

Esta biblioteca possui um ferramentas utilitárias de uso recorrente para aplicações de RPA em python.

## **Classe e funções**

Usa o Microsoft Entra ID (antiga Azure AD) para evitar execução não autorizada
auth_EntraID:        
    disclaimer : Mensagem sobre a necessidade de autenticação
    valida_grupo : Autentica o usuário e aborta se checa não pertencer ao grupo de segurança

    
**postgreSQL**
Interage com o banco de dados PostgreSQL
  - _.db_:               Inicia sessão com o banco
  - _.csv_df_:           Lê arquivo CSV e gera Dataframe (pandas) a partir dele
  - _.db_insert_df_:     Insere informações de Dataframe em tabela do banco com estrutura equivalente
  - _.db_select_:        Retorna um cursor a partir de uma query
  - _.db_update_:        Executa update em tabelas


**api_rest**
Interage com APIs RESTfull, especialmente providas para a plataforma Sienge
  - _.auth_base_:        Autentica (HTTPBasicAuth) sessão na API
  - _.auth_bearer_:      Autentica sessão na API pelos métodos: OAuth, JWT, Bearer  
  - _.endpoint_json_:    Realizad chama ao endpoint. Payload em formato `json` opcional.
  - _.trata_erro_sienge_: Retorna a mensagem de erro do Sienge caso código de retorno seja diferente de 200.
  - _.close_:            Encerra a sessão autenticada

**lbx_logger**
Manipula e formata as mensagens de saída do script para direcioná-las para tela (stdout) e/ou arquivo de log
  - _.add_:              Adiciona a mensagem a um _buffer_ sem exibir, acumulando até a próxima chamada em algum dos níveis abaixo.
  - _.print_:            Contorna o manipulador de log e imprime diretamente na tela (stdout), sem formatar a mensagem nem registrar no arquivo
  - _.debug, .info, .aviso, .erro, .critico_:  Classifica as mensagens por nível de severidade/relevância e rediciona a saída (arquivo, tela, tela+arquivo) conforme a configuração do nível
  - _.stop_logging_:   Interrompe a manipulação das saídas pelo logger e restaura as saídas padrão (stdout/stderr) para a tela 
  - _.filtra_:          Filtra os eventos do arquivo de log registrados em um intervalo de tempo específico

**misc**
Classe de miscelâneas/diversos
  - _.seleciona_arquivo_: Abre um picker do sistema operacionar para selecionar um *arquivo* e retorna seu path
  - _.seleciona_dir_:     Abre um picker do sistema operacionar para selecionar um *diretório* e retorna seu path
  - _.normaliza_:         Limpa caracteres especiais e espaços de strings e retorna tudo em minúsculo
  - _.get_cmd_window_:    Captura a referencia da janela atual (cmd.exe) para retornar o foco à ela depois de chamar os pickers 
  - _.maximize_console_:  Maxima a janela do console (cmd.exe)

## Instalação e uso:

### Instalação

```
pip install lbx_toolkit
```

### Uso
```
from lbx_toolkit import auth_EntraID, PostgreSQL, api_rest, lbx_logger
```
"""
import os
import sys
import re 
import locale
import datetime
import time
from time import sleep
import threading
import logging
from pathlib import Path
from unicodedata import normalize 
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import validators
import msal
import requests
from requests.auth import HTTPBasicAuth
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog
import pygetwindow as gw
import ctypes    
import subprocess
import platform
import socket
import argparse
import servicemanager
import win32serviceutil
import win32service
import win32event

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

class auth_EntraID: # Classe de autenticação de usuários no Microsoft Entra ID (antiga Azure AD)
    """
    #### Classe **auth_EntraID**

    Este recurso tem o propósito de controlar as permissões de execução do script usando as credencias do ambiente AD em nuvem da Microsoft (Azure AD >> Microsoft Entra ID), abortando se a autentição falhar ou o usuário não pertencer ao grupo.

    Essa classe possui apenas dois métodos:

    - `auth_EntraID.disclaimer()`: apenas exibe uma tela de informações/instruções ao usuário.

    - `auth_EntraID.valida_grupo([client_id], [client_secret], [tenant_id], timeout=60, log_file='auth_EntraID.log')`: efetua a autenticação do usuário e verifica se ele pertence ao grupo informado,  abortando a execução caso não pertença ao grupo ou a autenticação não seja validada no tempo estabelecido. Os argumentos `timeout` e `log_file` são opcionais e, se omitidos, os valores aqui atribuídos serão adotados como padrão.

    É necessário obter parametros da plataforma de identidade da Microsoft (AD Azure, agora Microsoft Entra ID), no [*Centro de administração do Microsoft Entra*](https://entra.microsoft.com).
    Sugerimos não armazenar estas ou outras informações sensíveis no script. Considere usar o pacote `dotenv` para isso.

    Os argumentos obrigatórios (posicionais) são:

    1) `tenant_id` corresponde ao campo *ID do Locatário*, que pode ser obtido na página [visão geral de identidade do domínio](https://entra.microsoft.com/#blade/Microsoft_AAD_IAM/TenantOverview.ReactView)

    2) `client_id` corresponde ao *ID do aplicativo (cliente)*, obtido na secção [_Identidade > Aplicativos > Registros de Aplicativo_](https://entra.microsoft.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade/quickStartType~/null/sourceType/Microsoft_AAD_IAM). Considere não reaproveitar aplicativos e criar um específico para essa finalidade.

    3) `secret_id` corresponde ao *Valor* do _ID secreto_ (não ao próprio ID Secreto) do aplicativo. Este token não é passivel de consulta após gerado e para obtê-lo, é necessário criar um novo segredo para o aplicativo na subsecção _"Certificados e Segredos"_, após clicar no nome do aplicativo exibo na indicada no item (2). O token (_Valor do segredo_) deve ser copiado e anotado no ato da criação, pois *não é possível consultá-lo posteriormente*.


    ```
    from lbx_toolkit import auth_EntraID

    client_id = 'SEU_CLIENT_ID'
    client_secret = 'SEU_CLIENT_SECRET'
    tenant_id = 'SEU_TENANT_ID'

    # inicializa instância
    auth = auth_EntraID(client_id, client_secret, tenant_id, timeout=60, log_file='auth_EntraID.log')  

    # exibe a mensagem padrão de aviso
    auth.disclaimer()

    auth.valida_grupo('Nome do Grupo de Distribuição') 
    # se usuário não pertencer a grupo informado, a execução do script é abortada.
    ```
    """
    def __init__(self, client_id, client_secret, tenant_id, grupo, timeout=60, log_file='auth_EntraID.log'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.timeout = timeout
        self.grupo = grupo
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.scope = ["https://graph.microsoft.com/.default"]
        self.redirect_uri = "http://localhost:8000"
        self.response = ""
        self.status_code = 0
        self.server = None
        self.log_file = log_file

        # Configura o logger
        logging.basicConfig(filename=log_file, level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        #
        #
    def valida_grupo(self): # Valida se o usuário autenticado pertence a grupo de segurança informado
        # Redireciona stdout e stderr para arquivos de log
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        sys.stdout = open('stdout.log', 'a')
        sys.stderr = open('stderr.log', 'a')

        # Configurações do Selenium
        chrome_options = Options()
        chrome_options.add_argument("--incognito")

        # Inicializa a aplicação MSAL
        try:        
            app = msal.ConfidentialClientApplication(
                self.client_id,
                authority=self.authority,
                client_credential=self.client_secret,
            )
        except BaseException as err:
            print(f'Falha ao iniciar aplicação MSAL: {err}')
            # Restaura saída padrão
            sys.stdout.close()
            sys.stderr.close()
            sys.stdout = original_stdout
            sys.stderr = original_stderr
            print(f'Script abortado por falha aplicação MSAL. Verifque logs: {self.log_file}, stdout.log e sterr.log')
            os._exit(0)

        # Inicia o fluxo de código de autorização
        try:
            flow = app.initiate_auth_code_flow(scopes=self.scope, redirect_uri=self.redirect_uri)
            auth_url = flow["auth_uri"]
            self.response = f"Acessando a URL de autenticação Microsoft Entra ID (antiga Azure AD): {auth_url}"
            self.logger.info(self.response)
        except BaseException as err:
            print(f'Falha no fluxo de autorização Microsoft Entra ID (antiga Azure AD): {err}')
            # Restaura saída padrão
            sys.stdout.close()
            sys.stderr.close()
            sys.stdout = original_stdout
            sys.stderr = original_stderr
            print(f'Script abortado por falha no fluxo de autorização Microsoft Entra ID (antiga Azure AD). Verifque logs: {self.log_file}, stdout.log e sterr.log')
            os._exit(0)            

        # Inicializa o ChromeDriver com redirecionamento de saída
        try:
            service = Service(ChromeDriverManager().install())
            service.start()
            driver = webdriver.Chrome(service=service, options=chrome_options)
            driver.get(auth_url)
        except BaseException as err:
            print(f'Falha na inicialização do Chrome: {err}')
            # Restaura saída padrão
            sys.stdout.close()
            sys.stderr.close()
            sys.stdout = original_stdout
            sys.stderr = original_stderr
            print(f'Script abortado na inicialização do Chrome. Verifque logs: {self.log_file}, stdout.log e sterr.log')
            os._exit(0)                    
        #
        #
        class AuthHandler(BaseHTTPRequestHandler):
            def log_message(self, format, *args):
                self.server.logger.info("%s - - [%s] %s\n" %
                                        (self.client_address[0],
                                         self.log_date_time_string(),
                                         format % args))
                #
                #
            def do_GET(self):
                parsed_path = urlparse.urlparse(self.path)
                query_params = urlparse.parse_qs(parsed_path.query)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                # Captura o código de autorização e o estado
                if 'code' in query_params and 'state' in query_params:
                    self.server.auth_code = query_params['code'][0]
                    self.server.state = query_params['state'][0]
                    self.wfile.write(b"""
                                    <!DOCTYPE html>
                                    <html lang="pt_BR">
                                    <head>
                                        <meta charset="UTF-8">
                                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                        <style>
                                                body {
                                                    font-family: 'Arial', sans-serif;
                                                    background-color: #f8f9fa;
                                                    margin: 0;
                                                    font-size: 16px;
                                                    padding: 30px;
                                                    display: flex; *
                                                }

                                                .container {        
                                                    width: 100%;
                                                    margin: auto;
                                                    background-color: #ffffff;
                                                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                                                    padding: 16px;
                                                    text-align: center;
                                                    font-size: 16px;
                                                    border-radius: 8px;
                                                }

                                                h1 {    
                                                    font-size: 18px;
                                                    text-align: center;
                                                    color: #007bff;
                                                }
                                        </style>
                                     </head>
                                        <div class="container">
                                            <h1>Autentica&#231;&#227;o realizada com sucesso!</h1>
                                            Aguarde que esta p&#225;gina ser&#225; fechada automaticamente.<br>
                                            Se isto n&#227;o acontecer, pode fech&#225;-la manualmente.
                                        </div>
                                     </body></html>
                                     """)
                else:
                    self.wfile.write(b"""
                                    <!DOCTYPE html>
                                    <html lang="pt_BR">
                                    <head>
                                        <meta charset="UTF-8">
                                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                        <style>
                                                body {
                                                    font-family: 'Arial', sans-serif;
                                                    background-color: #f8f9fa;
                                                    margin: 0;
                                                    font-size: 16px;
                                                    padding: 30px;
                                                    display: flex; *
                                                }

                                                .container {        
                                                    width: 100%;
                                                    margin: auto;
                                                    background-color: #ffffff;
                                                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                                                    padding: 16px;
                                                    text-align: center;
                                                    font-size: 16px;
                                                    border-radius: 8px;
                                                }

                                                h1 {    
                                                    font-size: 18px;
                                                    text-align: center;
                                                    color: red;
                                                }
                                        </style>
                                     </head>
                                        <div class="container">
                                            <h1>Falha na autentica&#231;&#227;o!</h1>
                                            Esta p&#225;gina ser&#225; fechada automaticamente.<br>
                                            Se isto n&#227;o acontecer, pode fech&#225;-la manualmente.
                                        </div>
                                     </body></html>
                                     """)
                #
                #
        # Inicializa o servidor HTTP
        self.server = HTTPServer(('localhost', 8000), AuthHandler)
        self.server.logger = self.logger  # Passa o logger para o servidor

        # Função para monitorar o tempo limite
        def monitor_timeout():
            time.sleep(self.timeout)
            if not hasattr(self.server, 'auth_code'):
                self.response = "tempo limite para autenticação foi excedido"
                self.status_code = 490
                self.logger.error(self.response)
                sys.stdout.close()
                sys.stderr.close()
                sys.stdout = original_stdout
                sys.stderr = original_stderr
                print(f'Código retorno: {self.status_code} ', end='') ## self.status_code = 200, usuário pertence ao grupo informado. self.status_code = 299, grupo existe mas usuário NÃO pertence à ele. Erros retornam 4xx.
                print(f'Resposta: {self.response}', end='\n\n')  
                print('Falha na autenticação! Execução abortada!')
                driver.quit()
                self.server.server_close()
                os._exit(0)       
            #
            #
        # Inicia a thread para monitorar o tempo limite
        timeout_thread = threading.Thread(target=monitor_timeout)
        timeout_thread.start()

        # Espera pelo código de autorização
        self.response = "Esperando pela autenticação..."
        self.logger.info(self.response)
        self.server.handle_request()

        # Restaura stdout e stderr
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = original_stdout
        sys.stderr = original_stderr

        # Verifica se o código de autorização foi obtido dentro do tempo limite
        if not hasattr(self.server, 'auth_code'):
            return

        # Obtém o código de autorização e o estado capturados pelo servidor HTTP
        auth_code = self.server.auth_code
        state = self.server.state

        # Adquire o token usando o código de autorização, verificando o estado
        try:
            result = app.acquire_token_by_auth_code_flow(flow, {"code": auth_code, "state": state})
        except ValueError as e:
            self.response = f"Erro ao obter o token de acesso: {e}"
            self.status_code = 401
            self.logger.error(self.response)
            driver.quit()
            return

        if "access_token" in result:
            access_token = result['access_token']
            headers = {
                'Authorization': 'Bearer ' + access_token
            }

            # Obtém o email do usuário autenticado
            me_response = requests.get(
                'https://graph.microsoft.com/v1.0/me',
                headers=headers
            )
            self.status_code = me_response.status_code
            if me_response.status_code == 200:
                me_data = me_response.json()
                user_email = me_data['userPrincipalName']
                self.response = f"Email do usuário autenticado: {user_email}"
                self.logger.info(self.response)

                # Verifica se o usuário pertence ao grupo
                group_name = self.grupo

                # Obtém o ID do usuário
                user_response = requests.get(
                    f'https://graph.microsoft.com/v1.0/users/{user_email}',
                    headers=headers
                )
                self.status_code = user_response.status_code
                if user_response.status_code == 200:
                    user_data = user_response.json()
                    user_id = user_data['id']

                    # Pesquisa o grupo pelo nome
                    group_response = requests.get(
                        f"https://graph.microsoft.com/v1.0/groups?$filter=displayName eq '{group_name}'",
                        headers=headers
                    )
                    self.status_code = group_response.status_code
                    if group_response.status_code == 200:
                        group_data = group_response.json()
                        if 'value' in group_data and len(group_data['value']) > 0:
                            group_id = group_data['value'][0]['id']

                            # Verifica se o usuário está no grupo
                            members_response = requests.get(
                                f'https://graph.microsoft.com/v1.0/groups/{group_id}/members',
                                headers=headers
                            )
                            self.status_code = members_response.status_code
                            if members_response.status_code == 200:
                                members_data = members_response.json()
                                if 'value' in members_data:
                                    user_in_group = any(member['id'] == user_id for member in members_data['value'])
                                    if user_in_group:
                                        self.response = f"O usuário {user_email} liberado para uso desta aplicação."
                                    else:
                                        self.response = f"O usuário {user_email} NÃO liberado para uso desta aplicação. Solicite acesso à TI."
                                        self.status_code = 299
                                else:
                                    self.response = "Resposta da API de membros não contém a chave 'value'."
                                    self.status_code = 460
                            else:
                                self.response = f"Erro na resposta da API de membros: {members_response.status_code}"
                                self.response += f"\n{members_response.json()}"
                        else:
                            self.response = f"Grupo '{group_name}' não encontrado."
                            self.status_code = 470
                    else:
                        self.response = f"Erro na resposta da API de grupos: {group_response.status_code}"
                        self.response += f"\n{group_response.json()}"
                else:
                    self.response = f"Erro na resposta da API de usuário: {user_response.status_code}"
                    self.response += f"\n{user_response.json()}"
            else:
                self.response = f"Erro ao obter informações do usuário: {me_response.status_code}"
                self.response += f"\n{me_response.json()}"
        else:
            self.response = f"Erro ao obter o token de acesso: {result.get('error')}"
            self.response += f"\n{result.get('error_description')}"
            self.status_code = 480
    
        # Fecha o navegador
        driver.quit()
        service.stop()

        # Define o retorno
        print(f'\nCódigo retorno: {self.status_code} ', end='') ## self.status_code = 200, usuário pertence ao grupo informado. self.status_code = 299, grupo existe mas usuário NÃO pertence à ele. Erros retornam 4xx.
        print(f'Resposta: {self.response}', end='\n\n')  
        if self.status_code == 200:
            print('Acesso autorizado!')
        else:
            print('Permissões inválidas! Execução abortada!')
            os._exit(0)        
        #
        #
    def disclaimer(self): # Mostra o aviso do funcionamento e necessidade de autenticação
        input(f"""
              
        Para ser utilizado de forma adequada e segura, este script requer autenticação no Microsoft Entra ID (antiga Azure AD).
        Também requer que seu usuário pertença a um grupo de segurança específico. Se você não tem a segurança que tem permissão de uso, solicite previamente à TI.
        
        Para continuar, é necessário fornecer suas credenciais, aquelas que costumeiramente utiliza para acessar os serviços de e-mail corporativo.
        Uma janela de navegador será aberta e você será direcionado à tela de Logon do Microsoft Entra ID.
        Faça o Logon fornecendo usuário, senha e validação de duplo fator (no autenticador da Microsoft, instalado em seu celular).        
        Após a autenticação, a janela do navegador será fechada e o script iniciará o processo de execução.

        Você tem {self.timeout} segundos para realizar a autenticação ou a execução será abortada.

        Tecle [ENTER] para continuar ...
        
        """)
        #
        #
class postgreSQL: # Classe de acesso e interação com banco PostgreSQL
    """
    #### Classe **postgreSQL**

    Recursos de interação com o banco de dados relacional PostgreSQL

    1) O método `postgreSQl.db()` exige que as credenciais e parametros de acesso sejam fornecidas em um *dicionário* com, ao mínimo, o seguinte formato:

    ```
    credenciais = {
                    'dbname': 'NOME_BANCO',
                    'user': 'USUARIO'',        
                    'password': 'SENHA',     
                    'host': 'IP_OU_DNS_SERVIDOR',
                    'port': 'PORTA_POSTGRESQL',  ## padrão = 5432
                }

    conexao = postgreSQL.db(credenciais)
    ```

    O nome do schema é ser declarado no contexto da query, mas se desejar alterar o schema padrão, adicione *`'options' : '-c search_path=[NOME_SCHEMA]',`* ao dicionário.

    Qualquer argumento de conexão previsto no pacote *psycopg2* são aceitos como entrada no dicionário acima.

    2) O método `postgreSQl.csv_df()` lê arquivo texto do tipo CSV e o converte para o objeto Dataframe do `pandas`. A assinatura da função exige que se forneça o caminho do arquivo CSV e, opcionalmente o caracter delimitador. Se o caracter demilitador não for informado, será assumido `;`. Considere usar a função `Path` para tratar o caminho do arquivo de origem.

    ```
    from pathlib import Path
    arquivo_csv = Path('./diretorio/arquivo_exemplo.csv')
    dados = postgreSQL.csv_df(arquivo_csv, CsvDelim=',') # usando vírgula como separador. se omisso, assume ";'
    ```

    3) O método `postgreSQl.db_insert_df()` insere dados a partir de um Dataframe (pandas) em uma tabela do banco com estrutura de colunas equivalente.

    A assinatura da função é `postgreSQL.db_insert_df([conexao], [dataframe_origem], [tabela_destino], Schema=None, Colunas=None, OnConflict=None)`

    É necessário que os nomes das colunas do dataframe coincidam com o nome das colunas da tabela. 
    Não há como traduzir/compatibilizar (de-para) nomes de colunas entre o dataframe e a tabela.

    Os três primeiros parametros são posicionais e correspondem, respectivamente, (1) ao objeto da conexão com o banco, (2) ao objeto que contém o dataframe e (3) ao nome da tabela de destino.
    Assume-se que a tabela pertença ao schema padrão (definido na variável _search_path_ do servidor). Caso a tabela de destino esteja em um _schema_ diferente do padrão, deve-se informar seu nome no parâmetro opcional `Schema`.

    O parametro opcional `Colunas` espera um objeto do tipo _lista_ que contenha a relação das colunas a serem importadas. 
    As colunas listadas neste objeto precisam existir nas duas pontas (dataframe e tabela).
    Caso seja omisso, todas as colunas do dataframe serão inseridas na tabela. Neste caso, admite-se que haja colunas na tabela que não exitam no dataframe (serão gravadas como NULL), mas o contrário provocará erro. 

    O último parametro opcional `OnConflict` espera uma declaração para tratar o que fazer caso o dado a ser inserido já exista na tabela, baseado na cláusula [*ON CONFLICT*](https://www.postgresql.org/docs/current/sql-insert.html#SQL-ON-CONFLICT) do comando INSERT. A claúsula deve ser declarada explicita e integralmente nessa variável (clausula, _target_ e _action_) e não há crítica/validação desse argumento, podendo gerar erros se declarado inconforme com o padrão SQL.

    Exemplo de uso:

    ```
    from lbx_toolkit import postgreSQL
    from pathlib import Path

    credenciais = {
                    'dbname': 'NOME_BANCO',
                    'user': 'USUARIO'',        
                    'password': 'SENHA',     
                    'host': 'IP_OU_DNS_SERVIDOR',
                    'port': 'PORTA_POSTGRESQL',  ## padrão = 5432
                }

    conexao = postgreSQL.db(credenciais)

    arquivo_csv = Path('./diretorio/arquivo_exemplo.csv')
    dados = postgreSQL.csv_df(arquivo_csv, CsvDelim=',') # usando vírgula como separador. se omisso, assume ";'

    postgreSQL.db_insert_df(conexao, dados, 'teste_table', Schema='meu_esquema', OnConflict='on conflict (coluna_chave_primaria) do nothing')

    # conexão com o banco precisa ser fechada explicitamente após a chamada do método, caso não seja mais utilizada:
    conexao.close()
    ```

    4) O método `postgreSQl.db_select()` executa consultas no banco de dados e retorna um `cursor` com o resultado.

    A assinatura da função é `postgreSQL.db_select([conexao], [query])`

    São permitidas apenas instruções de consulta (podendo serem complexas, por exemplo, com uso de [CTE](https://www.postgresql.org/docs/current/queries-with.html)). A presença de outras instruções SQL de manipulação de dados e metadados não são permitidas e abortarão a execução da query, se presentes.

    O `cursor` é fechado no contexto do método, antes do retorno, *não podendo* ser manipulado após recebido como retorno da função.

    A função retorna *dois objetos*, o primeiro contendo os dados do cursor, o segundo, contendo os nomes das respectivas colunas.

    Exemplo de uso:

    ```
    from lbx_toolkit import postgreSQL
    from pathlib import Path

    credenciais = {
                    'dbname': 'NOME_BANCO',
                    'user': 'USUARIO'',        
                    'password': 'SENHA',     
                    'host': 'IP_OU_DNS_SERVIDOR',
                    'port': 'PORTA_POSTGRESQL',  ## padrão = 5432
                }

    conexao = postgreSQL.db(credenciais)

    query = 'select * from meu_esquema.teste_table'

    dados, colunas = postgreSQL.db_select(conexao, query)
    conexao.close()
    ```

    5) O método `postgreSQl.db_update()` executa updates no banco

    A assinatura da função é `postgreSQL.db_update([conexao], [query])`

    São permitidas apenas instruções de update. A presença de outras instruções SQL de manipulação de dados e metadados não são permitidas e abortarão a execução da query.

    A função retorna *a quantidade de linhas alteradas*.

    Exemplo de uso:

    ```
    from lbx_toolkit import postgreSQL
    from pathlib import Path

    credenciais = {
                    'dbname': 'NOME_BANCO',
                    'user': 'USUARIO'',        
                    'password': 'SENHA',     
                    'host': 'IP_OU_DNS_SERVIDOR',
                    'port': 'PORTA_POSTGRESQL',  ## padrão = 5432
                }

    conexao = postgreSQL.db(credenciais)

    query = "update meu_esquema.teste_table set coluna='novo_valor' where pk='chave'"

    result = postgreSQL.db_update(conexao, query)
    conexao.close()
    ```

    """    
    def __init__(self, config, logger=None):
        self.logger = logger if not logger is None else lbx_logger(None, logging.DEBUG, '%(levelname)s: %(message)s') # se não fornecer o logger, vai tudo para o console

        try:
            self.Conexao = psycopg2.connect(**config)  ## na chamada de uma função/método, o * explode os valores de um dicionário em argumentos posicionais (só valores) e ** explode discionário em argumentos nominais (nome=valor)
        except Exception as Err:
            raise
        #
        #
    def csv_df(self, CsvPath, CsvDelim=';'): # Le arquivo CSV e gera Dataframe do Pandas
        try:
            DataFrame = pd.read_csv(CsvPath, delimiter=CsvDelim)  # Verifique se o delimitador é ';'
            DataFrame.replace({np.nan: None}, inplace=True)  ## troca 'NaN' por None (null no postgresql)
            return DataFrame
        except Exception as Err:
            raise
        #
        #
    def db_insert_df(self, DataFrame, Tabela, Schema=None, Colunas=None, OnConflict=None): # Insere os dados de um dataframe em uma tabela equivalente no banco (exige mesma estrutura de colunas)
        # Essa função exige que os nomes dos cabeçalhos das colunas do CSV sejam os mesmos das colunas da tabela de destino
        Colunas = Colunas or DataFrame.columns.tolist()     # Caso não seja fornecida a lista de colunas, assume as colunas do DataFrame
        Valores = [tuple(Linha) for Linha in DataFrame[Colunas].values]    
        Schema = Schema or 'public'
        Query = f'insert into {Schema}.{Tabela} ({', '.join(Colunas)}) values %s '
        if not OnConflict is None:
            Query = Query + OnConflict

        try:
            self.Cursor = self.Conexao.cursor() 
            execute_values(self.Cursor, Query, Valores)  
            self.Conexao.commit()
        except Exception as Err:
            self.Conexao.rollback()
            raise
        finally:        
            self.Cursor.close()
            #Conexao.close() ## conexão precisa ser fechada explicitamente fora da classe
        #
        #
    def db_select(self, Query): # Retorna um cursor à partir de um select
        BlackList = ['INSERT ', 'DELETE ', 'UPDATE ', 'CREATE ', 'DROP ', 'MERGE ', 'REPLACE ', 'CALL ', 'EXECUTE ']
        if any(element in Query.upper() for element in BlackList):
            BlackListed = [element for element in BlackList if element in Query.upper()]          
            self.logger.erro(f'{__name__}: Este método permite apenas consultas. A query informada possui as seguintes palavras reservadas não aceitas: {BlackListed} e não foi executada!')
            return None    
        else:
            try:
                self.Cursor = self.Conexao.cursor()
                self.Cursor.execute(Query)
                Dados = self.Cursor.fetchall()
                Colunas = [Col[0] for Col in self.Cursor.description]
                self.Conexao.commit()
                self.Cursor.close()
                return Dados, Colunas
            except Exception as Err:
                self.Conexao.rollback()
                raise   
        #
        #
    def db_update(self, Query): # Retorna um cursor à partir de um select
        UpdRows = 0
        BlackList = ['INSERT ', 'DELETE ', 'SELECT ', 'CREATE ', 'DROP ', 'MERGE ', 'REPLACE ', 'CALL ', 'EXECUTE ']
        if any(element in Query.upper() for element in BlackList):
            BlackListed = [element for element in BlackList if element in Query.upper()]          
            self.logger.erro(f'{__name__}: Este método permite apenas updates. A query informada possui as seguintes palavras reservadas não aceitas: {BlackListed} e não foi executada!')
            return None            
        else:
            try:
                self.Cursor = self.Conexao.cursor()
                self.Cursor.execute(Query)
                UpdRows = self.Cursor.rowcount
                self.Conexao.commit()
                self.Cursor.close()
                return UpdRows
            except Exception as Err:
                self.Conexao.rollback()
                raise  
        #
        #
class api_rest: # Classe para interação com APIs Rest (especialmente Sienge)
    """
    #### Classe **api_rest**

    Destina-se a interatir com APIs RESTfull, em especial as publicadas pela SoftPlan para a [Plataforma Sienge](https://api.sienge.com.br/docs/).

    A classe deve ser instanciada conforme sintaxe abaixo:

    `api_rest(url, credenciais, cadencia, timeout=6, logger=None, headers={"Content-Type": "application/json"}, verify=True)`

    São nessários 2 parâmetros posicionais obrigatórios, e 5 parametros nominais facultativos (valor padrão, se omisso, indicado na sintaxe acima):
    - `url`: o endereço da URL de autenticação da API
    - `crednciais`: Dicionário com credenciais de autenticação. 
    - `cadencia` Número máximo de chamadas *por segudo* à API 
    - `timeout` Tempo máximo (segundos) para aguardar retorno à chamada. Padrão 6s, se omisso.
    - `logger` O objeto _log handler_ para lidar com as informações de saída. Se não informado, todas as saídas serão direcionadas para a stdout.
    - `headers` Cabeçalhos _http_ para a requisição à API.
    - `verify` Verifica a validade do certificado SSL do servidor de destino da requisição.

    Quanto às credenciais de autenticação, assim como a classe de interação com o PostgreSQL, elas precisam ser fornecidas na forma de um *dicionário*. 
    Para o método `api_rest.aut_basic()`, o formato deve ser: 
    ```
    credenciais = {
                    'user': 'USUARIO_API',
                    'password': 'TOKEN_USUARIO'
                }
    ```
    Caso a autenticação seja pelo método `api_rest.aut_bearer()`, o dicionário deve corresponder ao formato previsto pelo endpoint e seu conteúdo será enviado como um JSON ao endereço indicado no parametro `url`


    A classe possui 3 métodos: 
    - `api_rest.auth_basic()`: instanciamento da sessão autenticando pelo método HTTPBasicAuth
    - `api_rest.auth_bearer()`: instanciamento da sessão autenticando pelos métodos OAuth, JWT, Bearer    
    - `api_rest.endpoint_json([endereço], [método], payload=None)`: para a chamada ao endpoint
    - `close()` para encerra a instância/sessão

    O consumo é feito pelo método `api_rest.endpoint_json` que suporta apenas APIs cujo payload (opcional) seja aceito no formato JSON. 

    Esse método espera 2 parametros posicionais obrigatórios: o endereço do endpoint e o verbo (get, post, patch ou put), tendo parametro opcional o objeto de 'payload' (json). 
    Note que o endereço do endpoint deve ser informado completo. A URL informada no instanciamento da classe corresponde apenas ao endereço de autenticação. 

    O tempo, em segundos, transcorrido entre a chamada a atual e a chamada anterior ao endpoint pode ser consultado pelo argumento `.Intervalo` no objeto recebido do retorno à chamada ao método `.endpoint_json`. 

    Da mesma forma, o tempo de espera imposto para respeitar a cadência do webservcie também pode ser consultado pelo argumento `.Espera`.

    Exemplo de uso:

    ```
    from lbx_toolkit import api_rest

    UrlBase=r'https://api.sienge.com.br/lbx/public/api/v1'
    Credenciais = {
                    'user': 'USUARIO_API',
                    'password': 'TOKEN_USUARIO'
                }
    ApiSienge = api_rest(UrlBase,Credenciais,2.5) # limite de 2 requisições/segundo para cadência de chamada ao endpoint
    Auth = ApiSienge.auth_basic()

    Nutitulo=input('Numero do título:')
    Nuparcela=input('Numero da parcela:')
    Vencimento=input('Vencimento [AAAA-MM-DD]:')
    Payload = {
                    "dueDate": f"{Vencimento}"
                }
    EndPoint = f'{UrlBase}/bills/{Nutitulo}/installments/{Nuparcela}'

    #chama o endpoint e recebe o retorno no objeto AlteraVcto
    AlteraVcto = ApiSienge.endpoint_json(EndPoint, 'patch', Payload)
    ```

    No exemplo acima não é esperado que o endpoint retorne nenhum dado (`patch`).

    Quando se usa o verbo `get` e se espera o retorno de algum dado, use o método `.json` do pacote `request` para acessar o objeto recebido.

    Para uso em APIs com autenticação JWT (JSON Web Token), OAuth, Bearer Token Authentication, a construção é a mesma indicada acima, bastando-se usar `.auth_bearer()` ao invés de _.auth_basic()_, e ajustar o dicionário `credenciais` informado no instanciamento da classe, que deve ser estruturado conforme o padrão fornecido peo mantendor da API e será enviado como payload ao endpoint (`json=credenciais`). 

    """
    def __init__(self, url, credenciais, cadencia=3, timeout=6, logger=None, headers={"Content-Type": "application/json"}, verify=True):
        self.logger = logger if not logger is None else lbx_logger(None, logging.DEBUG, '%(levelname)s: %(message)s') # se não fornecer o logger, vai tudo para o console

        if not validators.url(url):
            self.logger.critico('URL inválida: {url}. Primeiro parametro precisar uma URL válida. Script abortado', exit=1)
        if not isinstance(credenciais, dict):
            self.logger.critico('O segundo parametro posicional precisa ser um dicionário. Script abortado', exit=1)

        self.RetEndPoint = None  # Inicializa self.RetEndPoint como None            
        self.Headers = headers
        self.Verify = verify            
        self.Url = url
        self.Timeout = timeout
        self.Credenciais = credenciais
        self.Cadencia = 1/cadencia  ## candencia corresponde a chamadas por segundo, não minuto
        self.TempoUltReq = None 
        self.Intervalo = self.Cadencia + 1     
        #
        #
    def controla_cadencia(self): ## para controle apenas, não deve ser chamada fora da classe
        # Verificar o tempo atual
        Agora = time.time()
        
        # Calcular intervalo entre requisições
        if self.TempoUltReq:
            self.Intervalo = Agora - self.TempoUltReq
        else:
            self.Intervalo = float('inf')  # Primeira requisição não espera
        
        # Calcular o tempo de espera necessário para respeitar o limite
        if self.Intervalo < self.Cadencia:
            self.Espera = self.Cadencia - self.Intervalo
            time.sleep(self.Espera)
            return self.Espera
        else:
            self.Espera = 0
            return self.Espera, self.Intervalo
        #
        #
    def auth_basic(self): # Autentica e abre sessão na API 
        if not self.Credenciais['user'] or not self.Credenciais['password']:
            self.logger.critico('Dicionário de credenciais não possui chaves "user" e/ou "password". Script abortado', exit=1)             
        try:          
            self.Sessao = requests.Session()
            #Sessao.auth = (ApiUser, ApiPass)
            self.Sessao.auth = HTTPBasicAuth(self.Credenciais['user'], self.Credenciais['password'])
            Auth = self.Sessao.post(self.Url)  
            #print(f'Status: {Auth.status_code}')
            #print(f'Retorno: {Auth.text}')
            return self.Sessao
        except Exception as Err:
            self.logger.critico(f"Falha ao autenticar API: {Err}. URL: {self.Url}", exit=1)
        #
        #
    def auth_bearer(self): # Autentica e abre sessão na API
        #self.UrlLogin = UrlLogin if UrlLogin is not None else self.Url
        try:          
            self.Sessao = requests.Session()
            Token = self.Sessao.post(self.Url, headers=self.Headers, json=self.Credenciais, verify=self.Verify)            
            self.Headers.update({"Authorization": f"Bearer {Token.text}"})
            if 200 <= Token.status_code <= 299:
                self.Sessao.status_code = Token.status_code
                self.Sessao.token = Token.text
                return self.Sessao
            else:
                self.logger.critico(f"Erro ao autenticar API: {Token.status_code} - {Token.text}", exit=1)    
        except Exception as Err:
            self.logger.critico(f"Falha ao autenticar API: {Err}. URL: {self.Url}", exit=1)    
        #
        #
    def endpoint_json(self, endpoint, metodo, payload=None): # Interage com End Point
        self.ult_tempo_req = time.time() 
        self.Metodo = metodo.lower()
        #self.EndPoint = self.Url + endpoint
        self.EndPoint = endpoint
        self.Payload = payload
        MetodosAceitos = ['post', 'get', 'patch', 'put']
        if not any(element in self.Metodo for element in MetodosAceitos):
            self.logger.critico(f'Método {self.Metodo} não previsto. Abortando chamada!', exit=1)
        else:
            ChamadaApi = f'self.Sessao.{self.Metodo}(self.EndPoint, timeout=self.Timeout, headers=self.Headers, verify=self.Verify)' if self.Payload is None else f'self.Sessao.{self.Metodo}(self.EndPoint, timeout=self.Timeout, headers=self.Headers, verify=self.Verify, json=self.Payload)'
            self.controla_cadencia()
            self.TempoUltReq = time.time()   
            try: 
                self.RetEndPoint = eval(ChamadaApi)
                if self.RetEndPoint.status_code >= 500:
                    self.logger.critico(f'Erro {self.RetEndPoint.status_code} na chamada do endpoint: {Err}\nEndpoint: {self.EndPoint}\nResposta: {self.RetEndPoint.text}', exit=1)   
                self.RetEndPoint.Espera = self.Espera ## adiona o tempo de espera ao retorno da API
                self.RetEndPoint.Intervalo = self.Intervalo ## adiciona o intervalo entre chamada ao retorno da API                                
                return self.RetEndPoint
            except requests.exceptions.ReadTimeout as Err:
                self.logger.critico(f'Excedido tempo limite {self.Timeout} para retorno do endpoint: {Err}\nEndpoint: {self.EndPoint}', exit=1)            
            except Exception as Err:
                self.logger.critico(f'Falha na chamada do endpoint: {Err}\nEndpoint: {self.EndPoint}\nCodigo retorno: {self.RetEndPoint.status_code}\nResposta:{self.RetEndPoint.text}', exit=1)
        #
        #
    def trata_erro_sienge(CodRet, Retorno):
        if not 200 <= CodRet <= 299:        
            try:
                DicRetorno = eval(Retorno.replace('null','None').replace(r'\n\t',' '))
                if 'clientMessage' in DicRetorno and DicRetorno['clientMessage'] not in ['None', None, '', ' ', 'null']:
                    MsgErro = DicRetorno['clientMessage']
                elif 'developerMessage' in DicRetorno and DicRetorno['developerMessage'] not in ['None', None, '', ' ', 'null']:
                    MsgErro = DicRetorno['developerMessage']
                elif 'message' in DicRetorno and DicRetorno['message'] not in ['None', None, '', ' ', 'null']:
                    MsgErro = DicRetorno['message']
                else:
                    MsgErro = Retorno
            except:
                MsgErro = Retorno.replace(r'\n\t',' ')        
            finally:
                return MsgErro
        else:
            return Retorno      
        #
        #
    def close(self): # Encerra a cessão
        self.Sessao.close()                   
        #
        #
class lbx_logger: # Classe para gerenciar a saída para log
    r"""
    #### Classe **lbx_logger**

    Essa classe requer a importação do módulo `logging` no script em que for instanciada e tem o propósito de manipular/formatar as mensagens de saída do script, alterando o formato e redirecionando destino padrão (stdout e stderr) para uma combinação de tela e/ou arquivo.

    O comportamento padrão é registrar todas as saídas *simultaneamente* em tela e no arquivo com endereço informado no parâmetro `log_file_path`. Se este parametro for omisso no instanciamento da classe, as mensagens serão exibidas apenas na tela.

    A mensagens devem ser classificadas por grau de severidade/relevância, da menor para a maior, na seguinte ordem: *debug, info, warning (aviso), error (erro), critical (critico)*

    A classificação do nível de serveridade da mensagem se dá pelo método escolhido para invocar a mensagem, correspondente aos níveis de severidade equivalentes.

    A classe deve ser instanciada conforme sintaxe abaixo:

    `lbx_logger(log_file_path=None, log_level=logging.DEBUG, formato_log='%(asctime)s - %(levelname)s - %(message)s', modulo=None, ignore_console=None, ignore_file=None):`

    Todos os parametros são nominativos e facultativos. Em caso de omissão, os valores padrão são assumidos conforme o exemplo acima.

    Os parametros para o instanciamento da classe são:

    - `log_file_path` Define o caminho e o nome do arquivo de log. Se omisso, as mensagens serão todas direcionadas apenas para a tela.
    - `log_level` Define o nível mínimo de severidade das mensagens a serem manipuladas pelo logger. Se omisso, será assumido o nível mais baixo (_debug_). As mensagens com nível abaixo do especificado são descartadas. Os níveis devem ser informados de acordo com a sintaxe acima (prefixados com _logging._ e com o nome do nível em inglês e maiúsculas). Exemplo: 
    - `logging.DEBUG` para manipular chamadas do método *.debug()* e acima.
    - `logging.INFO` para manipular chamadas do método *.info()* e acima.
    - `logging.WARNING` para manipular chamadas do método *.aviso()* e acima.
    - `logging.ERROR` para manipular chamadas do método *.erro()* e acima.
    - `logging.CRITICAL` para manipular chamadas do método *.critico()* e acima.        
    - `formato_log` Define o formato em que a mensagem será apresentada. Se omisso, o padrá é *DATA_HORA - NIVEL - MENSAGEM*. Para maiores opções veja: [Atributos de log](https://docs.python.org/3/library/logging.html#logrecord-attributes)
    - `modulo` Nome do módulo para o qual os logs serão monitorados. Permite instanciar várias vezes a classe para criar manipuladores diferentes para módulos diferente. Informe o nome do módulo para criar um log específico para ele ou simplesmente omita o parametro para criar um log para o script em geral.
    - `ignore_console` Lista com os níveis de severidade a serem ignorados para *apresentação na tela*, registrando *apenas no arquivo* (quando informado no parametro `log_file_path`) e obedecendo ao nível mínimo estabelecido no parametro `log_level`. Note que omitir o parametro `log_file_path` e incluir um nível na lsita `ignore_console` implica em ignorar/suprimir esse nível de mensagem de qualquer apresentação.
    - `ignore_file` Mesma lógica do parametro `ignore_console`, mas com lógica invertida: suprime o registro do nível do arquivo e demonstra *apenas na tela*.

    1) As mensagem são manipuladas substituindo-se o comando `print()` pela chamada a um dos 5 métodos acima (_.add(), .debug(), .info(), .aviso(), .erro(), .critico()_). Exceto o método `.add()`, qualquer um dos demais métodos pode interromper a execução do script, através da passagem do parâmetro `exit`. Ao informar esse parametro na chamadada do método, atribua a ele o código de saída desejado (0 para normal, qualquer outro número para saída com erro). Exemplo:

    ```
    log.erro('Essa mensagem apenas resulta em uma mensagem de nível ERROR')
    log.erro('Essa mensagem resulta em uma mensagem de nível ERRO e encerra o script com código de retorno -1', exit=-1)
    ```

    Qualquer chamada ao comando `print()`, uma vez instanciado manipulador de log, será registada como uma chamada ao método _.info()_ e registrada com este nível de severidade. 
    Para retornar ao comportamente padrão do comando print, ou interromper o manipulador, faça chamada ao método `.stop_logging()`

    2) O método _.add()_ não exibe/grava imediatamente a mensagem, mas apenas a diciona a _buffer_. Todas as chamas a _.add()_ irão concatenar a mensagem recebida até a próxima chamada em algum dos níveis _.debug(), .info(), .aviso(), .erro(), .critico()_. Na primeira chama de um destes níveis após uma (ou mais) chamada(s) ao método _.add()_ o *buffer* será concatenado à mensagem recebida por um destes métodos e o resultado será manipulado pelo log conforme os parametros definidos no intanciamento da classe e o método chamado. Essa função é útil para tratar mensagens com retorno condicional. Exemplo:

    ```
    log.add('Mensagem 1# ') ## não será exibida/registrada
    log.add('Mensagem 2# ') ## não será exibida/registrada
    log.info('Mensagem 3) ## será exibida/registrada como nível "info" e com texto: "Mensagem 1# Mensagem 2# Mensagem 3"
    ```

    3) Os métodos que exibem as mensagens (`.debug()`,`.info()`,`.aviso()`, `.erro()`, `.critico()`) possuem 3 parametros: `message`, `corte=None`, `exit=None`.

    - `message`: posicional e obrigatório. corresponde à mensagem a ser exibida
    - `corte`: o tamanho máximo da mensagem a ser exibida. opcional e se omitido, exibe a mensagem inteira. se fornecido, corta a mensagem no comprimento informado
    - `exit`: opcional. se informado (requer um código de retorno), aborta o script com o código informado. se omisso (padrão) a mensagem apenas é minutada pelo log, sem interferir no funcionamento do script

    4) O método `.filtra()` possui 3 parametros posicionais, todos opcionais: `log_file`, `dh_ini`, `dh_fim`.

    Se os 3 forem omitidos, serão exibidas as entradas de log do arquivo corrente, definido no instanciamento da classe `lbx_logger`, registradas na última hora. Deste modo, o valor padrão para `dh_fim` é `now()`  e para `dh_ini` é `now()` menos 1 hora.

    Caso queira filtrar os registro de outro arquivo de log, que não seja o do script corrente, informe o endereço do arquivo no primeiro parametro.

    E caso queira alterar alterar o período de filtragem, informe nos parametros 2 e 3 a data/hora de início e fim do período. Estes dois parametros aceitam tanto um objeto do tipo `datetime` como uma string (que será convertida para datetime), desde que ela esteja no formato `dd/mm/aaaa hh:mm:[ss]` (segundos são opcionais).

    Considerando que os parametros são posicionais, caso queira omitir apenas um dos parametros, preencha a posição do parametro a ser omitido com `None`.

    A saída dessa função retorna um objeto, que pode ser salvo em disco ou impresso na tela.


    5) Exemplos de uso:

    ```
    from lbx_toolkit import lbx_logger 
    import logging
    import os
    from pathlib import Path

    DirBase = Path('./')  # diretório corrente do script
    BaseName = os.path.splitext(os.path.basename(__file__))[0] # nome do script sem extensão
    LogFile = Path(DirBase, BaseName + '.log') # salva logs no diretório corrente, em um arquivo nomeado com nome do script + extensão ".log"

    ### instancia o manipulador para tratar todas as mensagens (nível DEBUG acima), 
    #   mas suprime a apresentação em tela das mensagens de nível "DEBUG" na tela, 
    #   apenas registrando-as somente no arquivo
    #   e sumprime o registro no arquivo das mensagens de nível "ERROR", 
    #   mostrando-as apenas na tela
    log = lbx_logger(LogFile, logging.DEBUG, ignore_console=[logging.DEBUG], ignore_file=[logging.ERROR]) 

    # Exemplo de mensagens de log
    log.debug('Esta é uma mensagem de debug') 
    log.info('Esta é uma mensagem informativa')
    log.add('Esta mensagem não será exibida agora, mas acumulada no buffer# ')
    log.aviso('Esta é uma mensagem de aviso')
    log.erro('Esta é uma mensagem de erro')
    log.erro('Esta é uma mensagem erro muito comprida e será limitada a 40 caracteres, o restante será cortado e ingorado ao ser manipulado', 40)
    log.critico('Esta é uma mensagem crítica')

    # Exemplo de função que gera uma exceção
    def funcao_com_erro():
        raise ValueError('Este é um erro de exemplo')

    # Testando redirecionamento de print e captura de exceção
    print('Mensagem de teste via print')
    try:
        funcao_com_erro()
    except Exception as e:
        print(f'Capturado um erro: {e}')

    log.erro('Essa é uma mensagem de erro e abortará a execução do script', exit=1)

    log.info('Essa mensagem não será exibida pois o script foi abortado na mensagem anterior')

    # obtem os registros de log da última hora (comportamento padrão)
    filtra_log = log.search() 

    # obtem os registros das últimas 6 horas
    ultimas_6h = datetime.datetime.now() - datetime.timedelta(hours=6) ## carimbo de tempo de 6 horas atrás !!! requer>> import datetime
    filtra_log = log.search(None, ultimas_6h) # None no 1º parametro impõe o log do arquivo corrente como padrão (definido em 'LogFile' e apontado no instanciamento da classe)

    # obtem os registros do dia 14/01/2020 até 3h atrás
    ultimas_3h = datetime.datetime.now() - datetime.timedelta(hours=3) ## carimbo de tempo de 6 horas atrás !!! requer>> import datetime
    filtra_log = log.search(None, '14/01/2020 00:00', ultimas_3h) # 

    # obtem os registros do horário comercial do dia 23/12/2023 do arquivo salvo em C:\temp\outro_arquivo.log
    Outro_Log = Path(r'c:\temp\outro_arquivo.log')
    filtra_log = log.search(Outro_Log, '23/12/2023 08:00', '23/12/2023 18:00') # 

    # salva conteúdo filtrado em um arquivo:
    filtrado = 'filtered_log.txt'
    with open(filtado, 'w', encoding='ISO-8859-1') as output_file:  # indique o enconding conforme salvo (UTF-8 ou ISO-8859-1)
        output_file.writelines(filta_log)    

    # mostra o conteúdo filtrado na tela
    print(''.join(filtra_log))

    # mostra o conteúdo filtrado na tela, listando apenas as os registros do nível "DEBUG"
    for line in filtered_lines:
        if "DEBUG" in line:
            print(line, end='')
    ```
    """    
    class LevelFilter(logging.Filter):    
        def __init__(self, levels_to_ignore):
            self.levels_to_ignore = levels_to_ignore
            #
            #         
        def filter(self, record):
            return record.levelno not in self.levels_to_ignore
            #
            #
    def __init__(self, log_file_path=None, log_level=logging.DEBUG, formato_log='%(asctime)s - %(levelname)s - %(message)s', modulo=None, ignore_console=None, ignore_file=None):
        self.ignore_file = [] if ignore_file is None else ignore_file       
        self.ignore_console = [] if ignore_console is None else ignore_console
        self.modulo = __name__ if modulo is None else modulo
        self.logger = logging.getLogger(self.modulo)
        self.logger.setLevel(log_level)
        self.msg = ''
        self.log_file_path = log_file_path
        
        if log_file_path:
            # Criando um handler para escrever em um arquivo de log
            file_handler = logging.FileHandler(self.log_file_path)
            file_handler.setLevel(log_level)  # Sempre registrar tudo no arquivo
            
            # Criando um handler para exibir no console
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)  # Registrar DEBUG e acima no console
            
            # Adicionando filtro para ignorar certos níveis no console e no arquivo
            file_handler.addFilter(self.LevelFilter(self.ignore_file))
            console_handler.addFilter(self.LevelFilter(self.ignore_console))

            # Definindo o formato das mensagens de log
            formatter = logging.Formatter(formato_log)
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            # Adicionando os handlers ao logger
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
        else:
            # Tudo direcionado para o console
            console_handler = logging.StreamHandler()
            console_handler.setLevel(log_level)  # Registrar no console
            
            # Adicionando filtro para ignorar certos níveis no console e no arquivo
            console_handler.addFilter(self.LevelFilter(self.ignore_console))        

            # Definindo o formato das mensagens de log
            formatter = logging.Formatter(formato_log)
            console_handler.setFormatter(formatter)
            
            # Adicionando o handler ao logger
            self.logger.addHandler(console_handler)
        
        # Redirecionando exceções para o logger
        sys.excepthook = self.handle_exception
        
        # Redirecionando saída padrão
        self.original_stdout = sys.stdout
        sys.stdout = self
        #
        #
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        self.logger.error("Exceção não prevista", exc_info=(exc_type, exc_value, exc_traceback))
        #
        #
    def print(self, *args, **kwargs):
        # Imprime diretamente na saída padrão
        print(*args, **kwargs, file=self.original_stdout)
        #
        #
    def add(self, message, corte=None):
        message = message[:corte] if corte else message
        self.msg = self.msg + message if not message is None else self.msg
        #
        #     
    def write(self, message):
        if message.strip():  # Ignorar mensagens vazias
            self.logger.info(message.strip())
        #
        #
    def flush(self):
        pass  # Método necessário para compatibilidade com sys.stdout
        #
        #
    def debug(self, message, corte=None, exit=None):
        self.msg = self.msg + message if not message is None else self.msg
        msg = self.msg[:corte] if corte else self.msg
        self.logger.debug(msg)
        self.msg = ''
        if exit:
            os._exit(exit)
        #
        #
    def info(self, message, corte=None, exit=None):
        self.msg = self.msg + message if not message is None else self.msg
        msg = self.msg[:corte] if corte else self.msg
        self.logger.info(msg)
        self.msg = ''
        if exit:
            os._exit(exit)        
        #
        #     
    def aviso(self, message, corte=None, exit=None):
        self.msg = self.msg + message if not message is None else self.msg
        msg = self.msg[:corte] if corte else self.msg
        self.logger.warning(msg)
        self.msg = ''
        if exit:
            os._exit(exit)
        #
        #
    def erro(self, message, corte=None, exit=None):
        self.msg = self.msg + message if not message is None else self.msg
        msg = self.msg[:corte] if corte else self.msg
        self.logger.error(msg)
        self.msg = ''
        if exit:
            os._exit(exit)
        #
        #
    def critico(self, message, corte=None, exit=None):
        self.msg = self.msg + message if not message is None else self.msg
        msg = self.msg[:corte] if corte else self.msg
        self.logger.critical(msg)
        self.msg = ''
        if exit:
            os._exit(exit)
        #
        #
    def stop_logging(self):
        # Restaurar o stdout original
        sys.stdout = self.original_stdout
        # Remover handlers do logger
        handlers = self.logger.handlers[:]
        for handler in handlers:
            handler.close()
            self.logger.removeHandler(handler)
        #
        #
    def filtra(self, log_file, dh_ini, dh_fim):
        # Validar parametros de entrada
        if dh_ini:
            if not isinstance(dh_ini, datetime.datetime):
                if not re.fullmatch(r'([0-3][0-9]/[0-1][0-2]/[1-2][0-9]{3} [0-2][0-9]\:[0-6][0-9])(\:[0-6][0-9]){0,1}', dh_ini):
                    self.logger.error(f'Data/Hora início {dh_ini} em formato inválido. Informe um objeto do tipo "datetime" ou uma string no formato "dd/mm/aaaa hh:mm:[ss]"')
                    return None                
                elif len(dh_ini) == 16:  # Formato 'dd/mm/yyyy hh:mm'
                    dh_ini += ":00"
                try:
                    self.inicio = datetime.datetime.strptime(dh_ini, '%d/%m/%Y %H:%M:%S')
                except:
                    self.logger.error(f'Data/Hora início {dh_ini} em formato inválido. Informe um objeto do tipo "datetime" ou uma string no formato "dd/mm/aaaa hh:mm:[ss]"')
                    return None
            else:
                self.inicio = dh_ini
        else:
            self.inicio = datetime.datetime.now() - datetime.timedelta(hours=1) ## assume a última hora como intervalo, se omisso

        if dh_fim:
            if not isinstance(dh_fim, datetime.datetime):
                if not re.fullmatch(r'([0-3][0-9]/[0-1][0-2]/[1-2][0-9]{3} [0-2][0-9]\:[0-6][0-9])(\:[0-6][0-9]){0,1}', dh_ini):
                    self.logger.error(f'Data/Hora fim {dh_fim} em formato inválido. Informe um objeto do tipo "datetime" ou uma string no formato "dd/mm/aaaa hh:mm:[ss]"')
                    return None                
                elif len(dh_fim) == 16:  # Formato 'dd/mm/yyyy hh:mm'
                    dh_fim += ":00"
                try:
                    self.fim = datetime.datetime.strptime(dh_fim, '%d/%m/%Y %H:%M:%S')
                except:
                    self.logger.error(f'Data/Hora fim {dh_fim} em formato inválido. Informe um objeto do tipo "datetime" ou uma string no formato "dd/mm/aaaa hh:mm:[ss]"')
                    return None
            else:
                self.fim = dh_fim
        else:
            self.fim = datetime.datetime.now() ## assume a última hora como intervalo, se omisso

        if not log_file and not self.log_file_path:
            self.logger.critical('Nenhum arquivo de log disponível. Log desta instância configurado apenas para exibição em tela, sem registro em arquivo')
            return None
        elif not log_file and self.log_file_path:
            log_file_path = self.log_file_path
        elif log_file:
            if Path(log_file).is_file():
                log_file_path = log_file
            else:
                self.logger.critical(f'Arquivo de log {log_file} não existe!')
                return None
        else:
            self.logger.critical('Erro validação arquivo de entrada. Abortando!')
            return None
                   
        # Função para verificar se a linha está dentro do intervalo de tempo
        def is_within_time_range(timestamp, dh_inicio, dh_fim):
            return dh_inicio <= timestamp <= dh_fim

        # Ler e filtrar o arquivo de log com a codificação ISO-8859-1
        with open(log_file_path, 'r', encoding='ISO-8859-1') as log_file:
            log_lines = log_file.readlines()

        # Variável para armazenar o último timestamp válido
        last_valid_timestamp = None
        filtered_lines = []

        for line in log_lines:
            try:
                # Extraia a data e a hora da linha
                timestamp_str = line.split()[0] + " " + line.split()[1]
                timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
                last_valid_timestamp = timestamp
                if is_within_time_range(timestamp, self.inicio, self.fim):
                    filtered_lines.append(line)
            except Exception as e:
                # Caso a linha não tenha um carimbo de tempo, use o último timestamp válido
                if last_valid_timestamp and is_within_time_range(last_valid_timestamp, self.inicio, self.fim):
                    filtered_lines.append(line)

        # Retornar o objeto contendo as linhas filtradas
        return filtered_lines
        #
        #         
class misc: # Classe de miscelâneas
    """
    #### Classe **misc**

    Classe que reune pequenas funções uteis para agilizar tarefas comuns.

    Sintaxe e exemplos de uso. Parametros omissos assume  os valores padrão indicados abaixo:

    - `Arquivo = seleciona_arquivo(DirBase, TiposArquivo=[('Todos os arquivos', '*.*')], Titulo='Selecionar arquivo')`
    - `Diretório = seleciona_dir(DirBase=Path(r'./'), Titulo='Selecionar diretório'):`
    - `NomeLimpo = normaliza('String # SEM Noção!') #>>> string_sem_nocao`
    - `cmd_window = get_cmd_window()`
    - `maximize_console()`    
    """
    def __init__(self):
        pass
        #
        #    
    def seleciona_arquivo(DirBase, TiposArquivo=[('Todos os arquivos', '*.*')], Titulo='Selecionar arquivo'): # Picker para selecionar arquivo
        root = tk.Tk()
        root.withdraw()  # Esconde a janela principal do Tkinter
        Arquivo = filedialog.askopenfilename(initialdir=DirBase, filetypes=TiposArquivo, title=Titulo)
        Arquivo = Path(Arquivo)
        root.destroy()
        return Arquivo
        #
        #
    def seleciona_dir(DirBase=Path(r'./'), Titulo='Selecionar diretório'): # Picker para selecionar diretório
        root = tk.Tk() # objeto picker  (Tkinter)para selecionar arquivos e diretórios
        root.withdraw()  # Esconde a janela principal do Tkinter
        Diretorio = filedialog.askdirectory(initialdir=DirBase, title=Titulo)
        Diretorio = Path(Diretorio)
        root.destroy()
        return Diretorio
        #
        #
    def normaliza(Original): # Limpa e padroniza nomes
        Lixo = r'/\\?%§ªº°`´^~*:|"<>!@#$%¨&*()_+=-[]{}"\' ' 
        Normalizar = normalize('NFKD', Original).encode('ASCII', 'ignore').decode('ASCII')
        RemoverLixo = [c if c not in Lixo else '_' for c in Normalizar]    
        Limpo = "".join(RemoverLixo)
        Limpo = re.sub(r'\.(?=.*\.)', '_', Limpo) # troca todos os pontos por underline
        Limpo = re.sub(r'_+', '_', Limpo)  # limpa as reptições do underline
        return Limpo.lower()
        #
        #
    def get_cmd_window(): # Captura a referencia da janela atual para retornar o foco à ela depois de chamar os pickers
        pid = os.getpid()
        windows = gw.getWindowsWithTitle("")
        for window in windows:
            if window.title and window.visible and window.topleft:
                return window
        return None
        #
        #
    def maximize_console(): # Ajustar o buffer de console
        # os.system('mode con: cols=500 lines=100')
        # Obter o handle da janela do console
        kernel32 = ctypes.WinDLL('kernel32')
        user32 = ctypes.WinDLL('user32')
        hWnd = kernel32.GetConsoleWindow()
        if hWnd:
            # Definir as dimensões da tela
            user32.ShowWindow(hWnd, 3)  # 3 = SW_MAXIMIZE  
        #
        #
class ConfigManager: # Inicializa e recupera variáveis em ambiente de intercâmbio entre classes
    """
        Como Funciona
        Singleton Pattern: ConfigManager é um singleton que garante que todas as partes do código usem a mesma instância e, portanto, compartilhem a mesma configuração.
        Inicialização com Argumentos Dinâmicos: O método initialize usa **kwargs para aceitar qualquer número de pares chave-valor, armazenando-os no dicionário _config da instância.
        Método Genérico get: O método get aceita uma chave como argumento e retorna o valor correspondente do dicionário _config.
        Método set: O método set permite adicionar ou atualizar dinamicamente valores no dicionário _config.
        Método reset: O método reset limpa todas as configurações armazenadas, permitindo uma nova inicialização do ConfigManager com novos valores    
    """
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._config = {}
        return cls._instance
        #
        #
    @classmethod
    def initialize(cls, **kwargs):
        instance = cls()
        for key, value in kwargs.items():
            instance._config[key] = value
        #
        #
    @classmethod
    def get(cls, key):
        return cls._instance._config.get(key)
        #
        #
    @classmethod
    def set(cls, key, value):
        cls._instance._config[key] = value
        #
        #
    @classmethod
    def reset(cls):
        cls._instance._config = {}
        #
        #
    #
    #
class Servicer(): # Cria um daemon para rodar como serviço
    """
        Classe base que implementa as rotinas padrão para a criação dameons/serviços do windows.
        Além de iniciar e interromper o daemon/serviço, a classe implementar os métodos daemon_logs() e cleanup(), dependencias de run() e stop() que criam um arquivo de log do serviço/daemon (não do script em si) e um arquivo PID para o monitor de serviços.
        Os métodos padrão são init(), run() e stop() e não devem ser redefinidos/sobrecarregados.
        Para ser funcional, é necessária a criação de uma classe local que herde essa classe e redefina (por sobrecarga) ao menos os métodos on_run, on_start e args_parser(). on_init é opcional.
        Outros métodos complementares são oferidos para init, run e stop, permitindo injetar código no ínicio (pre) e fim (pós) os respectivos métodos (on_init_pre(), on_init_pos(), on_run_pre(), on_run_pos(), on_stop_pre(), on_stop_pos())
    """
    def __init__(self, Log=None, piddir=None):#TODO: ao criar uma classe padrão usar args/kwargs para lidar como parametros variáveis no instanciamento
        # PRE-REQUISITOS/DEPENDÊNCIAS: 
        self.log = ConfigManager.get('log')
        self.kwargs = ConfigManager.get('argparse_cfg')
        self.kwopts = ConfigManager.get('argparse_opt')                
        self.ambiente = ConfigManager.get('ambiente')         
        if self.log is None or not isinstance(self.log, lbx_logger):
            raise ValueError(f'Argumento "log" é mandatório e deve ser uma instância de "lbxtoolkit.lbx_logger"') 
        if self.kwargs is None:
            raise ValueError(f'Argumento "argparse_cfg" é mandatório e deve ser um dicionário com ao mínimo as chaves: [description, usage, usage, add_help, formatter_class] para configuração do módulo argpase') 
        if self.kwopts is None:
            raise ValueError(f'Argumento "argparse_opt" é mandatório e deve ser uma lista de dicionários ao mínimo as chaves: [short, long, action, help] para tratamento dos argumentos recebidos da linha de comando') 
        if self.ambiente is None or self.ambiente not in ['Linux', 'Windows', 'Serviço']:
            raise ValueError(f'Argumento "ambiente" é mandatório e deve ser uma string com um dos seguintes valores: [Linux, Windows, Serviço]') 
                
        self.on_init_pre() ## método opcional a ser definito por sobrecarga na função local

        # Argumentos padrão obrigatórios       
        self.LogFile = Path('.',os.path.splitext(os.path.basename(__file__))[0] + '.daemon') if not Log else Log
        self.OS = platform.system()
        self.PID = os.getppid()     
        self.IP = socket.gethostbyname(socket.gethostname())
        self.Host = socket.gethostname()
        self.Usuario = os.getlogin() if self.OS == 'Windows' else os.path.expanduser('~').split(r'/')[1]
        self.Me = os.path.abspath(__file__)
        self.PIDDir = Path('.') if not piddir else piddir
        self.PIDFile =  Path(self.PIDDir,str(self.PID))
        self.exit = False
        self.mode = '[DAEMON (console)]'

        self.on_init() ## método opcional a ser definito por sobrecarga na função local

        self.on_init_pos() ## método opcional a ser definito por sobrecarga na função local                
        #
        #
    def main(self):
        #kwargs = ConfigManager.get('argparse_cfg')
        #kwopts = ConfigManager.get('argparse_opt')                
        #ambiente = ConfigManager.get('ambiente')                
        if len(sys.argv) == 1 and self.ambiente == 'Serviço': ## VEM DAQUI https://gist.github.com/drmalex07/10554232?permalink_comment_id=2555358#gistcomment-2555358        
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(ServicoWindows)
            servicemanager.StartServiceCtrlDispatcher()
        elif len(sys.argv) > 1 and sys.argv[1] == 'install':
                ServicoWindows.SvcInstall()
        elif len(sys.argv) > 1 and sys.argv[1] == 'remove':
                ServicoWindows.SvcRemove()            
        else:
            if len(sys.argv) > 1 and sys.argv[1] in ['start', 'stop', 'restart', 'debug']:
                win32serviceutil.HandleCommandLine(ServicoWindows)
            else:        
                self.parser = argparse.ArgumentParser(**self.kwargs)
                for opt in self.kwopts:
                    self.parser.add_argument(opt['short'], opt['long'], action=opt['action'], help=opt['help'])
                self.args = self.parser.parse_args()        

                self.args_paser() ## tratamento dos arguemntos deve ser redefindo por sobrecarga no na função local
            #
            #             
    def run(self):
        """Inicia a execução do do serviço"""

        self.on_run_pre() ## método opcional a ser definito por sobrecarga na função local    
        
        self.daemon_log('START')
        ## Gera o PIDFile
        self.log.add(f'Iniciando daemon [PID: {self.PID}] para monitorar os processos que rodam como serviço/daemon monitorados em: {self.PIDDir}... ')
        try:
            with open(self.PIDFile, 'w', encoding='utf-8') as f:
                f.write(self.Me + ';' + str(self.LogFile))    
        except Exception as Err:
            self.stop('CRASH')
            self.log.erro(f'Erro [{Err}] ao salvar PIDFile: {self.PIDFile}')  
        self.log.info(f'Ok!')  ## trocar para debug em prd ??

        self.on_run()  # função principal para interreper o daemon/serviço, definir localmente por sobrecarga (criar classe que herde essa classe e defina essa função)  

        self.on_run_pos() ## método opcional a ser definito por sobrecarga na função local    
        #
        #
    def stop(self, evento='STOP'):
        """Interrompe o daemon/serviço"""

        self.on_stop_pre() ## método opcional a ser definito por sobrecarga na função local        

        self.daemon_log(evento)
        self.on_stop() # função principal para interreper o daemon/serviço, definir localmente por sobrecarga (criar classe que herde essa classe e defina essa função)
        self.cleanup()
        self.exit=True

        self.on_stop_pos() ## método opcional a ser definito por sobrecarga na função local        
        #
        #
    def cleanup(self): ## Elimina o arquivo PID do processo se estiver rodando como daemon
        """Método auxiliar utilizado no stop() para limpar o o PID file na interrupção"""

        self.on_cleanup_pre() ## método opcional a ser definito por sobrecarga na função local        

        if self.PIDFile: ## verifica se está rodando como daemon
            if Path(self.PIDFile).exists():
                Path(self.PIDFile).unlink()  ##exclui o pidfile do daemon se o arquivo existir        
                self.PIDFile = None

        self.on_cleanup_pos() ## método opcional a ser definito por sobrecarga na função local       
        #
        #
    def daemon_log(self, evento=None): ## Gerar log de início/interrupção do serviço
        """Método auxiliar utilizado alimentar log do histórico de inicialização/interrupção do serviço/daemon"""

        evento = 'CHECK' if not evento else evento
        evento = evento.upper()
        TimeStamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        Message  = f'{TimeStamp} - {evento} - {self.OS} - {self.Host}/{self.IP} - PID: {self.PID} - {self.Usuario} - {self.Me}'
        try:
            with open(self.LogFile, 'a') as file: 
                file.write(Message + '\n') 
        except Exception as Err:
            self.log.erro(f'Erro [{Err}] ao gravar status do daemon em {self.LogFile}')                
        #
        #
    def on_init_pre(self):
        pass
    def on_init_pos(self):
        pass
    def on_init(self):
        pass
    def on_cleanup_pre(self):
        pass
    def on_cleanup_pos(self):
        pass
    def on_cleanup(self):
        pass
    def on_run_pre(self):
        pass
    def on_run_pos(self):
        pass
    def on_run(self):
        pass
    def on_stop_pre(self):
        pass
    def on_stop_pos(self):
        pass
    def on_stop(self):
        pass
    def args_paser(self):
        pass
    #
    #
class ServicoWindows(win32serviceutil.ServiceFramework): # Gerencia a execução/instalação como serviço do windows
    _svc_name_ = None
    _svc_display_name_ = None
    _svc_description_ = None   
    def __init__(self, args):
        self.log = ConfigManager.get('log')
        self.daemon = ConfigManager.get('daemon')
        self.config = ConfigManager.get('config')        

        if self.log is None or not isinstance(self.log, lbx_logger):
            raise ValueError(f'Argumento "log" é mandatório e deve ser uma instância de "lbxtoolkit.lbx_logger"')
        elif self.daemon is None or not hasattr(self.daemon, 'run') or not hasattr(self.daemon, 'stop'):
            raise ValueError(f'Argumento "daemon" é mandatório e deve possuir os métodos run() e stop()')        
        elif self.config is None or not 'name' in self.config or not 'display_name' in self.config or not 'description' in self.config:
            raise ValueError(f'Argumento "config" é mandatório e deve ser um dicionário contendo as chaves/valores para "name", "display_name" e "description"')
        elif [chave for chave in self.config if self.config[chave] is None]:
            raise ValueError(f'Argumento "config" ({self.config}) possui as seguintes chaves com valores inválidos [None]: {[chave for chave in self.config if self.config[chave] is None]:}')

        self._svc_name_ = self.config['name']
        self._svc_display_name_ = self.config['display_name']
        self._svc_description_ = self.config['description']
        #super().__init__(args)

        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(5)
        self.stop_requested = False      
        self.isAlive = True     
        #
        #   
    @staticmethod 
    def SvcInstall(): # Instala o script como um serviço do windows
        ## use @staticmethod quando precisar referenciar o método sem instanciar a classe e não precisar de acesso a instâncias ou à própria classe
        ## se precisar acessar métodos ou atributos da classe e não da instância, use @classmethod, mas isso implcia em passar (cls) e não (self) na definição método
        try:

            log = ConfigManager.get('log')
            daemon = ConfigManager.get('daemon')   
            config = ConfigManager.get('config')   
            service_path = ConfigManager.get('service_path') if ConfigManager.get('service_path') else os.path.abspath(sys.argv[0])                     

            if log is None or not isinstance(log, lbx_logger):
                raise ValueError(f'Argumento "log" é mandatório e deve ser uma instância de "lbxtoolkit.lbx_logger"')
            elif daemon is None or not hasattr(daemon, 'run') or not hasattr(daemon, 'stop'):
                raise ValueError(f'Argumento "daemon" é mandatório e deve possuir os métodos run() e stop()')  
            elif config is None or not 'name' in config or not 'display_name' in config or not 'description' in config:
                raise ValueError(f'Argumento "config" é mandatório e deve ser um dicionário contendo as chaves/valores para "name", "display_name" e "description"')
            elif [chave for chave in config if config[chave] is None]:
                raise ValueError(f'Argumento "config" ({config}) possui as seguintes chaves com valores inválidos [None]: {[chave for chave in config if config[chave] is None]:}')

            _svc_name_ = config['name'] 
            _svc_display_name_ = config['display_name']
            _svc_description_ = config['description']

            IP = socket.gethostbyname(socket.gethostname())
            Host = socket.gethostname()
            OS = platform.system()
            Usuario = os.getlogin() if OS == 'Windows' else os.path.expanduser('~').split(r'/')[1]
            # Delete the service
            query = subprocess.run(["sc", "query", _svc_name_], capture_output=True, text=True)
            if _svc_name_ in query.stdout:
                if 'RUNNING' in query.stdout:
                    log.add(f'Parando serviço  [{_svc_display_name_} ({_svc_name_})] em {IP}/{Host}({Usuario})...\n')
                    try:
                        stop = subprocess.run(["sc", "stop", _svc_name_], capture_output=True)
                        saida = stop.stdout.decode('cp850').strip()
                        sleep(5)
                        log.info(f': {saida}')
                    except Exception as Err:
                        log.erro(f'Erro ao parar serviço: {saida}')
                delete = subprocess.run(["sc", "delete", _svc_name_], capture_output=True)
                saida = delete.stdout.decode('cp850').strip()
                if delete:
                    log.info(f'Excluindo serviço pre-existente [{_svc_display_name_} ({_svc_name_})] em {IP}/{Host}({Usuario}): {saida}')
            # Create the service
            python_path = Path(os.path.join(os.getenv('VIRTUAL_ENV'), 'Scripts', 'python.exe'))
            install = subprocess.run(
                                        [
                                            'sc', 
                                            'create', 
                                            _svc_name_,
                                            'binPath=',
                                            f'{python_path} {service_path}',
                                            'DisplayName=', 
                                            _svc_display_name_,
                                            'start=delayed-auto',
                                        ]
                                    , capture_output=True)    
            saida = install.stdout.decode('cp850').strip()
            log.info(f'Criando novo serviço [{_svc_display_name_} ({_svc_name_})] em {IP}/{Host}({Usuario}): {saida}')
            # Set the service description
            descricao = subprocess.run(
                                        [
                                            'sc', 
                                            'description', 
                                            _svc_name_, 
                                            _svc_description_,
                                        ]
                                        , capture_output=True)    
            saida = descricao.stdout.decode('cp850').strip()
            log.info(f'Ajustando descrição do novo serviço [{_svc_display_name_} ({_svc_name_})]: {saida}')
        except Exception as Err:
            log.erro(f'Falha ao tentar criar o serviço [{_svc_display_name_} ({_svc_name_})]')     
            raise   
        #
        #
    @staticmethod 
    def SvcRemove(): # Remove o serviço do windows
        ## use @staticmethod quando precisar referenciar o método sem instanciar a classe e não precisar de acesso a instâncias ou à própria classe
        ## se precisar acessar métodos ou atributos da classe e não da instância, use @classmethod, mas isso implcia em passar (cls) e não (self) na definição método
        try:

            log = ConfigManager.get('log')
            daemon = ConfigManager.get('daemon')   
            config = ConfigManager.get('config')                    

            if log is None or not isinstance(log, lbx_logger):
                raise ValueError(f'Argumento "log" é mandatório e deve ser uma instância de "lbxtoolkit.lbx_logger"')
            elif daemon is None or not hasattr(daemon, 'run') or not hasattr(daemon, 'stop'):
                raise ValueError(f'Argumento "daemon" é mandatório e deve possuir os métodos run() e stop()')  
            elif config is None or not 'name' in config or not 'display_name' in config or not 'description' in config:
                raise ValueError(f'Argumento "config" é mandatório e deve ser um dicionário contendo as chaves/valores para "name", "display_name" e "description"')
            elif [chave for chave in config if config[chave] is None]:
                raise ValueError(f'Argumento "config" ({config}) possui as seguintes chaves com valores inválidos [None]: {[chave for chave in config if config[chave] is None]:}')

            _svc_name_ = config['name'] 
            _svc_display_name_ = config['display_name']

            IP = socket.gethostbyname(socket.gethostname())
            Host = socket.gethostname()
            OS = platform.system()
            Usuario = os.getlogin() if OS == 'Windows' else os.path.expanduser('~').split(r'/')[1]
            # Delete the service
            query = subprocess.run(["sc", "query", _svc_name_], capture_output=True, text=True)
            if _svc_name_ in query.stdout:
                if 'RUNNING' in query.stdout:
                    log.add(f'Parando serviço  [{_svc_display_name_} ({_svc_name_})] em {IP}/{Host}({Usuario})...\n')
                    try:
                        stop = subprocess.run(["sc", "stop", _svc_name_], capture_output=True)
                        saida = stop.stdout.decode('cp850').strip()
                        sleep(5)
                        log.info(f': {saida}')
                    except Exception as Err:
                        log.erro(f'Erro ao parar serviço: {saida}')
                delete = subprocess.run(["sc", "delete", _svc_name_], capture_output=True)
                saida = delete.stdout.decode('cp850').strip()
                if delete:
                    log.info(f'Excluindo serviço pre-existente [{_svc_display_name_} ({_svc_name_})] em {IP}/{Host}({Usuario}): {saida}')
        except Exception as Err:
            log.erro(f'Falha ao tentar excluir o serviço [{_svc_display_name_} ({_svc_name_})]')     
            raise 
        #
        #           
    def SvcStop(self): # Para a execução do serviço
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.stop_requested = True
        self.isAlive = False
        self.daemon.stop('STOP')
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        #
        #
    def SvcDoRun(self): # Inicia o serviço
        #self.ReportServiceStatus(win32service.SERVICE_START_PENDING)     
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        self.daemon.mode='[SERVIÇO (windows)]' 
        self.RunAsDaemon()              
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE, 
                              servicemanager.PYS_SERVICE_STARTED, (self._svc_name_, ''))  
        #
        #
    @staticmethod 
    def RunAsDaemon(): # Executa o script como um daemon
        ## use @staticmethod quando precisar referenciar o método sem instanciar a classe e não precisar de acesso a instâncias ou à própria classe
        ## se precisar acessar métodos ou atributos da classe e não da instância, use @classmethod, mas isso implcia em passar (cls) e não (self) na definição método

        log = ConfigManager.get('log')
        daemon = ConfigManager.get('daemon')   
        config = ConfigManager.get('config')                

        if log is None or not isinstance(log, lbx_logger):
            raise ValueError(f'Argumento "log" é mandatório e deve ser uma instância de "lbxtoolkit.lbx_logger"')
        elif daemon is None or not hasattr(daemon, 'run') or not hasattr(daemon, 'stop'):
            raise ValueError(f'Argumento "daemon" é mandatório e deve possuir os métodos run() e stop()')  
        elif config is None or not 'name' in config or not 'display_name' in config or not 'description' in config:
            raise ValueError(f'Argumento "config" é mandatório e deve ser um dicionário contendo as chaves/valores para "name", "display_name" e "description"')
        elif [chave for chave in config if config[chave] is None]:
            raise ValueError(f'Argumento "config" ({config}) possui as seguintes chaves com valores inválidos [None]: {[chave for chave in config if config[chave] is None]:}')
              
        PID = daemon.PID if daemon.PID else os.getppid()
        OS = daemon.OS if daemon.OS else platform.system()
        mode = daemon.mode if daemon.mode else '[DAEMON (console)]'
        IP = daemon.IP if daemon.IP else socket.gethostbyname(socket.gethostname())
        Host = daemon.Host if daemon.Host else socket.gethostname()
        Usuario = daemon.Usuario if daemon.Usuario else os.getlogin() if OS == 'Windows' else os.path.expanduser('~').split(r'/')[1]

        try:                
            Kill = f'taskkil /F /PID {PID}' if OS=='Windows' else f'kill -9 {PID}'
            Stop = f'use Ctrl+C (ou excepcionalmente [{Kill}])' if mode=='[DAEMON (console)]' else f'PARE o serviço [{config['display_name']} ({config['name']})]'
            log.info(f'Executando como {mode} em {Host}/{IP}({Usuario}). Para encerrar {Stop}...') 
            daemon.run()
        except KeyboardInterrupt:
            daemon.stop('STOP')
            log.info('Execução encerrada por Ctrl+C! [pego fora do daemon')
        except Exception as Err:
            daemon.stop('CRASH')
            log.erro(f'Interrompido por erro não previsto [pego fora do daemon]: [{Err}]')            
        finally:
            log.info('daemon encerrado!')               
        #
        #