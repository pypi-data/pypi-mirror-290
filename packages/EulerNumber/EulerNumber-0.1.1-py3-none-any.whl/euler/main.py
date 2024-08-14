def factorial(n):
  result = 1
  for i in range(1, n + 1):
      result *= i
  return result

def euler(x):
  e=1
  for j in range(1, x):
    e=e+1/factorial(j)
  return e
