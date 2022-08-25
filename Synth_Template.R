#Just a little more practice with the Synth package
#The data here is totally contrived, but our goal is to
#Make a template for using this package

library(dplyr)
library(Synth)

data("synth.data")

#Lets rescale things before we start building matrices
synth.data$X1=100*synth.data$X1


#The Synthetic Control functions require matrices formatted in a very specific manner
#However, they include a little utility to format everything for us. How nice of them.

rev_data=dataprep(foo=synth.data,
                  dependent = 'Y',
                  predictors = c('X1','X2','X3'),
                  predictors.op = 'mean',
                  
                  #Define time parameters
                  time.predictors.prior = c(1984:1989),
                  time.variable = c('year'),
                  
                  #Define unit parameters
                  unit.variable = c('unit.num'),
                  unit.names.variable = c('name'),
                  
                  #Identify treatment unit
                  treatment.identifier = 7,
                  
                  #Identify control units
                  controls.identifier = unique(synth.data$unit.num)[-2],
                  
                  time.optimize.ssr = c(1984:1990),
                  time.plot = c(1984:1994)
                  )

#Okay now we've got our properly formatted list of matrices. Lets form our syntheic control
#weights with the Synth function.

synth_out=synth(rev_data)

#Beautiful, stunning, impeccable!
#Recover weights in a table
synth_tables=synth.tab(synth_out, dataprep.res = rev_data)
print(synth_tables)

#Construct series and gaps plots
path.plot(synth_out, dataprep.res = rev_data)
gaps.plot(synth_out, dataprep.res = rev_data)





