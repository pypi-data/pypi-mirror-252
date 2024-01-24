import torch.nn as nn
import torch

class conv2DBatchNormRelu(nn.Module):
    def __init__(self,in_channels,out_channels,kernel_size,stride,padding,
                 bias=True,dilation=1,is_batchnorm=True):
        super(conv2DBatchNormRelu,self).__init__()
        if is_batchnorm:
            self.cbr_unit=nn.Sequential(
                nn.Conv2d(in_channels,out_channels,kernel_size=kernel_size,stride=stride,padding=padding,
                          bias=bias,dilation=dilation),
                nn.BatchNorm2d(out_channels),
                nn.ReLU(inplace=True),
            )
        else:
            self.cbr_unit=nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=kernel_size, stride=stride, padding=padding,
                          bias=bias, dilation=dilation),
                nn.ReLU(inplace=True)
            )

    def forward(self,inputs):
        outputs=self.cbr_unit(inputs)
        return outputs

class segnetDown2(nn.Module):
    def __init__(self,in_channels,out_channels):
        super(segnetDown2,self).__init__()
        self.conv1=conv2DBatchNormRelu(in_channels,out_channels,kernel_size=3,stride=1,padding=1)
        self.conv2=conv2DBatchNormRelu(out_channels,out_channels,kernel_size=3,stride=1,padding=1)
        self.maxpool_with_argmax=nn.MaxPool2d(kernel_size=2,stride=2,return_indices=True)

    def forward(self,inputs):
        outputs=self.conv1(inputs)
        outputs=self.conv2(outputs)
        unpooled_shape=outputs.size()
        outputs,indices=self.maxpool_with_argmax(outputs)
        return outputs,indices,unpooled_shape

class segnetDown3(nn.Module):
    def __init__(self,in_channels,out_channels):
        super(segnetDown3,self).__init__()
        self.conv1=conv2DBatchNormRelu(in_channels,out_channels,kernel_size=3,stride=1,padding=1)
        self.conv2=conv2DBatchNormRelu(out_channels,out_channels,kernel_size=3,stride=1,padding=1)
        self.conv3=conv2DBatchNormRelu(out_channels,out_channels,kernel_size=3,stride=1,padding=1)
        self.maxpool_with_argmax=nn.MaxPool2d(kernel_size=2,stride=2,return_indices=True)

    def forward(self,inputs):
        outputs=self.conv1(inputs)
        outputs=self.conv2(outputs)
        outputs=self.conv3(outputs)
        unpooled_shape=outputs.size()
        outputs,indices=self.maxpool_with_argmax(outputs)
        return outputs,indices,unpooled_shape


class segnetUp2(nn.Module):
    def __init__(self,in_channels,out_channels):
        super(segnetUp2,self).__init__()
        self.unpool=nn.MaxUnpool2d(2,2)
        self.conv1=conv2DBatchNormRelu(in_channels,out_channels,kernel_size=3,stride=1,padding=1)
        self.conv2=conv2DBatchNormRelu(out_channels,out_channels,kernel_size=3,stride=1,padding=1)

    def forward(self,inputs,indices,output_shape):
        outputs=self.unpool(inputs,indices=indices,output_size=output_shape)
        outputs=self.conv1(outputs)
        outputs=self.conv2(outputs)
        return outputs

class segnetUp3(nn.Module):
    def __init__(self,in_channels,out_channels):
        super(segnetUp3,self).__init__()
        self.unpool=nn.MaxUnpool2d(2,2)
        self.conv1=conv2DBatchNormRelu(in_channels,out_channels,kernel_size=3,stride=1,padding=1)
        self.conv2=conv2DBatchNormRelu(out_channels,out_channels,kernel_size=3,stride=1,padding=1)
        self.conv3=conv2DBatchNormRelu(out_channels,out_channels,kernel_size=3,stride=1,padding=1)

    def forward(self,inputs,indices,output_shape):
        outputs=self.unpool(inputs,indices=indices,output_size=output_shape)
        outputs=self.conv1(outputs)
        outputs=self.conv2(outputs)
        outputs=self.conv3(outputs)
        return outputs

class SegNet(nn.Module):
    def __init__(self,in_channels=3,num_classes=21):
        super(SegNet,self).__init__()
        self.down1=segnetDown2(in_channels=in_channels,out_channels=64)
        self.down2=segnetDown2(64,128)
        self.down3=segnetDown3(128,256)
        self.down4=segnetDown3(256,512)
        self.down5=segnetDown3(512,512)

        self.up5=segnetUp3(512,512)
        self.up4=segnetUp3(512,256)
        self.up3=segnetUp3(256,128)
        self.up2=segnetUp2(128,64)
        self.up1=segnetUp2(64,64)
        self.finconv=conv2DBatchNormRelu(64,num_classes,3,1,1)

    def forward(self,inputs):
        down1,indices_1,unpool_shape1=self.down1(inputs)
        down2,indices_2,unpool_shape2=self.down2(down1)
        down3,indices_3,unpool_shape3=self.down3(down2)
        down4,indices_4,unpool_shape4=self.down4(down3)
        down5,indices_5,unpool_shape5=self.down5(down4)

        up5=self.up5(down5,indices=indices_5,output_shape=unpool_shape5)
        up4=self.up4(up5,indices=indices_4,output_shape=unpool_shape4)
        up3=self.up3(up4,indices=indices_3,output_shape=unpool_shape3)
        up2=self.up2(up3,indices=indices_2,output_shape=unpool_shape2)
        up1=self.up1(up2,indices=indices_1,output_shape=unpool_shape1)
        outputs=self.finconv(up1)

        return outputs

if __name__=="__main__":
    inputs=torch.ones(1,3,224,224)
    model=segnet()
    print(model(inputs).size())
    print(model)
