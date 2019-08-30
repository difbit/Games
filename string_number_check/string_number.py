
import time
import operator

def calculate_string(n, steps):

    if len(str(n)) == 1:
        return steps

    number = str(n)

    numbers = [int(i) for i in str(n)]

    result = 1
    for i in numbers:
        result *= i

    steps += 1

    return calculate_string(result, steps)

step_collection = []

tic = time.clock()

print "Write a number:"
range_is = raw_input()

for i in range(1, int(range_is)):

    steps = 0
    step_collection.append((calculate_string(i, steps), i))

toc = time.clock()

print step_collection

first_value = [x[0] for x in step_collection]

index, value = max(enumerate(first_value), key=operator.itemgetter(1))

print "NUMBER IS: ", step_collection[index]

print "TIME TAKEN: ", toc - tic
