
import torch
from torch import nn
from torchvision.models import MobileNet_V2_Weights, mobilenet_v2


class Detection(nn.Module):
    def __init__(self):
        super().__init__()
        net = mobilenet_v2(weights=MobileNet_V2_Weights.DEFAULT)
        net.features[0][0] = nn.Conv2d(
            1, 32,
            kernel_size=3,
            stride=2,
            padding=1,
            bias=False)

        net.classifier = nn.Identity()  # type: ignore
        self.net = nn.Sequential(
            net,
            nn.Linear(1280, 4))

    def forward(self, x):
        return self.net(x)


def fix_state_dict(state_dict):
    return {
        k.replace('net.net', 'net'): v
        for k, v in state_dict.items()}


def load_state_dict(path_ckpt: str):
    ckpt = torch.load(path_ckpt, map_location=torch.device('cpu'))
    return fix_state_dict(ckpt['state_dict'])


def load_detection():
    detection = Detection()
    detection.load_state_dict(load_state_dict('detection.ckpt'))
    return detection.eval()
