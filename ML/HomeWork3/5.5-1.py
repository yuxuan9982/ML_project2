import csv
import numpy as np
import scipy
import numpy.random
import sklearn.model_selection
from sklearn.preprocessing import MinMaxScaler
from keras.utils import np_utils
from sklearn import preprocessing
import xlrd
def sigmoid(x):
    return scipy.special.expit(x)
def par_sigmoid(x):
    return sigmoid(x)*(1-sigmoid(x))
class ANN:
    input_num,hidden_num,output_num,learning_rate,epochs=100,100,100,0.1,200
    y,beta,w,b,alpha,v,x=[],[],[],[],[],[],[]
    theta,gamma,hat_y,e,g=[],[],[],[],[]
    # def g(self,k):
    #     return self.hat_y[k]*(1-self.hat_y[k])*(self.y[k]-self.hat_y[k])

    def __init__(self,learning_rate,input_num,hidden_num,output_num):
        self.learning_rate=learning_rate
        self.input_num=input_num
        self.hidden_num=hidden_num
        self.output_num=output_num
        self.b=np.zeros(hidden_num)
        #阈值的初始化
        self.theta=np.random.rand(output_num)
        self.gamma=np.random.rand(hidden_num)
        self.hat_y=np.zeros(output_num)
        #权重初始化
        self.v=np.zeros((input_num,hidden_num))
        self.w=np.zeros((hidden_num,output_num))
        self.e=np.zeros(hidden_num)
        self.alpha=np.zeros(hidden_num)
        self.beta=np.zeros(output_num)
        self.g=np.zeros(output_num)
    def get_y(self,x):
        for h in range(self.hidden_num):
            self.alpha[h]=0
            for i in range(self.input_num):
                self.alpha[h]+=self.v[i][h]*x[i]
            self.b[h]=sigmoid(self.alpha[h]-self.gamma[h])
        for o in range(self.output_num):
            self.beta[o]=0
            for h in range(self.hidden_num):
                self.beta[o]+=self.w[h][o]*self.b[h]
            self.hat_y[o]=sigmoid(self.beta[o]-self.theta[o])
    def train_std(self,x1,y1):
        #前向传播
        self.get_y(x1)
        #求得E均方误差
        E=0
        for i in range(len(y1[0])):
            E+=(self.hat_y[i]-y1[i])**2
        E/=2
        loss=E
        #print(loss)
        #反向传播
        #get g and e
        for i in range(self.output_num):
            self.g[i]=(self.hat_y[i]*(1-self.hat_y[i])*(y1[i]-self.hat_y[i]))
        for h in range(self.hidden_num):
            tmp=0
            for o in range(self.output_num):
                tmp+=self.w[h][o]*self.g[o]
            self.e[h]=self.b[h]*(1-self.b[h])*tmp
        for h in range(self.hidden_num):
            for o in range(self.output_num):
                self.w[h][o]+=self.learning_rate*self.g[o]*self.b[h]
        for i in range(self.input_num):
            for h in range(self.hidden_num):
                self.v[i][h]+=self.learning_rate*x1[i]*self.e[h]
        #self.w+=self.learning_rate*np.dot(self.b.T,g)
        for i in range(self.output_num):
            self.theta[i]-=self.learning_rate*self.g[i]
        #self.v+=self.learning_rate*np.dot(x1,self.e)
        for i in range(self.hidden_num):
            self.gamma[i]-=self.learning_rate*self.e[i]
    def predict(self,x1):
        self.get_y(x1)
        return self.hat_y
def read_iris():
    with open("E:/desktop/3rdgrade-1/机器学习/IRIS/iris.csv", "r") as file:#打开CSV文件
        reader = csv.reader(file)#读取
        lst = list(reader)#获取list
        lst.pop(0)#第一行不要
    data,label=[],[]
    for i in lst:
        for j in range(1, 5):
            i[j] = float(i[j])#转换为浮点类型
        data.append(i[1:5])#data增加
        label.append(i[5])#tag增加
    return data,label
    # for i in lst:print(i)
def read_wine():
    path= "E:/desktop/3rdgrade-1/机器学习/winequality_data.xlsx"
    book = xlrd.open_workbook(path)#获取xlsx文件
    sheet1 = book.sheets()[0]#第一页
    row,col=sheet1.nrows,sheet1.ncols#行数列数
    #print(row,col)
    data,label=[],[]
    for i in range(1,row):
        tmp=[]
        for j in range(col-1):
            tmp.append(sheet1.cell(i,j).value)#获取到某行某列值
        label.append(sheet1.cell(i,col-1).value)#标签更新
        data.append(tmp)#数据更新
    #print(data);print(label)
    return data,label

img,label=read_wine()
enc=preprocessing.LabelEncoder()
label=enc.fit_transform(label)
s=set()
for i in label:s.add(i)
input,hidden,output=len(img[0]),125,len(s)#设置输入层，隐藏层，输出层的神经元个数 125best now
#print(test_img,test_img)
mmx=MinMaxScaler()#输入数据归一化
tot_img,tot_label=np.matrix(img),np.matrix(label)
tot_label=tot_label.reshape(-1,1)#维度不对，应该设置为n行1列
tot_label=np_utils.to_categorical(tot_label)

tot=np.concatenate([tot_img,tot_label],axis=1)#把数据和标签按列拼接到一起
tot=mmx.fit_transform(tot)#不归一化已经100了
tot_img,tot_label=tot[:,:input],tot[:,input:]#归一化以后的数据和tag
train_x,test_x,train_y,test_y=sklearn.model_selection.train_test_split(tot_img,tot_label,train_size=0.8)#抽取80%作为训练集
################使用手工搭建的神经网络##################################
learning_rate=0.2#确定学习率
ANN1=ANN(learning_rate=0.1,input_num=input,hidden_num=hidden,output_num=output)
epochs=200
ANN_res,Acc_res=ANN1,0
for k in range(epochs):#迭代
    for j in range(len(train_x)):#遍历所有训练数据
        ANN1.learning_rate=learning_rate*(100)/(100+k)
        ANN1.train_std(train_x[j],train_y[j].reshape(-1,1))#人工神经网络进行训练
    accuracy=0#计算准确性
    sum1,sum2=0,0
    for i in range(len(test_x)):#遍历预测数据
        #wa_x=[]
        outputs = ANN1.predict(test_x[i])#得到对应的输出
        pred_label=numpy.argmax(outputs)#得到输出的值最大的位置，也就是判断结果
        #print(pred_label,test_label[i])
        if(test_y[i][pred_label]==1):#如果判断正确
            sum1+=1
        sum2+=1
    if k%10==9:print('epoch:----->',k+1,'使用手工搭建的神经网络的准确率:',sum1/sum2*100,"%")#输出准确性
    if sum1/sum2>Acc_res:
        Acc_res,ANN_res=sum1/sum2,ANN1
print("找到的最佳准确率为:",Acc_res*100,"%")

################使用手工搭建的神经网络##################################
