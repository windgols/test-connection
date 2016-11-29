from __future__ import division
from sklearn import *
import sys
import dicts

dic = dicts.getEECSdict()
courseidlist = []
coursenamelist = []
for key,value in dic.iteritems():
    courseidlist.append(key)
    for item in value.split():
        coursenamelist.append(item)

def processingdata(file):# {{{
    set = []
    newinstance = 0
    wordbag = []
    bag = []
    newline = ''
    isclass = False
    for line in file:
        line = line.strip('\n')
        if line.strip():
            if newinstance==0:#start a new sentence
                newline = line
                wordbag = line.split()
                bag += wordbag
                newinstance = 1
            elif isclass:
                if line.strip('\n').endswith('>'):
                    line = line[:-1]
                if line.split('=')[0] == 'name':
                    org = line.split('=')[1]
                    new = ('/B '+'/I '*(len(org.split())-1))[:-1]
                    newline = newline.replace(org,new)
                if line.split('=')[0] == 'id':
                    org = line.split('=')[1]
                    new = '/B'
                    newline = newline.replace(org,new)
            if newinstance ==1 and line.startswith('<class'):
                isclass = True
            if newinstance ==1 and line.startswith('<instructor'):
                isclass = False
        else:
            newinstance = 0
            if isclass:#start process the word
                tmp = wordbag + newline.split()
            else:
                tmp = wordbag + ['/O']*len(wordbag)
            isclass = False
            wordbag = []
            newline = ''
            if tmp:
                set.append(tmp)
    return bag, set# }}}

def buildfeature(inputset):# {{{
    feature = []
    result = []
    for item in inputset:
        l = int(len(item)/2)
        previous_upper = 0
        for i in range(l):
            word = item[i]
            vec =[]
            vec.append(le.transform(word)) #token value
            vec.append(previous_upper)# previous word is all upper
            if word.isupper():#word is upper
                vec.append(1)
                previous_upper =1
            else:
                vec.append(0)
                previous_upper =0
            if word[0].isupper():#start with upper
                vec.append(1)
            else:
                vec.append(0)
            vec.append(len(word))#length of word
            if word.isdigit():#only numbers
                vec.append(1)
            else:
                vec.append(0)
            if word in courseidlist:# in course id list
                vec.append(1)
            else:
                vec.append(0)
            if word in coursenamelist:# in course name list
                vec.append(1)
            else:
                vec.append(0)
            feature.append(vec)
            if item[i+l] == '/B':
                category = 1
            elif item[i+l] == '/I':
                category = 2
            else:
                category = 3
            result.append(category)
    return feature , result# }}}

with open(sys.argv[1]) as train:#'NLU.train' sys.argv[]
    bag1, train_set = processingdata(train)
with open(sys.argv[2]) as test:#'NUL.test'
    bag2, test_set = processingdata(test)

le = preprocessing.LabelEncoder()
le.fit(bag1+bag2)
train_feature , train_result = buildfeature(train_set)
test_feature, test_result = buildfeature(test_set)
clf = tree.DecisionTreeClassifier()
clf = clf.fit(train_feature,train_result)
pred = clf.predict(test_feature)
right_count = 0
for i in range(len(pred)):
    if pred[i] == test_result[i]:
        right_count += 1
accuracy = right_count/len(pred)
print ('Accuracy is {0:.3%}'.format(accuracy))

#output file
tmp = ['']*len(pred)
for i in range(len(pred)):
    if pred[i] == 1:
        tmp[i] = '/B'
    if pred[i] == 2:
        tmp[i] = '/I'
    if pred[i] == 3:
        tmp[i] = '/O'
f = open('NLU.test.out','w+')
index = 0
for i in range(len(test_set)):
    sentence = test_set[i]
    length = int(len(sentence)/2)
    sentence = sentence[0:length]
    f.write(" ".join(sentence)+'\n')
    for t in range(length):
        sentence[t] = sentence[t] + tmp[index]
        index += 1
    f.write(" ".join(sentence)+'\n'*2)
f.close
