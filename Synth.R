#Replication of Abadie 2003 using the synth package


library(Synth)

data(basque)

#Step one:  form list object for synth control estimation
#Convert data to work with synth package
#We need to tell the package what our predictors are
rev_data=dataprep(foo=basque,
         predictors = c("school.illit","school.prim","school.high",'invest'),
         predictors.op = 'mean',
         dependent='gdpcap', #Outcome variable
         unit.variable = "regionno", #Specify which var represents individual
         time.variable = c('year'), #Specify which variable represents time
         treatment.identifier = 17, #Speicfy which region code is Basque country
         controls.identifier = c(2:16,18), #Controls to make a synthetic Basque country
         time.predictors.prior = c(1964:1969),
         time.optimize.ssr = c(1962:1969),
         time.plot=c(1955:1997),
   
)
#The dataprep function creates a list 

#Step two: standardize 
#We've got problems! Namely, the schooling variables are in counts, so the largest category (primary)
#Will get all the weight. We need to standardize our variable scale.

#Lets convert schooling variables to population proportions
lower=which(rownames(rev_data$X0)=="school.illit")
upper=which(rownames(rev_data$X0)=="school.high")

#Convert schooling measures to proportions -- control provinces
#Grab total counts
totals=sum(rev_data$X1[lower:upper])

#Convert to props
rev_data$X1[lower:upper,]=rev_data$X1[lower:upper]/totals

#Convert schooling measures to proportions -- treatment province
#Grab total counts
totals=sum(rev_data$X0[lower:upper])

#Convert to props
rev_data$X0[lower:upper,]=(100*scale(rev_data$X0[lower:upper,],
                                     center=FALSE,
                                     scale=colSums(rev_data$X0[lower:upper,])))


#Okay now that our standardization is complete lets actually recover some weights
#Find optimal weights on other provinces to construct a synthetic Basque Country
synth_out=synth(data.prep.obj = rev_data)
synth_tables=synth.tab(dataprep.res = rev_data, synth.res=synth_out)

#Display province wieghts
print(synth_tables)

#Visualize results
#Visual 1: Path plots -- Basque and synthetic Basque
path.plot(synth.res = synth_out,
          dataprep.res = rev_data,
          Ylab = c("per-capita GDP"),
          Xlab = c("year"),
          Ylim=c(0,10)
          )

gaps.plot(synth.res = synth_out,
          dataprep.res = rev_data,
          Ylab=c('GDP gap'),
          Xlab=c('year')
)
    
#Notice that post treatment (i.e. Separatist terrorism in the 1970s) GDP falls below
#sythetic predictions! The synthetic control works! Huzzah!












