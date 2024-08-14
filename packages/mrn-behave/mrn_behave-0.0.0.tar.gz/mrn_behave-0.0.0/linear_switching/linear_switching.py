import torch
from torch import nn
from torch import Tensor

class LinearSwitching(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.z_0 = nn.Parameter(torch.randn(size=(1,)))
        self._coefs = nn.Parameter(torch.ones(size=(8,)))
        self._offsets = nn.Parameter(torch.zeros(size=(8,)))
        self.inv_temp = nn.Parameter(torch.rand(size=(1,)))
    
    def forward(self, z: Tensor, obs: Tensor):
        coefs = self._coefs[obs].unsqueeze(1)
        offsets = self._offsets[obs].unsqueeze(1)
        return coefs * z + offsets
    
    @property
    def coefs(self):
        return self._coefs.detach().clone()
    
    @property
    def offsets(self):
        return self._offsets.detach().clone()