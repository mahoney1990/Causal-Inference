library(tidyverse)
#Data set: 
data <- read_csv("https://raw.githubusercontent.com/gckc123/ExampleData/main/smoking_psyc_distress.csv")

#Logit to predict treatment status
stage_one=glm(smoker~sex+indigeneity+high_school+partnered+remoteness,
            data=data,
            family = "binomial")

#Extract vectors
scores=predict(stage_one)
probs=exp(predict(stage_one))
smoke=data$smoker
distress=data$psyc_distress

#Build new dataframe
mat=matrix(0,length(smoke),3)
mat[,1]=scores
mat[,2]=smoke
mat[,3]=distress

match_data=data.frame(mat)
colnames(match_data)=c('scores','smoke','distress')
rm(mat)

#Sort by smoke variable, decending. This will make things easier for us
match_data=match_data[order(-smoke),]
index=which(match_data$smoke==1)

#Implement 1 Nearest Neighbor to find closest scores of smokers with nonsmokers
#Linear search is inefficient, but we've got enough computer to do it (we'll add a better
#algorithm later)

#Split data into smokers and nonsmokers
smokers=match_data[index,]
nonsmokers=match_data[-c(index),]

#Grab lengths
N=length(smokers[,1])   #Number of smokers
M=length(nonsmokers[,1]) #Number of nonsmokers


match_index=matrix(0,N,1)
treatment=matrix(0,N,1)

for(i in 1:N){
  #Vector of zeros to hold our distances
  diff_scores=matrix(0,M,1)
  
  #Grab ith smoker score
  smoke_score=smokers$scores[i]
  
  #Loop through nonsmoker scores, find the closest 
  diff_scores=abs(smoke_score-nonsmokers$scores)

  #Here, we are tracking the match index for each smoker, not nessesary by doable  
  match_index[i]=which.min(diff_scores)

  #Indiv treatment effect is the difference between distress scores fro each treatment
  # and its closest nonsmoking counterpart. 
  treatment[i]=(smokers$distress[i]-nonsmokers$distress[match_index[i]])
}

#Average over all smokers -- lets see how miserable these guys are.
treatment_effect=sum(treatment)/N
print(treatment_effect)

#Quick t-test for sanity
var_distress=var(treatment)
t_val=treatment_effect/sqrt(var_distress/N)

print(t_val) #Damn, they really are more miserable













