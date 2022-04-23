#!/usr/bin/env python3

import pickle
# NO ADDITIONAL IMPORTS ALLOWED!

# Note that part of your checkoff grade for lab 2 will be based on the
# style/clarity of your code.  As you are working through the lab, be on the
# lookout for things that would be made clearer by comments/docstrings, and for
# opportunities to rearrange aspects of your code to avoid repetition (for
# example, by introducing helper functions).


def acted_together(data, actor_id_1, actor_id_2):
    a=0
    actor1_films=[]
    actor2_films=[]
    for i in range(len(data)):
        if actor_id_1 in data[i]:
            actor1_films.append(data[i][2])
        if actor_id_2 in data[i]:
            actor2_films.append(data[i][2])
    for i in range(len(actor1_films)):
        if actor1_films[i] in actor2_films:
            a=1
        if a==1:
            return True
        else:
            return False
#iterate just once, if first is actor1 and second is actor 2 vice versa

def dictionarify(data):
    actor_book={}
    for i in range(len(data)):
        if data[i][0] not in actor_book:
            actor_book[data[i][0]]=set()
        if data[i][1] not in actor_book:
            actor_book[data[i][1]]=set()
        actor_book[data[i][0]].add(data[i][1])
        actor_book[data[i][1]].add(data[i][0])
    return actor_book

def actors_with_bacon_number(data, n):
    actor_book=dictionarify(data)
    start=4724
    a=0
    current_level={start}
    seen={start}
    while a<n and len(current_level)>0:
        next_level=set()
        for node in current_level:
            for s in actor_book[node]:
                if s not in seen:
                    next_level.add(s)
                    seen.add(s)
        current_level=next_level.copy()
        a=a+1
    return current_level

def bacon_path(data, actor_id):
    return actor_to_actor_path(data,4724,actor_id)


def actor_to_actor_path(data, actor_id_1, actor_id_2):
    def goal_test_function(node):
        return node==actor_id_2
    return actor_path(data,actor_id_1,goal_test_function)

def movie_path(data,actor_id_1,actor_id_2):
    actor_path=actor_to_actor_path(data,actor_id_1,actor_id_2)
    movie_list={}
    movies_path=[]
    movie_names_path=[]
    with open('resources/movies.pickle','rb') as f:
        movies_pickle=pickle.load(f)
    inverted_movies_pickle=dict(map(reversed, movies_pickle.items()))
    for i in range(len(data)):
        movie_list[(data[i][0],data[i][1])]=data[i][2]
        movie_list[(data[i][1],data[i][0])]=data[i][2]
    for i in range(len(actor_path)-1):
        this_tuple=(actor_path[i],actor_path[i+1])
        movies_path.append(movie_list[this_tuple])
    for i in movies_path:
        movie_names_path.append(inverted_movies_pickle[i])
    return movie_names_path

def actor_path(data, actor_id_1, goal_test_function):
    actor_book=dictionarify(data)
    start=actor_id_1
    current_level={start}
    seen={start}
    parents={}
    path=[]
    Trueness={goal_test_function(actor_id_1)}
    while (any(Trueness)!=True) and (len(current_level)>0):
        Trueness=set()
        next_level=set()
        for node in current_level:
            for s in actor_book[node]:
                if s not in seen:
                    next_level.add(s)
                    seen.add(s)
                    parents[s]=node
        current_level=next_level.copy()
        for i in current_level:
            Trueness.add(goal_test_function(i))
    new_set=current_level.copy()
    for i in current_level:
        if goal_test_function(i)!=True:
            new_set.remove(i)
    if len(new_set)!=0:
        new_list=list(new_set)
        b=new_list[0]
        a=b
        if b in parents:
            while a!=actor_id_1:
                path.append(a)
                a=parents[a]
            path.append(actor_id_1)
            path.reverse()
            return path
        elif actor_id_1 in current_level:
            return [actor_id_1] 
        else:
            return None
    else:
        return None
##actor_to_actor_path becomes actor_path
def movie_list(data):
    movie_book={}
    for i in range(len(data)):
        if data[i][2] not in movie_book:
            movie_book[data[i][2]]=set()
        if data[i][0] not in movie_book[data[i][2]]:
            movie_book[data[i][2]].add(data[i][0])
        if data[i][1] not in movie_book[data[i][2]]:
            movie_book[data[i][2]].add(data[i][1])
    return movie_book

def actors_connecting_films(data, film1, film2):
    actor_book=dictionarify(data)
    movie_book=movie_list(data)
    start=movie_book[film1]
    current_level=set(start)
    seen=set(start)
    parents={}
    path=[]
    Trueness=set()
    def goal_test_function(x):
        return x in movie_book[film2]
    for i in start:
        Trueness.add(goal_test_function(i))
    while (any(Trueness)!=True) and (len(current_level)>0):
        Trueness=set()
        next_level=set()
        for node in current_level:
            for s in actor_book[node]:
                if s not in seen:
                    next_level.add(s)
                    seen.add(s)
                    parents[s]=node
        current_level=next_level.copy()
        for i in current_level:
            Trueness.add(goal_test_function(i))
    new_set=current_level.copy()
    for i in current_level:
        if goal_test_function(i)!=True:
            new_set.remove(i)
    if len(new_set)!=0:
        new_list=list(new_set)
        b=new_list[0]
        a=b
        if b in parents:
            while a not in movie_book[film1]:
                path.append(a)
                a=parents[a]
            path.append(parents[path[-1]])
            path.reverse()
            return path
        elif movie_book[film1]==current_level:
            return [movie_book[film1][0]] 
        else:
            return None
    else:
        return None


if __name__ == '__main__':
    # with open('resources/names.pickle', 'rb') as f:
    #     smalldb = pickle.load(f)
    # print(smalldb['Katrin Luise'])
    # for name in smalldb.keys():
    #     if smalldb[name]==141719:
    #         wanted=name
    # print (wanted)
    with open('resources/small.pickle','rb') as f:
        small_pickle=pickle.load(f)
    with open('resources/names.pickle','rb') as f:
        name_id=pickle.load(f)
    with open('resources/tiny.pickle','rb') as f:
        tiny_pickle=pickle.load(f)
    with open('resources/large.pickle','rb') as f:
        large_pickle=pickle.load(f)
    with open('resources/movies.pickle','rb') as f:
        movies_pickle=pickle.load(f)
    #print(actors_with_bacon_number(small_pickle,2))
    #print(actors_with_bacon_number(large_pickle,6))
    #print(tiny_pickle)  
    #print(name_id)
    reversed_nameid = dict(map(reversed, name_id.items()))
    def name_from_id(id):
        return reversed_nameid[id]
    #print(movie_list(tiny_pickle))
    print(actors_connecting_films(large_pickle,18860, 75181))
    ppl = {536472, 44795, 240045, 19534}
    # print(actor_to_actor_path(large_pickle,10526,536472))
    # print(actor_to_actor_path(large_pickle,10526,44795))
    # print(actor_to_actor_path(large_pickle,10526,240045))
    # print(actor_to_actor_path(large_pickle,10526,19534))    
    # print(actor_path(large_pickle, 10526, lambda p: p in ppl))
    # names=[]
    # id1=name_id['Geoffrey Wigdor']
    # id2=name_id['Sven Batinic']
    # print(movie_path(large_pickle,id1,id2))
    # id1=name_id['Robert Huber']
    # id2=name_id['Mary Kate Schellhardt']
    # a=actor_to_actor_path(large_pickle,id1,id2)
    # for i in a:
    #     names.append(name_from_id(i))
    # print(names)
    # id1=name_id['Tatsuya Ishiguro']
    # a=bacon_path(large_pickle,id1)
    # for i in a:
    #     names.append(name_from_id(i))
    # print(names)
#    for i in actors_with_bacon_number(large_pickle,6):
#         names.add(name_from_id(i))
    #print(dictionarify(tiny_pickle))
    #id1=name_id['Natascha McElhone']
    #id2=name_id['Matt Dillon']
    #id1=name_id['Noureddine El Ati']
    #id2=name_id['Stanley Tucci']
    #print(acted_together(small_pickle,id1,id2))

        
    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.