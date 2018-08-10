# init list
fruit = ['apple', 'orange', 'grape', 'kiwi', 'orange', 'apple']

# function to report the frequency of every item in the list, passing fruit into function
def analyze_list(fruit):

    # init counts dictionary
    counts = {}

    # for loop over fruit
    for item in fruit:

        # check to see if item has a count
        if item in counts:

            # if true, incriment count by 1
            counts[item] = counts[item] + 1
        else:
            # if false, assign the value of 1 to item
            counts[item] = 1

    # return the dict to make it accessable outside the function
    return counts

# analyze the list and call the function
counts = analyze_list(fruit)

# print the dictionary at the end.
print(counts)
