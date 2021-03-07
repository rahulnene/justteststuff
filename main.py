n = int(input())  # number of capitals
m = int(input())  # number of geolocations for which to find the closest capital

def d(lat1,long1,lat2,long2):
    return True

capitals = []
messages = dict()
for i in range(n):
    capitals.append(input().split())
for i in range(n):
    messages[capitals[i][0]] = input()

for i in range(m):
    travel_geoloc = input()
for i in range(m):
    input()

print(capitals)
print(messages)