from __future__ import division
import sys, math
class Instance:
    count=0
    def __init__(self,sentence,bags,sense):
        self.sentence = sentence
        self.bags=bags
        self.sense=sense
        Instance.count += 1
senselist = []
def processingdata(file):
    dataset = []
    sentence = ''
    for line in file:
        line = line.strip('\n')
        if line.startswith('Student:'):
            sentence = line.strip('Student: ')
            continue
        if line.startswith('Advisor: '):
            sense = line.split()[1].strip('[]')
            senselist.append(sense)
            dataset.append(Instance(sentence, sentence.split(),sense))            
    return dataset
with open(sys.argv[1]) as train:
    train_set = processingdata(train)
with open(sys.argv[2]) as test:
    test_set = processingdata(test)
senselist = list(set(senselist))
sense_dic = {}
PS = {}
for item in senselist:
    sense_dic[item] = {}