from leitorDeFluxo import LeitorDeFluxo
from tipoToken import TipoToken
from error import Error

class analisadorSintatico:
    
    def __init__(self):
        self.tokens = LeitorDeFluxo("fluxoDeTokens").fluxoDeTokens      # Lista de tokens
        self.compilationUnit()

    def existeToken(self, i):
        return i < len(self.tokens)

    #compilationUnit::=[package qualifiedIdentifier ;] {import qualifiedIdentifier ;} {typeDeclaration} EOF
    def compilationUnit(self):
        indice = 0;
        if not self.existeToken(indice):
            return indice
        
        if self.tokens[indice] == TipoToken.PCPackage.name:
            indice = self.qualifiedIdentifier(indice+1)
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(TipoToken.SepPontoEVirgula.name) # Token Esperado
            if self.tokens[indice] == TipoToken.SepPontoEVirgula.name:
                indice += 1
            else:
                Error.RecebeuTokenInesperado(TipoToken.SepPontoEVirgula.name, self.tokens[indice])
        
        if not self.existeToken(indice):
            return indice

        while self.tokens[indice] == TipoToken.PCImport.name:
            indice = self.qualifiedIdentifier(indice+1)
            if not self.existeToken(indice):
                Error.EsperaTokenFimArquivo(TipoToken.SepPontoEVirgula.name) # Token Esperado
            if self.tokens[indice] == TipoToken.SepPontoEVirgula.name:
                indice += 1
            else:
                Error.RecebeuTokenInesperado(TipoToken.SepPontoEVirgula.name, self.tokens[indice])

        while self.existeToken(indice):
            indice = self.typeDeclaration()

        return indice

    # qualifiedIdentifier ::= <identifier> {. <identifier>}
    def qualifiedIdentifier(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.Variavel.name) # Token Esperado
            return indice
        if self.tokens[indice] == tipoToken.Variavel.name:
            indice += 1
            while self.tokens[indice] == tipoToken.SepPonto.name:
                indice += 1
                if not self.existeToken(indice):
                    Error.EsperaTokenFimArquivo(TipoToken.Variavel.name) # Token Esperado
                if self.tokens[indice] == tipoToken.Variavel.name:
                    indice += 1
                else:
                    Error.RecebeuTokenInesperado(TipoToken.Variavel.name, self.tokens[indice])
        else:
            Error.RecebeuTokenInesperado(TipoToken.Variavel.name, self.tokens[indice])
        return indice

    # typeDeclaration ::= modifiers classDeclaration
    def typeDeclaration(self, indice):
        indice = self.modifiers(indice)
        indice = self.classDeclaration(indice)
        return indice

    # modifiers ::= {public | protected | private | static | abstract}
    def modifiers(self, indice):
        modif = [TipoToken.PCPublic.name, TipoToken.PCProtected.name, TipoToken.PCPrivate.name, TipoToken.PCStatic.name, TipoToken.PCAbstract.name]
        if not self.existeToken(indice):
            return indice
        while self.tokens[indice] in modif:
            indice += 1
        return indice
 

    # classDeclaration ::= class <identifier> [extends qualifiedIdentifier] classBody
    def classDeclaration(self, indice):
        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.PCClass.name) # Token Esperado
            return indice
        if not self.tokens[indice] == TipoToken.PCClass.name:
            Error.RecebeuTokenInesperado(TipoToken.PCClass.name, self.tokens[indice])
        indice += 1

        if not self.existeToken(indice):
            Error.EsperaTokenFimArquivo(TipoToken.Variavel.name) # Token Esperado
        if not self.tokens[indice] == TipoToken.Variavel.name:
            Error.RecebeuTokenInesperado(TipoToken.Variavel.name, self.tokens[indice])
        indice += 1

        if self.tokens[indice] == TipoToken.PCExtends.name:
            indice = self.qualifiedIdentifier(indice + 1)
    
        indice = self.classBody(indice)
        return indice

    ########### REFATORAR ERROS DAQUI PRA BAIXO #######################
    # Eduardo

    # classBody ::= { {modifiers memberDecl} }
    def classBody(self, indice):
        if not self.existeToken(indice):
            Error(TipoToken.SepAbreChave.name)
            return indice
        if not self.tokens[indice] == TipoToken.SepAbreChave.name:
            Error(self.tokens[indice], TipoToken.SepAbreChave.name, "tokenInesperado")
        indice += 1
        while self.tokens[indice] != TipoToken.SepFechaChave.name:
            if not self.existeToken(indice):
                return indice
            indice = self.modifiers(indice)
            indice = self.memberDecl(indice)
        return indice + 1  

    # memberDecl ::= <identifier> // constructor
    #                    formalParameters block
    #                | (void | type) <identifier> // method
    #                    formalParameters (block | ;)
    #                | type variableDeclarators ; // field
    def memberDecl(self, indice):
        if not self.existeToken(indice):
            Error("memberDecl")
            return indice
       
        if self.tokens[indice] == tipoToken.Variavel.name:  # CONSTRUTOR
            if self.existeToken(indice + 1) and self.tokens[indice + 1] == TipoToken.SepAbreParentese.name:
                indice += 1
                indice = self.formalParameters(indice)
                indice = self.block(indice)
                return indice

        elif self.tokens[indice] == tipoToken.PCVoid.name:
            indice += 1
            if not self.existeToken(indice):
                Error("Identificador")
                return indice

        else:
            indice = funcaoType(indice)
            if not self.existeToken(indice):
                Error("inesperado")
                return indice
            if self.tokens[indice] == TipoToken.Variavel.name: # METHOD
                if self.existeToken(indice + 1) and self.tokens[indice + 1] != TipoToken.SepAbreParentese.name:
                    indice += 1
                    indice = self.formalParameters(indice)
                    if not self.existeToken(indice):
                        Error("inesperado")
                        return indice
                    if self.tokens[indice] != TipoToken.SepPontoEVirgula.name:
                        indice = self.block(indice)
                    else:
                        indice += 1
                    return indice
            # FIELD
            indice = self.variableDeclarators(indice)
            if not self.existeToken(indice):
                Error("Identificador")
                return indice
            if self.tokens[indice] != TipoToken.SepPontoEVirgula.name:
                Error(self.tokens[indice], TipoToken.SepPontoEVirgula.name, "tokenInesperado")
            return indice 

        if self.tokens[indice] == TipoToken.Variavel.name: # METHOD no caso do VOID
            indice = self.formalParameters(indice)
        if not self.existeToken(indice):
            Error("inesperado")
            return indice
        if self.tokens[indice] != TipoToken.SepPontoEVirgula.name:
            indice = self.block(indice)
        else:
            indice += 1
        return indice

    # block ::= { {blockStatement} }
    def block(self, indice):
        if not self.existeToken(indice):
            Error(TipoToken.SepAbreChave)
            return indice
        if not self.token[indice] == TipoToken.SepAbreChave.name:
            Error(self.tokens[indice], TipoToken.SepAbreChave.name, "tokenInesperado")
        indice += 1
        while self.token[indice] != TipoToken.SepFechaChave.name:
            if not self.existeToken(indice):
                Error(TipoToken.SepAbreChave)
                return indice
            indice = self.blockStatement(indice)
        return indice + 1
    
    # blockStatement ::= localVariableDeclarationStatement | statement
    def blockStatement(self, indice):
        if not self.existeToken(indice):
            Error(TipoToken.Variavel)
            return indice
        if ehUmType: 
            indice = self.localVariableDeclarationStatement(indice)
        else:
            indice = self.statement(indice)
        return indice

    # statement ::= block | <identifier> : statement | if parExpression statement [else statement]
    #               | while parExpression statement  | return [expression] ; | ; | statementExpression ;
    def statement(self, indice):
        if not self.existeToken(indice):
            Error("statement")
            return indice

        if self.tokens[indice] == tipoToken.SepAbreChave.name:           # block
            indice = self.block(indice)
            return indice

        if self.tokens[indice] == tipoToken.Variavel.name:             # <identifier>
            if not self.tokens[indice] == tipoToken.SepDoisPontos.name:
                Error(self.tokens[indice],  tipoToken.SepDoisPontos.name, "tokenInesperado")
                return indice
            indice += 1
            if not self.existeToken(indice):
                Error("statement")
                return indice
            return self.statement(indice)

        if self.tokens[indice] == tipoToken.PCIf.name:                 # if
            indice = self.parExpression(indice + 1)
            indice = self.statement(indice + 1)
            if not self.existeToken(indice):
                Error("statement")
                return indice

            if self.tokens[indice] == tipoToken.PCElse.name:
                indice = self.statement(indice + 1)
                if not self.existeToken(indice):
                    Error("statement")
                    return indice

            return indice

        if self.tokens[indice] == tipoToken.PCWhile.name:              # while
            indice = self.parExpression(indice + 1)
            indice = self.statement(indice + 1)
            return indice

        if self.tokens[indice] == tipoToken.PCReturn.name:             # return
            indice += 1
            if(acabaramOsTokens(tokens, i)):
                erroEstouro(TipoToken.SepPontoVirgula.name)
                return indice
            if self.tokens[i].tipoToken != TipoToken.SepPontoVirgula:
                indice = self.expression(indice)
                if(acabaramOsTokens(tokens, i)):
                    erroEstouro(TipoToken.SepPontoVirgula.name)
                    return indice
                if not self.tokens[indice] == tipoToken.SepPontoEVirgula.name:
                    Error(self.tokens[indice],  tipoToken.SepPontoEVirgula.name, "tokenInesperado")
            else:
                return indice + 1

        if self.tokens[indice] == tipoToken.SepPontoEVirgula.name:     # ;
            return indice + 1

        else:                                                          # statementExpression
            return statementExpression(indice + 1)

    # formalParameters ::= ( [formalParameter {, formalParameter}] )
    def formalParameters(self, indice):
        if not self.existeToken(indice):
            Error(self.tokens[indice], TipoToken.SepAbreParentese.name, "tokenInesperado")
            return indice
        if self.tokens[indice] == tipoToken.SepAbreParentese.name:
            indice = self.formalParameter(indice + 1)
            if not self.existeToken(indice):
                Error(self.tokens[indice], TipoToken.SepFechaParentese.name, "tokenInesperado")
                return indice
            while self.tokens[indice] == tipoToken.SepVirgula.name:
                indice += 1
                if not self.existeToken(indice):
                    Error("FormalParameter")
                    return indice
                indice = self.formalParameter(indice)
            if self.tokens[indice] != TipoToken.SepFechaParentese:
                Error(self.tokens[indice], TipoToken.SepFechaParentese.name, "tokenInesperado")
        return indice + 1

    # formalParameter ::= type <identifier>
    def formalParameter(self, indice);
        if not self.existeToken(indice):
            Error(TipoToken.PCChar)
            return indice
        indice = self.funcaoType(indice + 1)
        if not self.existeToken(indice):
            Error(TipoToken.PCChar)
            return indice
        if self.tokens[indice] != TipoToken.Variavel.name:
            Error(self.tokens[indice], TipoToken.Variavel.name, "tokenInesperado")
        return indice + 1

    # parExpression ::= ( expression )
    def parExpression(self, indice):
        if not self.existeToken(indice):
            Error(TipoToken.PCChar)
            return indice
        if self.tokens[indice] == TipoToken.SepAbreParentese.name:
            indice = self.expression(indice + 1)
            if not self.existeToken(indice):
                Error(TipoToken.PCChar)
                return indice
            if self.tokens[indice] != TipoToken.SepFechaParentese.name:
                Error(self.tokens[indice], TipoToken.SepFechaParentese.name, "tokenInesperado")
                indice += 1
        else:
            Error(self.tokens[indice], TipoToken.SepAbreParentese.name, "tokenInesperado")
        return indice

    # localVariableDeclarationStatement ::= type variableDeclarators ;
    def localVariableDeclarationStatement(self, indice):
        if not self.existeToken(indice):
            Error(TipoToken.PCChar)
            return indice
        indice = self.funcaoType(indice)
        if not self.existeToken(indice):
            Error(TipoToken.PCChar)
            return indice
        indice = self.variableDeclarators(indice) 
        if not self.existeToken(indice):
            Error(TipoToken.PCChar)
            return indice
        if self.tokens[indice] != TipoToken.SepPontoEVirgula.name:
            Error(self.tokens[indice], TipoToken.SepPontoEVirgula.name, "tokenInesperado")
            return indice += 1
            
    # variableDeclarators ::= variableDeclarator {, variableDeclarator}
    def variableDeclarators(self, indice):
        if not self.existeToken(indice):
            Error(TipoToken.PCChar)
            return indice
        indice = self.variableDeclarator(indice)
        if not self.existeToken(indice):
            Error(TipoToken.PCChar)
            return indice
        while self.tokens[indice] == tipoToken.SepVirgula.name:
            indice += 1
            if not self.existeToken(indice):
                Error("variableDeclarator")
                return indice
            indice = self.variableDeclarator(indice)
        return indice + 1

    # variableDeclarator ::= <identifier> [= variableInitializer]
    def variableDeclarator(self, indice):
        if not self.existeToken(indice):
            Error(TipoToken.Variavel)
            return indice
        if self.tokens[indice] == tipoToken.Variavel.name:
            indice += 1
        if not self.existeToken(indice):
            Error(TipoToken.Variavel)
            return indice

        if self.tokens[indice] == tipoToken.OPIgual.name:
            indice += 1
            if not self.existeToken(indice):
                Error("variableInitializer")
                return indice
            indice = self.variableInitializer(indice)
        else:
            return indice 

    # variableInitializer ::= arrayInitializer | expression
    def variableInitializer(self, indice):
        if not self.existeToken(indice):
            Error(TipoToken.Variavel)
            return indice
        if self.tokens[indice] == TipoToken.SepAbreChave.name: 
            indice = self.arrayInitializer(indice)
        else:
            indice = self.expression(indice)
        return indice

    # arrayInitializer ::= { [variableInitializer {, variableInitializer}] }
    def arrayInitializer(self, indice):
        if not self.existeToken(indice):
            Error(TipoToken.Variavel)
            return indice
        if not self.tokens[indice] == TipoToken.SepAbreChave.name:
           Error(self.tokens[indice], TipoToken.SepAbreChave.name, "tokenInesperado")
           return indice
        indice = self.variableInitializer(indice + 1)
        if not self.existeToken(indice):
            Error(TipoToken.Variavel)
            return indice
        while self.tokens[indice] == TipoToken.SepVirgula.name:
            indice = self.variableInitializer(indice + 1)
            if not self.existeToken(indice):
                Error(TipoToken.Variavel)
                return indice
        if not self.tokens[indice] == TipoToken.SepFechaChave.name:
           Error(self.tokens[indice], TipoToken.SepFechaChave.name, "tokenInesperado")
           return indice
        indice += 1
        return indice
        
    # arguments ::= ( [expression {, expression}] )
    def arguments(self, indice):
        if not self.existeToken(indice):
            Error(TipoToken.Variavel)
            return indice
        if not self.tokens[indice] == TipoToken.SepAbreParentese.name:
           Error(self.tokens[indice], TipoToken.SepAbreParentese.name, "tokenInesperado")
           return indice
        indice += 1
        if not self.tokens[indice] == TipoToken.SepFechaParentese.name:
            indice = self.expression(indice)
            if not self.existeToken(indice):
                Error(TipoToken.Variavel)
                return indice
            while self.tokens[indice] == TipoToken.SepVirgula.name:
                indice = self.expression(indice + 1)
                if not self.existeToken(indice):
                    Error(TipoToken.Variavel)
                    return indice
        if not self.tokens[indice] == TipoToken.SepFechaParentese.name:
            Error(self.tokens[indice], TipoToken.SepFechaParentese.name, "tokenInesperado")
            return indice
        indice += 1
        return indice

    # type ::= referenceType | basicType
    def funcaoType(self, indice):
        if not self.existeToken(indice):
            Error(TipoToken.PCChar)
            return indice
        if self.ehUmReferenceType(indice):
            indice = self.referenceType(indice + 1)
        elif self.ehUmBasicType(indice):
            indice = self.basicType(indice + 1)
        else
            Error("referenceType, basicType")
        return indice

    # basicType ::= boolean | char | int
    def basicType(self, indice):
        if not self.existeToken(indice):
            Error(TipoToken.PCChar)
            return indice
        tiposBasicos = [TipoToken.PCBoolean.name, TipoToken.PCChar.name, TipoToken.PCInt.name]
        if self.tokens[indice] not in tiposBasicos:
            return indice
        return indice + 1

    # referenceType ::= basicType [ ] {[ ]} | qualifiedIdentifier {[ ]}
    def referenceType(self, indice):
        if not self.existeToken(indice):
            Error(TipoToken.PCChar)
            return indice

        if self.ehUmBasicType(indice):
            indice = self.basicType(indice)
            
            if not self.existeToken(indice):
                Error(TipoToken.PCChar)
                return indice

            if self.tokens[indice] == TipoToken.SepAbreColchete.name:
                indice += 1
            if not self.existeToken(indice):
                Error(TipoToken.PCChar)
                return indice
            if self.tokens[indice] == TipoToken.SepFechaColchete.name:
                indice += 1
            if not self.existeToken(indice):
                Error(TipoToken.PCChar)
                return indice
        elif self.ehUmQualifiedIdentifier(indice):
            indice = self.qualifiedIdentifier(indice)
        else:
            Error("basicType, qualifiedIdentifier")
            return indice

        if not self.existeToken(indice):
            Error(TipoToken.PCChar)
            return indice

        while self.tokens[indice] == TipoToken.SepAbreParentese.name:
            indice += 1
            if not self.existeToken(indice):
                Error(TipoToken.PCChar)
                return indice
            if self.tokens[indice] != TipoToken.SepFechaParentese.name:
                Error(TipoToken.PCChar)
                return indice
            indice += 1

        return indice

    # statementExpression ::= expression // but must have side-effect, eg i++
    def statementExpression(self, indice):
        if not self.existeToken(indice):
            Error(TipoToken.PCChar)
            return indice
        indice = self.expression(indice)
        return indice

    # expression ::= assignmentExpression
    def expression(self, indice):
        if not self.existeToken(indice):
            Error(TipoToken.PCChar)
            return indice
        indice = self.assignmentExpression(indice)
        return indice


    # assignmentExpression ::= conditionalAndExpression [(= | +=) assignmentExpression]
    def assignmentExpression(self, indice):
        if not self.existeToken(indice):
            Error(TipoToken.PCChar)
            return indice
        indice = conditionalAndExpression(indice)
        if not self.existeToken(indice):
            Error(TipoToken.PCChar)
            return indice

        if self.tokens[indice] == TipoToken.Recebe.name or self.tokens[indice] == TipoToken.OPSomaERecebe.name: 
            indice = assignmentExpression(indice + 1)

        return indice

    # conditionalAndExpression ::= equalityExpression {&& equalityExpression}
    def conditionalAndExpression(self, indice):
        if not self.existeToken(indice):
            Error(TipoToken.PCChar)
            return indice
        indice = equalityExpression(indice)
        if not self.existeToken(indice):
            Error(TipoToken.PCChar)
            return indice

        while self.tokens[indice] == TipoToken.OPAnd.name:
            indice = equalityExpression(indice + 1)

        return indice

    # equalityExpression ::= relationalExpression {== relationalExpression}
    def equalityExpression(self, indice):
        if not self.existeToken(indice):
            Error(TipoToken.PCChar)
            return indice
        indice = relationalExpression(indice)
        if not self.existeToken(indice):
            Error(TipoToken.PCChar)
            return indice

        while self.tokens[indice] == TipoToken.OPIgual.name:
            indice = relationalExpression(indice + 1)

        return indice

    # relationalExpression ::= additiveExpression [(> | <=) additiveExpression | instanceof referenceType]
    def relationalExpression(self, indice):
        if not self.existeToken(indice):
            Error(TipoToken.PCChar)
            return indice
        indice = additiveExpression(indice)
        if not self.existeToken(indice):
            Error(TipoToken.PCChar)
            return indice

        if self.tokens[indice] == TipoToken.OPMaior.name or self.tokens[indice] == TipoToken.OPMenorIgual.name: 
            indice = additiveExpression(indice + 1)
        elif self.tokens[indice] == TipoToken.PCInstanceOf.name:
            indice = referenceType(indice + 1)

        return indice

    # additiveExpression ::= multiplicativeExpression {(+ | -) multiplicativeExpression}
    def additiveExpression(self, indice):
        if not self.existeToken(indice):
            Error(TipoToken.PCChar)
            return indice
        indice = multiplicativeExpression(indice)
        if not self.existeToken(indice):
            Error(TipoToken.PCChar)
            return indice

        while self.tokens[indice] == TipoToken.OPSoma.name or self.tokens[indice] == TipoToken.OPMenos.name:
            indice = multiplicativeExpression(indice + 1)

        return indice

    # multiplicativeExpression ::= unaryExpression {* unaryExpression}
    def  multiplicativeExpression(self, indice):
        if not self.existeToken(indice):
            Error(TipoToken.PCChar)
            return indice
        indice = unaryExpression(indice)
        if not self.existeToken(indice):
            Error(TipoToken.PCChar)
            return indice

        while self.tokens[indice] == TipoToken.OpMultiplica.name:
            indice = unaryExpression(indice + 1)

        return indice

    # unaryExpression ::= ++ unaryExpression | - unaryExpression | simpleUnaryExpression
    def  unaryExpression(self, indice):
        if not self.existeToken(indice):
            Error(TipoToken.PCChar)
            return indice

        if self.tokens[indice] == TipoToken.OPIncrementa.name:
            indice = simpleUnaryExpression(indice + 1)
        elif self.tokens[indice] == TipoToken.OPMenos.name:
            indice = simpleUnaryExpression(indice + 1)
        else:
            indice = simpleUnaryExpression(indice)

    # simpleUnaryExpression ::= ! unaryExpression | ( basicType ) unaryExpression 
    #                           | ( referenceType ) simpleUnaryExpression | postfixExpression
    def simpleUnaryExpression(self, indice):
        if not self.self.existeToken(indice):
            Error(TipoToken.PCChar)
            return indice

        if self.tokens[indice] == TipoToken.OPNao.name:
            return unaryExpression(indice + 1)

        if self.tokens[indice] == TipoToken.SepAbreParentese.name:
            indice += 1
            if not self.self.existeToken(indice):
                Error(TipoToken.PCChar)
                return indice
            if ehUmBasicType(indice) and self.tokens[indice + 1] != TipoToken.SepAbreColchete.name: # ( basicType ) unaryExpression  
                indice = self.basicType(indice)
                if not self.self.existeToken(indice):
                    Error(TipoToken.PCChar)
                    return indice
                if not self.tokens[indice] == TipoToken.SepFechaParentese.name:
                    Error(self.tokens[indice], TipoToken.SepFechaParentese.name, "tokenInesperado")
                    return indice
                indice = self.unaryExpression(indice + 1)
            else:
                indice = self.referenceType(indice)
                if not self.self.existeToken(indice):
                    Error(TipoToken.PCChar)
                    return indice
                if not self.tokens[indice] == TipoToken.SepFechaParentese.name:
                    Error(self.tokens[indice], TipoToken.SepFechaParentese.name, "tokenInesperado")
                    return indice
                indice = self.simpleUnaryExpression(indice + 1)
            return indice

        return postfixExpression(indice)

    # postfixExpression ::= primary {selector} {--}
    def postfixExpression(self, indice):
        if not self.self.existeToken(indice):
            Error(TipoToken.PCChar)
            return indice
        indice = primary(indice) 
        if not self.self.existeToken(indice):
            Error(TipoToken.PCChar)
            return indice
        while self.tokens[indice] == TipoToken.SepPonto.name or tokens[indice].tipoToken == TipoToken.SepAbreColchete.name:
            indice = selector(indice)
        if not self.self.existeToken(indice):
            Error(TipoToken.PCChar)
            return indice
        while self.tokens[indice] == TipoToken.OPDecrementa.name:
            indice += 1
        return indice

    # selector ::= . qualifiedIdentifier [arguments] | [ expression ]
    def selector(self, indice):
        if not self.existeToken(indice):
            Error(TipoToken.Variavel)
            return indice
        if self.tokens[indice] == TipoToken.SepPonto.name:
            indice = self.qualifiedIdentifier(indice + 1)
            if self.tokens[indice] == TipoToken.SepAbreParentese.name:
                indice = arguments(indice + 1)
            return indice
        if self.tokens[indice] == TipoToken.SepAbreColchete.name:
            indice = self.expression(indice + 1)
            if not self.existeToken(indice):
                Error(TipoToken.SepAbreColchete.name)
                return indice
            if not self.tokens[indice] == TipoToken.SepFechaColchete.name:
                Error(self.tokens[indice], TipoToken.SepFechaColchete.name, "tokenInesperado")
                return indice
        return indice

    # primary ::= parExpression | this [arguments] | super (arguments | . <identifier> [arguments])
    #                           | literal | new creator | qualifiedIdentifier [arguments]
    def primary(self, indice):
        if not self.existeToken(indice):
            Error("Primary")
            return indice

        if self.tokens[indice] == TipoToken.SepAbreParentese.name:      # parExpression
            indice = self.parExpression(indice)
            return indice

        if self.tokens[indice] == TipoToken.PCThis.name:          # This
            indice += 1
            if not self.existeToken(indice):
                return indice
            if self.tokens[indice] == TipoToken.SepAbreParentese.name:
                indice = self.arguments(indice)
                return indice
            return indice

        if self.tokens[indice] == TipoToken.PCSuper.name:                   # Super
            indice += 1
            if not self.existeToken(indice):
                Error("Primary")
                return indice

            if self.tokens[indice] == TipoToken.SepAbreParentese.name:
                indice = self.arguments(indice)
                return indice

            if self.tokens[indice] == TipoToken.SepPonto.name:
                indice += 1
                if not self.tokens[indice] == TipoToken.Variavel.name:
                    Error(self.tokens[indice], TipoToken.SepFechaColchete.name, "tokenInesperado")

                if not self.existeToken(indice):
                    return indice
                if self.tokens[indice] == TipoToken.SepAbreParentese.name:
                    indice = self.arguments(indice)
                return indice

            return indice + 1

        if(eUmLiteral(indice)):          # literal
            indice = literal(indice)
            return indice
        if(tokens[indice].tipoToken == TipoToken.PCNew):        # New
            indice = creator(indice + 1)
            return indice
        aux = indice
        indice = self.qualifiedIdentifier(indice)               # senao Qualidifiertify
        if not self.existeToken(indice):
            return indice

        if self.tokens[indice] == TipoToken.SepAbreParentese.name:
            indice = self.arguments(indice)
        if(aux == indice):
            indice += 1
        return indice

    # creator ::= (basicType | qualifiedIdentifier) ( arguments 
    #                                               | [ ] {[ ]} [arrayInitializer] 
    #                                               | newArrayDeclarator )
    def creator(self, indice):
        if not self.existeToken(indice):
            Error(TipoToken.SepAbreColchete.name)
            return indice
        if self.ehUmType(indice):
            if self.ehUmBasicType(indice):
                indice = self.basicType(indice)
            else:
                indice = self.qualifiedIdentifier(indice)

            if not self.existeToken(indice):
                Error(TipoToken.SepAbreParentese.name)
                return indice

            if(self.tokens[indice].tipoToken == TipoToken.SepAbreParentese.name): #arguments
                indice = arguments(indice)
                return indice

            if(self.tokens[indice].tipoToken == TipoToken.SepAbreColchete.name): 
                if(self.tokens[indice + 1].tipoToken == TipoToken.SepFechaColchete.name) or
                    (self.tokens[indice + 1].tipoToken == TipoToken.SepFechaChave.name): 
                    while self.tokens[indice] == TipoToken.SepAbreColchete.name:
                        indice += 1
                        if not self.existeToken(indice):
                            Error(TipoToken.PCChar)
                            return indice
                        if self.tokens[indice] != TipoToken.SepFechaParentese.name:
                            Error(TipoToken.PCChar)
                            return indice
                        indice += 1
                    if self.tokens[indice].tipoToken == TipoToken.SepFechaChave.name:
                        indice = self.arrayInitializer(indice)
                        return indice
                    if not self.tokens[indice] == TipoToken.SepFechaColchete.name:
                        Error(self.tokens[indice], TipoToken.SepFechaColchete.name, "tokenInesperado")
                        return indice
                return self.newArrayDeclarator(indice + 1)
        else:
            Error("Um type")
            return indice


    # newArrayDeclarator ::= [ expression ] {[ expression ]} {[ ]}
    def newArrayDeclarator(self, indice):
        if not self.existeToken(indice):
            Error(TipoToken.SepAbreColchete.name)
            return indice
        if not self.tokens[indice] == TipoToken.SepAbreColchete.name:
            Error(self.tokens[indice], TipoToken.SepAbreColchete.name, "tokenInesperado")
            return indice 
        indice = expression(indice + 1)
        if not self.tokens[indice] == TipoToken.SepFechaColchete.name:
            Error(self.tokens[indice], TipoToken.SepFechaColchete.name, "tokenInesperado")
            return indice 
        indice += 1
        while self.existeToken(indice) and self.tokens[indice] == TipoToken.SepAbreColchete.name:
            indice = expression(indice + 1)
            if not self.existeToken(indice):
                Error(TipoToken.SepFechaColchete.name)
                return indice
            if not self.tokens[indice] == TipoToken.SepFechaColchete.name:
                Error(self.tokens[indice], TipoToken.SepFechaColchete.name, "tokenInesperado")
                return indice 
            indice += 1

        while self.existeToken(indice) and self.tokens[indice] == TipoToken.SepAbreColchete.name:
            indice += 1
            if not self.existeToken(indice):
                Error(TipoToken.SepFechaColchete.name)
                return indice
            if not self.tokens[indice] == TipoToken.SepFechaColchete.name:
                Error(self.tokens[indice], TipoToken.SepFechaColchete.name, "tokenInesperado")
                return indice
            indice += 1

        return indice

    # literal ::= <int_literal> | <char_literal> | <string_literal> | true | false | null
    def literal(self, indice):
        if not self.existeToken(indice):
            Error(TipoToken.Variavel)
            return indice
        literais = [TipoToken.Int.name, TipoToken.Char.name, TipoToken.String.name, TipoToken.PCTrue.name, TipoToken.PCFalse.name, TipoToken.PCNull.name]
        if not self.tokens[indice] in literais:
            return indice
        return indice + 1

    #################### FUNÇÕES AUXILIARES ####################
    def ehUmType(self, indice):
        return ehUmBasicType(indice) or ehUmReferenceType(indice)

    def ehUmBasicType(self,indice):
        tiposBasicos = [TipoToken.PCBoolean.name, TipoToken.PCChar.name, TipoToken.PCInt.name]
        if self.existeToken(indice) and self.tokens[indice] in tiposBasicos:
            return True
        return False

    def ehUmReferenceType(self,indice):
        if self.existeToken(indice) and self.ehUmBasicType(indice):
            indice += 1
            if self.existeToken(indice) and self.tokens[indice] == TipoToken.SepAbreColchete.name:
                indice += 1
            if self.existeToken(indice) and self.tokens[indice] == TipoToken.SepFechaColchete.name:
                return True
        elif self.existeToken(indice) and self.ehUmQualifiedIdentifier(indice):
            return True
        else : 
            return False

    def ehUmQualifiedIdentifier(self,indice):
        return self.existeToken(indice) and self.tokens[indice] == TipoToken.Variavel.name

    def eUmLiteral(self,indice):
        if((self.tokens[indice] == TipoToken.Int.name) or (self.tokens[indice] == TipoToken.Char.name) or
           (self.tokens[indice] == TipoToken.String.name) or (self.tokens[indice] == TipoToken.PCTrue.name) or
           (self.tokens[indice] == TipoToken.PCFalse.name) or (self.tokens[indice] == TipoToken.PCNull.name)):
            return True
        return False

if __name__ == "__main__":
    analisador = analisadorSintatico()