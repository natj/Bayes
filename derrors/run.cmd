model in model.bug
data in data8.4.dat.R.txt
compile, nchains(3)
initialize
update 1000
monitor set intrscat, thin(10)
monitor set a, thin(10)
monitor set b, thin(10)
update 100000
coda *
data to useddata
