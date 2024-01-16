''' 2ºProjeto de FP 
    Francisco Ferro Pereira 
    francisco.ferro.pereira@tecnico.ulisboa.pt '''

#####################
#### TAD GERADOR ####
#####################

def valida_arg_g(b,s):

    '''
    Função auxiliar que faz as validações dos argumentos da função cria_gerador
    '''    
    if type(b)!=int or type(s)!=int:
        return False
    
    if b not in (32,64) or s<=0: 
        return False
    
    if (b == 32 and s > 0xFFFFFFFF ) or (b == 64 and s > 0xFFFFFFFFFFFFFFFF):
        return False

    return True


def cria_gerador(b, s):
    '''
    Esta função recebe um inteiro b correspondente a um número de bits do gerador e um inteiro positivo s correspondente
    à seed ou estao inicial, e devolve o gerador correspondente.

    Caso os argumentos sejam inválidos gera um ValueError com a seguinte mensagem: 'cria_gerador: argumentos invalidos'.
    '''

    if not valida_arg_g(b,s):
        raise ValueError('cria_gerador: argumentos invalidos')
    
    return [b,s]
    

def cria_copia_gerador(g):
    '''
    Esta função recebe um gerador e devolve um cópia nova do gerador.
    '''
    copia_gerador = []
    copia_gerador.append(obtem_bits(g))
    copia_gerador.append(obtem_estado(g))
    return copia_gerador

def obtem_estado(g):    
    '''
    Esta função devolve o estado atual do gerador sem o alterar.
    '''    
    return g[1]

def obtem_bits(g):
    '''
    Esta função devolve o número de bits do gerador.
    '''
    return g[0]

def define_estado(g,s):
    '''
    Esta função define o novo valor do estado do gerador g como sendo s, e devolve s.
    '''    
    g[1] = s    
    return s
    
def atualiza_estado(g):
    
    '''
    Esta função atualiza o estado do gerador g de acordo com o algoritmo xorshift de geração de números pseudoaleatórios,
    e devolve-o.
    '''
    if g[0]==32:
        s = obtem_estado(g) 
        s ^= ( s << 13 ) & 0xFFFFFFFF
        s ^= ( s >> 17 ) & 0xFFFFFFFF
        s ^= ( s << 5 ) & 0xFFFFFFFF
        define_estado(g,s)
        return s

    else:
        s = obtem_estado(g) 
        s ^= ( s << 13 ) & 0xFFFFFFFFFFFFFFFF
        s ^= ( s >> 7 ) & 0xFFFFFFFFFFFFFFFF
        s ^= ( s << 17 ) & 0xFFFFFFFFFFFFFFFF
        define_estado(g,s)
        return s

def eh_gerador(arg):
    '''
    Esta função devolve True caso o seu argumento seja um TAD gerador e False caso contrário.
    '''
    if type(arg) != list or len(arg)!=2: 
        return False
            
    return valida_arg_g(obtem_bits(arg),obtem_estado(arg))
    

def geradores_iguais(g1,g2):
    '''
    Esta função devolve True apenas se g1 e g2 são geradores iguais. Caso contrário devolve False.
    '''
    if obtem_bits(g1) == obtem_bits(g2) and obtem_estado(g1) == obtem_estado(g2):
        return True    
    return False
          
    
def gerador_para_str(g):
    '''
    Esta função devolve a cadeia de carateres que representa o seu argumento como mostrado nos exemplos.
    '''
    return 'xorshift{}(s={})'.format(obtem_bits(g),obtem_estado(g))


###############################
#### FUNÇÕES DE ALTO NÍVEL ####
###############################

def gera_numero_aleatorio(g,n):

    '''
    Esta função atualiza o estado do gerador g e devolve um número aleatório no intervalo [1,n] obtido a partir do novo
    estado s de g como 1 + mod(s,n), em que mod() corresponde à operação resto da divisão inteira.
    '''
    atualiza_estado(g)    
    return 1 + obtem_estado(g) % n 


def gera_carater_aleatorio(g,c):

    '''
    Esta função atualiza o estado do gerador g e devolve um caratér aleatório o intervalo 'A' e o caratér maiúsculo c.
    Este é obtido a partir do novo estado s de g como o caratér na posição mod(s,l) da cadeia de carateres de tamanho l
    formada por todos os carateres entre 'A' e c.
    '''
    atualiza_estado(g)

    # Cria uma lista com todos os caracteres entre A e c maiúsculo 
    lista_letras = list(map(chr, range(65, ord(c)+1)))

    # Junta todos os caracteres da lista numa string
    cad_carateres = ''.join(lista_letras)
       
    return cad_carateres[obtem_estado(g) % len(cad_carateres)]


########################
#### TAD COORDENADA ####
########################

def valida_args_c(col,lin):
    
    '''
    Função auxiliar que valida os argumentos da coordenada
    '''
    if type(col)!=str or type(lin)!=int:
        return False

    if len(col)!=1 or not(ord('A')<=ord(col)<=ord('Z')): 
        return False 

    if lin>99 or lin<=0:
        return False
    
    return True 

def cria_coordenada(col,lin):
    '''
    Esta função recebe os valores correpondentes à coluna (col) e linha (lin) e devolve a coordenada correps
    '''
    if not valida_args_c(col,lin):
        raise ValueError('cria_coordenada: argumentos invalidos')

    return (col,lin)


def obtem_coluna(c):
    '''
    Devolve a coluna (col) da coordenada c
    '''
    return c[0]


def obtem_linha(c):
    '''
    Devolve a linha (lin) de c
    '''
    return c[1]


def eh_coordenada(arg):
    '''
    Devolve True caso o seu argumento seja um TAD coordenada e False caso contrário.
    '''    
    if type(arg)!=tuple or len(arg)!=2: 
        return False    
    
    return valida_args_c(obtem_coluna(arg),obtem_linha(arg))
    

def coordenadas_iguais(c1,c2):
    '''
    Devolve True apenas se c1 e c2 são iguais, caso contrário devolve False.
    '''
    return obtem_coluna(c1)==obtem_coluna(c2) and obtem_linha(c1)==obtem_linha(c2)        
        


def coordenada_para_str(c):    
    '''
    Devolve a cadeia de carateres que representa o seu argumento.
    '''
    # Função que adiciona à string de saída um 0 no caso de numero da linha<10
    def adiciona_0(linha):
        return '0'+ str(obtem_linha(c)) if linha<10 else str(obtem_linha(c))
	
    return '{}{}'.format(obtem_coluna(c),adiciona_0(obtem_linha(c)))


def str_para_coordenada(s):
    '''
    Devolve a coordenada representada pelo seu argumento.
    '''
    return (s[0],int(s[2])) if int(s[1:len(s)])<10 else (s[0],int(s[1:len(s)]))
   
    

###############################
#### FUNÇÕES DE ALTO NÍVEL ####
###############################

def obtem_coordenadas_vizinhas(c):
    '''
    Devolve um tuplo com as coordenadas vizinhas à coordenada c, começando pela coordenada na diagonal acima-esquerda
    de c e seguindo no sentido horário.
    '''
    coordenadas_vizinhas = []

    # Adiciona nesta ordem as seguintes coordenadas se estas existirem (diag esq sup, acima, diag dir sup)
    for coluna in range(ord(obtem_coluna(c))-1,ord(obtem_coluna(c))+2):
        
        if eh_coordenada((chr(coluna),obtem_linha(c)-1)):
        
            coordenadas_vizinhas.append(cria_coordenada(chr(coluna),obtem_linha(c)-1))
                
    # Adiciona a coordenada à direita se esta existir
    if eh_coordenada(((chr(ord(obtem_coluna(c))+1),obtem_linha(c)))): 
        coordenadas_vizinhas.append(cria_coordenada(chr(ord(obtem_coluna(c))+1),obtem_linha(c)))
  
    # Adiciona nesta ordem as seguintes coordenadas se estas existirem (diag dir inf, abaixo, diag esq inf)
    for coluna in range(ord(obtem_coluna(c))+1,ord(obtem_coluna(c))-2,-1):

        if eh_coordenada(((chr(coluna),obtem_linha(c)+1))):

            coordenadas_vizinhas.append(cria_coordenada(chr(coluna),obtem_linha(c)+1))

    # Adiciona a coordenada à esquerda se esta existir
    if eh_coordenada(((chr(ord(obtem_coluna(c))-1),obtem_linha(c)))):
        coordenadas_vizinhas.append(cria_coordenada(chr(ord(obtem_coluna(c))-1),obtem_linha(c)))
        
    return tuple(coordenadas_vizinhas)


def obtem_coordenada_aleatoria(c,g):

    '''
    Recebe uma coordenada c e um TAD gerador g, e devolve uma coordenada gerada aleatoriamente, em que c define a maior
    coluna e maior linha possíveis. É gerada, em sequência, primeiro a coluna e depois a linha da coordenada resultado.
    '''
    coordenada_aleatoria = cria_coordenada(gera_carater_aleatorio(g,obtem_coluna(c)), gera_numero_aleatorio(g,obtem_linha(c)))
    return coordenada_aleatoria


#####################
#### TAD PARCELA ####
#####################

def cria_parcela():
    '''
    Devolve uma parcela tapada sem mina escondida.
    '''        
    return ['tapada',False] # False - não tem mina , True - tem mina

def cria_copia_parcela(p):
    '''
    Recebe uma parcela p e devolve uma nova cópia da parcela.
    '''
    copia_parcela = []
    copia_parcela.append(p[0])
    copia_parcela.append(p[1])
    return copia_parcela


def limpa_parcela(p):
    '''
    Modifica destrutivamente a parcela p modificando o seu estado para limpa, e devolve a própria parcela.
    '''
    p[0] = 'limpa'
    return p


def marca_parcela(p):
    '''
    modifica destrutivamente a parcela p modificando o seu estado para marcada com uma bandeira, e devolve a própria parcela.
    '''
    p[0] = 'marcada'
    return p


def desmarca_parcela(p):
    '''
    Modifica destrutivamente a parcela p modificando o seu estado para tapada, e devolve a própria parcela.
    '''
    p[0] = 'tapada'
    return p 


def esconde_mina(p):
    '''
    Modifica destrutivamente a parcela p escondendo uma mina na parcela, e devolve a própria parcela.

    '''
    p[1] = True
    return p


def eh_parcela(arg):

    '''
    Devolve True caso o seu argumento seja um TAD parcela e False caso contrário.
    '''
    if type(arg)==list and len(arg)==2 and type(arg[0]) == str and arg[0] in ('tapada','limpa','marcada') and type(arg[1])==bool and arg[1] in (True,False):        
        return True 
    return False



def eh_parcela_tapada(p):
    
    ''' 
    Devolve True caso a parcela p se encontre tapada e False caso contrário.
    '''
    if p[0]=='tapada':
        return True
    return False


def eh_parcela_marcada(p):
    '''
    Devolve True caso a parcela p se encontre marcada com uma bandeira e False caso contrário.

    '''
    if p[0] == 'marcada':
        return True
    return False


def eh_parcela_limpa(p):

    '''
    Devolve True caso a parcela p se encontre limpa e False caso contrário.

    '''    
    if p[0] == 'limpa':
        return True    
    return False 


def eh_parcela_minada(p):
    '''
    Devolve True caso a parcela p esconda uma mina e False caso contrário.
    '''
    if p[1] == True:
        return True
    return False


def parcelas_iguais(p1,p2):
    '''
    Devolve True apenas se p1 e p2 sãoo parcelas e são iguais.
    '''
    if p1[0]==p2[0] and p1[1]==p2[1]:
        return True
    return False


def parcela_para_str(p):
    '''
    Devolve a cadeia de caracteres que representa a parcela em função do seu estado: parcelas tapadas ('#'), 
    parcelas marcadas ('@'),parcelas limpas sem mina ('?') e parcelas limpas com mina ('X').
    '''
        
    if eh_parcela_tapada(p):
        return '#'
        
    if eh_parcela_marcada(p):
        return '@'
        
    if eh_parcela_limpa(p) and not eh_parcela_minada(p):
        return '?'
        
    if eh_parcela_limpa(p) and eh_parcela_minada(p):
        return 'X'
    
###############################
#### FUNÇÕES DE ALTO NÍVEL ####
###############################

def alterna_bandeira(p):
    '''
    Recebe uma parcela p e modifica-a destrutivamente da seguinte forma: 
    Desmarca se estiver marcada e marca se estiver tapada, devolvendo True.
    Em qualquer outro caso, não modifica a parcela e devolve False.
    '''

    if eh_parcela_marcada(p):
        desmarca_parcela(p)
        return True
    
    if eh_parcela_tapada(p):        
        marca_parcela(p)
        return True
    
    return False


###################
#### TAD CAMPO ####
###################

def cria_campo(c,l):
    '''
    Recebe uma cadeia de carateres e um inteiro correspondentes à última coluna e à última linha de um campo de minas, 
    e devolve o campo do tamanho pretendido formado por parcelas tapadas sem minas. O construtor verifica 
    a validade dos seus argumentos, gerando um ValueError com a mensagem 
    cria campo: argumentos invalidos' caso os seus argumentos não sejam válidos.
    '''

    if type(c)!=str or len(c)!=1 or not('A'<=c<='Z')  or type(l)!=int or not(1<=l<=99):
        raise ValueError('cria_campo: argumentos invalidos')
    
    # Lista com as colunas de 'A' a c
    colunas_campo = [chr(c) for c in range(ord('A'), ord(c) + 1)] 
    
    # Lista com as linhas de 1 até l
    linhas_campo = [l for l in range(1,l+1)] 

    # lista com todas as coordenadas ordenadas por coluna | ex: (A1,A2,A3,B1,B2,B3...etc)
    lista_coordenadas = [cria_coordenada(c,l) for l in linhas_campo for c in colunas_campo] 
    
    # lista com todas as parcelas ordenadas da mesma forma que as coordenadas 
    lista_parcelas = [cria_parcela() for i in linhas_campo for i in colunas_campo]
    
    return {'ultima_coluna': c, 'ultima_linha': l , 'linhas': linhas_campo ,'colunas': colunas_campo, 'parcelas': lista_parcelas  , 'coordenadas': lista_coordenadas}


def cria_copia_campo(m):
    '''
    Recebe um campo e devolve uma nova cópia do campo.
    '''
    
    m_copia = cria_campo(obtem_ultima_coluna(m),obtem_ultima_linha(m))
        
    return m_copia


def obtem_ultima_coluna(m):
    '''
    Devolve a cadeia de caracteres que corresponde à última coluna do campo de minas.
    '''
    return m['ultima_coluna']



def obtem_ultima_linha(m):
    '''
    Devolve o valor inteiro que corresponde à última linha do campo de minas.
    '''
    return m['ultima_linha']


def obtem_parcela(m,c):
    '''
    Devolve a parcela do campo m que se encontra na coordenada c.
    '''    
    # A parcela e a coordenada correspondem por índice na lista_parcelas e lista_coordenadas, respetivamente
    indice_coordenada = m['coordenadas'].index(c)
    
    return m['parcelas'][indice_coordenada]


def obtem_coordenadas(m,s):
    '''
    Devolve o tuplo formado pelas coordenadas ordenadas em ordem ascendente de esquerda à direita e de cima a baixo das parcelas
    dependendo do valor de s: 'limpas' para as parcelas limpas, 'tapadas' para as parcelas tapadas, 'marcadas' para as 
    parcelas marcadas, e 'minadas' para as parcelas que escondem minas.
    '''
    lista_resultado = []
            
    for c in m['coordenadas']:
                                        
        if s == 'minadas' and eh_parcela_minada(obtem_parcela(m,c)):
            
            lista_resultado.append(c)
        
        if  s == 'tapadas' and eh_parcela_tapada(obtem_parcela(m,c)):

            lista_resultado.append(c)

        if s == 'marcadas' and eh_parcela_marcada(obtem_parcela(m,c)):

            lista_resultado.append(c)
        
        if s == 'limpas' and eh_parcela_limpa(obtem_parcela(m,c)):

            lista_resultado.append(c)
    
    return tuple(lista_resultado)

def obtem_numeros_minas_vizinhas(m,c):
    '''
    Devolve o número de parcelas vizinhas da parcela na coordenada c que escondem uma mina.
    '''
    num_minas_vizinhas = 0

    for c in obtem_coordenadas_vizinhas(c):
        if eh_coordenada_do_campo(m,c) and eh_parcela_minada(obtem_parcela(m,c)):
            num_minas_vizinhas +=1
    
    return num_minas_vizinhas

def eh_campo(arg):
    '''
    Devolve True caso o seu argumento seja um TAD campo e False caso contrário.
    '''
    if type(arg)==dict and len(arg)==6 and {'ultima_coluna','ultima_linha','linhas','colunas','parcelas','coordenadas'} == arg.keys() and type(arg['ultima_coluna'])==str and type(arg['ultima_linha']== int and type('linhas')==list and type(arg['colunas']==list) and type(arg['parcelas'])==list and type(arg['coordenadas']==list)):
        return True        
    return False

def eh_coordenada_do_campo(m,c):
    '''
    Devolve True se c é uma coordenada válida dentro do campo m.
    '''
    if eh_coordenada(c) and c in m['coordenadas']:
        return True    
    return False


def campos_iguais(m1,m2):
    '''
    Devolve True apenas se m1 e m2 forem campos e forem iguais.
    '''
    if m1['ultima_coluna']==m2['ultima_coluna'] and m1['ultima_linha']==m2['ultima_linha'] and m1['linhas']==m2['linhas'] and m1['colunas']==m2['colunas'] and m1['parcelas']==m2['parcelas'] and m1['coordenadas']==m2['coordenadas']:         
        return True
    return False


def campo_para_str(m):
    '''
    Devolve uma cadeia de caracteres que representa o campo de minas como mostrado nos exemplos.
    '''   
    # Junta numa string os nomes das colunas ex: 'ABCDE' 
    colunas = ''.join([c for c in m['colunas']])

    # Adiciona um 0 antes do numero da linha para linhas<10 ex: [01,02,03,04,05]
    linhas_menores_10 = ['0'+str(l) for l in m['linhas'] if l<10]
    
    linhas_maiores_10 = [str(l) for l in m['linhas'] if l>=10]

    # Vai concatenar as listas caso haja 10 ou mais linhas, senão devolve só as linhas<10
    linhas = linhas_menores_10 + linhas_maiores_10 if len(linhas_maiores_10)>0 else linhas_menores_10
    
        
    def linha_parcela_para_str(m):
        '''
        Função auxiliar de campo_para_str que recebe um campo e transforma uma parcela na sua string correspondente. 
        
        No caso da parcela ser limpa e não minada, devolve o número de minas vizinhas, se estas existirem, senão
        devolve uma parcela vazia.          
        '''
        resultado = []
        lista_parcelas = m['parcelas']
        for i in range(0,len(lista_parcelas)):
        
            if eh_parcela_limpa(lista_parcelas[i]) and not eh_parcela_minada(lista_parcelas[i]):

                # Se tiver minas vizinhas, a parcela passa a ser o número de minas vizinhas   
                if obtem_numeros_minas_vizinhas(m,m['coordenadas'][i])>0:                    
                    resultado.append(str(obtem_numeros_minas_vizinhas(m,m['coordenadas'][i])))
                     
                else:
                    # Se não tiver minas vizinhas e a parcela é limpa, esta passa a ser um espaço
                    resultado += [' ']
                                
            else:

                # Caso não seja limpa e minada transforma a parcela na sua string
                resultado.append(parcela_para_str(lista_parcelas[i]))
        
        return resultado
    
    
    def divide_parcelas_por_linhas(lista_parcelas, num_linhas):
        '''
        Função auxiliar de campo_para_str

        Recebe uma lista de parcelas em string e o número de linhas de um campo e devolve uma lista de listas, com cada
        lista a corresponder a uma linha de parcelas.
        '''    
        length = len(lista_parcelas)                
        return [lista_parcelas[i*length // num_linhas: (i+1)*length // num_linhas] for i in range(num_linhas)]


        
    # Lista de listas, em que cada lista corresponde a uma linha de parcelas
    linhas_parcela = divide_parcelas_por_linhas(linha_parcela_para_str(m),len(m['linhas']))    
    
    
    def linhas_c(linhas_parcela):
        '''
        Função auxiliar de campo_para_str

        Recebe uma lista de listas, com cada lista a representar uma linha de parcelas do campo e
        devolve uma string com todas as linhas do campo.
        '''
        x = ''
        for i in range(0,len(linhas_parcela)):
            
            # Junta as parcelas em cada lista de linhas_parcela                       
            p = ''.join(linhas_parcela[i])

            # Concatena as strings das linhas todas, adicionando um \n entre cada uma           
            x += f'{linhas[i]}|{p}|\n'
        return x

    return f"   {colunas}\n  {'+'}{'-'*len(m['colunas'])}{'+'}\n{linhas_c(linhas_parcela)}  {'+'}{'-'*len(m['colunas'])}{'+'}"


###############################
#### FUNÇÕES DE ALTO NÍVEL ####
###############################

def coloca_minas(m,c,g,n):
    '''
    Modifica destrutivamente o campo m escondendo n minas em parcelas dentro do campo. As n coordenadas são geradas 
    sequencialmente utilizando o gerador g, de modo a que não coincidam com a coordenada c nem com nenhuma parcela vizinha 
    desta, nem se sobreponham com minas colocadas anteriormente.
    '''

    # Enquanto houver minas por colocar
    while not (n==0):
        
        c_aleatoria = obtem_coordenada_aleatoria(cria_coordenada(obtem_ultima_coluna(m),obtem_ultima_linha(m)),g)

        if c_aleatoria!=c and c_aleatoria not in obtem_coordenadas_vizinhas(c) and not eh_parcela_minada(obtem_parcela(m,c_aleatoria)):
        
            esconde_mina(obtem_parcela(m,c_aleatoria))

            n = n - 1  
    
    return m



def limpa_campo(m,c):
    '''
    Modifica destrutivamente o campo limpando a parcela na coordenada c, devolvendo-o. Se não houver 
    nenhuma mina vizinha escondida, limpa iterativamente todas as parcelas vizinhas tapadas. 
    Caso a parcela se encontre já limpa, a operação não tem efeito.
    '''
    
    # Se a parcela já se encontra limpa retorna o campo
    if eh_parcela_limpa(obtem_parcela(m,c)):
        return m
    
    # Limpa a parcela da coordenada de entrada
    limpa_parcela(obtem_parcela(m,c))

    # Caso a parcela seja minada, limpa só essa parcela e para de limpar o campo
    if eh_parcela_minada(obtem_parcela(m,c)):
        return m
    
    # Se existir minas vizinhas, limpa apenas a coordenada de entrada e para de limpar o campo
    if obtem_numeros_minas_vizinhas(m,c) > 0:
        return m 

    # Se não existirem minas vizinhas, limpa as coordenadas vizinhas e repete o processo nas coordenadas vizinhas (recursão)
    for x in obtem_coordenadas_vizinhas(c):
        if eh_coordenada_do_campo(m,x) and eh_parcela_tapada(obtem_parcela(m,x)):       
            # Se tiver minas vizinhas, limpa apenas a parcela de x
            if obtem_numeros_minas_vizinhas(m,x)>0:
                limpa_parcela(obtem_parcela(m,x))
            else:
            # Se não tiver minas vizinhas a x, repete o processo todo    
                limpa_campo(m,x)

    return m
        
############################
#### FUNÇÕES ADICIONAIS ####
############################

def jogo_ganho(m):
    '''
    É uma função auxiliar que recebe um campo do jogo das minas e devolve True se todas as parcelas sem minas 
    se encontram limpas, ou False caso contrário.
    '''   
    
    # Se o número de parcelas tapadas + número de parcelas marcadas for igual à ao número de parcelas minadas, ganhou-se o jogo
    if len(obtem_coordenadas(m,'tapadas')) + len(obtem_coordenadas(m,'marcadas')) == len(obtem_coordenadas(m,'minadas')):
        return True    
    return False 


def turno_jogador(m):
    '''
    Recebe um campo de minas e oferece ao jogador a opção de escolher uma ação e uma coordenada. 
    Modifica destrutivamente o campo de acordo com ação escolhida, devolvendo False caso o jogador tenha limpo uma parcela 
    que continha uma mina, ou True caso contrário. A função deve repetir as mensagens de input até o jogador introduzir uma
    ação válida ('L' ou 'M') e uma coordenada válida que se pretenda limpar ou marcar.
    '''
            
    
    # Valida o input da ação
    action = input('Escolha uma ação, [L]impar ou [M]arcar:')
    while action!='L' and action!='M':
        action = input('Escolha uma ação, [L]impar ou [M]arcar:')

    # Valida o input da coordenada        
    c = str_para_coordenada(input('Escolha uma coordenada:'))             
    while not eh_coordenada_do_campo(m,c):
            c = str_para_coordenada(input('Escolha uma coordenada:'))
    
    if action =='L':
        limpa_campo(m,c)
        
        if eh_parcela_minada(obtem_parcela(m,c)):
            return False
        return True
    
    if action == 'M':
        alterna_bandeira(obtem_parcela(m,c))
        return True

        
def minas(c,l,n,d,s):
    '''
    É a função principal que permite jogar o jogo. Recebe uma str e 4 valores inteiros correspondentes, respetivamente, a:
    última coluna c; última linha l; número de parcelas com minas n; dimensão do gerador de números d; 
    e estado inicial ou seed s para a geração de números aleatórios. 
    
    A função devolve True se o jogador conseguir ganhar o jogo, ou False caso contrário.

    Gera ValueError com a mensagem: 'minas: argumentos invalidos' para argumentos inválidos
    '''
    
    if type(c)!= str or type(l)!= int or type(n)!= int or type(d)!=int or type(s)!=int:
        raise ValueError('minas: argumentos invalidos')
    
    if len(c)!=1 or not 'A'<=c<='Z':
        raise ValueError('minas: argumentos invalidos')
    
    if l<=0 or l>99:
        raise ValueError('minas: argumentos invalidos')
    
    # Lista com todos as colunas  
    colunas = [chr(c) for c in range(ord('A'), ord(c) + 1)]
    
    if n<=0 or n>(len(colunas) * l) - 9:
        raise ValueError('minas: argumentos invalidos')
        
    if d not in (32,64):
        raise ValueError('minas: argumentos invalidos')
    
    if s<=0:
        raise ValueError('minas: argumentos invalidos')
    
    if (d == 32 and s > 0xFFFFFFFF ) or (d == 64 and s > 0xFFFFFFFFFFFFFFFF):
        raise ValueError('minas: argumentos invalidos')
        
         
    m = cria_campo(c,l)
    g = cria_gerador(d,s)
    
    num_parcelas_marcadas = len(obtem_coordenadas(m,'marcadas'))    
    num_bandeiras = f'   [Bandeiras {num_parcelas_marcadas}/{n}]'

    print(num_bandeiras)
    print(campo_para_str(m))

    # Verifica se a string de input da coordenada incialmente escolhida pertence ao campo.       
    c_i = str_para_coordenada(input('Escolha uma coordenada:'))
    while not eh_coordenada_do_campo(m,c_i):
        c_i = str_para_coordenada(input('Escolha uma coordenada:'))
        

    # Coloca n minas no campo de forma aleatória. As minas não podem estar na c_i nem nas suas vizinhas
    coloca_minas(m,c_i,g,n)
    
    # Limpa a parcela da coordenada c_i e as suas vizinhas
    limpa_campo(m,c_i)
        
    while not jogo_ganho(m):
        
        num_parcelas_marcadas = len(obtem_coordenadas(m,'marcadas'))    
        num_bandeiras = f'   [Bandeiras {num_parcelas_marcadas}/{n}]'
        print(num_bandeiras)
        print(campo_para_str(m))
        
        # Se for limpa uma parcela com mina, a mina detona e o jogo acaba.
        if not turno_jogador(m):
            print(num_bandeiras)
            print(campo_para_str(m))
            print('BOOOOOOOM!!!')
            return jogo_ganho(m)

    print(num_bandeiras)
    print(campo_para_str(m))
    print('VITORIA!!!')     
    return jogo_ganho(m)


try:
    minas('K', 8, 10, 32, 12345)
except ValueError as e:
    print(f"Error: {e}")
# Esta é a submissão final