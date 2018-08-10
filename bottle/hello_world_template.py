import bottle

@bottle.route('/')
def home_page():
    mythings = ['apple', 'orange', 'banana', 'peach']
    return bottle.template('hello_world', {'username':'Ryan', 'things': mythings})

bottle.debug(True)
bottle.run(hosts='localhost', port=8080)
