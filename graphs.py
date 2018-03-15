import matplotlib.pylab as p

from data_functs import get_meals_for_the_week



username = session['username']
events = get_meals_for_the_week(username)

dinners = [event.meal for event in events]


lists = sorted(d.items())

x,y = zip(*lists)

p.plot(x, y)
p.show()