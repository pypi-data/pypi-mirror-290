# SNOWSHEWS: Supernova NeutrinO SHockwave Effects With SNEWPY

![image](https://github.com/SNEWS2/SNOSHEWS/assets/44247426/b7afb17b-b242-404e-ba54-d6a0fd447257)
Image by dreamstudio.ai

## Installation Instructions

1) You will need the packages `python-devel` (in Linux), [pybind11](https://pypi.org/project/pybind11/) and [setuptools](https://pypi.org/project/setuptools/)

2) Modify `setup.py` to use the correct libraries and paths. 

3) To compile enter 
```
sudo python3 setup.py install
````

4) If you don't want to sudo you may want to use the option
```
--install-lib=destination/directory/
```

## Troubleshooting:

6) You may have to set the `PYTHONPATH` environment variable to your PWD
   and/or wherever the `SNOSHEWS` module was installed

7) If the script cannot find the module you may need to put the *.so library in the same directory
   as your script. The *.so library is in one of the subfolders in the build directory. 

8) `SNOSHEWS` uses [OpenMP](https://www.openmp.org/). You may want to set the `OMP_NUM_THREADS` environment variable to a reasonable number for your machine. 


