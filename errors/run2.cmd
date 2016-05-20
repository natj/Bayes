model in model.bug
data in molaro.dat.R.txt
compile, nchains(3)
initialize
update 1000
monitor set sigmai, thin(10)
monitor set alpha, thin(10)
monitor set beta, thin(10)
update 100000
coda *
data to useddata
