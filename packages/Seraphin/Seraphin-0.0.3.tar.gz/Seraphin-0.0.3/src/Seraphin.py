################################################
# Mersenne Twister PRNGs (pseudorandom number generators) 
#https://github.com/james727/MTP/blob/master/mersenne_twister.py

#a verifier avec javascript https://stackoverflow.com/questions/48935719/python-and-javascript-pseudo-random-number-generator-prng

class mersenne_rng(object):
    def __init__(self, seed = 5489):
        self.state = [0]*624
        self.f = 1812433253
        self.m = 397
        self.u = 11
        self.s = 7
        self.b = 0x9D2C5680
        self.t = 15
        self.c = 0xEFC60000
        self.l = 18
        self.index = 624
        self.lower_mask = (1<<31)-1
        self.upper_mask = 1<<31

        # update state
        self.state[0] = seed
        for i in range(1,624):
            self.state[i] = self.int_32(self.f*(self.state[i-1]^(self.state[i-1]>>30)) + i)

    def twist(self):
        for i in range(624):
            temp = self.int_32((self.state[i]&self.upper_mask)+(self.state[(i+1)%624]&self.lower_mask))
            temp_shift = temp>>1
            if temp%2 != 0:
                temp_shift = temp_shift^0x9908b0df
            self.state[i] = self.state[(i+self.m)%624]^temp_shift
        self.index = 0

    def get_random_number(self):
        if self.index >= 624:
            self.twist()
        y = self.state[self.index]
        y = y^(y>>self.u)
        y = y^((y<<self.s)&self.b)
        y = y^((y<<self.t)&self.c)
        y = y^(y>>self.l)
        self.index+=1
        return self.int_32(y)

    def int_32(self, number):
        return int(0xFFFFFFFF & number)
        
################################################

#blum blum shub
#https://jeremykun.com/2016/07/11/the-blum-blum-shub-pseudorandom-generator/

# a rester car encryptage et decryptage
#https://www.gkbrk.com/wiki/blum-blum-shub/

import random


def decompose(n):
    exponentOfTwo = 0

    while n % 2 == 0:
        n = n // 2  # using / turns large numbers into floats
        exponentOfTwo += 1

    return exponentOfTwo, n


def isWitness(possibleWitness, p, exponent, remainder):
    if pow(possibleWitness, remainder, p) == 1:
        return False

    if any(pow(possibleWitness, 2**i * remainder, p) == p - 1 for i in range(exponent)):
        return False

    return True


def probablyPrime(p, accuracy=100):
    if p == 2 or p == 3:
        return True
    if p < 2 or p % 2 == 0:
        return False

    exponent, remainder = decompose(p - 1)

    for _ in range(accuracy):
        possibleWitness = random.randint(2, p - 2)
        if isWitness(possibleWitness, p, exponent, remainder):
            return False

    return True


if __name__ == "__main__":
    n = 1

    while not probablyPrime(n, accuracy=100):
        n = random.getrandbits(512)

    print("{} is prime".format(n))

import random
 
def goodPrime(p):
    return p % 4 == 3 and probablyPrime(p, accuracy=100)
 
def findGoodPrime(numBits=512):
    candidate = 1
    while not goodPrime(candidate):
        candidate = random.getrandbits(numBits)
    return candidate
 
def makeModulus():
    return findGoodPrime() * findGoodPrime()
 
def parity(n):
    return sum(int(x) for x in bin(n)[2:]) % 2
 
class BlumBlumShub(object):
    def __init__(self, seed=None):
        self.modulus = makeModulus()
        self.state = seed if seed is not None else random.randint(2, self.modulus - 1)
        self.state = self.state % self.modulus
 
    def seed(self, seed):
        self.state = seed
 
    def bitstream(self):
        while True:
            yield parity(self.state)
            self.state = pow(self.state, 2, self.modulus)
 
    def bits(self, n=20):
        outputBits = ''
        for bit in self.bitstream():
            outputBits += str(bit)
            if len(outputBits) == n:
                break
 
        return outputBits
################################################
#https://github.com/dkull/Isaac-CSPRNG

"""
        3-Clause BSD Licensed implementation of the Isaac CSPRNG for Python3
        https://opensource.org/licenses/BSD-3-Clause
        Usage:
            import Isaac()
            x = Isaac.Isaac(seed_vector = 32bint*256)
            y = x.rand(42) # 0<= y <= 41
"""

mod = 2 ** 32


def mix(a, b, c, d, e, f, g, h):
    a ^= 0xFFFFFFFF & b << 11
    d = (d + a) % mod
    b = (b + c) % mod
    b ^= 0x3FFFFFFF & (c >> 2)
    e = (e + b) % mod
    c = (c + d) % mod
    c ^= 0xFFFFFFFF & d << 8
    f = (f + c) % mod
    d = (d + e) % mod
    d ^= e >> 16
    g = (g + d) % mod
    e = (e + f) % mod
    e ^= 0xFFFFFFFF & f << 10
    h = (h + e) % mod
    f = (f + g) % mod
    f ^= 0x0FFFFFFF & (g >> 4)
    a = (a + f) % mod
    g = (g + h) % mod
    g ^= 0xFFFFFFFF & h << 8
    b = (b + g) % mod
    h = (h + a) % mod
    h ^= 0x007FFFFF & (a >> 9)
    c = (c + h) % mod
    a = (a + b) % mod
    return a, b, c, d, e, f, g, h


class Isaac(object):
    def __init__(self, seed_vector=[0] * 256):
        self.mm = [0] * 256
        self.randrsl = seed_vector
        self.randcnt = 0
        self.aa = 0
        self.bb = 0
        self.cc = 0

        self.__randinit__(True)

    def rand(self, mod=2 ** 32):
        if self.randcnt == 256:
            self.__isaac__()
            self.randcnt = 0
        res = self.randrsl[self.randcnt] % mod
        self.randcnt += 1
        return res

    def __isaac__(self):
        self.cc += 1
        self.bb += self.cc
        self.bb &= 0xFFFFFFFF

        for i in range(256):
            x = self.mm[i]
            switch = i % 4
            xorwith = None
            if switch == 0:
                xorwith = (self.aa << 13) % mod
            elif switch == 1:
                xorwith = self.aa >> 6
            elif switch == 2:
                xorwith = (self.aa << 2) % mod
            elif switch == 3:
                xorwith = self.aa >> 16
            else:
                raise Exception("math is broken")
            self.aa = self.aa ^ xorwith
            self.aa = (self.mm[(i + 128) % 256] + self.aa) % mod
            y = self.mm[i] = (self.mm[(x >> 2) % 256] + self.aa + self.bb) % mod
            self.randrsl[i] = self.bb = (self.mm[(y >> 10) % 256] + x) % mod

    def __randinit__(self, flag):
        a = b = c = d = e = f = g = h = 0x9E3779B9
        self.aa = self.bb = self.cc = 0

        for x in range(4):
            a, b, c, d, e, f, g, h = mix(a, b, c, d, e, f, g, h)

        i = 0
        while i < 256:
            if flag:
                a = (a + self.randrsl[i]) % mod
                b = (b + self.randrsl[i + 1]) % mod
                c = (c + self.randrsl[i + 2]) % mod
                d = (d + self.randrsl[i + 3]) % mod
                e = (e + self.randrsl[i + 4]) % mod
                f = (f + self.randrsl[i + 5]) % mod
                g = (g + self.randrsl[i + 6]) % mod
                h = (h + self.randrsl[i + 7]) % mod

            a, b, c, d, e, f, g, h = mix(a, b, c, d, e, f, g, h)
            self.mm[i : i + 7 + 1] = a, b, c, d, e, f, g, h
            i += 8

        if flag:
            i = 0
            while i < 256:
                a = (a + self.mm[i]) % mod
                b = (b + self.mm[i + 1]) % mod
                c = (c + self.mm[i + 2]) % mod
                d = (d + self.mm[i + 3]) % mod
                e = (e + self.mm[i + 4]) % mod
                f = (f + self.mm[i + 5]) % mod
                g = (g + self.mm[i + 6]) % mod
                h = (h + self.mm[i + 7]) % mod
                a ^= 0xFFFFFFFF & b << 11
                d = (d + a) % mod
                b = (b + c) % mod
                b ^= 0x3FFFFFFF & (c >> 2)
                e = (e + b) % mod
                c = (c + d) % mod
                c ^= 0xFFFFFFFF & d << 8
                f = (f + c) % mod
                d = (d + e) % mod
                d ^= e >> 16
                g = (g + d) % mod
                e = (e + f) % mod
                e ^= 0xFFFFFFFF & f << 10
                h = (h + e) % mod
                f = (f + g) % mod
                f ^= 0x0FFFFFFF & (g >> 4)
                a = (a + f) % mod
                g = (g + h) % mod
                g ^= 0xFFFFFFFF & h << 8
                b = (b + g) % mod
                h = (h + a) % mod
                h ^= 0x007FFFFF & (a >> 9)
                c = (c + h) % mod
                a = (a + b) % mod
                self.mm[i : i + 7 + 1] = a, b, c, d, e, f, g, h
                i += 8
        self.__isaac__()
        self.randcnt = 256


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
from decimal import *

def racin(A=2, n=2, x0=1,number_decimal=10000, number_iteration=1000):
	#x0 dooit être différent de 0 !
	D=Decimal
	getcontext().prec=number_decimal
	A = D(A)
	n = D(n)
	x=x0= D(x0)
	precision=D('0E-'+str(number_decimal))
	i=0
	#x=x0
	test=False
	while (i<number_iteration)and (test==False):
		c=x
		x=x-((x**(n)-A)/(n*x**(n-1)))
		#if x-c==precision:test=True !!!! a verifier serieusement
		if x-c>0 and x-c<precision:test=True
		if x-c<0 and c-x<precision:test=True
		#car abs ne fonctionnement pas
		i=i+1
	print (x-c)
	print (precision)
	print(i)
	return c
	
def ym23(seed=12345,number_block=3,length_block=123):
	length_seed=8
	length=number_block*length_block
	#########################################
	#Calcul d'une liste de nombre premier
	nb_prime = 1000
	prime=[]
	n=1
	while len(prime)<nb_prime:
		#for n in range(2,nb_prime + 1):
		n+=1
		for i in prime:
			if (n % i) == 0:
				break
		else:
			prime+=[n]
	#########################################	
	block=[]
	for i in range(number_block):	
		r=seed % 1000
		p1=prime[r]
		q=seed//1000
		q=q % 1000
		p2=prime[q]
		random=str(racin(A=p1,n=p2,number_decimal=length_block+length_seed))
		random = ''.join( x for x in random if x not in ".")
		seed=int(random[-length_seed:])
		random=random[:length_block]
		block+=[random]
	return block
	

#https://www.geeksforgeeks.org/python-slicing-extract-k-bits-given-position/	
#extract_bit = lambda num, k, p: bin(num)[2:][p:p+k]
def extract_bits(num, p, k):
    # Décalage à droite de num pour que le bit à la position p soit en position 0
    shifted_num = num >> p
    
    # Masque pour extraire les k bits
    mask = (1 << k) - 1
    
    # Appliquer le masque pour extraire les k bits
    extracted_bits = shifted_num & mask
    
    return extracted_bits

#inversion des bit d'un nombre binaire

def invert_bits(num):
    # Calcul de la longueur du nombre binaire
    bit_length = num.bit_length()
    
    # Générer un masque de bits avec tous les bits à 1 de la même longueur que le nombre d'entrée
    all_ones = (1 << bit_length) - 1
    
    # Inverser les bits en utilisant l'opération XOR avec le masque
    inverted_num = num ^ all_ones
    
    return inverted_num


#inverse symetrise un nombre binaire
#x bit
#def inv_symetri_bit(x):return bin(x)[:1:-1]
def reverse_bits(num):
    # Calcul de la longueur du nombre binaire
    bit_length = num.bit_length()
    
    # Initialiser le résultat à 0
    reversed_num = 0
    
    # Parcourir chaque bit de l'entrée
    for i in range(bit_length):
        # Décaler les bits du résultat vers la gauche pour faire de la place pour le prochain bit
        reversed_num <<= 1
        
        # Ajouter le bit de droite de num (et le mettre à la droite du résultat)
        reversed_num |= (num & 1)
        
        # Décaler le nombre d'entrée vers la droite pour traiter le prochain bit
        num >>= 1
    
    return reversed_num

# Exemple d'utilisation
binary_num = 0b111001  # Représentation binaire (décimal 20)
reversed_binary_num = reverse_bits(binary_num)
print(f"Nombre binaire original: {bin(binary_num)}")
print(f"Nombre binaire inversé: {bin(reversed_binary_num)}")
#mutiplexage binaire
def interleave_bits(num1, num2):
	# Find the maximum length of the binary representation of both numbers
	if num1.bit_length()>num2.bit_length():max_len=num1.bit_length()
	else:max_len=num1.bit_length()
	
	# Initialize the result variable
	result = 0
	# Iterate through each bit position
	for i in range(max_len):
	    # Extract the i-th bit from num1 and num2
	    bit1 = (num1 >> i) & 1
	    bit2 = (num2 >> i) & 1

	    # Interleave the bits in the result
	    result |= (bit1 << (2 * i + 1)) | (bit2 << (2 * i))

	return result
 
import mpmath

def extract_bits_of_pi(k=1000, num_bits=1024):
    # Définir la précision pour mpmath (suffisante pour extraire les bits)
    mpmath.mp.dps = k + num_bits  # Nombre de chiffres après la virgule pour pi
    
    # Calcul de Pi
    pi_value = mpmath.pi
    
    # Convertir pi en une chaîne binaire
    pi_binary = mpmath.nstr(pi_value, mpmath.mp.dps).replace('.', '')
    pi_binary = bin(int(pi_binary))
    
    # Extraire les bits à partir de la position k
    start_index = k
    end_index = k + num_bits
    extracted_bits = pi_binary[2:][start_index:end_index]  # Ignorer le '0b' en tête
    
    return extracted_bits
    
def concatenate_binaries(bin1, bin2):
    # Calculer la longueur en bits de bin2
    length_bin2 = bin2.bit_length()

    # Décaler bin1 vers la gauche de la longueur de bin2 bits
    bin1_shifted = bin1 << length_bin2

    # Effectuer un OU binaire pour concaténer les deux nombres
    concatenated_bin = bin1_shifted | bin2

    return concatenated_bin

# Exemple d'utilisation
binary_num_start = extract_bits_of_pi()
k=10
p=2
print('binary_num_start : ',binary_num_start)
extract=extract_bits(int(binary_num_start,2), p, k)
print('extract : ',bin(extract))
inv_bit=invert_bits(extract)
print('invert extract',bin(inv_bit))
print('concat',bin(concatenate_binaries(extract, inv_bit)))
##########################   
# Example usage:
n=0b110011001
binary_num = 0b11011010  # Représentation binaire (décimal 214)
num1 = 0b11110  # Binary: 1011 (11 in decimal)
num2 = 0b01001  # Binary: 1100 (12 in decimal)

# Interleave the bits
result = interleave_bits(num1, num2)

print(bin(num1),' : ',bin(num2),'multiplexage : ',bin(result))  # Output will be 0b11011001 (217 in decimal)
print(bin(num2),'inversion des bit ; ',bin(invert_bits(num2)))
print(bin(n),'symetrie ; ',bin(reverse_bits(n)))
p=0
k=4
print(bin(binary_num),'extract ; ',bin(extract_bits(binary_num, p, k)))

##########################
class YM24(object):
    def __init__(self):
        print('Seraphin is live')
#########################
