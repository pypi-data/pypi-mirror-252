"""
论文原址： <https://arxiv.org/pdf/1512.03385.pdf>
Deep Residual Learning for Image Recognition
resnet50, resnet101, resnet152
Obtained from torchvision.models.resnet
"""
import torch
import torch.nn as nn

__all__ = ['resnet18', 'resnet34', 'resnet50', 'resnet101', 'resnet152']

def conv3x3(in_planes, out_planes, stride=1, groups=1, dilation=1):
    """3x3 convolution with padding"""
    return nn.Conv2d(in_planes, out_planes, kernel_size=3, stride=stride,
                     padding=dilation, groups=groups, bias=False, dilation=dilation)

def conv1x1(in_planes, out_planes, stride=1):
    """1x1 convolution"""
    return nn.Conv2d(in_planes, out_planes, kernel_size=1, stride=stride, bias=False)


class BasicBlock(nn.Module):
    def __init__(self, inplanes, planes, stride=1, downsample=None, groups=1,
                 base_width=64, dilation=1, norm_layer=None):
        super(BasicBlock, self).__init__()
        if norm_layer is None:
            norm_layer = nn.BatchNorm2d
        if groups != 1 or base_width != 64:
            raise ValueError('BasicBlock only supports groups=1 and base_width=64')
        if dilation > 1:
            raise NotImplementedError("Dilation > 1 not supported in BasicBlock")
        # Both self.conv1 and self.downsample layers downsample the input when stride != 1
        self.conv1 = conv3x3(inplanes, planes, stride)
        self.bn1 = norm_layer(planes)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = conv3x3(planes, planes)
        self.bn2 = norm_layer(planes)
        self.downsample = downsample
        self.stride = stride

    def forward(self, x):
        identity = x

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)

        if self.downsample is not None:
            identity = self.downsample(x)

        out += identity
        out = self.relu(out)

        return out

class Bottleneck(nn.Module):
    # Bottleneck in torchvision places the stride for downsampling at 3x3 convolution(self.conv2)
    # while original implementation places the stride at the first 1x1 convolution(self.conv1)
    # according to "Deep residual learning for image recognition"https://arxiv.org/abs/1512.03385.
    # This variant is also known as ResNet V1.5 and improves accuracy according to
    # https://ngc.nvidia.com/catalog/model-scripts/nvidia:resnet_50_v1_5_for_pytorch.

    expansion = 4

    def __init__(self, inplanes, planes, stride=1, downsample=None, groups=1,
                 base_width=64, dilation=1, norm_layer=None):
        super(Bottleneck, self).__init__()
        if norm_layer is None:
            norm_layer = nn.BatchNorm2d
        width = int(planes * (base_width / 64.)) * groups
        # Both self.conv2 and self.downsample layers downsample the input when stride != 1
        self.conv1 = conv1x1(inplanes, width)
        self.bn1 = norm_layer(width)
        self.conv2 = conv3x3(width, width, stride, groups, dilation)
        self.bn2 = norm_layer(width)
        self.conv3 = conv1x1(width, planes * self.expansion)
        self.bn3 = norm_layer(planes * self.expansion)
        self.relu = nn.ReLU(inplace=True)
        self.downsample = downsample
        self.stride = stride

    def forward(self, x):
        identity = x

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu(out)

        out = self.conv3(out)
        out = self.bn3(out)

        if self.downsample is not None:
            identity = self.downsample(x)

        out += identity
        out = self.relu(out)

        return out


class ResNet(nn.Module):
    def __init__(self, block, layers, num_classes=1000, zero_init_residual=False,
                 groups=1, width_per_group=64, replace_stride_with_dilation=None,
                 norm_layer=None):
        super(ResNet, self).__init__()
        if norm_layer is None:
            norm_layer = nn.BatchNorm2d
        self._norm_layer = norm_layer

        self.inplanes = 64
        self.dilation = 1
        if replace_stride_with_dilation is None:
            # each element in the tuple indicates if we should replace
            # the 2x2 stride with a dilated convolution instead
            replace_stride_with_dilation = [False, False, False]
        if len(replace_stride_with_dilation) != 3:
            raise ValueError("replace_stride_with_dilation should be None "
                             "or a 3-element tuple, got {}".format(replace_stride_with_dilation))
        self.groups = groups
        self.base_width = width_per_group
        self.conv1 = nn.Conv2d(3, self.inplanes, kernel_size=7, stride=2, padding=3,
                               bias=False)
        self.bn1 = norm_layer(self.inplanes)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
        self.layer1 = self._make_layer(block, 64, layers[0])
        self.layer2 = self._make_layer(block, 128, layers[1], stride=2,
                                       dilate=replace_stride_with_dilation[0])
        self.layer3 = self._make_layer(block, 256, layers[2], stride=2,
                                       dilate=replace_stride_with_dilation[1])
        self.layer4 = self._make_layer(block, 512, layers[3], stride=2,
                                       dilate=replace_stride_with_dilation[2])
        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512 * block.expansion, num_classes)

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
            elif isinstance(m, (nn.BatchNorm2d, nn.GroupNorm)):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)

        # Zero-initialize the last BN in each residual branch,
        # so that the residual branch starts with zeros, and each residual block behaves like an identity.
        # This improves the model by 0.2~0.3% according to https://arxiv.org/abs/1706.02677
        if zero_init_residual:
            for m in self.modules():
                if isinstance(m, Bottleneck):
                    nn.init.constant_(m.bn3.weight, 0)
                elif isinstance(m, BasicBlock):
                    nn.init.constant_(m.bn2.weight, 0)

    def _make_layer(self, block, planes, blocks, stride=1, dilate=False):
        norm_layer = self._norm_layer
        downsample = None
        previous_dilation = self.dilation
        if dilate:
            self.dilation *= stride
            stride = 1
        if stride != 1 or self.inplanes != planes * block.expansion:
            downsample = nn.Sequential(
                conv1x1(self.inplanes, planes * block.expansion, stride),
                norm_layer(planes * block.expansion),
            )

        layers = []
        layers.append(block(self.inplanes, planes, stride, downsample, self.groups,
                            self.base_width, previous_dilation, norm_layer))
        self.inplanes = planes * block.expansion
        for _ in range(1, blocks):
            layers.append(block(self.inplanes, planes, groups=self.groups,
                                base_width=self.base_width, dilation=self.dilation,
                                norm_layer=norm_layer))

        return nn.Sequential(*layers)

    def _forward_impl(self, x):
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

    def forward(self, x):
        return self._forward_impl(x)

def resnet18(num_classes, **kwargs):
    return ResNet(BasicBlock, [2, 2, 2, 2], num_classes=num_classes, **kwargs)

def resnet34(num_classes, **kwargs):
    return ResNet(BasicBlock, [3, 4, 6, 3], num_classes=num_classes, **kwargs)

def resnet50(num_classes, **kwargs):
    return ResNet(Bottleneck, [3, 4, 6, 3], num_classes=num_classes, **kwargs)

def resnet101(num_classes, **kwargs):
    return ResNet(Bottleneck, [3, 4, 23, 3], num_classes=num_classes, **kwargs)

def resnet152(num_classes, **kwargs):
    return ResNet(Bottleneck, [3, 8, 36, 3], num_classes=num_classes, **kwargs)

if __name__=="__main__":
    import torchsummary
    input = torch.ones(2, 3, 224, 224).cpu()
    net = resnet50(num_classes=4)
    net = net.cpu()
    out = net(input)
    print(out)
    print(out.shape)
    torchsummary.summary(net, input_size=(3, 224, 224))
    # Total params: 23,516,228

""" resnet50:
--------------------------------------------
Layer (type)               Output Shape
============================================
Conv2d-1                  [-1, 64, 112, 112]
BatchNorm2d-2             [-1, 64, 112, 112]
ReLU-3                    [-1, 64, 112, 112]
MaxPool2d-4               [-1, 64, 56, 56]
Conv2d-5                  [-1, 64, 56, 56]
BatchNorm2d-6             [-1, 64, 56, 56]
ReLU-7                    [-1, 64, 56, 56]
Conv2d-8                  [-1, 64, 56, 56]
BatchNorm2d-9             [-1, 64, 56, 56]
ReLU-10                   [-1, 64, 56, 56]
Conv2d-11                 [-1, 256, 56, 56]
BatchNorm2d-12            [-1, 256, 56, 56]
Conv2d-13                 [-1, 256, 56, 56]
BatchNorm2d-14            [-1, 256, 56, 56]
ReLU-15                   [-1, 256, 56, 56]
Bottleneck-16             [-1, 256, 56, 56]
Conv2d-17                 [-1, 64, 56, 56]
BatchNorm2d-18            [-1, 64, 56, 56]
ReLU-19                   [-1, 64, 56, 56]
Conv2d-20                 [-1, 64, 56, 56]
BatchNorm2d-21            [-1, 64, 56, 56]
ReLU-22                   [-1, 64, 56, 56]
Conv2d-23                 [-1, 256, 56, 56]
BatchNorm2d-24            [-1, 256, 56, 56]
ReLU-25                   [-1, 256, 56, 56]
Bottleneck-26             [-1, 256, 56, 56]
Conv2d-27                 [-1, 64, 56, 56]
BatchNorm2d-28            [-1, 64, 56, 56]
ReLU-29                   [-1, 64, 56, 56]
Conv2d-30                 [-1, 64, 56, 56]
BatchNorm2d-31            [-1, 64, 56, 56]
ReLU-32                   [-1, 64, 56, 56]
Conv2d-33                 [-1, 256, 56, 56]
BatchNorm2d-34            [-1, 256, 56, 56]
ReLU-35                   [-1, 256, 56, 56]
Bottleneck-36             [-1, 256, 56, 56]
Conv2d-37                 [-1, 128, 56, 56]
BatchNorm2d-38            [-1, 128, 56, 56]
ReLU-39                   [-1, 128, 56, 56]
Conv2d-40                 [-1, 128, 28, 28]
BatchNorm2d-41            [-1, 128, 28, 28]
ReLU-42                   [-1, 128, 28, 28]
Conv2d-43                 [-1, 512, 28, 28]
BatchNorm2d-44            [-1, 512, 28, 28]
Conv2d-45                 [-1, 512, 28, 28]
BatchNorm2d-46            [-1, 512, 28, 28]
ReLU-47                   [-1, 512, 28, 28]
Bottleneck-48             [-1, 512, 28, 28]
Conv2d-49                 [-1, 128, 28, 28]
BatchNorm2d-50            [-1, 128, 28, 28]
ReLU-51                   [-1, 128, 28, 28]
Conv2d-52                 [-1, 128, 28, 28]
BatchNorm2d-53            [-1, 128, 28, 28]
ReLU-54                   [-1, 128, 28, 28]
Conv2d-55                 [-1, 512, 28, 28]
BatchNorm2d-56            [-1, 512, 28, 28]
ReLU-57                   [-1, 512, 28, 28]
Bottleneck-58             [-1, 512, 28, 28]
Conv2d-59                 [-1, 128, 28, 28]
BatchNorm2d-60            [-1, 128, 28, 28]
ReLU-61                   [-1, 128, 28, 28]
Conv2d-62                 [-1, 128, 28, 28]
BatchNorm2d-63            [-1, 128, 28, 28]
ReLU-64                   [-1, 128, 28, 28]
Conv2d-65                 [-1, 512, 28, 28]
BatchNorm2d-66            [-1, 512, 28, 28]
ReLU-67                   [-1, 512, 28, 28]
Bottleneck-68             [-1, 512, 28, 28]
Conv2d-69                 [-1, 128, 28, 28]
BatchNorm2d-70            [-1, 128, 28, 28]
ReLU-71                   [-1, 128, 28, 28]
Conv2d-72                 [-1, 128, 28, 28]
BatchNorm2d-73            [-1, 128, 28, 28]
ReLU-74                   [-1, 128, 28, 28]
Conv2d-75                 [-1, 512, 28, 28]
BatchNorm2d-76            [-1, 512, 28, 28]
ReLU-77                   [-1, 512, 28, 28]
Bottleneck-78             [-1, 512, 28, 28]
Conv2d-79                 [-1, 256, 28, 28]
BatchNorm2d-80            [-1, 256, 28, 28]
ReLU-81                   [-1, 256, 28, 28]
Conv2d-82                 [-1, 256, 14, 14]
BatchNorm2d-83            [-1, 256, 14, 14]
ReLU-84                   [-1, 256, 14, 14]
Conv2d-85                 [-1, 1024, 14, 14]
BatchNorm2d-86            [-1, 1024, 14, 14]
Conv2d-87                 [-1, 1024, 14, 14]
BatchNorm2d-88            [-1, 1024, 14, 14]
ReLU-89                   [-1, 1024, 14, 14]
Bottleneck-90             [-1, 1024, 14, 14]
Conv2d-91                 [-1, 256, 14, 14]
BatchNorm2d-92            [-1, 256, 14, 14]
ReLU-93                   [-1, 256, 14, 14]
Conv2d-94                 [-1, 256, 14, 14]
BatchNorm2d-95            [-1, 256, 14, 14]
ReLU-96                   [-1, 256, 14, 14]
Conv2d-97                 [-1, 1024, 14, 14]
BatchNorm2d-98            [-1, 1024, 14, 14]
ReLU-99                   [-1, 1024, 14, 14]
Bottleneck-100            [-1, 1024, 14, 14]
Conv2d-101                [-1, 256, 14, 14]
BatchNorm2d-102           [-1, 256, 14, 14]
ReLU-103                  [-1, 256, 14, 14]
Conv2d-104                [-1, 256, 14, 14]
BatchNorm2d-105           [-1, 256, 14, 14]
ReLU-106                  [-1, 256, 14, 14]
Conv2d-107                [-1, 1024, 14, 14]
BatchNorm2d-108           [-1, 1024, 14, 14]
ReLU-109                  [-1, 1024, 14, 14]
Bottleneck-110            [-1, 1024, 14, 14]
Conv2d-111                [-1, 256, 14, 14]
BatchNorm2d-112           [-1, 256, 14, 14]
ReLU-113                  [-1, 256, 14, 14]
Conv2d-114                [-1, 256, 14, 14]
BatchNorm2d-115           [-1, 256, 14, 14]
ReLU-116                  [-1, 256, 14, 14]
Conv2d-117                [-1, 1024, 14, 14]
BatchNorm2d-118           [-1, 1024, 14, 14]
ReLU-119                  [-1, 1024, 14, 14]
Bottleneck-120            [-1, 1024, 14, 14]
Conv2d-121                [-1, 256, 14, 14]
BatchNorm2d-122           [-1, 256, 14, 14]
ReLU-123                  [-1, 256, 14, 14]
Conv2d-124                [-1, 256, 14, 14]
BatchNorm2d-125           [-1, 256, 14, 14]
ReLU-126                  [-1, 256, 14, 14]
Conv2d-127                [-1, 1024, 14, 14]
BatchNorm2d-128           [-1, 1024, 14, 14]
ReLU-129                  [-1, 1024, 14, 14]
Bottleneck-130            [-1, 1024, 14, 14]
Conv2d-131                [-1, 256, 14, 14]
BatchNorm2d-132           [-1, 256, 14, 14]
ReLU-133                  [-1, 256, 14, 14]
Conv2d-134                [-1, 256, 14, 14]
BatchNorm2d-135           [-1, 256, 14, 14]
ReLU-136                  [-1, 256, 14, 14]
Conv2d-137                [-1, 1024, 14, 14]
BatchNorm2d-138           [-1, 1024, 14, 14]
ReLU-139                  [-1, 1024, 14, 14]
Bottleneck-140            [-1, 1024, 14, 14]
Conv2d-141                [-1, 512, 14, 14]
BatchNorm2d-142           [-1, 512, 14, 14]
ReLU-143                  [-1, 512, 14, 14]
Conv2d-144                [-1, 512, 7, 7]
BatchNorm2d-145           [-1, 512, 7, 7]
ReLU-146                  [-1, 512, 7, 7]
Conv2d-147                [-1, 2048, 7, 7]
BatchNorm2d-148           [-1, 2048, 7, 7]
Conv2d-149                [-1, 2048, 7, 7]
BatchNorm2d-150           [-1, 2048, 7, 7]
ReLU-151                  [-1, 2048, 7, 7]
Bottleneck-152            [-1, 2048, 7, 7]
Conv2d-153                [-1, 512, 7, 7]
BatchNorm2d-154           [-1, 512, 7, 7]
ReLU-155                  [-1, 512, 7, 7]
Conv2d-156                [-1, 512, 7, 7]
BatchNorm2d-157           [-1, 512, 7, 7]
ReLU-158                  [-1, 512, 7, 7]
Conv2d-159                [-1, 2048, 7, 7]
BatchNorm2d-160           [-1, 2048, 7, 7]
ReLU-161                  [-1, 2048, 7, 7]
Bottleneck-162            [-1, 2048, 7, 7]
Conv2d-163                [-1, 512, 7, 7]
BatchNorm2d-164           [-1, 512, 7, 7]
ReLU-165                  [-1, 512, 7, 7]
Conv2d-166                [-1, 512, 7, 7]
BatchNorm2d-167           [-1, 512, 7, 7]
ReLU-168                  [-1, 512, 7, 7]
Conv2d-169                [-1, 2048, 7, 7]
BatchNorm2d-170           [-1, 2048, 7, 7]       
ReLU-171                  [-1, 2048, 7, 7]            
Bottleneck-172            [-1, 2048, 7, 7]             
AdaptiveAvgPool2d-173     [-1, 2048, 1, 1]           
Linear-174                [-1, 4]   
============================================        
"""