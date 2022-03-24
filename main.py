import pandas as pd
import networkx as nx
import numpy as np

'''
Class Snode

SNode is a mutable node which contains the list of champs associated 
with that particular origin or class. 
name = name of class or origin
champs = list of champions

No collaborators
'''
class SNode:
   champs = []
   def __init__(self, name, champs):
      if (self.champs.count(champs) == 0):
         print(champs)
         self.champs.append(champs) #list of champs 
      self.name = name #name of class or origin

class SGraph:
   def __init__(self):
      self.SList = {}
      
   #if champ is in specific synergy than add that synNode to possible 
   #list of class/origins   
   def findSyn(champList):
      possibleSyn = []
      for champ in champList:
         for synNode in SList:
            if (synNode.champs.find(champ)):
               possibleSyn.append(synNode.name)      
      
    
file = open("champEdge.txt", "rb")    
SDict = {}
with open("champEdge.txt") as file:
   for line in file:
      line = line.split(":")
      #print(line[1])
      #setting up data  
      name = line[0]      
      champ = line[1]
      print(name, champ)
      
      snode = SNode(name,champ)
      print(snode.champs)
      SDict[name] = snode      
      
      # SDict = "Name" : Synergy Node
      #Checks if class or origin exists in SDict if not add, if it is there update SNode.champs and add champ
'''      
      if (name in SDict and SDict[name].champs.count(champ) == 0):
         print(name)
         tempList = SDict[name].champs
         tempList.append(champ)
         SDict[name].champs = tempList
         print(tempList)
      else:
         snode = SNode(name,champ)
         SDict[name] = snode
      
print(SDict["Syndicate"].champs)
 '''
file.close()
'''
#f = open("champEdge.txt","w")
#G = nx.read_adjlist(file,  nodetype = Node, delimiter = "\n")

#print(nx.number_of_nodes(G))

for node in G:
   line = node.data.split(",")
   gname = line[0]
   temp = GNode(gname)
   for i in range(1,len(line)):
      if (line[i] != ""):
         f.write( line[i] + ":" +temp.name+ "\n")   
         
         

   

f.close()
f = open("champEdge2.csv","rb")
G2 = nx.read_edgelist(f, delimiter = ",")
f.close()

for node in G2:
   print(node)
print(nx.number_of_nodes(G2))

   file = open("champsVer2.csv", "rb")
   G = nx.read_adjlist(file,  nodetype = Node, delimiter = "\n")
   file.close()
   print(nx.number_of_nodes(G))
   for node in G:
      line = node.gold.split(",")
      name_str = line[0] + " " + line[1]
      #node.name = name_str
      print (line[:2])
   
   
   if node in G:
   
   
   def findSynergies(G):
       for node in G:
           if 
   '''  