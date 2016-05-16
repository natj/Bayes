model in neutrino_mo.bug
data in neutrino_da.dat
compile, nchains(3)
initialize
update 1000
monitor set m, thin(10)
update 10000
coda *
data to useddata
