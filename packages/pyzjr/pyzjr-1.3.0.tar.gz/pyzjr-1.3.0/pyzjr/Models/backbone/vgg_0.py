"""
论文原址： <https://arxiv.org/pdf/1409.1556v6.pdf>
VERY DEEP CONVOLUTIONAL NETWORKS FOR LARGE-SCALE IMAGE RECOGNITION
VGG16/VGG19 bn
Obtained from torchvision.models.vgg
"""
import torch
import torch.nn as nn

__all__ = ["vgg19_bn", "vgg16_bn"]

cfg = {
    'A' : [64, 64, 'M', 128, 128, 'M', 256, 256, 256,      'M', 512, 512, 512,      'M', 512, 512, 512,      'M'],
    'B' : [64, 64, 'M', 128, 128, 'M', 256, 256, 256, 256, 'M', 512, 512, 512, 512, 'M', 512, 512, 512, 512, 'M']
}

class VGG(nn.Module):
    def __init__(self, features, num_classes=1000, init_weights=True):
        super(VGG, self).__init__()
        self.features = features
        self.avgpool = nn.AdaptiveAvgPool2d((7, 7))
        self.classifier = nn.Sequential(
            nn.Linear(512 * 7 * 7, 4096),
            nn.ReLU(True),
            nn.Dropout(),
            nn.Linear(4096, 4096),
            nn.ReLU(True),
            nn.Dropout(),
            nn.Linear(4096, num_classes),
        )
        if init_weights:
            self._initialize_weights()

    def forward(self, x):
        x = self.features(x)
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x

    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.Linear):
                nn.init.normal_(m.weight, 0, 0.01)
                nn.init.constant_(m.bias, 0)

def make_layers(cfg, batch_norm=False):
    layers = []
    in_channels = 3
    for v in cfg:
        if v == 'M':
            layers += [nn.MaxPool2d(kernel_size=2, stride=2)]
        else:
            conv2d = nn.Conv2d(in_channels, v, kernel_size=3, padding=1)
            if batch_norm:
                layers += [conv2d, nn.BatchNorm2d(v), nn.ReLU(inplace=True)]
            else:
                layers += [conv2d, nn.ReLU(inplace=True)]
            in_channels = v
    return nn.Sequential(*layers)


def vgg16_bn(num_classes):
    model = VGG(make_layers(cfg['A'], batch_norm=True), num_classes=num_classes)
    return model

def vgg19_bn(num_classes):
    model = VGG(make_layers(cfg['B'], batch_norm=True), num_classes=num_classes)
    return model


if __name__=='__main__':
    import torchsummary
    input = torch.ones(2, 3, 224, 224).cpu()
    net = vgg16_bn(num_classes=4)
    net = net.cpu()
    out = net(input)
    print(out)
    print(out.shape)
    torchsummary.summary(net, input_size=(3, 224, 224))
    # Total params: 134,285,380

""" vgg16:
---------------------------------------------
Layer (type)               Output Shape
=============================================
Conv2d-1                  [-1, 64, 244, 244]
BatchNorm2d-2             [-1, 64, 244, 244]
ReLU-3                    [-1, 64, 244, 244]
Conv2d-4                  [-1, 64, 244, 244]
BatchNorm2d-5             [-1, 64, 244, 244]
ReLU-6                    [-1, 64, 244, 244]
MaxPool2d-7               [-1, 64, 122, 122]
Conv2d-8                  [-1, 128, 122, 122]
BatchNorm2d-9             [-1, 128, 122, 122]
ReLU-10                   [-1, 128, 122, 122]
Conv2d-11                 [-1, 128, 122, 122]
BatchNorm2d-12            [-1, 128, 122, 122]
ReLU-13                   [-1, 128, 122, 122]
MaxPool2d-14              [-1, 128, 61, 61]
Conv2d-15                 [-1, 256, 61, 61]
BatchNorm2d-16            [-1, 256, 61, 61]
ReLU-17                   [-1, 256, 61, 61]
Conv2d-18                 [-1, 256, 61, 61]
BatchNorm2d-19            [-1, 256, 61, 61]
ReLU-20                   [-1, 256, 61, 61]
Conv2d-21                 [-1, 256, 61, 61]
BatchNorm2d-22            [-1, 256, 61, 61]
ReLU-23                   [-1, 256, 61, 61]
MaxPool2d-24              [-1, 256, 30, 30]
Conv2d-25                 [-1, 512, 30, 30]
BatchNorm2d-26            [-1, 512, 30, 30]
ReLU-27                   [-1, 512, 30, 30]
Conv2d-28                 [-1, 512, 30, 30]
BatchNorm2d-29            [-1, 512, 30, 30]
ReLU-30                   [-1, 512, 30, 30]
Conv2d-31                 [-1, 512, 30, 30]
BatchNorm2d-32            [-1, 512, 30, 30]
ReLU-33                   [-1, 512, 30, 30]
MaxPool2d-34              [-1, 512, 15, 15]
Conv2d-35                 [-1, 512, 15, 15]
BatchNorm2d-36            [-1, 512, 15, 15]
ReLU-37                   [-1, 512, 15, 15]
Conv2d-38                 [-1, 512, 15, 15]
BatchNorm2d-39            [-1, 512, 15, 15]
ReLU-40                   [-1, 512, 15, 15]
Conv2d-41                 [-1, 512, 15, 15]
BatchNorm2d-42            [-1, 512, 15, 15]
ReLU-43                   [-1, 512, 15, 15]
MaxPool2d-44              [-1, 512, 7, 7]
AdaptiveAvgPool2d-45      [-1, 512, 7, 7]
Linear-46                 [-1, 4]
=============================================
"""