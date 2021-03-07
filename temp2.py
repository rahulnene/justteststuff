from time import perf_counter

t0 = perf_counter()
ans = []
nummaps = int(input())


def check(graph_in, cities_in):
    def neighborhood(city_temp):
        out = set([])
        for i in range(len(cities_in)):
            if graph_in[cities_in.index(city_temp)][i] == 1:
                out.add(cities_in[i])
        return list(out)

    def find_next(city_temp, visited_temp):
        for element in neighborhood(city_temp):
            if element in visited_temp:
                return "Cycled!"
            elif element not in visited_temp:
                return element
        return "End"

    for currentVertex in cities_in:
        visited = [currentVertex]
        while find_next(currentVertex, visited) not in ["Cycled!", "End"]:
            print(currentVertex)
            currentVertex = find_next(currentVertex, visited)
            visited.append(currentVertex)
        if find_next(currentVertex, visited) == "End":
            return 0
        if find_next(currentVertex, visited) == "Cycled!":
            return 1


for p in range(nummaps):
    cities = set()
    given = [x for x in input().split(" ")]
    roads = int(given[0])
    given = given[1:]
    for road in given:
        cities.add(road[0])
        cities.add(road[2])
    cities = list(cities)
    cities.sort()
    graph = [[0] * len(cities) for _ in range(len(cities))]
    for road in given:
        cityA = road[0]
        cityB = road[2]
        indA = cities.index(cityA)
        indB = cities.index(cityB)
        graph[indA][indB] = 1
        graph[indB][indA] = 1
        ans.append(check(graph, cities))

for a in ans:
    print(a, end=" ")

print("")
tf = perf_counter() - t0
print(tf, "seconds")
