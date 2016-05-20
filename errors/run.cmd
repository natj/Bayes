model in model.bug
data in data8.2.dat.R.txt
compile, nchains(3)
initialize
update 1000
monitor set A, thin(10)
monitor set B, thin(10)
monitor set mu, thin(10)
monitor set sigma, thin(10)
update 100000
coda *
data to useddata
