import sys

# try the operation
try:
    print( 5 / 0 )
# check any exceptions
except Exception as e:
    # handle the execption by printing it and moving on
    print('exception: ', type(e), e)

# print the string
print('but life goes on')
