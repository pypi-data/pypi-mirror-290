import os
import re 
from pathlib import Path
from unicodedata import normalize 
import tkinter as tk
from tkinter import filedialog
import pygetwindow as gw
import ctypes    

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
