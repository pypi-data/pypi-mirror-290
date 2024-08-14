import open_clip
import torch
import lpips

from huggingface_hub import hf_hub_download
from supersat.utils import TruncatedVGG19
from abc import ABC, abstractmethod

# Create a template for the loss functions
class super_loss(ABC, torch.nn.Module):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def forward(
        self, lr: torch.Tensor, sr: torch.Tensor, hr: torch.Tensor
    ) -> torch.Tensor:
        pass



class l1_loss(super_loss):
    def __init__(self):
        super().__init__()

    def forward(self, lr, sr, hr):
        return torch.mean(torch.abs(sr - hr))
    

class lpips_loss(super_loss):
    def __init__(
        self,
        to_true_color: bool = True,        
        rgb_bands: list = [0, 1, 2]
    ):
        super().__init__()
        self.loss_fn_alex = lpips.LPIPS(net='alex')
        self.to_true_color = to_true_color
        self.rgb_bands = rgb_bands

    def forward(self, lr, sr, hr):
        
        # Normalize the images to the range [0, 1]
        if self.to_true_color:
            sr = torch.clamp(sr * 3, 0, 1)
            hr = torch.clamp(hr * 3, 0, 1)
        
        # Normalize the images to the range [-1, 1]
        sr_1 = sr[:, self.rgb_bands] * 2 - 1
        hr_1 = hr[:, self.rgb_bands] * 2 - 1
        
        return self.loss_fn_alex(sr_1, hr_1).mean()


class opensrtest_loss(super_loss):
    def __init__(
        self,
        gradient_threshold: float = 0.50,
        ha_factor: float = 0.50,
        return_map: bool = False
    ):
        """ The opensrtest loss function

        Args:
            gradient_threshold (float, optional): The threshold
                value for the gradient. Defaults to 0.75.
            regularization_parameter (float, optional): The 
                regularization parameter. Defaults to 0.05.
            softmin_temperature (float, optional): The temperature
                for the softmin function. Defaults to 0.25.
            return_map (bool, optional): If the function should
                return the map. Defaults to False.
        """
        super().__init__()
        self.gradient_threshold = gradient_threshold
        self.ha_factor = ha_factor
        
    
    def normalized_difference(self, x: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
        """ By default, the function calculates the normalized
        difference between two tensors along the channel
        dimension. The function is defined as:        

        Args:
            x (torch.Tensor): The first tensor.
            y (torch.Tensor): The second tensor.

        Returns:
            torch.Tensor: The normalized difference between the
                two tensors.
        """
        return torch.mean(torch.abs(x - y) / (x + y), dim=1)

    def forward(
        self,
        lr: torch.Tensor,
        sr: torch.Tensor,
        hr: torch.Tensor
    ) -> torch.Tensor:
        """ The forward function calculates the opensrtest
        loss function. The function is defined as:                

        Args:
            lr (torch.Tensor): The low-resolution image.
            sr (torch.Tensor): The super-resolved image.
            hr (torch.Tensor): The high-resolution image.

        Returns:
            torch.Tensor: The opensrtest loss.
        """
        # Align the histograms of the SR and HR images
        #hr = hq_histogram_matching(hr, sr)
        
        # Generate a reference LR image
        lr_hat = torch.nn.functional.interpolate(
            input=lr,
            size=hr.shape[-2:],
            mode='bilinear',
            antialias=True
        )
        
        # Obtain the three distance metrics
        d_ref = self.normalized_difference(lr_hat, hr)
        d_om = self.normalized_difference(lr_hat, sr)
        d_im = self.normalized_difference(sr, hr)
        
        # Create a mask to filter out the gradients
        # with a magnitude below the threshold value
        gradient_threshold = d_ref.flatten().kthvalue(
                int(self.gradient_threshold * d_ref.numel())
        ).values.item()

        mask1 = (d_ref > gradient_threshold) * 1.
        mask2 = (d_im > gradient_threshold) * 1.
        mask3 = (d_om > gradient_threshold) * 1.
        mask = ((mask1 + mask2 + mask3) > 0) * 1.
        
        # Estimate the loss
        d_im_masked = torch.masked_select(d_im, mask.bool())        
        d_om_masked = torch.masked_select(d_om, mask.bool())
        ha_loss = d_im_masked + torch.exp(d_om_masked + d_im_masked - 1) * self.ha_factor
        
        return ha_loss.mean()


class clip_general_loss(super_loss):
    def __init__(
        self,
        to_true_color: bool = True,        
        rgb_bands: list = [0, 1, 2]
    ):
        super().__init__()
        self.clip_model, _, _ = open_clip.create_model_and_transforms(
            'ViT-B-16-SigLIP-256', pretrained='webli'
        )
        self.to_true_color = to_true_color
        self.rgb_bands = rgb_bands
        self.mean_norm = torch.tensor((0.48145466, 0.4578275, 0.40821073))
        self.std_norm = torch.tensor((0.26862954, 0.26130258, 0.27577711))

    def forward(self, lr, sr, hr):
        
        # Convert both images to 256x256
        sr = torch.nn.functional.interpolate(
            sr, size=(256, 256), mode='bilinear', antialias=True
        )

        hr = torch.nn.functional.interpolate(
            hr, size=(256, 256), mode='bilinear', antialias=True
        )

        # Normalize the images to the range [0, 1]
        if self.to_true_color:
            sr = torch.clamp(sr * 3, 0, 1)
            hr = torch.clamp(hr * 3, 0, 1)
        
        # Normalize the images B,C,H,W with a 1D tensor of 3 elements
        sr = (sr[:, self.rgb_bands] - self.mean_norm[None, :, None, None]) / self.std_norm[None, :, None, None]
        hr = (hr[:, self.rgb_bands] - self.mean_norm[None, :, None, None]) / self.std_norm[None, :, None, None]

        # Calculate the similarity
        emb_sr = self.clip_model.encode_image(sr)
        emb_hr = self.clip_model.encode_image(hr)
        l1_loss = torch.nn.functional.l1_loss(emb_sr, emb_hr)

        return l1_loss
    

class clip_rs_loss(super_loss):
    def __init__(
        self,
        to_true_color: bool = True,        
        rgb_bands: list = [0, 1, 2]
    ):
        super().__init__()

        hf_hub_download(
            "chendelong/RemoteCLIP", "RemoteCLIP-ViT-L-14.pt", cache_dir='checkpoints'
        )

        self.clip_model, _, _ = open_clip.create_model_and_transforms('ViT-L-14')
        self.mean_norm = torch.tensor((0.48145466, 0.4578275, 0.40821073))
        self.std_norm = torch.tensor((0.26862954, 0.26130258, 0.27577711))

        self.to_true_color = to_true_color
        self.rgb_bands = rgb_bands

    def forward(self, lr, sr, hr):
        
        # Convert both images to 256x256
        sr = torch.nn.functional.interpolate(
            sr, size=(224, 224), mode='bilinear', antialias=True
        )

        hr = torch.nn.functional.interpolate(
            hr, size=(224, 224), mode='bilinear', antialias=True
        )

        # Normalize the images to the range [0, 1]
        if self.to_true_color:
            sr = torch.clamp(sr * 3, 0, 1)
            hr = torch.clamp(hr * 3, 0, 1)
        
        # Normalize the images with the mean and standard deviation
        sr = (sr[:, self.rgb_bands] - self.mean_norm[None, :, None, None]) / self.std_norm[None, :, None, None]
        hr = (hr[:, self.rgb_bands] - self.mean_norm[None, :, None, None]) / self.std_norm[None, :, None, None]

        # Calculate the similarity
        emb_sr = self.clip_model.encode_image(sr)
        emb_hr = self.clip_model.encode_image(hr)
        l1_loss = torch.nn.functional.l1_loss(emb_sr, emb_hr)

        return l1_loss


class vgg_loss(super_loss):
    def __init__(
        self,
        to_true_color: bool = True,        
        rgb_bands: list = [0, 1, 2]
    ):
        super().__init__()
        self.vgg_loss = TruncatedVGG19(i=5, j=4)
        self.to_true_color = to_true_color
        self.rgb_bands = rgb_bands
        self.mean_norm = torch.tensor((0.485, 0.456, 0.406))
        self.std_norm = torch.tensor((0.229, 0.224, 0.225))

    def forward(self, lr, sr, hr):
        
        # Normalize the images to the range [0, 1]
        if self.to_true_color:
            sr = torch.clamp(sr * 3, 0, 1)
            hr = torch.clamp(hr * 3, 0, 1)
        
        # Normalize the images with the mean and standard deviation        
        sr_1 =  (sr[:, self.rgb_bands] - self.mean_norm[None, :, None, None]) / self.std_norm[None, :, None, None]
        hr_1 =  (hr[:, self.rgb_bands] - self.mean_norm[None, :, None, None]) / self.std_norm[None, :, None, None]
                                                                                              
        # Create the image embeddings
        emb_sr = self.vgg_loss(sr_1)
        emb_hr = self.vgg_loss(hr_1)

        return torch.nn.functional.l1_loss(emb_sr, emb_hr)