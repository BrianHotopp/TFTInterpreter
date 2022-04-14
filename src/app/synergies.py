import os

'''
Class Snode

SNode is a mutable node which contains the list of champs associated 
with that particular composition
name = name of composition
champs = list of champions

@effects prints a string representation of the SNode
printNode(self)

No collaborators
'''
class SNode:

   def __init__(self, name, champ):
      self.champs = [champ]
      self.name = name
      
   def printNode(self):
      print("NAME: ", self.name, "CHAMPS: ", self.champs)

'''
Class SGraph

This is a mutable graph which contains a dictionary of SNode nodes. Each node contains all the champions 
connected to a specific composition

SDict = Dictionary of SNodes
possibleUnits = list of possible units that would fill a composition
possibleComps = list of possible compositions
file = name of file containing all of the data 
line = current line we are reading from file
name = name of composition
champ = champoin associated with the name 
tempList = temporary list used to store current list of champions associated with a specific composition
champList = list of current champions on the board. this list is used in findSyn()

@param champList 
@effects creates list of compositions
@return possible list of units 
findComp(given champion list)

@effects reads in file and creates an SGraph
@modifies creates and fills the SDict with SNodes
readfile(self, given file name)

I collaborated with Brian Hotopp while creating findComp(given champ list) 
'''
class SGraph:
   def __init__(self):
      self.lvl4 = {
         0: ["poppy","ziggs","blitzcrank","vex"],
         1:["darius","morgana","senna","braum"],
         2:["ziggs","corki","vex","jinx"],
         3:["ziggs","gnar","vex","irelia"],
         4:["darius","zyra","braum","silco"],
         5:["jarvaniv","lucian","irelia","jinx"],
         6:["warwick","tryndamere","renata","silco"],
         7:["lucian","irelia","sivir","jinx"]
         }
      self.lvl5= { 0: ["caitlyn","zilean","jhin","seraphine","jayce"] }
      self.lvl6 ={}
      self.lvl7 = {}
      
   #find what comps have champs in there
   #if the comps already in possibleComps list skip
   #if not add that comp to possibleComps
   #Then match the comps from possibleComps 
   #return what units aren't in comps in possibleUnits
   
   
   def findComp(self,champList):
      for i in range (len(champList)):
         champList[i] = champList[i].lower()
      champList = set(champList)
      possibleUnits = {}
      possibleComps = {}
      
      if(len(champList) <= 4):
         for i in range(8):
            #lvl 4
            diffSet= set(self.lvl4.get(i)).difference(champList)
            if (len(diffSet) != len(self.lvl4.get(i)) and len(diffSet) != 0):
               index = i + 400
               possibleComps[index] = diffSet
      
         #lvl 5
      diffSet= set(self.lvl5.get(0)).difference(champList)
      if (len(diffSet) != len(self.lvl5.get(0))):
         possibleComps[500] = diffSet
            
      if(len(champList) >=5):
         for i in range(71):
            diffSet= set(self.lvl6.get(i)).difference(champList)
            if (len(diffSet) != len(self.lvl6.get(i)) and len(diffSet) != 5):
               index = i + 600
               possibleComps[index] = diffSet   
              
         for i in range(25):
            diffSet= set(self.lvl7.get(i)).difference(champList)
            if (len(diffSet) != len(self.lvl7.get(i))):
               index = i + 700
               possibleComps[index] = diffSet    
      
      if len(possibleComps) == 0:
         return []

      unitDict = possibleComps.popitem()
      unitSet = unitDict[1]
      for i in range (len(possibleComps)):
         unitDict = possibleComps.popitem()
         unitSet = unitSet.union(unitDict[1])
         possibleUnits["Consider buying these units: "] = unitSet

      return list(unitSet)
   
   def readFile(self):
      compIndex = -1
      lvl7_file = os.path.join(os.path.dirname(__file__), 'lvl7.txt')
      file = open(lvl7_file, "rb")
      
      with open(lvl7_file) as file:
         for line in file:
            line = line.split("[")
            line = line[1].split(",")
            compIndex += 1
            tempList = []
            for i in range (len(line)-1):
               name = line[i].strip('""')
               tempList.append(name)    
            name = line[-1].strip('""')  
            if(name[-1] == ']'):
               name = name[0:-3]
            else:
               name = name[0:-5]
            tempList.append(name)
            self.lvl7[compIndex] = tempList
      file.close()
      
      compIndex = -1
      lvl6_file = os.path.join(os.path.dirname(__file__), 'lvl6.txt')
      file = open(lvl6_file,"rb")
      with open(lvl6_file) as file:
         for line in file:
            line = line.split("[")
            line = line[1].split(",")
            compIndex += 1
            tempList = []
            for i in range (len(line)-1):
               name = line[i].strip('""')
               tempList.append(name)    
            name = line[-1].strip('""')  
            if(name[-1] == ']'):
               name = name[0:-3]
            else:
               name = name[0:-5]
            tempList.append(name)
            self.lvl6[compIndex] = tempList
      file.close()
'''
sample main:
G = SGraph() 
G.readFile()
G.findComp(["Lucian","irElia","sivir","jinx",'swain',"zilean"])
output: ['corki', 'galio', 'gnar', 'illaoi', 'viktor', 'singed', 'camille', 
         'zac', 'vex', 'orianna', 'alistar', 'poppy', 'seraphine', 'silco', 
         'ziggs', 'lulu', 'warwick', 'jarvaniv', 'vi', 'tryndamere', 'renata', 
         'tahmkench', 'blitzcrank', 'ezreal', 'jayce', 'jhin', 'caitlyn', 
         'sejuani', 'senna', 'gangplank']
'''