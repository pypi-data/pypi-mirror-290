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
import locale
from .lbx_logger import lbx_logger
from .config_manager import ConfigManager
from .service_windows import ServicoWindows
from .service import Servicer
from .auth_entra_id import auth_EntraID
from .postgresql import postgreSQL
from .api_rest import api_rest
from .misc import misc

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

__all__ = [
    "lbx_logger",
    "ConfigManager",
    "ServicoWindows",
    "Servicer",
    "auth_EntraID",
    "postgreSQL",
    "api_rest",
    "misc"
]
