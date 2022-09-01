# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 08:25:08 2022

@author: mahon
"""
import numpy as np
import pandas as pd
data=pd.read_csv("C:/Users/mahon/smoking.csv")

#We want to find out if people who smoke are more miserable than people who don't
#But people who smoke have different characteristics than people who do not. So we
#cannot just take a difference in average distress levels

#We need to build a matching alogirithm that will allow us to pair smokers with
#similar non smokers. We're going to start by building a linear search function...cause its easy

ctr=cluster()

def lin_search(X,Y):
    
    #Grab length of both vectors
    n=len(X)
    m=len(Y)
    
    #Define arrays to track distance and indices
    d_array=np.zeros([n,m])
    min_idx=np.zeros(n)
    
    #Loop through all X,Y pairs
    for i in range(n):
        for j in range(m):
            #Calculate distance between each X and each Y
            d_array[i,j]=ctr.dist([X[i]],[Y[j]])
        
        #For every X, 
        min_idx[i]=int(np.argmin(d_array[i,:]))
    
    min_idx=min_idx.astype(int)
    return min_idx




X=(data[['sex','high_school','indigeneity','age']]).to_numpy()

Y=data['smoker'].to_numpy()
smoke_idx=(Y==1)

#Lets estimate the probability that every observation is a smoker, logit time
#I'm gonna use sklearn's logit, cause I'm a little bitch

from sklearn.linear_model import LogisticRegression

#Its a little bit different from R. You've got to initalize a model object first
model = LogisticRegression(solver='liblinear', random_state=0)

#Fit and predict probabilities
model.fit(X,Y)
prop_scores=model.predict_proba(X)[:,1]

#Now, we split our data up into treated and untreated
smokers=prop_scores[smoke_idx]
nonsmokers=prop_scores[(1-smoke_idx).astype(np.bool)]

#Use our search function to find the nonsmoker who most closely resembles each smoker
match_idx=lin_search(smokers,nonsmokers)


#Our outcome variable is psyc_distress
smoke_avg=np.mean(data['psyc_distress'][smoke_idx])
nonsmoke_avg=np.mean(data['psyc_distress'][match_idx])

ATE=smoke_avg-nonsmoke_avg
print(ATE)

sd=np.std(data['psyc_distress'][smoke_idx])

#%% Ok lets refine that search alogoithm, we only need points to be close, not the closest
#Define c as tolerance. Nearest "good enough" neghibor

def lin_search_close(X,Y,c):
    
    #Grab length of both vectors
    n=len(X)
    m=len(Y)
    
    #Define arrays to track distance and indices
    d_array=np.zeros(n)
    min_idx=np.zeros(n)
    
    #Loop through all X,Y pairs
    for i in range(n):
        for j in range(m):
            #Calculate distance between each X and each Y
            d=ctr.dist([X[i]],[Y[j]])
            #Grab the first observation that is within c of X[i]
            if d<c:
                min_idx[i]=j
                #Go to next X    
                break
            
            if j==(m-1) and d>c:
                min_idx[i]=-1
                print("Error: tolerance too high. No match found for observation "+str(i))
        
    min_idx=min_idx.astype(int)
    return min_idx


#Quick Example to make sure it works
X=[1,2,3,4,5]
Y=[1.3,1.5,1.001]
c=.6

lin_search_close(X,Y,c)

#Now lets see how much faster this 'good enough' algorithim is....

import time

#Block one: linear search
start = time.time()
lin_search(smokers,nonsmokers)
end = time.time()
print(end - start)

start = time.time()
lin_search_close(smokers,nonsmokers,c=.05)
end = time.time()
print(end - start)

#Thats an imporvment of about a fctor of 60! But did we lose much precision?
match_idx=lin_search_close(smokers, nonsmokers,c=.01)

#Our outcome variable is psyc_distress
smoke_avg=np.mean(data['psyc_distress'][smoke_idx])
nonsmoke_avg=np.mean(data['psyc_distress'][match_idx])

ATE=smoke_avg-nonsmoke_avg
print(ATE)

#%%
#Yeah we did actually. Like everything else, there is a trade-off here: speed vs precision
#If you data set is like real big, there are memory considerations too. 
#What if we randomize order and do it like 10 times? Kind of like a bootstrap?

#Lets get that suffle command going
import sklearn
from sklearn.utils import shuffle

n_draws=20
ATE=0

start=time.time()

for i in range(n_draws):
    ns_distress=data['psyc_distress'][(1-smoke_idx).astype(np.bool)]
    ns_distress=ns_distress.values
    
    ns_shuffle, ns_distress_shuffle = sklearn.utils.shuffle(nonsmokers, ns_distress)
    
    match_idx=lin_search_close(smokers, ns_shuffle,c=.01)
    
    #Our outcome variable is psyc_distress
    smoke_avg=np.mean(data['psyc_distress'][smoke_idx])
    nonsmoke_avg=np.mean(ns_distress_shuffle[match_idx])
    
    ATE+=(smoke_avg-nonsmoke_avg)/n_draws

end=time.time()
print(end-start)
print(ATE)

#Alright its still much faster than the original model, but we lose almost no precision!


        