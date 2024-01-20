# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/06_data.transforms.ipynb.

# %% auto 0
__all__ = ['ListToTensor']

# %% ../../nbs/06_data.transforms.ipynb 2
from fastai.torch_basics import *
from fastai.data.core import *
from fastai.data.load import *
from fastai.data.all import *

# %% ../../nbs/06_data.transforms.ipynb 5
class ListToTensor(DisplayedTransform):
    def encodes(self, x): return tensor(x).long()
    def decodes(self, x): return L(x, use_list=True)
