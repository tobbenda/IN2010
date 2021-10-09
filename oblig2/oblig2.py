import csv
print("Oppgave 1")

# actor_tsv = open("actors.tsv")
actor_tsv = open("actors_short.tsv")
actors = csv.reader(actor_tsv, delimiter="\t")
actors_arr = []
for row in actors:
    actors_arr.append(row)

# movies_tsv = open("movies.tsv")
movies_tsv = open("movies_short.tsv")
movies = csv.reader(movies_tsv, delimiter="\t")

num_of_actors = len(actors_arr)
print('Number of actors:', num_of_actors)

print('Initiliazing matrix')
# row = [[]]*num_of_actors
Matrix = [[[] for j in range(num_of_actors)] for i in range(num_of_actors)]
print('Done initiliazing matrix')

movies_arr = []
for row in movies:
    movies_arr.append(row)

def findMovie(mov, movies):
    for movie in movies:
        if movie[0] == mov:
            return movie

'''
For hver actor (actor1), gå igjennom alle andre actors (actor2) 
og legg til alle felles filmer i matrisen på actor2.
'''

def prettyPrintMatrix(m):
    s = [[str(e) for e in row] for row in m]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))

for actor_i, actor in enumerate(actors_arr):
    actor_movies = actor[2:]
    for actor_i2, actor2 in enumerate(actors_arr):
        if(actor_i == actor_i2):
            continue
        actor2_movies = actor2[2:]
        
        for mov in actor2_movies:
            if(mov in actor_movies):
                prettyPrintMatrix(Matrix)
                movie = findMovie(mov, movies_arr)
                print('moviename:', movie[1])
                print(actor_i2, actor_i)
                Matrix[actor_i2][actor_i].append(movie[0])
                Matrix[actor_i2][actor_i].append(movie[2])

prettyPrintMatrix(Matrix)

