#Defining gcd of two numbers.................
def gcd(a,b):
  if a==0:
    if b>0:
      return b
    else:
      return -b
  elif b==0:
    if a>0:
      return a
    else:
      return -a
  else:
    if a>b:
      return gcd(b,a%b)
    else:
       return gcd(b,a)
  

# GCD for passing argument as tuple..........
def Gcd(*numbers):
  g=gcd(numbers[0],numbers[1])
  for i in range(len(numbers)):
    g=gcd(g,numbers[i])

  return g  



# GCD for passing argument as list.........
def Gcd_readnums(numbers):
  g=gcd(numbers[0],numbers[1])
  for i in range(len(numbers)):
    g=gcd(g,numbers[i])

  return g  




#reading csv files of numbers with newlines......
def read_num_csv(dir):
    with open(dir) as file:
        numbers=file.readlines()
        # print((numbers))
        num=[]
        for nums in numbers:
            numbers=nums.split(",")
            num=num+numbers
        k=[]
        for i in num:
            numbers=i.split()
            k=k+numbers

    k_=[]
    for i in k:
        i=int(i)
        k_.append(i)
    return k_



# Inverse under modulo operation.................
def inverse(a,n):
  for i in range(1,n):
    if (a*i)%n==1:
      return i
  else:
    return 0
  


# testing primality..............
def is_prime(n):
  if n == 1:
    return False


  for i in range(2, int(n**0.5) + 1):
    if n % i == 0:
      return False
  return True



# prime factorisation.............
def p_factorise(n):
  p_factors=[]
  for i in range(2,n+1):
    if n%i==0 and is_prime(i):
      p_factors.append(i)

  return p_factors



#Checking Carmichael number:
def is_carmichael(m):
    if m>2 and is_squarefree(m):
        for factor in p_factorise(m):
            if (m-1)%(factor-1)!=0:
                break
        else:
            return True
    return False

#Searching Camichael Numbers:
def search_carmichael(N):
   '''Finds Carmichael Upto N'''
   for i in range(1,N+1):
    if is_carmichael(i) and not is_prime(i):
        print(f"{i} is a Carmichael Number")



#Finding Index Of A prime Factor of A Number
def p_factor_index(m,p):
    index=1
    while True:
        if m%(p**index)==0:
            index=index+1
        elif m%(p**index)!=0:
            index=index
            break
        else:
            break    
    return index-1


#Checking Wheter given Number is Square Free or Not
def is_squarefree(m):
    '''Checks Wheter the given argument number is square free or not
    returning True or False respectively'''

    factors=p_factorise(m)
    for factor in factors:
        if p_factor_index(m,factor)!=1:
            return False
    return True


#factorial definition:
s=1
def factorial(n):
  
  if n==1 or n==0:
    return 1
  elif n<0:
    raise Exception("Your value is negative")

  else:
    return n*factorial(n-1)

# print(factorial(-2))

#Permutation:
def nPk(n,k):
  if n>0 and k>0 and n>=k: 
    return factorial(n)/factorial(n-k)
  else:
     raise Exception(f"Check the conditions whether: {n}>0,{k}>0,{n}>={k}?")


# print(nPk(2,3))

#Combination:

def nCk(n,k):
  if n>0 and k>0 and n>=k: 
    return factorial(n)/(factorial(k)*factorial(n-k))
  else:
     raise Exception(f"Check the conditions whether: {n}>0,{k}>0,{n}>={k}?")
   
