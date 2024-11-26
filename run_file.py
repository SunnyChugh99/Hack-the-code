import os

# Print a separator for clarity.
print('*----------------------------------*')

# Access and print the 'HOME' environment variable.
try:
  print(os.environ['FDC_TEST'])
except:
  print("os.environ['FDC_TEST'] not availble")

print('*----------------------------------*')