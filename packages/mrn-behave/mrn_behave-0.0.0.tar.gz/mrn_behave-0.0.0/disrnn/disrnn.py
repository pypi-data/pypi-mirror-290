import torch
import torch.distributions as dist
from torch import nn
from torch import Tensor

class MLP(nn.Module):
    def __init__(self,
                 input_size: int,
                 output_size: int,
                 hidden_size: list[int],
                 act: nn.Module=nn.ReLU) -> None:
        super(MLP, self).__init__()
        layers = []
        _prev_dim = input_size
        for hidden in hidden_size:
            layers.append(nn.Linear(_prev_dim, hidden))
            layers.append(act())
            _prev_dim = hidden
        layers.append(nn.Linear(_prev_dim, output_size))
        self.mlp = nn.Sequential(*layers)
        
            
    def forward(self, x: Tensor) -> Tensor:
        x_hat = self.mlp(x)
        return x_hat


class Bottleneck(nn.Module):
    def __init__(self) -> None:
        super().__init__()

    def compute_kld(self, mean: Tensor, var: Tensor, log_var: Tensor) -> Tensor:
        return -0.5 * torch.sum(1 + log_var - (mean ** 2) - var, dim=-1)
    
    def forward(self, x: Tensor, log_var: Tensor, multiplier: Tensor) -> Tensor:
        var = log_var.exp()
        std = var.sqrt()
        mean = torch.mul(multiplier, x)
        kld = self.compute_kld(mean, var, log_var)
        
        x_tilde = torch.randn_like(x) * std + mean

        return x_tilde, kld


class UpdateMLPs(nn.Module):
    def __init__(self, num_latents: int, in_size: int, hidden_size: list[int]) -> None:
        super().__init__()

        self.update_mlps = nn.ModuleList([MLP(in_size, 2, hidden_size) for mlp in range(num_latents)])
    
    def forward(self, x: Tensor, old_latents: Tensor):
        
        B, D, Z = x.size()

        new_latents = torch.zeros(size=(B, Z))
        for mlp_idx, mlp in enumerate(self.update_mlps):
            mlp_output = mlp(x[:, :, mlp_idx])
            u, w = mlp_output[:, 0], mlp_output[:, 1].sigmoid()
            z = old_latents[:, mlp_idx]
            new_latents[:, mlp_idx] = (1 - w) * z + u * w
        
        return new_latents


class DisRNN(nn.Module):
    def __init__(
            self,
            num_latents: int,
            num_obs: int,
            include_stimulus: bool,
            update_mlp_hidden_size: list[int],
            choice_mlp_hidden_size: list[int]
        ) -> None:
        super().__init__()

        self.update_mlp_in_size = num_latents + num_obs
        self.num_latents = num_latents

        self.z_0 = nn.Parameter(torch.randn(size=(num_latents,)))
        self.update_bottleneck_multiplier = nn.Parameter(torch.ones(size=(self.update_mlp_in_size, num_latents)))
        self.update_bottleneck_log_var = nn.Parameter(dist.Uniform(-3, -2).sample((self.update_mlp_in_size, num_latents)))
        self.global_bottleneck_multiplier = nn.Parameter(torch.ones(size=[num_latents]))
        self.global_bottleneck_log_var = nn.Parameter(dist.Uniform(-3, -2).sample([num_latents]))

        self.global_bottleneck = Bottleneck()
        self.update_bottleneck = nn.ModuleList([Bottleneck() for latent in range(num_latents)])
        self.update_mlp = UpdateMLPs(num_latents, self.update_mlp_in_size, update_mlp_hidden_size)

        if include_stimulus:
            self.choice_mlp = MLP(num_latents + 1, 2, choice_mlp_hidden_size)
        else:
            self.choice_mlp = MLP(num_latents, 2, choice_mlp_hidden_size)

    
    def forward(self, latents: Tensor, obs: Tensor, t_0: bool, s_t: Tensor=None):

        B, _ = latents.size()

        if t_0:
            latents = torch.expand_copy(self.z_0, (B, self.num_latents))
        x = torch.cat([latents, obs], dim=-1)

        update_mlp_inputs = torch.zeros(size=(B, self.update_mlp_in_size, self.num_latents))
        update_kld = torch.zeros(size=(B, self.num_latents))
        for idx, update_bottleneck in enumerate(self.update_bottleneck):
            x_tilde, kld = update_bottleneck(x, self.update_bottleneck_log_var[:, idx], self.update_bottleneck_multiplier[:, idx])
            update_mlp_inputs[:, :, idx] = x_tilde
            update_kld[:, idx] = kld

        new_latents = self.update_mlp(update_mlp_inputs, latents)
        z_tilde, global_kld = self.global_bottleneck(new_latents, self.global_bottleneck_log_var, self.global_bottleneck_multiplier)
        if s_t is not None:
            choice_mlp_input = torch.cat((z_tilde, s_t), dim=-1)
            y = self.choice_mlp(choice_mlp_input)
        else:
            y = self.choice_mlp(z_tilde)

        return y, z_tilde, global_kld, update_kld
    

    def forward_w_dropout(self, latents: Tensor, obs: Tensor, t_0: bool, global_threshold: float, update_threshold: float, s_t: Tensor=None):

        open_update_latents = (self.update_bottleneck_log_var.exp() <= update_threshold).int()
        
        open_global_latents = (self.global_bottleneck_log_var.exp() <= global_threshold).int()


        B, _ = latents.size()

        if t_0:
            latents = torch.expand_copy(self.z_0, (B, self.num_latents))
        x = torch.cat([latents, obs], dim=-1)

        update_mlp_inputs = torch.expand_copy(x.unsqueeze(-1), (B, self.update_mlp_in_size, self.num_latents))
        update_mlp_inputs *= open_update_latents

        new_latents = self.update_mlp(update_mlp_inputs, latents)
        new_latents *= open_global_latents

        if s_t is not None:
            choice_mlp_input = torch.cat((new_latents, s_t), dim=-1)
            y = self.choice_mlp(choice_mlp_input)
        else:
            y = self.choice_mlp(new_latents)

        return y, new_latents

    

    @property
    def update_sigmas(self):
        return torch.exp(self.update_bottleneck_log_var.clone().detach())
    @property
    def update_multipliers(self):
        return self.update_bottleneck_multiplier.clone().detach()

    @property
    def global_sigmas(self):
        return torch.exp(self.global_bottleneck_log_var.clone().detach())
    
    @property
    def global_multipliers(self):
        return self.global_bottleneck_multiplier.clone().detach()