
def s2b(rowstr):
	return bin(int.from_bytes((rowstr).encode(),'big'))[2:]+"00"

def b2s(b):
	return int('0b'+b[:-2],2).to_bytes(1, 'big').decode()

def chunk(rowbin, n=8):
	return [rowbin[i:i+n] for i in range(0, len(rowbin), n)]
