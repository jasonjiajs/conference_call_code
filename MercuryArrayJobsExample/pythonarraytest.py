import sys

print("Hello world!")
arraynumber = sys.argv[1]
print(arraynumber)

# If you run "sbatch pythonarraytest.sh" on Mercury, with an array 1-3, then print(sys.argv) returns:
# ['pythonarraytest.py', '1'] in the first out file, 
# ['pythonarraytest.py', '2'] in the second out file, and 
# ['pythonarraytest.py', '3'] in the third out file.

# To get '1', '2', and '3', use print(sys.argv[1]).
