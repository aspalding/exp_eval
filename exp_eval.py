from itertools import izip, islice
import sys

__author__ = 'andrew'

'''
Assumptions are made about the format of the input file. Sentences and knowledge bases
that do not conform to the notation provided by the sample will not evaluate correctly.
'''

#Parse each line individually.
def kb_model(line):
    expression_model = line.split(',')
    expression = expression_model[0]
    key = []
    value = []

    for pair in islice(expression_model,1,None):
        split = pair.split('=')
        key.append(split[0])
        if split[1] is 'T':
            value.append(True)
        elif split[1] is 'F':
            value.append(False)

    kb = {key:value for (key,value) in zip(key, value)}

    return [expression, kb]

#Isolate mark-up.
def split_clauses(sentence):
    sentence = sentence.replace('(', '')
    sentence = sentence.replace(')', '')
    sentence = sentence.replace(' ', '')

    clauses = sentence.split('^')
    return clauses

#Generate keys that can be passed to dictionary.
def split_keys(clauses):
    keys = []

    for clause in clauses:
        keys += [clause.split('V')]

    return keys

#Evaluate each part of expression.
def eval_clause(clause, knowledge):
    result = False
    for current_item, next_item in izip(clause, islice(clause,1,None)):
        if '~' in current_item:
            temp_item = current_item.replace('~', '')
            result = result or (not knowledge[temp_item] or knowledge[next_item])
        elif '~' in next_item:
            temp_item = next_item.replace('~', '')
            result = result or (knowledge[current_item] or not knowledge[temp_item])
        else:
            result = result or (knowledge[current_item] or knowledge[next_item])
    return result

#Evaluate sentence as a whole.
def eval_sentence(sentence, knowledge):
    result = True
    for clause in sentence:
        result = result and eval_clause(clause,knowledge)

    return result

#If the user supplies argument for their own text file, read that. Otherwise read the sample provided.
if(len(sys.argv) > 1):
    file = open(sys.argv[1], 'r')
else:
    print 'Evaluate your own file by passing python an argument.\nex:\t\t>python exp_eval.py file.txt\n'
    file = open('sample.txt', 'r')

#For each line in the file, evaluate the expression with the given knowledge base.
for line in file:
    line = line.replace('\n', '')
    current = kb_model(line)
    sent = current[0]
    kb = current[1]
    clauses = split_clauses(sent)
    keys_clause = split_keys(clauses)
    print 'Evaluating: \t', sent, ' = ', eval_sentence(keys_clause, kb)