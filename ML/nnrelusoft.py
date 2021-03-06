import numpy as np
#import warnings

#warnings.simplefilter(action = "ignore", category = RuntimeWarning)
class NN:
    def sig(self,x):
        return 1/(1+np.exp(-x))
    def sigprime(self,x):
        return self.relu(x)*(1-self.relu(x))
    def relu(self,x):
        #print(x)
        #print(np.maximum(0.01,x))
        return np.maximum(-0.01,x)
    def reluprime(self,x):
        x[x<=0] = 0
        x[x>0] = 1
        return x
    def soft(self,x):
        """Compute the softmax of vector x in a numerically stable way."""
        shiftx = x - np.max(x)
        exps = np.exp(shiftx)
        return exps / np.sum(exps)
        #return np.exp(x)/np.sum(np.exp(x))

    def softprime(self,x,row):
        s = x.reshape(-1,1)
        #print(s)
        #print(x.shape)
        #print((np.diagflat(s) - np.dot(s, s.T)).shape)
        jacobian = (np.diagflat(s) - np.dot(s, s.T))

        #print(jacobian.shape)
        rowone=jacobian[row,:]

        rowone=np.reshape(rowone,(1,-1))

        #sum=jacobian.sum(axis=1)
        #sum=np.reshape(sum,(1,-1))
        #diag=np.diag(jacobian,k=0)
        #diag=np.reshape(diag,(1,-1))
        #print(rowone.shape)
        #print(rowone)
        #column=np.zeros((len(jacobian),1))
        #print(len(jacobian))
        #for counter in range(len(jacobian)):
            #print(jacobian[counter:].sum())
        #    column[counter]=(jacobian[counter:].sum())/len(jacobian)
        #return column.T
        return rowone
        #return sum
        #return diag

        #return self.soft(x)*(1-self.soft(x))
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
        #print(self.reluprime(self.l2w))

    def feedforward(self,x):
        self.input=x
        #print(self.input)
        layer1=self.relu(np.dot(self.input,self.l1w))
        #print(np.dot(self.relu(np.dot(self.input,self.l1w)),self.l2w))
        return self.soft(np.dot(self.relu(np.dot(self.input,self.l1w)),self.l2w))
    def addw1(self,x):
        self.l1w+=x
    def addw2(self,x):
        self.l2w+=x
    def dw2(self,row):
        layer1=self.relu(np.dot(self.input,self.l1w))
        return np.dot(self.softprime(np.dot(layer1,self.l2w),row).T,layer1).T
    def dw1(self,row):
        layer1=self.relu(np.dot(self.input,self.l1w))
        #print(np.clip(np.dot(np.dot(self.input.T,self.softprime(np.dot(layer1,self.l2w),row)),self.l2w.T).T,-100000,100000))

        #print(self.reluprime(np.dot(self.input,self.l1w)))
        #return np.multiply(np.dot(np.dot(self.input.T,self.softprime(np.dot(layer1,self.l2w),row)),self.l2w.T).T,self.reluprime(np.dot(self.input,self.l1w)).T).T
        return np.multiply(np.dot(np.dot(self.input.T,self.softprime(np.dot(layer1,self.l2w),row)),self.l2w.T).T,self.reluprime(np.dot(self.input,self.l1w)).T).T
testInput=np.array([[0.2]])
wrt=0
print("input")
print(testInput)
newNN=NN(1,2,2)
print("output")
#print(newNN.feedforward(np.array([[-0.5,-0.5]])))
print(newNN.feedforward(testInput))

for x in range(1000):
    newNN.addw1(newNN.dw1(wrt))
    #newNN.addw2(newNN.dw2())
    #w2adder=0.01*newNN.dw2()
    #w2adder[:,0]*=-1
    #w2adder[:,1]*=-1
    #newNN.addw2(w2adder)
    newNN.addw2(newNN.dw2(wrt))
    #newNN.addw2(-newNN.dw2(wrt+1))
    #newNN.feedforward(np.array([[-0.5,-0.5]]))
    newNN.feedforward(testInput)





print("output")
#print(newNN.feedforward(np.array([[-0.5,-0.5]])))
print(newNN.feedforward(testInput))
print("d1")
print(newNN.dw1(wrt))
print("d2")
print(newNN.dw2(wrt))
