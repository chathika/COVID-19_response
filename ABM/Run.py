import nl4py

nl4py.startServer('C:/Program Files/NetLogo 6.1.1')

n = nl4py.newNetLogoHeadlessWorkspace()

# open the meta-ABM
n.openModel('COVID-19_Main.nlogo')

# select Massachusetts
region = 'MA'
n.command('set Region "{}"'.format(region))

#### Parameters ####
# a value between 0 and 1 for the moment, which basically removes that fraction of agents from the local ABMs
isolation_intensity = 0.5 
# delay with which isolation is to take place after the first infected individuals are released
isolation_start = 20 
n.command('set isolate-at-intensity {}'.format(isolation_intensity))
n.command('set tick-to-begin-isolation {}'.format(isolation_start))

n.command('setup') # local ABMs are initialized, with the typical number of visitors


#### Objectives ####
measurements = []
# measure the contagion
measurements.append('mean [ count people with [covid-19-symptomatic]] ls:of ls:models')
# measure the economic impact
measurements.append('mean [current-economic-performance] of turtles')

# schedule and run simulation
n.scheduleReportersAndRun(reporters=measurements, stopAtTick=100)

# wait for results
n.awaitScheduledReporterResults()

# shutdown
nl4py.stopServer()