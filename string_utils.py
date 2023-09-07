"""
funcions per treballar amb cadenes de text o strings
"""
def troba_vals(frase, patro):
    """
    funcio que busca en una frase quan es repeteix un cert patró, per exemple
    busca en la frase "asdfasdfasdf" on apareix el patro "df", enaquest cas:
    [2, 6, 10]

    """
    index = frase.find(patro)
    inds=[]
    while index != -1:
        inds.append(index)
        index = frase.find(patro,index+1)
    return inds

def troba_nessim_repe(frase, patro, n):
    """
    troba la enessima repetició dun patró a un text, 
    per exemple:
    busca en la frase "asdfasdfasdf" la repetició 2a del patro "df", és a la posició 6.

    """
    index = frase.find(patro)
    inds=[]
    reps=1
    while index != -1 and reps < n:
        inds.append(index)
        reps += 1
        index = frase.find(patro,index+1)
    
    if reps < n:
        raise Exception("Repetició nèssima-{} del patró {} no trobada :/".format(n,patro))
    return index


def extreu_paraula(frase, sep='"'):
    """
    aquesta funció agafa una frase i busca dos separadors iguals d'un caràcter
    i extreu el que hi ha entremig.
    Per exemple:
    si tenim la frase 'hola que tal .100.€ he rebut'
    i el separador .
    tornarà: 100

    Nota: Ha d'haver-hi exactament 2 separadors en tota la frase, ni més ni menys.
    """
    inds = troba_vals(frase,sep)
    if len(inds) != 2:
        raise Exception("there must be only two double quotes surrounding the ticker! Otherwise the program can't find the ticker value!")  
    return(frase[ (inds[0]+1):inds[1]])