# -*- coding: utf-8 -*-
#论文验证
import pandas as pd
import numpy as np
def GM11(x,n,k):
    '''
    x为原始序列
    n为往后预测的个数
    k为指示符号，k=0是表示累减还原式，k=1为导数还原式
    '''
    x1 = x.cumsum()#一次累加  
    z1 = (x1[:len(x1) - 1] + x1[1:])/2.0#紧邻均值  
    z1 = z1.reshape((len(z1),1))  
    B = np.append(-z1,np.ones_like(z1),axis=1)  
    Y = x[1:].reshape((len(x) - 1,1))
    #a为发展系数 b为灰色作用量
    [[a],[b]] = np.dot(np.dot(np.linalg.inv(np.dot(B.T, B)), B.T), Y)#计算参数  
    imitate = list()
    predict = list()
    der = list()
    if k==0:
        for index in range(0,x.shape[0]):
            imitate.append((x[0]-b/a)*np.exp(-a*(index))*(1-np.exp(a))) 
            der.append((x[0]-b/a)*np.exp(-a*index)*(pow(a,2)))
        for index in range(x.shape[0]+1,x.shape[0]+n+1):
            predict.append((x[0]-b/a)*np.exp(-a*(index-1))*(1-np.exp(a)))
        for index in range(0,x.shape[0]+n):
            der.append((x[0]-b/a)*np.exp(-a*index)*(pow(a,2)))
    else:
        for index in range(0,x.shape[0]):
            imitate.append((x[0]-b/a)*np.exp(-a*(index))*(-a)) 
        for index in range(x.shape[0]+1,x.shape[0]+n+1):
            predict.append((x[0]-b/a)*np.exp(-a*(index-1))*(-a)) 
        for index in range(0,x.shape[0]+n):
            der.append((x[0]-b/a)*np.exp(-a*index)*(pow(a,2)))
    return {
            'a':{'value':a,'desc':'发展系数'},
            'b':{'value':b,'desc':'灰色作用量'},
            'imitate':{'value':imitate,'desc':'模拟值'},
            'predict':{'value':predict,'desc':'预测值'},
            'der':{'value':der,'desc':'x0斜率'}
    } 

def FormatPrint(data,n):
    '''
    data是序列
    n为保留的小数位数
    '''
    data2=list()
    for d in data:
        d=round(d,n)
        data2.append(d)
    return data2

#输入
st=input('请输入待模拟预测的序列，用逗号（英文）隔开：')
data=list(map(eval,st.split(',')))#将字符串转化为数字
print("您输入的数据是：",data)
n=eval(input('需预测的个数：'))#注意键盘输入的是字符串，需要转化为数字
k=eval(input('请选择计算时间响应式x0时，运用累减还原式or导数还原式（0表示累减还原式，1表示导数还原式）：'))
while k!=0 and k !=1:
    print("请重新输入：")
    k=input('请选择计算时间相应式x0时，运用累减还原式or导数还原式（0表示累减还原式，1表示导数还原式）：')
fd=eval(input('结果需保留的小数位数：'))

#执行操作
d=np.array(data)
result = GM11(d,n,k)
a=result['a']['value']
b=result['b']['value']
imitate=result['imitate']['value']
predict=result['predict']['value']
der=result['der']['value']
imitate=FormatPrint(imitate,fd)
predict=FormatPrint(predict,fd)
der=FormatPrint(der,fd)

#输出
print('原始序列：',data)
print('发展系数：a=',a)
print('灰色作用量：b=',b)
#print('发展系数：a={:.2f}'.format(a))
#print('灰色作用量：b={:.2f}'.format(b))
print('模拟序列：',imitate)
print('预测序列：',predict)
print('x0斜率：',der)
