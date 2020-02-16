import random
import math
import pandas as pd
import numpy as np
import random

results = pd.DataFrame()
resultsValue = pd.DataFrame()

global finalPop
finalPop = [None]

class City:
    def __init__ (self, x, y):
        self.xVal = -1
        self.yVal = -1
        
        self.xVal = x
        self.yVal = y
    
class Agent:
    def __init__(self, val, agentId):
        self.genoma = [None] * (val + 1)
        self.distance = -1
        self.fitness = -1
        self.id = agentId
        self.probability = 0
        
    def getFitness(self):
        return self.fitness
    
    def setGenoma(self, newGene):
        self.genoma = list(newGene)

def citiesMatrix(val, cities):
    
    citiesArray = [None] * val
    
    for i in range (0,val):
        citiesArray[i] = City(cities.iat[i,0],cities.iat[i,1])
    
    return citiesArray
       
def initializePop(val):
    
    initPop = [None] * val
    
    for i in range (0, val):
        initPop[i] = Agent(val, i)
        
    return initPop

def initialEvaluation(genoma, citiesArray, index):
    
    citiesArray = citiesArray
    index = index
    euclidean = 0
    xp1 = 0
    yp1 = 0
    xp2 = 0
    yp2 = 0
    
    for j in range (0, len(genoma) - 1):
            
        xp1 = citiesArray[genoma[j]].xVal
        yp1 = citiesArray[genoma[j]].yVal
            
        xp2 = citiesArray[genoma[j+1]].xVal
        yp2 = citiesArray[genoma[j+1]].yVal
            
        euclidean += math.sqrt(((xp1 - xp2)**2) + ((yp1 - yp2)**2))
            
    return euclidean

def initialize(population, val):
    
    vals = [None] * val
    
    for i in range (0, len(vals)):
        vals[i] = i

    for i in range (0, len(population)):
        random.shuffle(vals)
        population[i].genoma = list(vals)

    for k in range (0, len(population)):
        population[k].genoma.append(population[k].genoma[0])
        
        
    return population

def breed(parent1, parent2):
    
    while True:
        
        child = []
        childP1 = []
        childP2 = []
        
        geneA = int(random.random() * len(parent1))
        geneB = int(random.random() * len(parent1))
        
        startGene = min(geneA, geneB)
        endGene = max(geneA, geneB)
              
        for i in range(startGene, endGene):
            childP1.append(parent1[i])

       
        childP2 = [item for item in parent2 if item not in childP1]
    
    
        child = childP1 + childP2
        
        if len(child) == 53:
            return child
        else:
            continue
    
def mutate (childGenoma, mutationRate): #mutação pelo método swap
    
    for i in range (0, len(childGenoma)):
        if(random.random() < mutationRate):
            swap = int(random.random() * len(childGenoma))
            
            city1 = childGenoma[i]
            city2 = childGenoma[swap]
            
            childGenoma[i] = city2
            childGenoma[swap] = city1
            
    childGenoma[len(childGenoma) - 1] = childGenoma[0]
    
    return childGenoma
    
class GA():
    
    global distanceVector
    distanceVector = [None] * 10000
    
    def __init__ (self, nCities, dataCities, iterator, mutationRate):
        self.nCities = nCities
        self.dataCities = dataCities
        self.iter = iterator
        self.popBestFit = []
        self.selected = []
        self.idSelec = []
        global finalPop
    
        #inicialização inicial dos elementos que serão iterados
        citiesArray = citiesMatrix(nCities, dataCities) #onde serão buscados os valores pra calcular a distancia
        population = initializePop(100) #cria a matriz de relação entre agente / cidade
        pop = initialize(population, nCities) #população com os agentes já com o DNA
        
        for i in range (0, len(pop)): #calculados os valores das distancias para cada agente
            pop[i].fitness = ((initialEvaluation(pop[i].genoma, citiesArray, i)))
        
        iterator = 0
        
        print("iniciando a evolução... ")
        while iterator < self.iter: #inicia-se as atividades de seleção / cruzamento / mutação
            total = 0
            probList = [] #tabela de probabilidades para o metodo da roleta
            tournament = []
            winner = []
            
############################# INÍCIO DA SELEÇÃO ################################################
            
            self.popBestFit = list(sorted(pop, key=lambda x: x.fitness))
            
            for i in range (0, len(pop)):
                self.popBestFit[i].fitness = ((initialEvaluation(self.popBestFit[i].genoma, citiesArray, i)))
            
            ################ROLETA##################
            
           # for i in range (0,len(self.popBestFit)):
            
             #   total += self.popBestFit[i].fitness
             
           # for i in range (0, len(self.popBestFit)):
                #probList.append(total / ((self.popBestFit[i].fitness * 100) / total))
                
            #self.selected = list(random.choices(self.popBestFit, weights = probList, k = int((len(self.popBestFit) / 2))))
            
            
            ############TORNEIO#############
            
            for i in range (0, int(len(self.popBestFit) / 2)):
                for i in range (0, int(len(self.popBestFit) /2)):
                    
                    tournament.append(random.choice(self.popBestFit))
                
                tournament = list(sorted(tournament, key=lambda x: x.fitness))
                
                winner.append(tournament[0])
            
            self.selected = list(winner)
   
            self.idSelec = [None] * len(self.selected)
            
            for i in range(0, len(self.selected)):
                self.idSelec[i] = self.selected[i].id
                
######################## FINAL DA SELEÇÃO - INÍCIO DO CRUZAMENTO ############################
            
            #CRUZAMENTO
            
            while self.selected != [] :
                candidate1 = None
                candidate2 = None
                childArray = [None]
                k = 0
                
                candidate1 = random.choice(self.selected)
                self.selected.remove(candidate1)
                
                if self.selected == [] :
                    break
                
                candidate2 = random.choice(self.selected)
                self.selected.remove(candidate2)
                
                childArray[k] = Agent(len(candidate1.genoma),-1)
                
            #CROSSOVER
                
                childArray[k].setGenoma(breed(candidate1.genoma , candidate2.genoma))
                childArray[k].genoma[len(childArray[k].genoma) - 1] = (childArray[k].genoma[0])
                
                k += 1
                                
            #MUTAÇÃO DOS FILHOS GERADOS
            
            for i in range (0, len(childArray)):
                
                childArray[i].genoma = list(mutate(childArray[i].genoma, mutationRate))
                
                
            for i in range (0, len(childArray)): #avaliação das distancias dos individuos gerados
                
                val = initialEvaluation(childArray[i].genoma, citiesArray, i)
                childArray[i].fitness = (val)
            
            for i in range (0, len(childArray)): #substituiçao dos individuos da antiga geração por individuos da nova geração
                for j in range (0, len(self.popBestFit)):
                    
                    if childArray[i].fitness < self.popBestFit[j].fitness:
                        
                        childArray[i].id = self.popBestFit[j].id
                        self.popBestFit[j] = childArray[i]
                        break
                
            self.popBestFit = list(sorted(self.popBestFit, key=lambda x: x.fitness))            
            
            finalPop = list(self.popBestFit[0].genoma)
            distanceVector[iterator] = self.popBestFit[0].fitness
                
            k += 1
            pop = list(self.popBestFit)
            self.selected = []
            print("geração:" + str(iterator))
            iterator += 1
        
if __name__ == "__GA__":
    main()
    
val = 52 #numero de ciades 
cities = pd.read_csv(f'distCidades2.csv', sep = ";") #arquivo contendo as distancias das cidades
mutationRate = 0.01 #taxa de mutação

GA(val, cities, 10000, mutationRate) #inicialização do algoritmo genético


print("melhor fitness: " + " " +str(distanceVector[len(distanceVector) - 1]))
    
print("melhor população: " + str(finalPop))

results[f'sim_{47}'] = distanceVector

results.to_csv(f'GA_genetic_algorithm.csv', index=False) 


    

    

         
        
        
        
        
        
        
        
        
        
        