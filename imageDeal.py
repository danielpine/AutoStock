# -*- coding: utf-8 -*-
import PIL
import numpy

idx=0


def coordinateSystemProbabilityDistributionAnalysis(SingalNumberNumpyArray,numarr):
    
    imm=SingalNumberNumpyArray
    
    AllOneArr=[]
    #Remove the border
    i=0
    for row in imm:
        if 0 not in row:
            AllOneArr.append(i)
        i+=1
    if len(AllOneArr)!=0:    
        imm=numpy.delete(imm,AllOneArr,axis=0)
    
    AllOneArr.clear()
    
    [rr,cc]=imm.shape
    for ccc in range(cc-1):
        #print(ccc,"+",imm[:,ccc])
        if 0 not in imm[:,ccc]:
            AllOneArr.append(ccc)
    if len(AllOneArr)!=0:
        imm=numpy.delete(imm,AllOneArr,axis=1)
    
    print("-------------")
    """
    for row in imm:
        print(row)
    """
    #Find the center
    
    [rr,cc]=imm.shape
    #print([rr,cc])
    center=[int(rr/2)+1,int(cc/2)]
    #print(center)
    #TW 第二象限
    #TH 第三象限
    #FO 第四象限
    
    [Ox,Oy]=center
    #ON 第一象限
    """
    print(imm[0:Ox,Oy:cc])
    print(imm[0:Ox,0:Oy])
    print(imm[Ox:rr,0:Oy])
    print(imm[Ox:rr,Oy:cc])
    """
    ON=imm[0:Ox,Oy:cc]
    TW=imm[0:Ox,0:Oy]
    TH=imm[Ox:rr,0:Oy]
    FO=imm[Ox:rr,Oy:cc]
    
    """
    print([
    count(ON,0),
    count(TW,0),
    count(TH,0),
    count(FO,0)]
    )
    """
    
    testArr=[
    count(ON,0),
    count(TW,0),
    count(TH,0),
    count(FO,0)]
    j=0
    for row in numarr:
        try:
            result=numpy.array(row)-numpy.array(testArr)
            #print(result)
            rltSum=0
            for i in result:
                rltSum+=abs(i)
            #print(rltSum)
            if rltSum < 60:
                return j
        except Exception as e:
            pass
        
        j+=1

def count(arr,target):
    c=0
    for row in arr:
       for col in row: 
           if col==target:
               c+=1
    return int(c*1000/(arr.shape[0]*arr.shape[1]))


def pretreatment(ima):
    ima=ima.convert('L')         #转化为灰度图像
    im=numpy.array(ima)        #转化为二维数组
    for i in range(im.shape[0]):#转化为二值矩阵
        for j in range(im.shape[1]):
            #print(im[i,j])
            if im[i,j]==255 or im[i,j]==218:
                im[i,j]=1
            else:
                im[i,j]=0
    return im
def identify(file,numarr):
    result=""
    #file="cut.jpg"
    ima=PIL.Image.open(file) #读入图像
    #ima=PIL.Image.open('cut.jpg') #读入图像
    im=pretreatment(ima)  #调用图像预处理函数
    with open("cut.txt","w") as f:
        for i in im:
            for j in i:
                f.write(str(j))
            f.write("\n")
            
    [r,c]=im.shape
    one=False
    temp=0
    
    for c in range(c-1):
        if 0 in im[:,c]:
            #print(im[:,c])
            one=True
        else:
            if one:
                one=False
                imm=im[:,temp:c]
                reNum=coordinateSystemProbabilityDistributionAnalysis(imm,numarr)
                result+=str(reNum)
                temp=c
    return result
























