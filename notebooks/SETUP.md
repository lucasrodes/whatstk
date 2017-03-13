# SETUP

If you are using a virtual environment, follow the steps below to setup it for the Jupyter Notebook.

First be sure that you are inside the virtual environment (note that out environment is named `.whatstkenv`).

`source activate .whatstkenv`

Next, run the following command to create a kernel for the Jupyter Notebook

python3 -m ipykernel install --user --name .whatstkenv --display-name "whatstkenv"

You should now be able to select the created kernel from the Jupyter menu bar (Kernel/Change kernel)

![](files/kernelsetup.png?raw=true)
