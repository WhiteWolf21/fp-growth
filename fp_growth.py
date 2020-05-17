#!/usr/bin/env python
# coding: utf-8

# In[44]:


# Implement important library

from __future__ import print_function
from collections import OrderedDict
from IPython.display import Image


# In[2]:


# variables:
# name of the node, a count
# nodelink used to link similar items
# parent vaiable used to refer to the parent of the node in the tree
# node contains an empty dictionary for the children in the node
class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode      #needs to be updated
        self.children = OrderedDict() 
# increments the count variable with a given amount    
    def inc(self, numOccur):
        self.count += numOccur
# display tree in text. Useful for debugging        
    def disp(self, ind=1):
        print ('  '*ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.disp(ind+1)


# In[3]:


# Test Tree Node

rootNode = treeNode('pyramid',9,None)

childNode = treeNode('eye',13,rootNode)

rootNode.children[childNode.name] = childNode


# In[4]:


rootNode.disp() # Display test tree

print("\n Children dictionary: " ,rootNode.children, "\n") # Display children dictionary of root node

print("Parent node: ",childNode.parent.name, "\n") # Display parent node of children node


# In[59]:


""" Constructing the FP-tree """

def createTree(dataSet, minSup=1): #create FP-tree from dataset
    headerTable = OrderedDict()

    #go over dataSet twice

    for trans in dataSet:#first pass counts frequency of occurance
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]

    print("Pass counts frequency of occurance: ",headerTable, '\n')

    for k in list(headerTable):  #remove items not meeting minSup
        if headerTable[k] < minSup: 
            del(headerTable[k])
            
    headerTable = OrderedDict([v for v in sorted(headerTable.items(), key=lambda p: p[1], reverse=True)])
    
    freqItemSet = tuple([v[0] for v in sorted(headerTable.items(), key=lambda p: p[1], reverse=True)])

    print("Remove items not meeting minSup and sort: ",headerTable, '\n')

    print("Frequent Items: ",freqItemSet, '\n')

    if len(freqItemSet) == 0: 
        return None, None  #if no items meet min support -->get out

    for k in headerTable:
        headerTable[k] = [headerTable[k], None] #reformat headerTable to use Node link 

    print("Reformat headerTable to use Node link: ",headerTable, '\n')

    retTree = treeNode('Null Set', 1, None) #create tree

    for tranSet, count in dataSet.items():  #go through dataset 2nd time
        localD = OrderedDict()
        for item in tranSet:  #put transaction items in order
            if item in freqItemSet:
                localD[item] = headerTable[item][0]

        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            print("Ordered Items: ",orderedItems, '\n')
            updateTree(orderedItems, retTree, headerTable, count)#populate tree with ordered freq itemset
            
        retTree.disp()
        print('\n')

    return retTree, headerTable #return tree and header table


# In[60]:


def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:#check if orderedItems[0] in retTree.children
        inTree.children[items[0]].inc(count) #incrament count
    else:   #add items[0] to inTree.children
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        if headerTable[items[0]][1] == None: #update header table 
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items) > 1:#call updateTree() with remaining ordered items
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)

def updateHeader(nodeToTest, targetNode):   
    while (nodeToTest.nodeLink != None):    
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


# In[61]:


""" Display FP-Tree """

def loadSimpDat():

    simpDat = [['I1', 'I2', 'I5'],
                ['I2', 'I4'],
                ['I2', 'I3'],
                ['I1', 'I2', 'I4'],
                ['I1', 'I3'],
                ['I2', 'I3'],
                ['I1', 'I3'],
                ['I1', 'I2', 'I3', 'I5'],
                ['I1', 'I2', 'I3']]
    
    # simpDat = [['r', 'z', 'h', 'j', 'p'],
    #            ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
    #            ['z'],
    #            ['r', 'x', 'n', 'o', 's'],
    #            ['y', 'r', 'x', 'z', 'q', 't', 'p'],
    #            ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]

    return simpDat

def createInitSet(dataSet):
    retDict = OrderedDict()
    for trans in dataSet:
        if (tuple(trans) in retDict):
            retDict[tuple(trans)] += 1
        else:
            retDict[tuple(trans)] = 1
    return retDict

simpDat = loadSimpDat()

initSet = createInitSet(simpDat)

print(initSet,'\n')

# display(Image(filename="ReorderTransaction.png", width=700, height=700))


# In[62]:


#The FP-tree

# display(Image(filename="FP-Tree.png", width=700, height=700))

myFPtree, myHeaderTab = createTree(initSet, 2)

# myFPtree, myHeaderTab = createTree(initSet, 3)

# display(Image(filename="FP-Tree.png", width=700, height=700))

myFPtree.disp()

print('\n',myHeaderTab,'\n')

print("I1's parent: ",myHeaderTab['I1'][1].parent.name,'\n')

print("I1's children: ",myHeaderTab['I1'][1].children,'\n')

print("I1's support count: ",myHeaderTab['I1'][1].count,'\n')

print("I1's nodelink support count: ",myHeaderTab['I1'][1].nodeLink.count,'\n')


# In[38]:


# """ Mining frequent items from an FP-tree """

def ascendTree(leafNode, prefixPath): #ascends from leaf node to root
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)

def findPrefixPath(basePat, treeNode): #treeNode comes from header table
    condPats = OrderedDict()
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1: 
            condPats[tuple(prefixPath[1:][::-1])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats


# In[63]:


# display(Image(filename="Mining.png", width=700, height=700))

print('\n', "Conditional Pattern Base", '\n')

print("I5: ",findPrefixPath('I5', myHeaderTab['I5'][1]), '\n')

print("I4: ",findPrefixPath('I4', myHeaderTab['I4'][1]), '\n')

print("I3: ",findPrefixPath('I3', myHeaderTab['I3'][1]), '\n')

print("I2: ",findPrefixPath('I2', myHeaderTab['I2'][1]), '\n')

print("I1: ",findPrefixPath('I1', myHeaderTab['I1'][1]), '\n')


# In[96]:


# display(Image(filename="Mining.png", width=700, height=700))

def mineTree(inTree, headerTable, minSup, preFix, freqItemList):

    bigL = [v[0] for v in sorted(headerTable.items(),key=lambda p: p[1])]
    
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        myCondTree, myHead = createTree(condPattBases,minSup)
        
        if myHead != None:
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)
            
            freqPatternGenerate = OrderedDict()
            
            for k in myHead.keys():
                subKey = [k]
                for x in newFreqSet:
                    subKey.append(x)
                freqPatternGenerate[tuple(subKey)] = myHead[k][0]
        
            print("Conditional tree for: ",newFreqSet)
            myCondTree.disp()
            print('\n')
            
            print("Frequent Patterns Generated: ",freqPatternGenerate, "\n")

freqItems = []

freqPatternGenerate = OrderedDict()

# mineTree(myFPtree,myHeaderTab,3,set([]), freqItems)

mineTree(myFPtree,myHeaderTab,2,set([]), freqItems)


# In[66]:


""" Constructing the FP-tree """

def createTree(dataSet, minSup=1): #create FP-tree from dataset
    headerTable = OrderedDict()

    #go over dataSet twice

    for trans in dataSet:#first pass counts frequency of occurance
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]

    for k in list(headerTable):  #remove items not meeting minSup
        if headerTable[k] < minSup: 
            del(headerTable[k])
            
    headerTable = OrderedDict([v for v in sorted(headerTable.items(), key=lambda p: p[1], reverse=True)])
    
    freqItemSet = tuple([v[0] for v in sorted(headerTable.items(), key=lambda p: p[1], reverse=True)])

    if len(freqItemSet) == 0: 
        return None, None  #if no items meet min support -->get out

    for k in headerTable:
        headerTable[k] = [headerTable[k], None] #reformat headerTable to use Node link 

    retTree = treeNode('Null Set', 1, None) #create tree

    for tranSet, count in dataSet.items():  #go through dataset 2nd time
        localD = OrderedDict()
        for item in tranSet:  #put transaction items in order
            if item in freqItemSet:
                localD[item] = headerTable[item][0]

        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            updateTree(orderedItems, retTree, headerTable, count)#populate tree with ordered freq itemset

    return retTree, headerTable #return tree and header table


# In[ ]:




