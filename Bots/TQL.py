
from math import *
from Kilobot import *
from sys import *
import random
import numpy
from collections import defaultdict
import datetime
import time

def load(sim):
    return QL(sim)

class QL(Kilobot): 
    def __init__(self, sim):
        Kilobot.__init__(self, sim)
	
	
	self.arquivo2 = open('TLarquivo.txt', 'wb')
	
	#### valores maximos #########
	self.MAXpassos=1000
	self.MAXepisodios = 100
	self.NumCasos = 20
	self.MAXobjetivo=5500;
	
	#############################

	
	self.passos = 0
	self.episodios=0
	
	
	self.objetivo=0;

	#QL
	self.QL = defaultdict(int)
	self.H = defaultdict(int)
	
	self.Casos = defaultdict(int)

	self.epsilon = 0.1
	self.alpha = 0.2
	self.gamma = 0.9
	self.actions = 4
	self.reward = -1
	
	#######################
	
        self.id = self.secretID

        
	self.estado1 =0
	self.estado2 =0
	self.primeira = 1
	
	######################agente
	self.Dfinal=300
	self.Dinicial=0
	self.D0=0
	self.D1=0
	self.px=0
	self.py=0
	self.qx=0
	self.qy=0
	self.posAg0=0
	self.posAg1=0
	self.var_data = [0x00, 0x00, 0x00]
	self.var_estado=[0,0]

	#aqui comeca
	
	if (self.id == 2):
	    self._resetQ()
	    self._resetCasos()
	    validacao= self._CarregaCasos() #carrega heuristica
	    if validacao == 0:
		print "Oh,Oh! Algo errado com o arquivo de regras"
		exit(-42)
	    
	self.t1 = time.time()

	self.program = [self.setmsg,
			self.run,
			self.loop
			]
	
	
	
###############################
    def run(self):
#
	if (self.id == 2):
#	    if(self.primeira==1): #reseta tabela Q
#		self._resetQ()
#		
#	    
#	    self.primeira = 0
	
################################## Aqui comeca o QL ##########################################################

	    self.vstateinicial=self._estado()  							# determinar o estado
	    self.Dinicial=self._ComparaCasos(self.vstateinicial)				#determina dist ate objetido
	    
	    
	    
	    self.action=self._Hchooseaction(self.vstateinicial)					#escolhe a acao
	    self._applyaction (self.action)							#executa a acao
	    self.vstatefinal=self._estado()							#determina o novo estado
	    
	    self.Dfinal=self._ComparaCasos(self.vstatefinal)					#determina distancia depois da acao
	    
	    self._updadeTransfer(self.Dinicial,self.Dfinal,self.vstateinicial,self.action)
	    
	    self.reward = self._reward(self.vstatefinal)					#recompensa
	    self._QL_update(self.vstateinicial,self.vstatefinal,self.reward,self.action) 	#atualiza QL
	    
	    #print self.Dinicial,self.Dfinal
	    
########################################

    def _QL_update(self,estado,estadoN,reward,action):
	
	self.best_a=self._chooseargmax(estadoN)
	self.QLNew=self._getQ(estadoN, self.best_a)
	self.QLold=self._getQ(estado, action)
	self.Qupdate=0
	
	#calcula delta
	delta= ((reward) + ((self.gamma*self.QLNew) - self.QLold))
	
	self.QL[estado[0],estado[1],action]=self.QLold+(self.alpha*delta)

#################################################################
    def _updadeTransfer(self,Di,Df,E,action):
	
	    if(Df>Di):
		self.H[E[0], E[1], action] = -10
	    if(Di>Df):
		self.H[E[0], E[1], action] = 10
	
###############################################################
    def _CarregaCasos(self): #
	
	print "Carregando Casos"
	caso=defaultdict(int)
	
	try:
	    self.casos = open('regras.txt', 'r')
	    loop0=0
	    loop1=0
	    loop2=0
	    for loop0 in range(self.NumCasos):
			caso=self.casos.readline()
			n_caso_a=caso[0]
			n_caso_b=caso[1]
			v_caso_a=caso[3]
			v_caso_b=caso[4]
			v_caso1=v_caso_a+v_caso_b
			v_caso_a=caso[6]
			v_caso_b=caso[7]
			v_caso2=v_caso_a+v_caso_b
			self.Casos[loop0,0]= int (v_caso1)
			self.Casos[loop0,1]= int (v_caso2)
			
			
	    return 1
	    
	except:
	    return 0

#################################################################
    def _ComparaCasos(self,estado):
	vx=estado[0]
	vy=estado[1]
	temp=1000
	estado_a=0
	estado_b=0
	
	for loop0 in range(self.NumCasos):
	    v1=(vx-self.Casos[loop0,0])*(vx-self.Casos[loop0,0])
	    v2=(vy-self.Casos[loop0,1])*(vy-self.Casos[loop0,1])
	    D=int(sqrt(v1+v2))
 
	return D	    


##################################################################

    def _resetCasos(self):
	print "Limpando tabela de Casos"
	for loop0 in range(10):
	    for loop1 in range(2):
		self.Casos[loop0,loop1] =0
		

    def _resetQ(self):
	print "Inicializando tabela Q"
	loop0=0
	loop1=0
	loop2=0
	
	for loop0 in range(200):
	    for loop1 in range(200):
		for loop2 in range(self.actions):
		    self.QL[loop0, loop1, loop2] = random.random()
		    self.H[loop0, loop1, loop2] = 0
		    
################################################################

    def _getQ(self, state, action):
	#print action
	self.value=self.QL[state[0],state[1],action]
	#print self.value
	return	self.value
    
##########################################################

    def _chooseaction(self, state):
	
	self.temp= -10000
	self.vQ =0
	self.action =0
	a=0
	
	#print state[0],state[1]
		
        if (random.random() < self.epsilon):
	    self.action=int(random.uniform(0,self.actions))
	
	else:
	   
	    
	    for a in range(self.actions):
		self.vQ = self.QL[state[0],state[1],a]
		if self.vQ > self.temp:
		    self.temp=self.vQ
		    self.action=a

        return self.action
    
####################################################
    def _Hchooseaction(self, state):
	
	self.temp= -10000
	self.vQ =0
	self.action =0
	a=0
		
        if (random.random() < self.epsilon):
	    self.action=int(random.uniform(0,self.actions))
	
	else:
	   
	    
	    for a in range(self.actions):
		self.vQ = self.QL[state[0],state[1],a]+self.H[state[0],state[1],a]
		if self.vQ > self.temp:
		    self.temp=self.vQ
		    self.action=a

        return self.action
    
####################################################

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


    def _estado(self):
    
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
    def _reward(self,estado):
	reward=0
	if estado[0] < 60 or estado[1] < 60 :
	    reward = 10
	if estado[0] < 60 and estado[1] < 60 :
	    reward = 100
	    self.objetivo += 1
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
	    
	
	if action ==3:
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
	
	
    def _grava(self, numero, valor ):
	print "Gravando tabela"
	s1=str(numero)
	s2=str(valor)
	self.adicionar = open("TLarquivo.txt","a")
	self.adicionar.write(s1)
	self.adicionar.write(' ')
	self.adicionar.write(s2)
	self.adicionar.write('\n')
	self.adicionar.close()
	
    def loop(self):
	
	if (self.id == 2):
	    self.passos += 1 # conta as interacoes
	
	#print "(Passos Ep)",self.passos,self.episodios
	
	
	#print self.interacao
	
        if (self.passos > self.MAXpassos): # interacoes
	    
	    print self.episodios, self.passos
	    self._grava(self.episodios,self.objetivo)
	    
	    
	    self.episodios +=1
	    self.passos = 0
	    #self.objetivo=0
	    
	    #print self.episodios, self.passos
	    #self.primeira = 1
	    
	if (self.episodios > self.MAXepisodios):
	    t2 = time.time()
	    diff=(datetime.datetime.fromtimestamp(self.t1) - datetime.datetime.fromtimestamp(t2))
	    print('difference is {0} seconds'.format(abs(diff.total_seconds())))
	    print "Final Simulacao"
	    #self.arquivo.close()
	    #self.PC -= 1
	    exit(-42)
            return
    
    
    
	
	
   
        
        


