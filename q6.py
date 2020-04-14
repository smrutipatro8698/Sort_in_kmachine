import sys
import argparse 
import numpy as np

parser = argparse.ArgumentParser() 
parser.add_argument('-n', default = "1000", help = "Number of input elements n")
parser.add_argument('-k', default = "4", help = "Number of input elements n")
parser.add_argument('-input', action = "store_true", help = "Display the n numbers to be sorted")
parser.add_argument('-output', action = "store_true", help = "Display the numbers in each machine after sorting")

  
# Read arguments from command line 
args = parser.parse_args() 
n = int(args.n)
k = int(args.k)

print("The number of elements to be sorted is", n,"\n")
print("The number of machines is",k,"\n")

##First generate random set of  integers##
X = np.random.random_integers(1, 100, n)
if(args.input):
	print("The n numbers to be sorted are: \n")
	print(X)

##Distribute numbers into machines##
##Since the numbers generated are random, we just partition them by order##
i = 0
m = np.zeros((k, int(n/k)))
for machine in range(0, k):
	for j in range(0, int(n/k)):
		m[machine][j] = X[i]
		i = i + 1

##Now locally sort numbers in each machine##
for machine in range(0, k):
	m[machine].sort()
	temp = np.array(m[machine])
	m[machine] = temp


leader  = []
p = int(n/(k*k))
#Now find k numbers from each machine at indices n/k2, 2n/k2,... and send it to leader#
for machine in range(0, k):
	for j in range(0,k):
		leader.append(m[machine][0 + j * p])

leader = np.asarray(leader)

##Now sort the leader and find k - 1 pivots ##
leader.sort()
leader = np.array(leader)


p = int(len(leader)/k)
pivots = []
for j in range(1, k):
	pivots.append(leader[j*p])
pivots = np.asarray(pivots)
#print(pivots)


#Now send these pivots to the other machines and give the ith partition to the ith machine##
new_m = []
j = 0
for machine in m:
	print("Machine",j + 1,"chunk sizes are as follows:")
	for i in range(0, len(pivots)):
		machine = np.asarray(machine)
		if(i != 0):
			partition_i = machine[(machine > pivots [i - 1]) & (machine <= pivots[i])]
			if(len(new_m) <= i):
				new_m.append(partition_i)
			else:
				new_m[i] = np.append(new_m[i], partition_i)
			print(len(partition_i))
		else:
			partition_i = machine[(machine >= 0) & (machine <= pivots[i])]
			if(len(new_m) == 0):
				new_m.append(partition_i)
			else:
				new_m[0] = np.append(new_m[0], partition_i)
			print(len(partition_i))
	partition_i = machine[(machine > pivots [i])]
	if(len(new_m) <= i + 1):
		new_m.append(partition_i)
	else:
		new_m[i + 1] = np.append(new_m[i + 1], partition_i)
	print(len(partition_i))
	j = j + 1

##Now locally sort numbers in each machine##
for machine in range(0, k):
	new_m[machine].sort()
	temp = np.array(new_m[machine])
	new_m[machine] = temp

j = 0
for machine in new_m:
	print("No. of elements in machine", j + 1, "is:",len(machine))
	if(args.output):
		print("Elements in machine", j + 1,"after sorting:\n")
		print(machine)
	j = j + 1
