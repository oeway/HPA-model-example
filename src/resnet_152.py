from torchvision.models import resnet152
from torch.nn import Linear

def Resnet152(pretrained = True):
    net152 = resnet152(pretrained)
    net152.fc = Linear(in_features=2048, out_features=28)
    return net152