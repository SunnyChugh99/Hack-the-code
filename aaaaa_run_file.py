import os
test

# Print a separator for clarity.
print('*----------------------------------*')

# Access and print the 'HOME' environment variable.
try:
  print(os.environ['FDC_TEST'])
except:
  print("os.environ['FDC_TEST'] not availble")

print('*RUN COMPLETE-----------------------*')


import fosforml
import sys

print(f'*Import working with - {sys.version}---------------*')
