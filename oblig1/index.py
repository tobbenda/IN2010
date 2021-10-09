queue = [1,2,3,4]
index = int(len(queue)/2)
print(index)
print(queue[index])
queue.insert(index, 'x')
print(queue)