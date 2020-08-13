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
    with open(directory + "/people.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(directory + "/movies.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(directory + "/stars.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(raw_input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(raw_input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(str(degrees) + " degrees of sepreation")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(str(i+1) + ":" + person1 + " and " + person2 + " starred in " + movie)


def shortest_path(source, target):

#    if source != target:
#        break
#    setofpeople_source = neighbors_for_person(source)
#    setofpeople_target = neighbors_for_person(target)
    path = []
    
    queue = QueueFrontier()
    queue.add(((source,0),path))
    while not queue.empty():
        node,path = queue.remove()
        person_id,movie_id = node
        if person_id == target:
            return path
        for movie_id,neighbor_id in neighbors_for_person(person_id):
            path_copy = path[:]
            path_copy.append((movie_id,neighbor_id))
            queue.add(((neighbor_id,movie_id),path_copy))
            
#    for i in setofpeople_source:
#        for j in setofpeople_target:
#            if i[1] == j[1]:
#                path.append(i)
#                path.append(j)
#                return path
#    for i in setofpeople_source:
#        setof = neighbors_for_person(i[1])
#        found = False
#        while found == False:
#            for j in setof:
#                if j[1] == target:
                    
                    
                    
                    
                
        
    
                
        
    
    print(source)
    print(target)
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    
    """
    
    # TODO
    raise NotImplementedError


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print("Which" + name + "?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print("ID:" + str(person_id) + ", Name:" + name + "Birth:" + birth)
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
