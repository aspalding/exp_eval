from itertools import izip, islice

__author__ = 'andrew'

key = ['jon', 'chris', 'frank', 'candy', 'beef']

value = [False, True, False, False, False]

kb = {key:item for (key,item) in zip(key,value)}


print 'desired result:'
print (kb['jon'] or kb['chris'] or kb['frank']) and (kb['candy'] or kb['beef'])


def split_clauses(sentence):
    sentence = sentence.replace('(', '')
    sentence = sentence.replace(')', '')
    sentence = sentence.replace(' ', '')

    clauses = sentence.split('^')
    return clauses

def split_keys(clauses):
    keys = []

    for clause in clauses:
        keys += [clause.split('V')]

    return keys



sent = '(jon V chris V frank) ^ (candy V beef)'
clauses = split_clauses(sent)
print clauses

keysinclauses = split_keys(clauses)
print keysinclauses

def eval_clause(clause, knowledge):
    result = True
    for current_item, next_item in izip(clause, islice(clause,1,None)):
        result = result and (knowledge[current_item] or knowledge[next_item])
    return result

def eval_sentence(sentence, knowledge):
    result = True
    for clause in sentence:
        result = result and eval_clause(clause,knowledge)

    return result

print(eval_sentence(keysinclauses,kb))


