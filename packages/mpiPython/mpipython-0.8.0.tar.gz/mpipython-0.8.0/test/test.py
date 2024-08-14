from mpiPython import MPIpy
MPI = MPIpy()

rank = MPI.rank()
size = MPI.size()

print("Hello from process {} out of {}".format(rank, size))