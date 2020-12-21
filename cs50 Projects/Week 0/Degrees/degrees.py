import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f) #
        for row in reader: # para cada fila en la lista cargada 
            people[row["id"]] = {# diccionario ident la persona con el id -> guarda los datos 
                "name": row["name"],
                "birth": row["birth"],
                "movies": set() # la persona puede aparecer en muchas peliculas 
            }
            if row["name"].lower() not in names: #verifica que el no este en el diccionario 
                names[row["name"].lower()] = {row["id"]}#iguala ese nombre a un id unico 
            else:
                names[row["name"].lower()].add(row["id"])#si no se encuentra agrega una fila de id 

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set() # nueva coleccion 
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f: 
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")# envia el directorio que utiliza 
    directory = sys.argv[1] if len(sys.argv) == 2 else "large" # lista large or small 

    # Load data from files into memory
    print("Loading data...")
    load_data(directory) 
    print("Data loaded.")

    source = person_id_for_name(input("source Name: ")) # consola pregunta por el nombre de source 
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("target Name: "))#consola pregunta por nombre d etarget 
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target) # busca el camino mas corto d ellegar a target 

    if path is None:
        print("Not connected.") # si no estan conectados 
    else:
        degrees = len(path) 
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees): # busca en la lista enviada 
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    start = Node(source,parent = None , action = None) # comienza con la persona source 

    num_explored = 0 # opciones exploradas 
    frontier = QueueFrontier() # utilizamos una cola 
    frontier.add(start) # agregamos  a la cola

    explored=set() # nodos explorados 
    while True:

     if frontier.empty(): #si la cola esta vacia, no hay matches 
        return None
     num_explored = num_explored +1 # aumenta contador de nodos explorados 
     nodo = frontier.remove() # remueve la cabeza de frontier 
     explored.add(nodo) # añadimos nodo al set de explorados 
     
     # neighbors for person -> retorna un set 
     #movie y persona recorren ese set 
     for movie , person in neighbors_for_person(nodo.state):
         #vemos si la frontier  realmente contiene a la persona 
        if not frontier.contains_state(person) and person not in explored:
            child = Node(person, nodo, (movie, person))
            # child es hijo del nodo source 
            if child.state == target: # si llega a ser el nodo que buscamos 
                return backtrack(child) # retorna una lista de todo el camino 
            frontier.add(child) #si no es lo añadimos a frontier 

    # TODO
    #raise NotImplementedError
def backtrack(nodo): 
    """ It´s going to send Node´s path as a list  
    """
    path = []

    while nodo.parent is not None: # recorre toda su linea 
        path.append(nodo.action) # añade a su path 
        nodo = nodo.parent # accede al nodo anterior 

    path.reverse() # los invierte en el orden corriente 
    return path # retorna el cmaino 

def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
