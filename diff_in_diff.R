#Just a quick little template for DID estimation I grabbed off a little
#example page from Princeton. Also a little practice with ggplot

library(foreign)
mydata = read.dta("http://dss.princeton.edu/training/Panel101.dta")

library(ggplot2)

#The outcome variable y is scaled to be massive. Lets fix that
mydata$y=mydata$y/1000000 #Much better

#Create dummy for post treatment period
year_idx=mydata$year>=1994
mydata$time=as.integer(treat_idx)

#Create dummies for treated nations
mydata$treatment=ifelse(mydata$country=='E' | 
                        mydata$country=='F' |
                        mydata$country=='G',1,0)

#Create interaction between time and treatment
mydata$interact=mydata$treatment*mydata$time

#The key assumption in DID is that in the pretreatment period there is a
#relatively constant difference between treated and controls. i.e. they 
#have parallel trends
treat_idx=which(mydata$treatment==1)
control_idx=which(mydata$treatment==0)

#Plots -- kinda looks like parallel trends, its hard to tell
ggplot(data=mydata, aes(x=year, y=y, group=country)) +
  geom_line(aes(color=country))+
  geom_point(aes(color=country))


#Plots -- kinda looks like parallel trends, its hard to tell
ggplot(data=mydata, aes(x=year, y=y, group=country)) +
  geom_line(aes(color=treatment))+
  geom_point(aes(color=treatment))

#Looks pretty parallel.But we still might have problems. Its possible that
#the outcome variable y influences assignment to treatment. Lets disabuse
#ourselves of that notion. Idea run a logit, see if y predicts treatment before 1994 

predata=mydata[mydata$year<1994,]
model=glm(treatment~y, data=predata,family='binomial')
summary(model)

#Ok were good. Now we just run a basic regression:

model=lm(y ~ time+treatment+interact,data=mydata)

#The coefficient on 'interact' is the DID effect. Looks like its significant!
summary(model)

