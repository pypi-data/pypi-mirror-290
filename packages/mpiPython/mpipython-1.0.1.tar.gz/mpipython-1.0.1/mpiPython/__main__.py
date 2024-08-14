"""
File: __main__.py
Modification Date: 8/12/24
Time Modified: 1:37pm CT
Created by: Judah Nava
Last Modified By: Judah Nava
Organization: Parallel Solvit LLC and MSUM CSIS Department
"""
import os, subprocess, sys

def find_mpich_arg(argv: list[str]):
    for i, arg in enumerate(argv):
        if arg.find("mpich=") != -1:
            return i
    return None


# This is getting the libcode file directory
cache = __file__[:]
callingDirectory = os.getcwd()
if cache.find("__main__.py") == -1:
    print(cache)
    print("Issue")
    exit(-1)
cache = cache.replace("__main__.py", "lib/libcode.c")

if cache.find("__main__.py") != -1:
    exit(-1)

# this pulls the bin directory for mpich
index = find_mpich_arg(sys.argv)
if index is not None:
    mpich_value = sys.argv[index].split('=')[1]
else:
    print("Issue3")
    exit(-1)


try:
    subprocess.run([mpich_value+"mpicc", cache, "-shared", "-fPIC", "-o",callingDirectory+"/libcode.so"])
    print("sucess")
except PermissionError as e:
    print("Does not have permission to access "+mpich_value+", please use sudo or root call")