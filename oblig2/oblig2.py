import csv
print("Oppgave 1")

graph = []

actor_tsv = open("actors_short.tsv")
actors = csv.reader(actor_tsv, delimiter="\t")
actors_arr = []
for row in actors:
    actors_arr.append(row)

movies_tsv = open("movies_short.tsv")
movies = csv.reader(movies_tsv, delimiter="\t")

num_of_actors = len(actors_arr)
Matrix = [[[] for x in range(num_of_actors)] for y in range(num_of_actors)] 

movies_arr = []
for row in movies:
    movies_arr.append(row)
    # nm_id = row[0]
    # for actor in actors_arr:
    #     if nm_id in actor:
    #         Matrix[]
    #         print(actor[0], row[0])
    #     else:
    #         print(actor[0])


## For hver actor, Gå igjennom filmene, 
# for hver film, finn actors som er i samme film
# fyll inn i matrisen for den actoren.
for actor_i, actor in enumerate(actors_arr):
    actor_movies = actor[2:]
    for actor_i2, actor2 in enumerate(actors_arr):
        if(actor_i == actor_i2):
            continue
        actor2_movies = actor2[2:]
        for mov in actor2_movies:
            if(mov in actor_movies):
                print('yeehaw')
                Matrix[actor_i2][actor_i].append(mov)


s = [[str(e) for e in row] for row in Matrix]
lens = [max(map(len, col)) for col in zip(*s)]
fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
table = [fmt.format(*row) for row in s]
print('\n'.join(table))

# print(Matrix)
        # for movie in actor_movies:
        #     if movie in actor2:
        #         print(movie, actor2[1])
        #         movie_arr = []
        #         for list in movies_arr:
        #             if (list[0] == movie):
        #                 movie_arr = list
        #                 Matrix[actor_i][actor_i2].append([movie_arr[0], movie_arr[2]])

# print(actors_arr[3])
# print(Matrix[3])

