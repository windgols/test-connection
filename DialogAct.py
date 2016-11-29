from __future__ import division
import sys, math, re
class Instance:
    count=0
    def __init__(self,sentence,bags,sense):
        self.sentence = sentence
        self.bags=bags
        self.sense=sense
        Instance.count += 1
sense_dic = {}
PS = {}
def processingdata(file, train):
    dataset = []
    sentence = ''
    count = 0
    for line in file:
        line = line.strip('\n')
        if line.startswith('Advisor: '):
            count += 1
            sense = line.split()[1].strip('[]')
            sense_dic[sense] = sense_dic.get(sense,{})
            if train:
                PS[sense] = PS.get(sense,0) + 1
            bags = sentence.split()
            if not bags:
                bags = ['']
            for item in bags:
                if train:
                    sense_dic[sense][item] =  sense_dic[sense].get(item,0)+1
                else:
                    for k in PS:
                        sense_dic[k][item] =  sense_dic[k].get(item,0)
            dataset.append(Instance(sentence, bags, sense))
        elif line.startswith('Student:'):
            sentence = line[9:]
        else:
            sentence = ''
    return count, dataset
with open(sys.argv[1]) as train:
    count, train_set = processingdata(train, True)
with open(sys.argv[2]) as test:
    _, test_set = processingdata(test, False)

for key,value in sense_dic.iteritems():
    if any(tmp==0 for tmp in value.values()):
        for k in value:
            value[k] = math.log((value[k]+1)/(len(value)+PS[key]))
    else:
        for k in value:
            value[k] = math.log(value[k]/PS[key])
for k in PS:
    PS[k] = math.log(PS[k]/count)
#start test
accuracy = 0
for item in test_set:
   maximum = float('-inf')
   label = ''
   for k in PS:
       score = PS[k]
       for i in item.bags:
           score += sense_dic[k][i]
       if score > maximum:
           label = k
           maximum = score
   if label == item.sense:
       accuracy += 1
accuracy = accuracy/len(test_set)
print 'Accuracy is {0:.3%}.'.format(accuracy)

