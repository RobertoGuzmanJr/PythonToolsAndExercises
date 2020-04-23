def permute1(seq):
	if not seq:
			return [seq]#returns the empty sequence if there is nothing in it
	else:
		res = []
		for i in range(len(seq)):
			rest = seq[:i] + seq[i+1:] #deletes the current node
			for x in permute1(rest): #permutes all the others
				res.append(seq[i:i+1] + x) #add node to the front
		return res

def permute2(seq):
	if not seq:
		yield seq
	else:
		for i in range(len(seq)):
			rest = seq[:i] + seq[i+1:]
			for x in permute2(rest):
				yield seq[i:i+1] + x