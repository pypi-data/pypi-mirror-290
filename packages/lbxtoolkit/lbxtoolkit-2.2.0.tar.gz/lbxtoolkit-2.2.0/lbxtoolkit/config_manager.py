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
