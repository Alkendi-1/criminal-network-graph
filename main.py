import pickle

def display_menu():
    print("---- Menu ----")
    print("1) Add suspect")
    print("2) Add accomplice")
    print("3) Display all suspects")
    print("4) Find potential accomplices")
    print("S) Statistics")
    print("E) Exit")

def display_suspect(suspect, graph):
    print(f"{suspect}:")
    accomplices = graph.get(suspect, set())
    for accomplice in accomplices:
        print(f"    {accomplice}")

def display_all_suspects(graph):
    print("---- All suspects ----")
    for suspect in graph:
        display_suspect(suspect, graph)

def find_potential_accomplices(suspect, graph):
    known_accomplices = graph.get(suspect, set())
    potential_accomplices = set()

    for accomplice in known_accomplices:
        potential_accomplices.update(graph.get(accomplice, set()))

    potential_accomplices.discard(suspect)
    potential_accomplices -= known_accomplices

    return {suspect: potential_accomplices}

def display_potential_accomplices(suspect, graph):
    print("---- Potential accomplices ----")
    print("Already known accomplices:")
    display_suspect(suspect, graph)

    potential = find_potential_accomplices(suspect, graph)
    print("\nPotential new accomplices:")
    for key in potential:
        print(f"{key}:")
        for p_accomplice in potential[key]:
            print(f"    {p_accomplice}")

def load_from_file(filename):
    try:
        with open(filename, 'rb') as file:
            graph = pickle.load(file)
        print("*** Graph loaded from file. ***")
        return graph
    except FileNotFoundError:
        print("*** File not found. Starting with empty graph. ***")
        return {}

def save_to_file(graph, filename):
    with open(filename, 'wb') as file:
        pickle.dump(graph, file)

def main():
    print("---- Criminals and their accomplices ----")
    filename = input("Enter path to graph file: ")
    graph = load_from_file(filename)

    while True:
        display_menu()
        choice = input("Enter your choice: ").strip().lower()

        if choice == '1':
            suspect = input("Enter suspect name: ").strip()
            if suspect not in graph:
                graph[suspect] = set()
                save_to_file(graph, filename)
            else:
                print("Suspect already exists.")

        elif choice == '2':
            suspect = input("Enter suspect name: ").strip()
            accomplice = input("Enter the name of the accomplice: ").strip()
            
            if suspect not in graph:
                graph[suspect] = set()
            if accomplice not in graph:
                graph[accomplice] = set()

            graph[suspect].add(accomplice)
            graph[accomplice].add(suspect)
            save_to_file(graph, filename)

        elif choice == '3':
            display_all_suspects(graph)

        elif choice == '4':
            suspect = input("Enter suspect name: ").strip()
            if suspect in graph:
                display_potential_accomplices(suspect, graph)
            else:
                print("Suspect not found in the graph.")

        elif choice == 's':
            num_suspects = len(graph)
            total_accomplices = sum(len(accomplices) for accomplices in graph.values())
            avg_accomplices = total_accomplices / num_suspects if num_suspects else 0

            print(f"Total number of suspects         : {num_suspects}")
            print(f"Number of accomplices on average : {avg_accomplices:.1f}")

        elif choice == 'e':
            break

        else:
            print("Invalid option. Please choose again.")

if __name__ == '__main__':
    main()