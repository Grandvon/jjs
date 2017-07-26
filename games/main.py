import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2

env=jinja2.Environment(loader=jinja2.FileSystemLoader(''))

class CssiUser(ndb.Model):
  """CssiUser stores information about a logged-in user.

  The AppEngine users api stores just a couple of pieces of
  info about logged-in users: a unique id and their email address.

  If you want to store more info (e.g. their real name, high score,
  preferences, etc, you need to create a Datastore model like this
  example).
  """
  first_name = ndb.StringProperty()
  last_name = ndb.StringProperty()

class MainHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    # If the user is logged in...
    ""
    main_template = env.get_template('signin.html')
    self.response.out.write(main_template.render())
    if user:
      email_address = user.nickname()
      cssi_user = CssiUser.get_by_id(user.user_id())
      signout_link_html = '<a class = edits href="%s">sign out</a>' % (
          users.create_logout_url('/'))
      # If the user has previously been to our site, we greet them!
      if cssi_user:
        self.response.write(''' <div class = edits>
            Welcome %s %s (%s)! <br> %s <br> </div>''' % (
              cssi_user.first_name,
              cssi_user.last_name,
              email_address,
              signout_link_html))
      # If the user hasn't been to our site, we ask them to sign up
      else:
        self.response.write('''<div class = edits>
            Welcome to our site, %s!  Please sign up! <br>
            <form method="post" action="/">
            First Name: <input type="text" name="first_name">
            Last Name: <input type="text" name="last_name">
            <input type="submit">
            </form><br> %s <br> </div>
            ''' % (email_address, signout_link_html))
    # Otherwise, the user isn't logged in!
    else:
      self.response.write('''<div class = edits>
        Please log in to use our site! <br>
        <a href="%s">Sign in</a> </div>''' % (
          users.create_login_url('/')))



  def post(self):
    main_template = env.get_template('signin.html')
    self.response.out.write(main_template.render())
    user = users.get_current_user()
    if not user:
      # You shouldn't be able to get here without being logged in
      self.error(500)
      return
    cssi_user = CssiUser(
        first_name=self.request.get('first_name'),
        last_name=self.request.get('last_name'),
        id=user.user_id())
    cssi_user.put()
    self.response.write('<div class = edits> Thanks for signing up, %s!</div>' %
        cssi_user.first_name)



class GameHandler(webapp2.RequestHandler):
  def get(self):
    main_template = env.get_template('mainpage.html')
    self.response.out.write(main_template.render())

class ReviewHandler(webapp2.RequestHandler):
  def get(self):
    main_template = env.get_template('gamepages.html')
    self.response.out.write(main_template.render())

class HistoryHandler(webapp2.RequestHandler):
  def get(self):
      main_template = env.get_template('history.html')
      self.response.out.write(main_template.render())

class BattleHandler(webapp2.RequestHandler):
  def get(self):
      main_template = env.get_template('battle.html')
      self.response.out.write(main_template.render())

class GameData(ndb.Model):
    stars = ndb.StringProperty()
class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        main_template = env.get_template('profile.html')
        self.response.out.write(main_template.render())

class Tekken7Handler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '4.75')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Tekken 7',
                                        'pic' : 'https://i.ytimg.com/vi/7NyPT_o5aOs/maxresdefault.jpg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))


class DriftingHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '3')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Drifting Lands',
                                        'pic' : 'https://steamdb.info/static/camo/apps/327240/header.jpg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class Dirt4Handler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Dirt 4',
                                        'pic' : '',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class ESHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'ESO: Morrowwind',
                                        'pic' : '',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class UnderPressureHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'GOTG Eps 2:Under Pressure',
                                        'pic' : '',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class TownOfLightHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'The Town of Light',
                                        'pic' : '',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class WipeoutHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Wipeout Omega Collection',
                                        'pic' : '',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class WonderBoyHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Wonder Boy',
                                        'pic' : '',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class ArmsHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Arms',
                                        'pic' : '',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))


class DeadByDayLightHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Dead by Daylight',
                                        'pic' : '',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class StormbloodHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Stormblood',
                                        'pic' : '',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class NexMachinaHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Nex Machina',
                                        'pic' : '',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class GetEvenHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Get Even',
                                        'pic' : '',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class DanganronpaHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Danganronpa: Ultra Despair Girls',
                                        'pic' : '',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class EliteHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Elite: Dangerous',
                                        'pic' : '',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class GolfClub2Handler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'The Golf Club 2',
                                        'pic' : '',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class ValkyriaHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Valkyria Revolution',
                                        'pic' : '',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class CBNSHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Crash Bandicoot N. Sane Trilogy',
                                        'pic' : '',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))













app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/homepage', GameHandler),
  ('/gaming-reviews', ReviewHandler),
  ('/history-of-gaming', HistoryHandler),
  ('/console-battle-arena', BattleHandler),
  ('/profile', ProfileHandler),
  ('/tekken', Tekken7Handler),
  ('/drifting-lands', DriftingHandler),
  ('/dirt-4', Dirt4Handler),
  ('/elder-scrolls', ESHandler),
  ('/under-pressure', UnderPressureHandler),
  ('/town-of-light', TownOfLightHandler),
  ('/wipeout', WipeoutHandler),
  ('/wonder-boy', WonderBoyHandler),
  ('/arms', ArmsHandler),
  ('/dead-by-daylight', DeadByDayLightHandler),
  ('/stormblood', StormbloodHandler),
  ('/nex-machina', NexMachinaHandler),
  ('/get-even', GetEvenHandler),
  ('/danganronpa', DanganronpaHandler),
  ('/elite', EliteHandler),
  ('/the-golf-club-2', GolfClub2Handler),
  ('/valkyria-revolution', ValkyriaHandler),
  ('/cbns-trilogy', CBNSHandler),
  ('/tekken', Tekken7Handler),
  ('/tekken', Tekken7Handler),
  ('/tekken', Tekken7Handler),

], debug=True)
