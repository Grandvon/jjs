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
class RatingSystem(webapp2.RequestHandler):
    def post(self):
        value= int(self.request.get('value')) # this will get the value from the field named username
        print value # this will write on the document

class GameData(ndb.Model):
    stars = ndb.StringProperty()
    review = ndb.StringProperty()
    user_name = ndb.StringProperty()
    game = ndb.StringProperty()


class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        email_address = user.nickname()
        var_user = {"first_name" : cssi_user.first_name,
        "last_name": cssi_user.last_name, "email_address" : email_address}

        main_template = env.get_template('profile.html')
        self.response.out.write(main_template.render(var_user))


<<<<<<< HEAD

=======
#The following handlers each follow the template for the gaming review page.
>>>>>>> 972175b044a4fb52627e4f3119d6a9aacda84bed
class Tekken7Handler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
<<<<<<< HEAD

        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = 'tekken', stars=self.request.get('stars'))
=======
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = 'tekken')
>>>>>>> 972175b044a4fb52627e4f3119d6a9aacda84bed
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == 'tekken')
        query = query.order(GameData.review)
        results = query.fetch()
<<<<<<< HEAD

        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == 'tekken')
        query = query.order(GameData.review)
        stars = query.fetch()




=======
>>>>>>> 972175b044a4fb52627e4f3119d6a9aacda84bed
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Tekken 7',
                                        'pic' : 'https://i.ytimg.com/vi/7NyPT_o5aOs/maxresdefault.jpg',
                                        'synopsis': "lorem ipsum...",
                                        'stars' : stars,
                                        'review': results,
                                        'game': 'tekken' }))



class DriftingHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = 'drifting-lands')
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == 'drifting-lands')
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Drifting Lands',
                                        'pic' : 'https://steamdb.info/static/camo/apps/327240/header.jpg',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': 'drifting-lands' }))

class Dirt4Handler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = 'dirt-4')
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == 'dirt-4')
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Dirt 4',
                                        'pic' : 'http://blogcdn.codemasters.com/wp-content/uploads/2017/01/Fiesta_Aus_3.jpg',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': 'dirt-4' }))

class ESHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'elder-scrolls'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'ESO: Morrowwind',
                                        'pic' : 'http://assets1.ignimgs.com/2017/01/31/esomorrowind-stills-naryu-1485890491125_1280w.jpg',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))

class UnderPressureHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'under-pressure'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'GOTG Eps 2:Under Pressure',
                                        'pic' : "https://dontfeedthegamers.com/wp-content/uploads/2017/05/telltale-guardians-episode-2.jpg",
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))


class TownOfLightHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'town-of-light'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'The Town of Light',
                                        'pic' : 'https://i.ytimg.com/vi/RAI3B0K9HiU/maxresdefault.jpg',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))

class WipeoutHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'wipeout'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Wipeout Omega Collection',
                                        'pic' : 'https://media.playstation.com/is/image/SCEA/wipeout-omega-collection-screen-08-us-03dec16?$MediaCarousel_Original$',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))

class WonderBoyHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'wonder-boy'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Wonder Boy',
<<<<<<< HEAD
                                        'pic' : '',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))
=======
                                        'pic' : 'https://i.ytimg.com/vi/ibKf66tVoFw/maxresdefault.jpg',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))
>>>>>>> 972175b044a4fb52627e4f3119d6a9aacda84bed

class ArmsHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'arms'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Arms',
<<<<<<< HEAD
                                        'pic' : '',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))
=======
                                        'pic' : 'http://content.newsinc.com/jpg/838/32428466/56430218.jpg?t=1495116180',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))
>>>>>>> 972175b044a4fb52627e4f3119d6a9aacda84bed


class DeadByDayLightHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'dead-by-daylight'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Dead by Daylight',
<<<<<<< HEAD
                                        'pic' : '',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))
=======
                                        'pic' : 'https://images4.alphacoders.com/721/721397.jpg',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))

>>>>>>> 972175b044a4fb52627e4f3119d6a9aacda84bed

class StormbloodHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'stormblood'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Stormblood',
<<<<<<< HEAD
                                        'pic' : '',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))
=======
                                        'pic' : 'http://cdn.mos.cms.futurecdn.net/F8MCdkAPcjJSSyoTPnGoV.jpg',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))
>>>>>>> 972175b044a4fb52627e4f3119d6a9aacda84bed

class NexMachinaHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'nex-machina'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Nex Machina',
<<<<<<< HEAD
                                        'pic' : '',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))
=======
                                        'pic' : 'https://media.playstation.com/is/image/SCEA/nex-machina-screen-03-ps4-us-03dec16?$MediaCarousel_Original$',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))
>>>>>>> 972175b044a4fb52627e4f3119d6a9aacda84bed

class GetEvenHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'get-even'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Get Even',
<<<<<<< HEAD
                                        'pic' : '',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))
=======
                                        'pic' : 'http://cdn.mos.cms.futurecdn.net/JZsnFaFsJjFDBhQa9MbuDc.jpg',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))
>>>>>>> 972175b044a4fb52627e4f3119d6a9aacda84bed

class DanganronpaHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'danganronpa'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Danganronpa: Ultra Despair Girls',
<<<<<<< HEAD
                                        'pic' : '',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))
=======
                                        'pic' : 'https://cdn.destructoid.com//ul/307925-2811075-trailer_danganronpaultra_despairgirls_20150220.jpg',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))
>>>>>>> 972175b044a4fb52627e4f3119d6a9aacda84bed

class EliteHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'elite'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Elite: Dangerous',
<<<<<<< HEAD
                                        'pic' : '',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))
=======
                                        'pic' : 'https://static.gamespot.com/uploads/original/1197/11970954/2823045-starport_anaconda.jpg',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))
>>>>>>> 972175b044a4fb52627e4f3119d6a9aacda84bed

class GolfClub2Handler(webapp2.RequestHandler):
    def get(self):
        name_url = 'the-golf-club-2'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'The Golf Club 2',
<<<<<<< HEAD
                                        'pic' : '',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))
=======
                                        'pic' : 'https://i.ytimg.com/vi/GpyT0XC4bv0/maxresdefault.jpg',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))
>>>>>>> 972175b044a4fb52627e4f3119d6a9aacda84bed

class ValkyriaHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'valkyria-revolution'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Valkyria Revolution',
<<<<<<< HEAD
                                        'pic' : '',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))
=======
                                        'pic' : 'https://cdn.vox-cdn.com/thumbor/yuU5RA7yAATMWZ2vd8h8jU6m6Eo=/0x0:1600x900/1200x800/filters:focal(672x322:928x578)/cdn.vox-cdn.com/uploads/chorus_image/image/50889561/valkyria_azure_revolution.0.jpg',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))

>>>>>>> 972175b044a4fb52627e4f3119d6a9aacda84bed

class CBNSHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'cbns-trilogy'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Crash Bandicoot N. Sane Trilogy',
<<<<<<< HEAD
                                        'pic' : '',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))









=======
                                        'pic' : 'https://media.playstation.com/is/image/SCEA/crash-bandicoot-n-sane-trilogy-screen-04-us-03dec16?$MediaCarousel_Original$',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))

class ThatsYouHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'thats-you'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "That's You!",
                                        'pic' : 'https://static.gamespot.com/uploads/screen_kubrick/1570/15709614/3256358-site_gameplay_thatsyou_20170703.jpg',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))

class MetalSlugHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'metal-slug-2'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Metal Slug 2 (re-release)",
                                        'pic' : 'http://cdn-static.denofgeek.com/sites/denofgeek/files/styles/article_width/public/2017/03/metal-slug-3.jpg?itok=TEoyTJ2s',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))

class WorldvsSwordHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'accel-world-vs-sword-art'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Accel World VS. Sword Art Online",
                                        'pic' : 'http://www.psu.com/media/articles/image/accelworld1.jpg',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))

class FableFortuneHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'fable-fortune'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Fable Fortune",
                                        'pic' : 'https://i.ytimg.com/vi/Lnw499IdZQM/maxresdefault.jpg',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))

class ZodiacHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'the-zodiac-age'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "FF XII: The Zodiac Age",
                                        'pic' : 'http://www.finalfantasyxii.com/img/home/final-fantasy-xii-character-group-shot.jpg',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))

class MinecraftHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'minecraft'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Minecraft: Story Mode Season 2",
                                        'pic' : 'https://cdn2.vox-cdn.com/uploads/chorus_asset/file/8645163/MC201_SeaTempleExterior_1920x1080.jpg',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))

class YonderHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'yonder'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Yonder: The Cloud Catcher Chronicles",
                                        'pic' : 'https://static1.squarespace.com/static/581d5d8220099e9ace514235/590dac0ecd0f684a2947bda3/590dac162e69cf3d4b372644/1494738229692/Bambex.jpg',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))

class MoonHuntersHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'moon-hunters'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Moon Hunters",
                                        'pic' : 'https://cdn.cultofmac.com/wp-content/uploads/2014/09/Moon-Hunters.jpg',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))

class CODHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'COD'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "COD: Mondern Warfare Remastered",
                                        'pic' : 'https://charlieintel.com/wp-content/uploads/2017/06/mwrimage.jpeg',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))

class Splatton2Handler(webapp2.RequestHandler):
    def get(self):
        name_url = 'splatton2'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Splatton 2",
                                        'pic' : 'http://ll-c.ooyala.com/e1/trdG92YjE6CHZOtl9h_Y5M-87LyNMK46/promo324080340',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))

class AvenColonyHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'aven-colony'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Aven Colony",
                                        'pic' : 'http://avencolony.com/wp-content/uploads/2016/08/promo1600x900.png?x16986',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))

class FateExtellaHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'fate-extella'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Fate/Extella:The Umbral Star",
                                        'pic' : 'https://www.gamecrate.com/sites/default/files/Fate%20Extella%20The%20Umbral%20Star%20-%201.jpg',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))

class FortniteHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'fortnite'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Fortnite",
                                        'pic' : 'https://static1.gamespot.com/uploads/original/1406/14063904/2880204-laststand_final_1080p+copy.png',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))

class PyreHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'pyre'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Pyre",
                                        'pic' : 'https://cdn.vox-cdn.com/uploads/chorus_asset/file/8903015/Pyre_May_2017_01.jpg',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))

class DanganronpaPCHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'danganronpaPC'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Danganronpa: Ultra Despair Girls (PC)",
                                        'pic' : 'https://cdn.destructoid.com//ul/307925-2811075-trailer_danganronpaultra_despairgirls_20150220.jpg',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))

class TacomaHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'tacoma'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Tacoma",
                                        'pic' : 'http://gameranx.com/wp-content/uploads/2016/03/tacoma-1.jpg',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))

class HellbladeHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'hellblade'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Hellblade:Senua's Sacrifice",
                                        'pic' : 'https://i.ytimg.com/vi/WOSDW_wxH3Y/maxresdefault.jpg',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))

class LawbreakersHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'lawbreakers'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Lawbreakers",
                                        'pic' : 'https://static.gamespot.com/uploads/original/536/5360430/3106269-lawbreakers_vangaurd_vs_titan.jpg',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))

class MegaManHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'mega-man'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Mega Man Legacy Collection 2",
                                        'pic' : 'https://c.slashgear.com/wp-content/uploads/2017/04/mega-man-legacy-collection-980x420.png',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))

class SonicManiaHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'sonic-mania'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Sonic Mania",
                                        'pic' : 'https://i.ytimg.com/vi/OiL3fqk5yRo/maxresdefault.jpg',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))

class UnchartedHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'uncharted'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Uncharted: The Lost Legacy",
                                        'pic' : 'https://apollo2.dl.playstation.net/cdn/UP9000/CUSA07737_00/FREE_CONTENT0SZAeSQd9jFnHHvJmvDm/PREVIEW_SCREENSHOT2_146393.jpg',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))

class MaddenHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'madden-nfl-18'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Madden NFL 18",
                                        'pic' : 'http://www.sportsgamersonline.com/wp-content/uploads/2017/02/tom-brady-madden-25-13-1200x630-c.jpg',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))

class AbsolverHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'absolver'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Absolver",
                                        'pic' : 'https://static.gamespot.com/uploads/original/536/5360430/3068853-absolver+-+screen+4.png',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))

class WarriorsHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'warriors-all-stars'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Warriors All-Stars",
                                        'pic' : 'https://cdn1.vox-cdn.com/uploads/chorus_asset/file/8323817/WarriorsAllStars_Screenshot06.jpg',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))

class GolfHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'everybodys-golf'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Everybody's Golf",
                                        'pic' : 'https://c1.staticflickr.com/3/2845/33305050694_de7e749473_b.jpg',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))

class MarioRabidsHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'mario-rabids'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Mario + Rabbids: Kingdom Battle",
                                        'pic' : 'http://gematsu.com/wp-content/uploads/2017/06/Mario-Rabbids-Kingdom-Battle-Announced-Init.jpg',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))

class YakuzaKiwamiHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'yakuza-kiwami'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Yakuza Kiwami",
                                        'pic' : 'https://www.bleedingcool.com/wp-content/uploads/2017/04/Yakuza-Kiwami.png',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))

class LifeIsStrangeHandler(webapp2.RequestHandler):
    def get(self):
        name_url = 'life-is-strange'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Life is Strange: Before the Storm",
                                        'pic' : 'https://cdn.vox-cdn.com/uploads/chorus_asset/file/8696367/e327ba76bf878c05dd80de3ff0361f35_1920_KR.jpg',
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'game': name_url }))
>>>>>>> 972175b044a4fb52627e4f3119d6a9aacda84bed




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
