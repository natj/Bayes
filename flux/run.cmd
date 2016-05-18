model in model.bug
data in data.dat
compile, nchains(3)
initialize
update 1000
monitor set s, thin(10)
update 100000
coda *
data to useddata
