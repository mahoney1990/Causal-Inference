# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 13:33:48 2022

@author: mahon
"""
##Define class for clustering. 
##Goal: clustered propensity matching

#Get a couple numerical packages
import numpy as np
import pandas as pd

#Now lets build a class to contain our distance and clustering functions
class cluster:
    
    def __init__(self, tol=.01):
        self.tol=tol
        
    def dist(self, x1,x2):
        inner=0
        n=len(x1)
    
        #Check lengths match
        if len(x1)!=len(x2):
            print("Get it together! Arrays must be of the same dimension!")
    
        #Build inner
        for i in range(n):
            inner+=(x1[i]-x2[i])**2
    
        #Square root that shit
        dist=(inner)**(1/2)
        return dist
    
    def kmeans(self, X,Y,n_clusters):
            #N features is number of columns in X
            n_features=len(X[0,:])
            size=len(X[:,0])
        
            #Define matrices for calculations
            initial_means=np.zeros([n_clusters,n_features])
            new_means=np.zeros([n_clusters,n_features])
            old_means=np.zeros([n_clusters,n_features])
            ranges=np.zeros([n_features,2])
            
            
            for i in range(n_features):
                ranges[i,0]=min(X[:,i])
                ranges[i,1]=max(X[:,i])
            
            #Import random package for RNG
            import random
            
            #Generate random inital guesses for cluster means
            for i in range(n_clusters):
                for k in range(n_features):
                    initial_means[i,k]=random.uniform(ranges[k,0],ranges[k,1])
            
            
            #Define matrix of distances row = observation, col=cluster, entry = distance from cluster mean
            mean_distances=np.zeros([size,n_clusters])
            
            #Vector of indicators for closest cluster mean
            cluster_label=np.zeros([size])
            
            for j in range(n_clusters):
                #Grab cluster means
                x1=initial_means[j,:]
                
                #Loops through each X value, calculate distance to each mean
                for k in range(size):
                    x=X[k,:]
                    mean_distances[k,j]=self.dist(x,x1)
            
            #Calculate category labels
            for k in range(size):
                cluster_label[k]=np.argmin(mean_distances[k,:])
            
            #Initialize label and count vectors
            cluster_label=cluster_label[:,np.newaxis]
            num_cat=np.zeros([n_clusters])
            
            #Build cluster means
            
            for i in range(n_clusters):
               num_cat[i]=(cluster_label==i).sum()
               index=(cluster_label==i).flatten()
               new_means[i,:]=sum(X[index,:])/num_cat[i]  ###Sometimes returns nans when num_cat is 0 -- fix it!###
            
                
            #Now iterate until convergence
            
            d=1
            tol=.01
            its=0
            
            olds=np.zeros([n_clusters,n_features])
            news=np.zeros([n_clusters,n_features])
            dev=np.zeros(n_clusters)
            olds=new_means
            
            while d>tol:
                its+=1
                print(its)
                
                for j in range(n_clusters):
                    #Grab cluster means
                    x1=olds[j,:]
                    
                    #Loops through each X value, calculate distance to each mean
                    for k in range(size):
                        x=X[k,:]
                        mean_distances[k,j]=self.dist(x,x1)
                
                #Calculate category labels
                for k in range(size):
                    cluster_label[k]=np.argmin(mean_distances[k,:])
                    
                for i in range(n_clusters):
                     num_cat[i]=(cluster_label==i).sum()
                     index=(cluster_label==i).flatten()
                     news[i,:]=sum(X[index,:])/num_cat[i]
            
                     dev[i]=self.dist(news[i,:],olds[i,:])
            
                d=max(dev)
                
                olds=news
            
            for i in range(n_clusters):
                print("Cluster "+str(i)+" Center: "+ str(news[i,:]))
                
            return cluster_label
            
#%% Test the class functions
#Create an instance of cluster class
ctr=cluster()

#import sklearn
import sklearn
from sklearn.datasets import make_blobs

#Create some fake data
size=200
n_features=3

X,Y = make_blobs(n_samples=size, centers=3,
                  random_state=0, cluster_std=.2, n_features=n_features)

ctr.kmeans(X,Y,3)




#%%
#Okay now lets get some data to cluster over
data=pd.read_csv("C:/Users/mahon/smoking.csv")

Y=data['smoker'].to_numpy()
X=(data[['sex','high_school','indigeneity','age']]).to_numpy()

n_clusters=3

#Get labels from clusters
labels=ctr.kmeans(X,Y,n_clusters=n_clusters)

#Build a new array
clustered_data=(np.array([labels.flatten(),Y,data['psyc_distress']])).transpose()

ATE=0

#Alright lets build some clustered treatment effects
for i in range(n_clusters):

    nonsmoker=clustered_data[(clustered_data[:,0]==i) & (clustered_data[:,1]==0) ,:]
    smoker=clustered_data[(clustered_data[:,0]==i) & (clustered_data[:,1]==1) ,:]
    
    treatment=np.mean(smoker[:,2])
    control=np.mean(nonsmoker[:,2])

    ATE+=treatment-control

ATE=ATE/n_clusters

print("Clustered Average Treatment Effct: " + str(ATE))











