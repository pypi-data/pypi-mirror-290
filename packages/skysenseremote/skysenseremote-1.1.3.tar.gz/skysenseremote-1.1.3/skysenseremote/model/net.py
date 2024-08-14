import os
import torch
import torchvision
import torch.nn as nn

def set_download_dir():
    os.environ['TORCH_HOME'] = r'./checkpoints'  # setting the environment variable

class deeplabv3(nn.Module):
    def __init__(self, backbone_name="deeplab50", out_channels=128, pretrained=False):
        super().__init__()
        # TODO
        set_download_dir()
        if backbone_name == "deeplab50":
            self.backbone = torchvision.models.segmentation.deeplabv3_resnet50(pretrained=False,
                                                                               num_classes=21)
            self.backbone.classifier = torch.nn.Sequential(*list(self.backbone.classifier.children())[:-1],
                                                           torch.nn.Conv2d(256, out_channels, kernel_size=(1, 1),
                                                                           stride=(1, 1)))

        elif backbone_name == "deeplab101":
            self.backbone = torchvision.models.segmentation.deeplabv3_resnet101(pretrained=False,
                                                                                num_classes=21)
            self.backbone.classifier = torch.nn.Sequential(*list(self.backbone.classifier.children())[:-1],
                                                           torch.nn.Conv2d(256, out_channels, kernel_size=(1, 1),
                                                                           stride=(1, 1)))
        else:
            raise RuntimeError("Specified backbone {} unknown".format(backbone_name))

    def forward(self, input):
        feats = self.backbone(input)["out"]
        return feats


class PMnet(nn.Module):
    def __init__(self, backbone="deeplab50", num_attnfeat=128):
        super().__init__()
        self.num_attnfeat = num_attnfeat
        self.backbone = deeplabv3(backbone_name=backbone, out_channels=num_attnfeat)
        self.mask = torch.nn.Sequential(
            torch.nn.Conv2d(self.num_attnfeat, self.num_attnfeat, 1),
            torch.nn.BatchNorm2d(self.num_attnfeat),
            torch.nn.ReLU(),
            torch.nn.Conv2d(self.num_attnfeat, 1, 1),
            torch.nn.Sigmoid())
        self.heat = torch.nn.Sequential(
            torch.nn.Conv2d(self.num_attnfeat + 1, self.num_attnfeat + 1, 1),
            torch.nn.BatchNorm2d(self.num_attnfeat + 1),
            torch.nn.ReLU(),
            torch.nn.Conv2d(self.num_attnfeat + 1, 1, 1))

    def sample_peaks(self, heat, nums=1):

        B, _, H, W = heat.shape
        assert H == W

        for b in range(B):
            x_b = heat[b]
            idx = torch.topk(x_b.flatten(), nums).indices
            idx_i = idx // W
            idx_j = idx % W
            idx = torch.cat((idx_i.unsqueeze(1), idx_j.unsqueeze(1)), dim=1)
            idx = idx.unsqueeze(0)
            if b == 0:
                graph = idx
            else:
                graph = torch.cat((graph, idx), dim=0)
        return graph

    def forward(self, img):
        features = self.backbone(img)
        mask = self.mask(features)
        heat = self.heat(torch.cat([mask, features], dim=1))
        if self.training:
            return mask, heat
        else:
            point = self.sample_peaks(heat=heat).squeeze(1)
            if point.shape[0] == 1:  # test
                return point, torch.max(heat).item()
            else:  # val
                return point


def count_trainable_params(model):
    count = 0
    for param in model.parameters():
        if param.requires_grad:
            count += param.numel()
    return count


if __name__ == '__main__':
    y = torch.randn((4, 3, 512, 512))
    net = PMnet()
    net.eval()
    print(count_trainable_params(model=net))
    # mask, heat, point = net(y)
    point = net(y)
    # print(mask.shape)
    # print(heat.shape)
    print(point.shape)
