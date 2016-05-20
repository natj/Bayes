model in model.bug
data in data9.1.2.dat.R.txt
compile, nchains(3)
initialize
update 1000
monitor set intrscat, thin(10)
monitor set alpha, thin(10)
monitor set beta, thin(10)
monitor set gamma, thin(10)
update 100000
coda *
data to useddata
