// practice sorting algorithms

import random 
import math

# generate a random, unsorted list of numbers to practice sorting algorithms on 

def create_unsorted(length, highest_value):
    
    unsorted_array = []

    for i in range(0, length):
        i = random.randint(1,highest_value)
        unsorted_array.append(i)
        
    return unsorted_array

# generate a random, unsorted list of numbers *that contains no duplicates* to practice sorting algorithms on 

def unsorted_noduplicates(length, highest_value):
    
    unsorted = []

    for i in range(0, length):
        i = random.randint(1,highest_value)
        
        unsorted = list(set(unsorted))
        
        while len(unsorted)< length:
            unsorted.append(i)
            
    return unsorted

# swap vlaues 

def swap(a, b):
    a, b = b, a
    
    return a, b
    
# create target number

target = random.randint(min(unsorted_array), max(unsorted_array))


def check_integers(trgt, lst = list):
    for i in lst:
        if i == trgt:
#         print("Checking list by each integer: ", target_yes, "is in the list.")
            return i
 
 def check_location(trgt, lst = list):
    for i in range(0,len(lst)):
        if lst[i] == trgt:
    #         print("Checking list by value at list location: ", target_yes, "is in the list at position", i)
            break

        
%%timeit
 
check_integers(target, unsorted)
 
%%timeit


# Binary Search 

target = 52

def binary_search(trgt, lst):

    if len(lst) == 1:
        if lst[0] == trgt:
#             print(f"Target {lst[0]} is in list.")
            return
        else:
#             print(f"Target {trgt} is not in the list.")
            return
    
    midpoint = int(round(len(lst)/2))
    
    # successful recursion! 
    
    if lst[midpoint] <= trgt:
        lst = lst[midpoint:]
        binary_search(trgt, lst)
    else:
        lst = lst[: midpoint]
        binary_search(trgt, lst)
        
        
        

def bubble_sort(lst = list):
    
#   set swap counter equal to zero so the while loop will begin 
    swap = -1 
    
    
    while swap != 0:
#         set swap counter equal to zero so only swaps made during this iteration will be counted 

        swap = 0

#         iterate through entire length of list, bubbling smaller variables to the left and larger variables to the right

        for i in range(0,len(lst)-1):
            if lst[i] > lst[i+1]:
                temp = lst[i]
                lst[i] = lst[i+1]
                lst[i+1] = temp
                swap += 1
    return lst


def selection_sort(lst = list):
    
    for i in range(0, len(lst)):
        while lst[i] < lst[i+1]:
            indx = i

            for j in range(i+1, len(lst)):
                if lst[indx] > lst[j]:
                    indx = j

                    lst[i], lst[indx] = lst[indx], lst[i]

    return lst
    

# Merge two sorted lists 

def merge_sorted(m1, m2):

i = 0
j = 0
k = 0

m = len(m1)
n = len(m2)

merged_array = array.array('i', (0,) * (m + n))

while i < m and j < n:
if m1[i] < m2[j]:
    merged_array[k] = m1[i]
    i += 1
    k += 1
else:
    merged_array[k] = m2[j]
    j += 1
    k += 1

while j < n:
merged_array[k] = m2[j]
k+=1
j+=1
while i < m:
merged_array[k] = m1[i]
k+=1
i+=1

return merged_array
