from decimal import *


# Swap function
def swap(list, pos1, pos2):
     
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list

# Fonction pour mélanger une liste `A` Fisher-Yates shuffle
def shuffle(A):
 
    # lit la liste de l'index le plus bas au plus haut
    for i in range(len(A) - 1):
        # génère un nombre aléatoire `j` tel que `i <= j < n`
        j = randrange(i, len(A))
 
        # échange l'élément courant avec l'index généré aléatoirement
        swap(A, i, j)
            
def PI(number_decimal=10000, number_iteration=18):

  #Pi by Almkvist Berndt 
  D=Decimal
  getcontext().prec=number_decimal
  a=n=D(1)
  g,z,half=1/D(2).sqrt(),D(0.25),D(0.5)
  for i in range(number_iteration):
    x=[(a+g)*half,(a*g).sqrt()]
    var=x[0]-a
    z-=var*var*n
    n+=n
    a,g=x
  return a*a/z
  
#Clacul d'une liste de max nombre premier

#Lire la saisie de l'utilisateur
max = 1000
prime=[]
n=1
while len(prime)<max:
  #for n in range(2,max + 1):
  n+=1
  for i in prime:
           if (n % i) == 0:
               break
  else:
             prime+=[n]
             
#calcul de la racine enieme

# Cette fonction basé sur la méthode de Newton-Raphson permet
#de déterminer la racine n-ième d'un nbre. err est l' erreur relative
# en cas de non convergence prendre tol grand (exemple  tol=0.5)
# x0 doit être sous la forme d'un réel (exple x0=1.0)

from math import *

def racin(A=2, n=2, x0=1):
      i=0
      x=x0
      tol=10e-8
      if x==0:
            print ("Erreur x0 doit être différent de zéro")
      else:
            while (i<3000):
                  c=x
                  x=x-((x**(n)-A)/(n*x**(n-1)))
                  q=x-c
                  err=fabs(q/x)
                  i=i+1
      if (err <tol):
            print ([ c, err])
      else:
            print (" le système ne converge pas. Ajuster le compteur i ou jouer sur tol ou sur x0")

D=Decimal
print(racin(D(2),D(2),D(1)))
