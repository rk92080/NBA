from scipy.special import expit
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def dframe(file):
    f=pd.read_csv(file)
    z=f.set_index('TeamID')
    return z


def logres_grad(X, y, beta):
    """
    returns the gradient of logistic regression model
    
    X- independent variables
    y- binary dependent variable (-1,1)
    beta- coefficent
    """
    n=len(X)
    y=y.reshape((-1,1))
    a=X*beta
    a=a.reshape(-1,X.shape[1])
    q=y*a
    s=expit(q)-1
    grad_arr= s*y*X
    grad=(np.sum(grad_arr,axis=0))/n
    
    return grad 

def grad_desc(X, y, n_iter=1000):
    """
    find the minimum of the log. regression function and sets beta to that values
    using several iterations and the gradient method above
    
    X- independent variables
    y- binary dependent variable (-1,1)
    n_iter- the number of iterations

    sol_path- a list of solutions, the kth entry corresponds to the beta 
            at iteration k        
    """
    sol_path = []
    b=np.full((1,X.shape[1]),0)
    sol_path.append(b)

    for i in range(n_iter):
        b=b-logres_grad(X,y,b)
        sol_path.append(b)

    return sol_path

def predict(X, beta):
    """
    predict probability based on regression model    

    beta- coefficients
    X- 2D numpy array of inputs
    
    y_hat- list of probablities   
    """
    y_hat= np.sum((X*beta),axis=1)
    y_hat=expit(y_hat)

    return y_hat

pre_a=dframe('clean_data.csv')

a=pre_a[pre_a.Year!=2018] #remove current season data from df
X=np.zeros((len(a),2)) #create input array 
X[:,-1]=(np.exp(a['dPTS'])-3) 
X[:,0]=1 #dummy column
y=a['Ring'] #input y array showning if they won ring
y=y.replace(0,-1)
y=np.array(y)
g=grad_desc(X,y) #implement gradient descent
beta=g[-1] #take final beta value
print(beta)
a.loc[:,'OR']=0 #create new column 
p=(predict(X,beta))
a.loc[:,'Prob']=p
a=a.sort_values('Year',ascending=False)
for i in np.arange(2005,2018):
    b=a[(a.Year==i) & (a.Playoffs==1)]
    q=np.sum(b['Prob'])
    for x,y in zip(list(b.index.values), b['Prob']):
        a.loc[x,'OR']=y/q
a=a[['Team','Year','OR','Prob','W','dPTS','Ring']]
a=a.sort_values('Prob',ascending=False)
plt.xlabel('dPTS')
plt.ylabel('Probability')
plt.plot(a[a.Ring==0]['dPTS'],a[a.Ring==0]['Prob'],'ko',alpha=.75)
plt.plot(a[a.Ring==1]['dPTS'],a[a.Ring==1]['Prob'],'ro',alpha=.75)
#a.to_csv('prob_data.csv')



#uncomment the section below to run model on 2018 season data
'''
#uncomment this section to run model on 2018 season data
beta=[[-3.36729583,  0.78270756]]
a18=pre_a[pre_a.Year==2018]
X=np.zeros((len(a18),2))
X[:,-1]=(np.exp(a18['dPTS'])-3)
X[:,0]=1
a18.loc[:,'OR']=0
p=predict(X,beta)
a18.loc[:,'Prob']=p
a18P=a18[a18.Playoffs==1]
q=np.sum(a18P['Prob'])
for x,y in zip(list(a18P.index.values),a18P['Prob']):
    a18.loc[x,'OR']=y/q
a18=a18[['Team','Year','OR','Prob','dPTS','W']]
a18=a18.sort_values('Prob',ascending=False)
a18.to_csv('2018_pd.csv')
'''
 
