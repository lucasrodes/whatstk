
If you are using a virtual environment, follow the steps below to setup it for the Jupyter Notebook.

### Enter your virtual environment

`. ../.whatstkenv/bin/activate`

### Install IPykernel

`pip3 install ipykernel`

### Create an IPython kernel

Next, run the following command to create a kernel in order to use our virtual environment in the Jupyter Notebook

`python3 -m ipykernel install --user --name .whatstkenv --display-name "whatstkenv"`

### Run Jupyter and choose your kernel

You should now be able to select the created kernel from the Jupyter menu bar (Kernel/Change kernel, see picture below).

`jupyter notebook`

![](files/kernelsetup.png?raw=true)
