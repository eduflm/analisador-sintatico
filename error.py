import inspect 
debug = False

def debugFunction(*args):
    argsExists = False
    if (len(args[0]) > 0):
        argsExists = True
    if argsExists and args[0][0] == True:
        print("------------------------------------")
        print ('Chamado pelo metodo:', inspect.stack()[2][3])
        print ('Chamado na linha:', inspect.stack()[2][2])
        print ('Chamado do arquivo:', inspect.stack()[2][1])
        print ('Pilha', inspect.stack())
        print("____________________________________\n")
    elif argsExists and args[0][0] == False:
        return
    elif debug:
        print("------------------------------------")
        print ('Chamado pelo metodo:', inspect.stack()[2][3])
        print ('Chamado na linha:', inspect.stack()[2][2])
        print ('Chamado do arquivo:', inspect.stack()[2][1])
        print ('Pilha', inspect.stack())
        print("____________________________________\n")

def endDebugFunction(*args):
    argsExists = False
    if (len(args[0]) > 0):
        argsExists = True
    if argsExists and args[0][0] == True:
        print("____________________________________")
        print("------------------------------------")
    elif argsExists and args[0][0] == False:
        return
    elif debug:
        print("____________________________________")
        print("------------------------------------")

class Error:

    @staticmethod
    def EsperaTokenFimArquivo(token, *args):
        debugFunction(args)
        print("Esperava o token: '"+str(token)+"' e recebeu um fim de arquivo")
        endDebugFunction(args)
    
    @staticmethod
    def NaoFoiPossivelLerMaisToken(nomefuncao, *args):
        debugFunction(args)
        print("Esperavamos um token na funcao "+ str(nomefuncao) +", porem terminou de forma inesperada")
        endDebugFunction(args)
    
    @staticmethod
    def RecebeuTokenInesperado(tokenEsperado, tokenRecebido, *args):
        debugFunction(args)
        print("Esperava o token:'" +str(tokenEsperado)+ "' e recebeu um '"+str(tokenRecebido)+"'")
        endDebugFunction(args)
    
