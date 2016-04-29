from math import *
from Kilobot import *
from sys import *
import random
import numpy
from collections import defaultdict
from timeit import default_timer as timer  #to determine the time of simulation

def load(sim):
    return QL(sim)

class QL(Kilobot): 
    def __init__(self, sim):
        Kilobot.__init__(self, sim)
	
	self.add = open("Qfile.txt",'wb')
	self.addtime = open("Run_Time.txt",'wb')
	
	self.steps = 0    #number of steps
	self.episodes=0   # number of episodes 
	
	self.goal=0;   #reach the goal ?
	
	self.MAXsteps=10000 #number maximum of steps 
	self.MAXepisodes = 100 #number maximum of episodes


	#QL
	self.QL = defaultdict(int)

	#Q-Learning configuration 

	self.epsilon = 0.1
	self.alpha = 0.2
	self.gamma = 0.9
	self.actions = 4
	self.reward = -1
	
	#######################
	
        self.id = self.secretID

        
	self.state1 =0
	self.state2 =0
	self.first = 1
	
	##########agent values to determine every states
	self.D0=0 #Distance of agent 0
	self.D1=0 #Distance of agent 1
	self.px=0 #value X of agent 0
	self.py=0 #value Y of agent 1
	self.qx=0
	self.qy=0
	
	
	self.posAg0=0  #where is the agent 0 ?
	self.posAg1=0  #where is the agent 1 ?

        self.distance = 0  #distance
	self.var_data = [0x00, 0x00, 0x00]
	self.var_state=[0,0]

	#The programa Start here !!!

	self.program = [self.setmsg,
			self.run,
			self.loop
			]
	
	
	
###############################
    def run(self):

	if (self.id == 2):
	    if(self.first ==1): #reset Q table !
		self._resetQ()
		start = timer() #start the times
	    
	    self.first = 0
	
################################## Here is the QL  ##########################################################

	    self.vstatefisrt=self._state()  							# Get the state.
	    self.action=self._chooseaction(self.vstatefisrt)					#choice action
	    self._applyaction (self.action)							#apply action
	    self.vstateend=self._state()							#save the new state
	    self.reward = self._reward(self.vstateend)					#get reward
	    self._QL_update(self.vstatefisrt,self.vstateend,self.reward,self.action) 	        #update QL
	    
	    #print self.vstatefisrt   # just to show if is working
	  
############################ UPDATE QL ###################################
    def _QL_update(self,state,stateN,reward,action):
	
	self.best_a=self._chooseargmax(stateN) #chose the best action
	self.QLNew=self._getQ(stateN, self.best_a) 
	self.QLold=self._getQ(state, action)
	self.Qupdate=0
	
	#delta value of QL
	delta= ((reward) + ((self.gamma*self.QLNew) - self.QLold))
	
	self.QL[state[0],state[1],action]=self.QLold+(self.alpha*delta)
	
	

########################################
    
	
##################   RESET QL TABLE ####################

    def _resetQ(self):
	print "table erased"
	loop0=0
	loop1=0
	loop2=0
	for loop0 in range(200):
	    for loop1 in range(200):
		for loop2 in range(self.actions):
		    self.QL[loop0, loop1, loop2] = random.random() #set the table with random numbers
		    
	
################# VALUE OF Q #############

    def _getQ(self, state, action):
	self.value=self.QL[state[0],state[1],action]
	return	self.value
    
###################CHOOSE ACTION ##############################

    def _chooseaction(self, state):
	
	self.temp= -10000
	self.vQ =0
	self.action =0
	a=0
		
        if (random.random() < self.epsilon):  #EXPLORATION 
	    self.action=int(random.uniform(0,self.actions))
	
	else:  #EXPLOTATION
	       
	    for a in range(self.actions):
		self.vQ = self.QL[state[0],state[1],a]
		if self.vQ > self.temp:
		    self.temp=self.vQ
		    self.action=a

        return self.action
    
################ CHOOSE ARG MAX ###############################

    def _chooseargmax(self, state):
	
	self.vstate2=state
	self.temp= -10000
	self.vQ
	self.action  	

	for a in range(self.actions):
	    self.vQ=self.QL[state[0],state[1], a]
	    if self.vQ > self.temp:
		self.temp=self.vQ
		self.action=a

        return self.action

####################################################

    def _state(self):
    
	self.get_message()
 
	self.set_color(3,0,0)

        if (self.msgrx[5] == 1):
		if(self.msgrx[0] == 0):
			self.px=self.msgrx[1]
			self.py=self.msgrx[2]
			#self.D0=self.msgrx[3]
			
		if(self.msgrx[0] == 1):
			self.qx=self.msgrx[1]
			self.qy=self.msgrx[2]
			#self.D1=self.msgrx[3]

	if (self.id == 2):
	    pos = self.pos.inttup()
	    p0x=(pos[0]-self.px)*(pos[0]-self.px)
	    p0y=(pos[1]-self.py)*(pos[1]-self.py)
	    self.D0=int(sqrt(p0x+p0y))
	    p1x=(pos[0]-self.qx)*(pos[0]-self.qx)
	    p1y=(pos[1]-self.qy)*(pos[1]-self.qy)
	    self.D1=int(sqrt(p1x+p1y))
	
	return self.D0,self.D1
    
 
####################################################################################
    def _reward(self,estate):
	reward=0
	if estate[0] < 60 or estate[1] < 60 :
	    reward = 10
	if estate[0] < 60 and estate[1] < 60 :
	    reward = 100
	    self.goal += 1
	else:
	    reward = -1
 
	return reward

####################################################################################
    def setup(self):
	  print self.secretID
	  
	  
	  
####################################################################################	  
    def _applyaction (self, action):
	if action ==0:
	    self.fullFWRD()
	    
	if action ==1:
	    self.fullCCW()
	    self.fullCCW()
	    self.fullCCW()
	    self.fullCCW()
	    self.fullCCW()
	    
	    
	    
	if action ==2:
	    self.fullCW()
	    self.fullCW()
	    self.fullCW()
	    self.fullCCW()
	    self.fullCCW()
	    
	
	if action ==3:    #do nothing
	    self.stop()
	

######################################################################################

    def setmsg(self):
	pos = self.pos.inttup()
	ID=self.id
	self.enable_tx()
	
	if(self.id == 0 or self.id == 1):
	    self.stop()
	     
	    self.message_out(ID,pos[0],pos[1])
	    #print pos[0], pos[1], self.id
	    #self.reset_rx()


    def hold(self):
        self.PC -= 1
	
	
    def _record(self, numero, valor ):
	print "Record Table"
	s1=str(numero)
	s2=str(valor)
	self.add = open("Qfile.txt","a")
	self.add.write(s1)
	self.add.write(' ')
	self.add.write(s2)
	self.add.write('\n')
	self.add.close()
	
	
    def loop(self):
	
	if (self.id == 2):
	    self.steps += 1 # number of steps
	
	#print "(steps Ep)",self.step,self.episode  #just to test
	
        if (self.steps > self.MAXsteps): # interacoes
    	    
	    self._record(self.episodes,self.goal)    
	    self.episodes +=1
	    self.steps=0
	    self.goal=0
	    
	if (self.episodes > self.MAXepisodes):
	    end = timer() #finish timer
	    TimeRun=end-start
	    print "Final Simulacao"
            print "The simulation run for" % TimeRun
	    #self.file.close()
	    #self.PC -= 1
	    exit(-42)
            return
    
    
    
	
	
   
        
        


