import torch
import torch.nn as nn
from torchvision.models.resnet import BasicBlock


class ResNet18(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=1, padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=1, padding=1)
        self.layer1 = nn.Sequential(
            BasicBlock(64, 64, 1, None, 1, 64, 1, nn.BatchNorm2d),
            BasicBlock(64, 64, 1, None, 1, 64, 1, nn.BatchNorm2d),
        )

        downsample_layer2 = nn.Sequential(
            nn.Conv2d(64, 128, (1, 1), (2, 2), bias=False),
            nn.BatchNorm2d(128)
        )
        self.layer2 = nn.Sequential(
            BasicBlock(64, 128, 2, downsample_layer2, 1, 64, 1, nn.BatchNorm2d),
            BasicBlock(128, 128, 1, None, 1, 64, 1, nn.BatchNorm2d)
        )

        downsample_layer3 = nn.Sequential(
            nn.Conv2d(128, 256, (1, 1), (2, 2), bias=False),
            nn.BatchNorm2d(256)
        )
        self.layer3 = nn.Sequential(
            BasicBlock(128, 256, 2, downsample_layer3, 1, 64, 1, nn.BatchNorm2d),
            BasicBlock(256, 256, 1, None, 1, 64, 1, nn.BatchNorm2d)
        )

        downsample_layer4 = nn.Sequential(
            nn.Conv2d(256, 512, (1, 1), (2, 2), bias=False),
            nn.BatchNorm2d(512)
        )
        self.layer4 = nn.Sequential(
            BasicBlock(256, 512, 2, downsample_layer4, 1, 64, 1, nn.BatchNorm2d),
            BasicBlock(512, 512, 1, None, 1, 64, 1, nn.BatchNorm2d)
        )
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512, 200)

    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.fc(x)

        return x
