import numpy as np
class NN:
    def sig(self,x):
        return 1/(1+np.exp(-x))
    def sigprime(self,x):
        return self.sig(x)*(1-self.sig(x))
    def soft(self,x):
        return np.exp(x)/np.sum(np.exp(x))
    def softprime(self,x):
        #s = x.reshape(-1,1)
        #print(x.shape)
        #print((np.diagflat(s) - np.dot(s, s.T)).shape)
        #return (np.diagflat(s) - np.dot(s, s.T))
        return self.soft(x)*(1-self.soft(x))
    def __init__(self,In,Hn,On):
        self.inputneurons=In
        hiddenneurons=Hn
        outputneurons=On
        self.input=np.random.uniform(-1,1,(1,self.inputneurons))
        self.l1w=np.random.uniform(-1,1,(self.inputneurons,hiddenneurons))
        self.l2w=np.random.uniform(-1,1,(hiddenneurons,outputneurons))
        print("weights1")
        print(self.l1w)
        print("weights2")
        print(self.l2w)
    def feedforward(self,x):
        self.input=x
        #print(self.input)
        layer1=self.sig(np.dot(self.input,self.l1w))
        return self.soft(np.dot(self.sig(np.dot(self.input,self.l1w)),self.l2w))
    def addw1(self,x):
        self.l1w+=x
    def addw2(self,x):
        self.l2w+=x
    def dw2(self):
        layer1=self.sig(np.dot(self.input,self.l1w))
        return np.dot(self.softprime(np.dot(layer1,self.l2w)).T,layer1).T
    def dw1(self):
        layer1=self.sig(np.dot(self.input,self.l1w))
        return np.multiply(np.dot(np.dot(self.input.T,self.softprime(np.dot(layer1,self.l2w))),self.l2w.T).T,self.sigprime(np.dot(self.input,self.l1w)).T).T
testInput=np.array([[0.3]])
print("input")
print(testInput)
newNN=NN(1,5,9)
print("output")
#print(newNN.feedforward(np.array([[-0.5,-0.5]])))
print(newNN.feedforward(testInput))
for x in range(10000):
    newNN.addw1(newNN.dw1())

    w2adder=newNN.dw2()
    w2adder[:,0]*=-1
    newNN.addw2(w2adder)
    #newNN.feedforward(np.array([[-0.5,-0.5]]))
    newNN.feedforward(testInput)




print("output")
#print(newNN.feedforward(np.array([[-0.5,-0.5]])))
print(newNN.feedforward(testInput))
print("d1")
print(newNN.dw1())
print("d2")
print(newNN.dw2())