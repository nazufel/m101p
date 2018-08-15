import bottle

# default index route
@bottle.route('/')
def home_page():
        mythings = ['apple', 'orange', 'banana', 'peach']
        return bottle.template('hello_world_form', {'username':'Ryan', 'things': mythings})

# post endpoint at /favorite_fruit
@bottle.post('/favorite_fruit')
def favorite_fruit():
    # gets the form element on the form
    fruit = bottle.request.forms.get('fruit')
    # check if the fruit element isn't there, it sets
    if (fruit == None or fruit == ""):
        fruit="No Fruit Selected"
    # returns the template with the new value added
#    return bottle.template('fruit_selection.tpl', {'fruit': fruit})

    bottle.reponse.set_cookie('fruit', fruit)
    bottle.redirect('/show_fruit')

@bottle.route('/show_fruit')
def show_fruit():
    fruit = bottle.request.get_cookie('fruit')

    return bottle.template('fruit_selection.tpl', {'fruit':fruit})

bottle.debug(True)
bottle.run(hosts='localhost', port=8080)
