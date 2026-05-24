import torch
import torch.nn as nn
import torchvision.models as models
from torchvision.models import mobilenet_v2, MobileNet_V2_Weights


class VideoModel(nn.Module):
    def __init__(self):
        super().__init__()

        base = mobilenet_v2(weights=MobileNet_V2_Weights.DEFAULT)
        self.cnn = base.features

        self.pool = nn.AdaptiveAvgPool2d((1, 1))

        self.lstm = nn.LSTM(1280, 64, batch_first=True)

        self.fc = nn.Linear(64, 2)

    def forward(self, x):
        B, T, C, H, W = x.shape

        x = x.view(B*T, C, H, W)
        feat = self.cnn(x)
        feat = self.pool(feat).view(B, T, -1)

        out, _ = self.lstm(feat)
        out = out[:, -1, :]

        return self.fc(out)
    