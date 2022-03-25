import pandas as pd
import networkx as nx
import numpy as np

'''
Class Snode

SNode is a mutable node which contains the list of champs associated 
with that particular origin or class. 
name = name of class or origin
champs = list of champions

@effects prints a string representation of the SNode
printNode()

No collaborators
'''
class SNode:

   def __init__(self, name, champ):
      self.champs = [champ]
      self.name = name #name of class or origin
      
   def printNode(self):
      print("NAME: ", self.name, "CHAMPS: ", self.champs)

'''
Class SGraph

This is a mutable graph which contains a dictionary of Synergy nodes. Each node contains all the champions 
connected to that origin or class. 
SDict = Dictionary of SNodes
possibleSyn = list of possible synergies. this list is returned in the findSyn()
file = name of file containing all of the data in edge list format 
line = current line we are reading from file
name = name of origin or class
champ = champoin associated with the name 
tempList = temporary list used to store current list of champions associated with a specific origin/ class
champList = list of current champions on the board. this list is used in findSyn()

@param champList 
@effects creates list of possible synergies
@return possible list of synergies
findSyn(given champion list)

@effects reads in file and creates an SGraph
@modifies creates and fills the SDict with SNodes
readfile()

I collaborated with Brian Hotopp while creating findSyn() 
'''
class SGraph:
   def __init__(self):
      self.SDict = {}
   #if champ is in specific synergy than add that synNode to possible 
   #list of class/origins   
   def findSyn(champList):
      possibleSyn = []
      for champ in champList:
         for synNode in SDict:
            if (SDict[synNode].champs.count(champ) == 1 and possibleSyn.count(synNode) == 0):
               possibleSyn.append(SDict[synNode].name)  
               
   def readFile():
      file = open("champEdge.txt", "rb")    
      with open("champEdge.txt") as file:
         for line in file:
            line = line.split(":")
            #print(line[1])
            #setting up data  
            name = line[0] 
            champ = line[1]
            # SDict = "Name" : Synergy Node
            #Checks if class or origin exists in SDict if not add, if it is there update SNode.champs and add champ      
            if (name in SDict and SDict[name].champs.count(champ) == 0):
               tempList = SDict[name].champs
               tempList.append(champ)
               SDict[name].champs = tempList         
            else:
               SDict[name] = SNode(name,champ) 
         file.close()
         
#"champEdge.txt"      
'''
champList = ['Ahri 4\n', 'Ashe 2\n', 'Braum 4\n', 'Darius 1\n', 'Morgana 3\n', 'Zyra 2\n']
print(SDict.keys())
possibleSyn = []
for champ in champList:
   for synNode in SDict:
      if (SDict[synNode].champs.count(champ) == 1 and possibleSyn.count(synNode) == 0):
         possibleSyn.append(SDict[synNode].name)    
print(possibleSyn)

#print(SDict["Syndicate"].champs)
''' 
