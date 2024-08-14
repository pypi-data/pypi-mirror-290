#2Dmatrix making:
def mat(m, n):
  A = []
  for i in range(m):
    a = []
    for j in range(n):
      x = float(input(f"Enter the element A[{i}][{j}]: "))
      a.append(x)

    A.append(a)
  return A


#3D Matrix Making
def mat3d(m, n, p):
  A = []
  for i in range(m):
    a = []
    for j in range(n):
      b = []
      for k in range(p):
        x = float(input(f"Enter the element A[{i}][{j}][{k}]: "))
        b.append(x)
      a.append(b)
    A.append(a)
  return A


#Finding determinant:
def det(A):
  m = len(A)
  n = len(A[0])
  s="Matrix is not a sqaure matrix"
  if m != n:
    return s
  elif n == 1:
    return A[0][0]
  else:
    s = 0
    for i in range(n):
      s = s + A[0][i] * ((-1)**i) * det(co_fac(A, 0, i))

  return s


#Co-factor finding:


def co_fac(A, i, j):
  m = len(A)
  n = len(A[0])
  B = []
  if m==n:
    if m==1:
      return [[1]]

    else:
      for k in range(m):
        if k != i:
          a = []
          for p in range(n):
            if p != j:
              a.append(A[k][p])
          B.append(a)
      return B

  else:
    return "Matrix is not a sqaure matrix"


#Finding transposed matrix:


def trans(A):
  m = len(A)
  n = len(A[0])
  B=[] 
  for i in range(n):
    a=[]
    for j in range(m):
      a.append(A[j][i])
    B.append(a)  
  return B

#Finding inverse of a matrix:

def inv(A):
  m=len(A)
  n=len(A[0])
  d=det(A)
  if d != 0 and not isinstance(d, str): 
    if n==1:
      return[[1/A[0][0]]]
    else:
      B=[]
      for i in range(m):
        a=[]
        for j in range(n):
          x= (1/d)*((-1)**(i+j))
          a.append(x*det(co_fac(A,i,j)))
        B.append(a)

      return trans(B)

  else:
    return "Matrix is not invertible"




#matrix multiplication

def mul(A,B):
  m=len(A)
  n=len(A[0])
  p=len(B)
  q=len(B[0])
  if n==p:
    C=[]
    for i in range(m):
      a=[]
      for j in range(q):
        x=0
        for k in range(n):
          x=x+A[i][k]*B[k][j]
        a.append(x)
      C.append(a)
    return C 

  else:
    return "Matrix multiplication is not possible"
  



#solving system of equation(square system)

def sol(A,B):
  d=det(A)
  if d != 0 and not isinstance(d, str):
    return mul(inv(A),B)

  else:
    return "Unique solution may not exist"
  

