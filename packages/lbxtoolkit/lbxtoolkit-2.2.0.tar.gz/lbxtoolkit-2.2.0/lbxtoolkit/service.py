from .config_manager import ConfigManager
from .service_windows import ServicoWindows
from .lbx_logger import lbx_logger
import os
import sys
import datetime
from pathlib import Path
import platform
import socket
import argparse
import servicemanager
import win32serviceutil

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

        config = ConfigManager.get('config')        

        if config is None or not 'name' in config or not 'display_name' in config or not 'description' in config:
            raise ValueError(f'Argumento "config" é mandatório e deve ser um dicionário contendo as chaves/valores para "name", "display_name" e "description"')
        elif [chave for chave in config if config[chave] is None]:
            raise ValueError(f'Argumento "config" ({config}) possui as seguintes chaves com valores inválidos [None]: {[chave for chave in config if config[chave] is None]:}')

        ServicoWindows._svc_name_ = config['name']
        ServicoWindows._svc_display_name_ = config['display_name']
        ServicoWindows._svc_description_ = config['description']        
                     
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
