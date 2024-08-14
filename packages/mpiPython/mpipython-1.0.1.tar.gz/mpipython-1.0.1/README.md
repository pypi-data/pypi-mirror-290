## Installing and Using mpiPython on Debian-based Systems

### Overview
This guide outlines the steps to install and use mpiPython on Debian-based systems.

### Prerequisites
* **Debian-based system** (e.g., Ubuntu, Debian)
* **`build-essential`** package installed (provides necessary compilers and tools)
* **'mpich'** the program is made to work with this, you can either have it installed by package manager or custom compiled with '--enable-shared'
* **Python 3.10 to 3.12**

### Installation Steps
1. **Install required packages:**
   ```bash
   sudo apt install build-essential mpich
   ```
2. **Install mpiPython:**
   ```bash
   pip install mpiPython
   ```

### Explanation
* **`build-essential`**: Provides necessary tools like the C compiler for building mpiPython.
* **`pip install mpiPython`**: Installs the mpiPython package.

### Additional Notes
* **MPICH Installation:** Ensure that MPICH is installed with the `--enable-shared` flag during compilation. This is crucial for mpiPython to function correctly.
* **Python Version:** This guide assumes Python 3.10 to 3.12. Adjust commands accordingly if using a different Python version.
* **Error Handling:** If you encounter errors, check the logs or output of the commands for more details.
* **Virtual Environments:** Consider using virtual environments to isolate Python environments and avoid conflicts.

### Using mpiPython
Once installed, you can import and use mpiPython in your Python scripts:

```python
from mpiPython import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print("Hello from process {} out of {}".format(rank, size))
```

By following these steps, you should have a working mpiPython environment on your Debian-based system.
 
**Would you like to know more about specific use cases or troubleshooting mpiPython?**
