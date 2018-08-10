# m101p
Repo for Python code written for [M101P: MongoDB for Developers course](https://university.mongodb.com/courses/M101P/about).

# Notes on Python - How to Read the Code

## Versions
Python version is 3.6.6
Pip version is 9.0.3
pymongo version is 3.0.0

### Code formatting

Since I'm using Python 3 and the class is using 2.6, I think, my code will be formatted differently. For example, from the ```python_basics/for_loops.py``` script, the class examples show  ```print``` functions do not use parentheses ```()``` to encase printed variables.
```python
# init array
fruit = ['apple', 'orange', 'grape']

# init new empty array
new_fruit = []

# for loop to loop over fruit array
for item in fruit:
    # print the item in the array
    print item

    # append the printed item to a new list
    new_fruit.append(item)

# print the new list
print new_fruit
```
My code is as follows:

```python
# init array
fruit = ['apple', 'orange', 'grape']

# init new empty array
new_fruit = []

# for loop to loop over fruit array
for item in fruit:
    # print the item in the array
    print(item)

    # append the printed item to a new list
    new_fruit.append(item)

# print the new list
print(new_fruit)
```
I believe this is due to the examples being Python2 and not Python3, but I'm not 100% on that. Either way, encasing variables with ```()``` for my code works. I'm happy with that.

### Executing Python 3

I'm developing on Linux and the alias ```alias python='python3'``` defined in my ```~/.bashrc``` file. Every time I call ```python``` on the CLI, I actually call ```python3```. I did the same for Pip, but I'm not sure if that matters. It works so I'm leaving it.
