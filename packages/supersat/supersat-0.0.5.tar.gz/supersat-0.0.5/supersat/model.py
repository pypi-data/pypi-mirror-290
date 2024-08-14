import torch
from typing import Union, Tuple, Optional
from supersat.utils import sequential, activation_fn


def conv_layer(
    in_channels: int,
    out_channels: int,
    kernel_size: Union[int, Tuple[int, int]]
) -> torch.nn.Conv2d:
    """
    Create a 2D convolutional layer with adaptive padding.
    
    Args:
        in_channels (int): Number of input channels.
        out_channels (int): Number of output channels.
        kernel_size (Union[int, Tuple[int, int]]): Size of the convolution kernel.
        bias (bool): Whether to include a bias term. Default is True.
        
    Returns:
        nn.Conv2d: A 2D convolutional layer with the specified parameters.
    """
    
    if isinstance(kernel_size, int):
        kernel_size = (kernel_size, kernel_size)
    
    padding = (kernel_size[0] // 2, kernel_size[1] // 2)

    return torch.nn.Conv2d(
        in_channels=in_channels,
        out_channels=out_channels,
        kernel_size=kernel_size,
        padding=padding
    )


def pixelshuffle_block(
    in_channels: int,
    out_channels: int,
    upscale_factor: int = 2,
    kernel_size: int = 3
) -> torch.nn.Sequential:
    """Create a pixel shuffle block to upsample features according 
    to `upscale_factor`.
    
    This block consists of a convolutional layer followed by a pixel 
    shuffle operation, which rearranges elements in a tensor to 
    upscale the spatial resolution.
    

    Args:
        in_channels (int): Number of input channels.
        out_channels (int): Number of output channels.
        upscale_factor (int, optional): Factor by which to upscale the 
            spatial resolution. Default is 2.
        kernel_size (int, optional): Size of the convolution 
            kernel. Default is 3.

    Returns:
        torch.nn.Sequential: A Sequential container with a convolutional 
            layer followed by a pixel shuffle operation.
    """
    # Create a convolutional layer with adaptive padding
    conv = conv_layer(
        in_channels=in_channels,
        out_channels=out_channels * (upscale_factor ** 2),
        kernel_size=kernel_size
    )
    
    # Create a pixel shuffle layer to upscale the spatial resolution
    pixel_shuffle = torch.nn.PixelShuffle(upscale_factor)

    # Return a Sequential container with the convolutional and pixel shuffle layers
    return sequential(conv, pixel_shuffle)


class Conv3XC(torch.nn.Module):
    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        width: int = 3,
        gain: int = 1
    ):
        """
        Initialize the Conv3XC module.

        Args:
            in_channels (int): Number of input channels.
            out_channels (int): Number of output channels.
            gain (int): Gain factor for the first convolution. Default is 1.
            stride (int): Stride of the convolution. Default is 1.
            bias (bool): Whether to include a bias term in the
                convolution layers. Default is True.
            relu (bool): Whether to apply a Leaky ReLU activation
                function. Default is False.
        """
        super(Conv3XC, self).__init__()
        self.weight_concat = None
        self.bias_concat = None
        self.update_params_flag = False
        self.kernel_size = width

        # Define the shortcut convolution layer
        self.sk = torch.nn.Conv2d(
            in_channels=in_channels,
            out_channels=out_channels,
            kernel_size=1
        )
        
        # Define the main sequence of convolution layers
        self.conv = torch.nn.Sequential(
            torch.nn.Conv2d(
                in_channels=in_channels, 
                out_channels=in_channels * gain, 
                kernel_size=1
            ),
            torch.nn.Conv2d(
                in_channels=in_channels * gain,
                out_channels=out_channels * gain,
                kernel_size=width
            ),
            torch.nn.Conv2d(
                in_channels=out_channels * gain,
                out_channels=out_channels,
                kernel_size=1
            ),
        )


    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass through the Conv3XC module.

        Args:
            x (torch.Tensor): Input tensor.

        Returns:
            torch.Tensor: Output tensor.
        """

        # Pad x according to the width of the convolution
        to_pad = (self.kernel_size - 1) / 2

        # if the width is not odd return error
        if to_pad % 1 != 0:
            raise ValueError(
                "The width of the convolution must be an odd number."
            )
        to_pad = int(to_pad)
        x_pad = torch.nn.functional.pad(x, (to_pad, to_pad, to_pad, to_pad))
        out = self.conv(x_pad) + self.sk(x)    
        return out


class SPAB(torch.nn.Module):
    def __init__(
        self,
        in_channels: int,
        mid_channels: Optional[int] = None,
        out_channels: Optional[int] = None,
        width: int = 3,
        activation: Optional[str] = 'silu'
    ) -> torch.nn.Module:
        """ Initialize the SPAB module.

        Args:
            in_channels (int): Number of input channels.
            mid_channels (Optional[int], optional): Number of intermediate channels.
                If not specified, defaults to `in_channels`.
            out_channels (Optional[int], optional): Number of output channels.
                If not specified, defaults to `in_channels`.
            bias (bool, optional): Whether to include a bias term in the
                convolution layers. Default is False.
        
        Returns:
            torch.nn.Module: The SPAB module.
        """

        super(SPAB, self).__init__()
        mid_channels = mid_channels or in_channels
        out_channels = out_channels or in_channels

        self.in_channels = in_channels

        # Define convolutional layers with Conv3XC
        self.c1_r = Conv3XC(in_channels, mid_channels, gain=2, width=width)
        self.c2_r = Conv3XC(mid_channels, mid_channels, gain=2, width=width)
        self.c3_r = Conv3XC(mid_channels, out_channels, gain=2, width=width)

        # Define activation functions
        self.act1 = activation_fn(activation)

    def forward(self, x):
        """ The forward pass of the SPAB module.

        Args:
            x (torch.Tensor): Input tensor. It has shape (batch_size, in_channels, height, width).            

        Returns:
            torch.Tensor: Output tensor after applying attention mechanism.
        """

        # First convolution and activation
        out1 = self.c1_r(x)
        out1_act = self.act1(out1)

        # Second convolution and activation
        out2 = self.c2_r(out1_act)
        out2_act = self.act1(out2)

        # Third convolution
        out3 = self.c3_r(out2_act)

        # Compute similarity attention
        sim_att = torch.sigmoid(out3) - 0.5

        # Apply attention mechanism
        out = (out3 + x) * sim_att

        return out, out1, sim_att


class SuperSat(torch.nn.Module):
    """
    Swift Parameter-free Attention Network for Efficient Super-Resolution
    """

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        upscale: Optional[int] = 4,
        feature_channels: Optional[int] = 48,
        depth: Optional[int] = 6,
        width: Optional[int] = 3,
        activation: Optional[str] = 'silu'
    ):
        super(SuperSat, self).__init__()
        
        self.conv_1 = Conv3XC(
            in_channels=in_channels, out_channels=feature_channels, width=width
        )
        self.blocks = torch.nn.ModuleList([

            SPAB(feature_channels, width=width, activation=activation) for _ in range(depth)
        ])

        self.conv_2 = Conv3XC(feature_channels, feature_channels, gain=2, width=width)        
        self.conv_cat = conv_layer(feature_channels * (depth + 2), feature_channels, kernel_size=1)
        self.upsampler = pixelshuffle_block(feature_channels, out_channels, upscale_factor=upscale)

    def forward(self, x: torch.Tensor, save_attention_maps: bool = False) -> torch.Tensor:
        """ The forward pass of the SPAN module

        Args:
            x (torch.Tensor): Input tensor. It has shape 
                (batch_size, in_channels, height, width).
            save_attention_maps (bool, optional): Whether to save
                intermediate features. Default is False.

        Returns:
            torch.Tensor: Output tensor after applying the SPAN model.
        """
                
        out_feature = self.conv_1(x)        
        out_b = out_feature
        attention_maps = []
        intermediate_features = []

        # Apply the SPAB blocks
        for block in self.blocks:
            out_b, intermediate_feature, attention_map = block(out_b)
            intermediate_features.append(intermediate_feature)
            if save_attention_maps:
                attention_maps.append(attention_map)

        # Concatenate the features and apply the final convolution
        out_b = self.conv_2(out_b)
        concat_features = torch.cat([out_feature, out_b] + intermediate_features, dim=1)
        out = self.conv_cat(concat_features)
        output = self.upsampler(out)
        
        if save_attention_maps:
            return output, attention_maps

        return output