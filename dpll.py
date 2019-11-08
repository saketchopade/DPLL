class Node(object): 
        def __init__(self, pos, neg):
        	self.pos = pos
        	self.neg = neg

class Pure_Node(object): 
        def __init__(self, c_val, b_val):
        	self.c_val = c_val
        	self.b_val = b_val

class Most_Frequent_Node(object): 
        def __init__(self, c_val, p_val,n_val):
        	self.c_val = c_val
        	self.p_val = p_val
        	self.n_val = n_val


'''
DPLL Algo
1] Resolve Unit clauses(Single literal in a clause)
2] Resolve Pure literals(Literal that occurs in the same sense in all clauses)
3] Resolve Most frequent literals(Literal that occurs the most no of times)
'''





def find_unit_clause(predicates):
	uc = list()
	for p in predicates:
		if len(p) == 1:
			uc.append(p[0])
	for element in uc:							# If a literal and it's negation present as unit clause then unsatisfied
		if str('!'+element) in uc:
			return list()

	return uc		 



def unit_clause_util(d, predicates):
	if len(predicates)==0:
		return -1
	unit_clause = find_unit_clause(predicates)
	size = len(unit_clause)
	#print('Number of Unit Clause ' + str(size))
	for u in unit_clause:
		if u[0] == '!':								# Negative Unit Clause
			i = 0
			v = u[1:]
			while i < len(predicates):
				p = predicates[i]
				if u in p:
					for element in p:
						if element[0] == '!':
							d[element[1:]].neg = d[element[1:]].neg - 1
						else:
							d[element].pos = d[element].pos - 1
					predicates.pop(i)
					i = i - 1
				elif v in p:
					if len(p) == 1:
						return 0
					p.remove(v)
					d[v].pos = d[v].pos - 1
					if len(p) == 0:
						predicates.pop(i)
						i = i - 1
				if len(predicates)==0:
					return -1
				i = i + 1
			d.pop(v)
			
		else:										# Positive Unit Clause
			i = 0
			v = '!' + u
			while i < len(predicates):
				p = predicates[i]
				if u in p:
					for element in p:
						if element[0] == '!':
							d[element[1:]].neg = d[element[1:]].neg - 1
						else:
							d[element].pos = d[element].pos - 1
					predicates.pop(i)
					i = i - 1
				elif v in p:
					if len(p) == 1:
						return 0
					p.remove(v)
					d[u].neg = d[u].neg - 1
					if len(p) == 0:
						predicates.pop(i)
						i = i - 1
				if len(predicates)==0:
					return -1
				i = i + 1
			d.pop(u)

	return 0



def pure_literal(d):
	l = list()
	for key in d:
		if d[key].pos > 0 and d[key].neg == 0:
			pn = Pure_Node(key, 1)
			l.append(pn)
		elif d[key].pos == 0 and d[key].neg > 0:
			pn = Pure_Node(key, 0)
			l.append(pn)
	return l



def pure_literal_util(d, predicates):
	pure_literals = list()
	change = 0
	while change == 0:
		change = 1
		pure_literals = pure_literal(d)
		'''
		print("Pure Literals")
		for p in pure_literals:
			print(str(p.c_val) + '\t' + str(p.b_val))
		'''
		for u in pure_literals:
			#print('Chosen\t' + str(u.c_val))
			change = 0
			if u.b_val == 0:							# Negative
				i = 0
				v = '!' + u.c_val
				while i < len(predicates):
					p = predicates[i]
					if v in p:
						for element in p:
							if element[0] == '!':
								d[element[1:]].neg = d[element[1:]].neg - 1
							else:
								d[element].pos = d[element].pos - 1
						predicates.pop(i)
						i = i - 1
					i = i + 1
				d.pop(u.c_val)
				
			else:										# Positive
				i = 0
				while i < len(predicates):
					p = predicates[i]
					if u.c_val in p:
						for element in p:
							if element[0] == '!':
								d[element[1:]].neg = d[element[1:]].neg - 1
							else:
								d[element].pos = d[element].pos - 1
						predicates.pop(i)
						i = i - 1
					i = i + 1
				d.pop(u.c_val)

			'''
			print('Done pure literal')
			for p in predicates:
				print(p)
			for k in d:
				print(str(k) +'\t'+ str(d[k].pos) +'\t'+ str(d[k].neg))
			'''

def most_freq_literal(d):
	max_count = 0
	b = 0 
	for key in d:
		if max_count < d[key].pos +  d[key].neg:
			max_count = d[key].pos +  d[key].neg
			max_lit = key
	if d[max_lit].pos > d[max_lit].neg:
		b = 1									# Positive
	elif d[max_lit].pos < d[max_lit].neg:
		b = 0									# Negative
	else:
		b = -1									# Equally likely
	return (max_lit, b)


def most_freq_literal_util(d, predicates):
	u, b = most_freq_literal(d)
	#print ('Most frequent literal\t' + str(u) + '\t' + str(b))				# b = 1 means true, b = 0 means false, b = -1 half-half treated as false initially 
	retval = 0
	#d1 = dict(d)
	d1 = dict()
	for key in d:
		m = Node(d[key].pos, d[key].neg)
		d1[key] = m
	predicates1 = list()
	for p in predicates:
		predicates1.append(p.copy())
	#d2 = d.copy()
	d2 = dict()
	for key in d:
		m = Node(d[key].pos, d[key].neg)
		d2[key] = m
	predicates2 = list()
	for p in predicates:
		predicates2.append(p.copy())
	'''
	print('Here 0')
	for p in predicates1:
		print(p)
	print('\n')
	for p in predicates2:
		print(p)
	'''
	if b == 1:
		i = 0
		v = '!' + u
		while i < len(predicates1):
			p = predicates1[i]
			if u in p:
				for element in p:
					if element[0] == '!':
						d1[element[1:]].neg = d1[element[1:]].neg - 1
					else:
						d1[element].pos = d1[element].pos - 1
				predicates1.pop(i)
				i = i - 1
			elif v in p:
				if len(p) == 1:
					return 0
				p.remove(v)
				d1[u].neg = d1[u].neg - 1
				if len(p) == 0:
					predicates1.pop(i)
					i = i - 1
			i = i + 1
		d1.pop(u)
	elif b == 0:
		i = 0
		v = '!' + u
		while i < len(predicates1):
			p = predicates1[i]
			if v in p:
				for element in p:
					if element[0] == '!':
						d1[element[1:]].neg = d1[element[1:]].neg - 1
					else:
						d1[element].pos = d1[element].pos - 1
				predicates1.pop(i)
				i = i - 1
			elif u in p:
				if len(p) == 1:
					return 0
				p.remove(u)
				d1[u].pos = d1[u].pos - 1
				if len(p) == 0:
					predicates1.pop(i)
					i = i - 1
			i = i + 1
		d1.pop(u)
	else:
		i = 0
		v = '!' + u
		while i < len(predicates1):
			p = predicates1[i]
			if v in p:
				for element in p:
					if element[0] == '!':
						d1[element[1:]].neg = d1[element[1:]].neg - 1
					else:
						d1[element].pos = d1[element].pos - 1
				predicates1.pop(i)
				i = i - 1
			elif u in p:
				if len(p) == 1:
					return 0
				p.remove(u)
				d1[u].pos = d1[u].pos - 1
				if len(p) == 0:
					predicates1.pop(i)
					i = i - 1
			i = i + 1
		d1.pop(u)
	
	if len(predicates1)==0:
		return -1
	'''
	print('Predicate 1')
	for p in predicates1:
		print(p)
	print('Dict 1')
	print(d1)
	print('Predicate 2')
	for p in predicates2:
		print(p)
	'''
	retval = unit_clause_util(d1, predicates1)
	if retval != -1:
		#d1 = dict(d)
		#predicates1 = list(predicates)
		pure_literal_util(d1, predicates1)
		if len(predicates1)==0:
			return -1
		'''
		print('Here 1')
		for p in predicates1:
			print(p)
		print('Here 11')
		for p in predicates2:
			print(p)
		'''
		retval = most_freq_literal_util(d1, predicates1)
		if retval != -1:
			'''
			print('Here 2')
			for p in predicates2:
				print(p)
			'''
			# False value assignment failed for equally likely most frequent literal. Now check with True value
			if b == -1:
				#print('Here 3\t' + str(u))
				i = 0
				v = '!' + u
				while i < len(predicates2):
					p = predicates2[i]
					if u in p:
						for element in p:
							if element[0] == '!':
								d2[element[1:]].neg = d2[element[1:]].neg - 1
							else:
								d2[element].pos = d2[element].pos - 1
						predicates2.pop(i)
						i = i - 1
					elif v in p:
						if len(p) == 1:
							return 0
						p.remove(v)
						d2[u].neg = d2[u].neg - 1
						if len(p) == 0:
							predicates2.pop(i)
							i = i - 1
					i = i + 1
				if len(predicates2)==0:
					return -1
				'''
				print('Here 4')
				for p in predicates2:
					print(p)
				'''
				d2.pop(u)
				retval = unit_clause_util(d2, predicates2)
				if retval != -1:
					pure_literal_util(d2, predicates2)
					if len(predicates2)==0:
						return -1
					retval = most_freq_literal_util(d2, predicates2)
					return retval
				else:
					return -1
		else:
			return -1
	return -1
	




if __name__ == '__main__':
	fin = open('input1.txt','r')
	lines = fin.readlines()
	predicates = list()					# List of predicates
	unit_clause = list()				# List of unit clauses
	d = dict()							# dictionary to store literal and their positive and negative occurances
	# Iterate over all predicates
	for line in lines:
		pred=list()
		count = 0
		words = line.split(' ')			# List of all literals in a predicate
		for word in words:
			if word[-1] == '\n':
				word = word[:-1]
			temp_word = word
			pred.append(temp_word)
			if word[0] == '!':
				temp_word = word[1:]
			if temp_word not in d:
				d[temp_word] = Node(0, 0)
			if word[0] == '!':
				d[temp_word].neg = d[temp_word].neg + 1
			else:
				d[temp_word].pos = d[temp_word].pos + 1
			count = count + 1
		if count == 1:
			unit_clause.append(temp_word)
		predicates.append(pred)
	
	for p in predicates:
		print(p)
	print('Symbol\t Pos occurances\t Neg occurances')
	for k in d:
		print(str(k) +'\t\t'+ str(d[k].pos) +'\t\t'+ str(d[k].neg))
	

	# Unit clauses
	retval = unit_clause_util(d, predicates)						# -1 = Satisfied
	#print('After unit clause\t' +  str(retval))
	if retval != -1:
		#Pure Literals
		pure_literal_util(d, predicates)
		#print('Done initial pure literals')
		if len(predicates) == 0:
			print('Satisfied.Model found.KB does not entail alpha.')
		else:
			d_d = dict(d)
			predicates_p = list(predicates)
			retval = most_freq_literal_util(d_d, predicates_p)
			if retval == -1:
				print('Satisfied.Model found.KB does not entail alpha.')
			else:
				print('Unsatisfied.Model not found.KB entails alpha.')
	else:
		print('Satisfied.Model found.KB does not entail alpha.')
	
	

