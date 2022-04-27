#!python

class SNode:
   """
   SNode is a mutable node which contains the list of champs associated 
   with that particular composition.
   """
   def __init__(self, name, champ) -> None:
      """
      Initialize an SNode object with the list of units and name of composition.
      Args:
         name: name of composition
         champ: list of units
      """
      self.champs = [champ]
      self.name = name
      
   def printNode(self) -> None:
      """
      Prints the name of the composition and the units.
      """
      print("NAME: ", self.name, "CHAMPS: ", self.champs)

'''
Class SGraph



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

'''
class SGraph:
   def __init__(self) -> None:
      """
      Initialize an SGraph object.
      This is a mutable graph which contains a dictionary of SNode nodes.
      Each node contains all the champions connected to a specific composition.
      """
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

   def findComp(self, champList: list) -> list:
      """
      Find what comps have units in the given list.
      Args:
         champList: list of units
      Returns:
         unit list containing the given list
      """

      #if the comps already in possibleComps list skip
      #if not add that comp to possibleComps
      #Then match the comps from possibleComps 
      #return what units aren't in comps in possibleUnits
      for i in range (len(champList)):
         champList[i] = champList[i].lower()
      champList = set(champList)
      possibleUnits = {}
      possibleComps = {}
      
      # level 4
      if(len(champList) <= 4):
         for i in range(8):
            diffSet= set(self.lvl4.get(i)).difference(champList)
            if (len(diffSet) != len(self.lvl4.get(i)) and len(diffSet) != 0):
               index = i + 400
               possibleComps[index] = diffSet
      
      #lvl 5
      diffSet= set(self.lvl5.get(0)).difference(champList)
      if (len(diffSet) != len(self.lvl5.get(0))):
         possibleComps[500] = diffSet
            
      # levels 6 and 7
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
      
      unitDict = possibleComps.popitem()
      unitSet = unitDict[1]
      for i in range (len(possibleComps)):
         unitDict = possibleComps.popitem()
         unitSet = unitSet.union(unitDict[1])
         possibleUnits["Consider buying these units: "] = unitSet

      return list(unitSet)
   
   def readFile(self) -> None:
      """
      Read the level 6 and 7 files.
      """
      compIndex = -1
      file = open("lvl7.txt","rb")
      with open("lvl7.txt") as file:
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
      file = open("lvl6.txt","rb")
      with open("lvl6.txt") as file:
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

if __name__ == '__main__':
   G = SGraph() 
   G.readFile()
   G.findComp(["Lucian","irElia","sivir","jinx",'swain',"zilean"])
   # output: ['corki', 'galio', 'gnar', 'illaoi', 'viktor', 'singed', 'camille', 
   #          'zac', 'vex', 'orianna', 'alistar', 'poppy', 'seraphine', 'silco', 
   #          'ziggs', 'lulu', 'warwick', 'jarvaniv', 'vi', 'tryndamere', 'renata', 
   #          'tahmkench', 'blitzcrank', 'ezreal', 'jayce', 'jhin', 'caitlyn', 
   #          'sejuani', 'senna', 'gangplank']