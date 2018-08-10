# init dictionary
people = {'name': 'Bob', 'hometown': 'Palo Alto', 'favorite_color': 'red'}

# loop
for item in people:
    # check if 'favorite_color' is in the list and assigns value to 'item'
    if (item == 'favorite_color'):
        #print value of item - red
        print(people[item])
