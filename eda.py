import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import cross_val_score

def dframe(file): #method created to streamline opening csv files and setting the desired index
    f=pd.read_csv(file)
    z=f.set_index('TeamID')
    return z

def poly_analyze(ind,dep,df,f=1,cross_val=False):
    #ind=list or string dep=string df=pandas dataframe f=features   
    #method created to preform linear (f=1) and polyonomial regression on x varibales and a y variables pulled from a pandas df
    
    #creating arrays from data
    if type(ind)==list:
        l=len(ind)
    else: l=1
    x=df[ind].values.reshape([-1,l]) 
    y=df[dep].values.reshape([-1,1])

    #preforms regression analysis using sklearn methods    
    poly=PolynomialFeatures(f,include_bias=True)
    pf=poly.fit_transform(x,y)
    model=LinearRegression(fit_intercept=False)
    model.fit(pf,y)
    y_pred=model.predict(pf)
    print(model.score(pf,y))
    
    #if desired could check cross validation score of analysis
    if cross_val:
        c=cross_val_score(model, pf, y)
        print(np.mean(c))
        
    return x,y,y_pred

def graph(x,y,y_pred,out=None,xlab='x',ylab='y'): #method created to esaily vsialize results of poly_analyze method (above)
    plt.figure()
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.plot(x,y,'ko', alpha=.5)
    plt.plot(x,y_pred,'ro',linewidth=1.0, alpha=.5)
    if out!=None:
        plt.savefig(out)

a=dframe('Team_Data.csv')
b=dframe('clean_data.csv')
b=b.sort_values('Year')
ind=['aPTS','PTS']
x,y,z=poly_analyze(ind,'W',a,f=1,cross_val=True)
graph(x[:,1],y,z,xlab='PTS and aPTS',ylab='W')