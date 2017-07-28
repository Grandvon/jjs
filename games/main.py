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

class ResultsHandler(webapp2.RequestHandler):
  def get(self):
      consoles = ['ps4', 'xbox', 'pc', 'console', 'switch', 'vr']
      var_poll = {}
      for console in consoles:

          var_poll[console] = len(PollData.query(PollData.vote == console).fetch())

      main_template = env.get_template('pollresults.html')
      self.response.out.write(main_template.render(var_poll))

  def post(self):
      consoles = ['ps4', 'xbox', 'pc', 'console', 'switch', 'vr']
      for console in consoles:
          if self.request.get(console):
              polldata = PollData(vote = console)
              polldata.put()

      self.get()




class PollData(ndb.Model):
    vote = ndb.StringProperty()

class GameData(ndb.Model):
    stars = ndb.StringProperty()
    review = ndb.StringProperty()
    user_name = ndb.StringProperty()
    game = ndb.StringProperty()


class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            main_template = env.get_template('profile.html')
            self.response.out.write(main_template.render({"alert": ("Please go to the sign in page and sign in.")}))
        else:
            cssi_user = CssiUser.get_by_id(user.user_id())
            email_address = user.nickname()
            var_user = {"first_name" : cssi_user.first_name,
            "last_name": cssi_user.last_name, "email_address" : email_address}
            main_template = env.get_template('profile.html')
            self.response.out.write(main_template.render(var_user))


#The following handlers each follow the template for the gaming review page.
class Tekken7Handler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name + " " + cssi_user.last_name, game = 'tekken')
        alert = ''
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == 'tekken')
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Tekken 7',
                                        'pic' : 'https://i.ytimg.com/vi/7NyPT_o5aOs/maxresdefault.jpg',
                                        'synopsis': "After the events of Tekken 6, the war between the Mishima Zaibatsu and G Corporation still continues along with the disappearance of Jin Kazama. Meanwhile, a investigative journalist who lost his wife and son during the war that Jin started (and whom also narrates throughout part of the game) begins narrating about the Mishima Zaibatsu and G Corporation.",
                                        'review': results,
                                        'game': 'tekken',
                                        'rating': rating,
                                        'alert': alert}))



class DriftingHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = 'drifting-lands')
        alert = ''
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == 'drifting-lands')
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Drifting Lands',
                                        'pic' : 'https://steamdb.info/static/camo/apps/327240/header.jpg',
                                        'synopsis': "Drifting Lands takes place in the skies of a shattered planet. Centuries ago a huge cataclysm fragmented and froze this world in a state of partial disintegration. Powerful and mysterious gravitational anomalies keep the huge chunks of rock from drifting away in space or collapsing into a single body. <br><br>The last floating continents fit for human civilization are controlled by big private corporations acting as totalitarian states. These so called nations compete fiercely to survive and exploit every available natural resources.",
                                        'review': results,
                                        'game': 'drifting-lands',
                                        'rating': rating,
                                        'alert': alert }))

class Dirt4Handler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = 'dirt-4')
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == 'dirt-4')
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Dirt 4',
                                        'pic' : 'http://blogcdn.codemasters.com/wp-content/uploads/2017/01/Fiesta_Aus_3.jpg',
                                        'synopsis': "Dirt 4 is a rally-themed racing video game developed by Codemasters. It is the twelfth game in the Colin McRae Rally series and the sixth title to carry the Dirt name. The game launched on Microsoft Windows, PlayStation 4 and Xbox One in June 2017.",
                                        'review': results,
                                        'game': 'dirt-4',
                                        'rating': rating,
                                        'alert': alert }))

class ESHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'elder-scrolls'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'ESO: Morrowwind',
                                        'pic' : 'http://assets1.ignimgs.com/2017/01/31/esomorrowind-stills-naryu-1485890491125_1280w.jpg',
                                        'synopsis': "The Elder Scrolls Online is a massively multiplayer online role-playing video game developed by ZeniMax Online Studios and published by Bethesda Softworks. It was originally released for Microsoft Windows and OS X in April 2014.",
                                        'review': results,
                                        'game': name_url,

                                        'alert': alert }))

class UnderPressureHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'under-pressure'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'GOTG Eps 2:Under Pressure',
                                        'pic' : "https://dontfeedthegamers.com/wp-content/uploads/2017/05/telltale-guardians-episode-2.jpg",
                                        'synopsis': "Star-Lord and the rest of the gang travel across the galaxy to search for answers and look for help from old friends while trying to outrun some genocidal enemies. \"Under Pressure\" also promises to delve into Rocket Raccoon's dark past.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))


class TownOfLightHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'town-of-light'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'The Town of Light',
                                        'pic' : 'https://i.ytimg.com/vi/RAI3B0K9HiU/maxresdefault.jpg',
                                        'synopsis': "The Town of Light is a psychological horror adventure game developed by LKA. It was released for the PC on February 26, 2016 and PS4 and Xbox One on June 6, 2017.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class WipeoutHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'wipeout'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Wipeout Omega Collection',
                                        'pic' : 'https://media.playstation.com/is/image/SCEA/wipeout-omega-collection-screen-08-us-03dec16?$MediaCarousel_Original$',
                                        'synopsis': "Wipeout is a series of futuristic anti-gravity racing video games developed by Sony Studio Liverpool, formerly known as Psygnosis.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class WonderBoyHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'wonder-boy'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Wonder Boy',
                                        'pic' : 'https://i.ytimg.com/vi/ibKf66tVoFw/maxresdefault.jpg',
                                        'synopsis': "The Wonder Boy series, also known as the Monster World series, is a franchise of video games published by Sega and developed by Westone Bit Entertainment.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class ArmsHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'arms'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Arms',
                                        'pic' : 'http://content.newsinc.com/jpg/838/32428466/56430218.jpg?t=1495116180',
                                        'synopsis': "Arms is a fighting game developed and published by Nintendo for the Nintendo Switch, released worldwide in June 2017.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))


class DeadByDayLightHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'dead-by-daylight'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Dead by Daylight',
                                        'pic' : 'https://images4.alphacoders.com/721/721397.jpg',
                                        'synopsis': "Dead by Daylight is an asymmetric survival horror video game developed by Behavior Interactive and published by Starbreeze Studios.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))


class StormbloodHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'stormblood'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Stormblood',
                                        'pic' : 'http://cdn.mos.cms.futurecdn.net/F8MCdkAPcjJSSyoTPnGoV.jpg',
                                        'synopsis': "From the mightiest of mountains to the darkest of depths, adventurers have braved all manner of dangers for want of spoils and glory. In an endeavor to bring ever richer experiences to the intrepid heroes of Eorzea, two esteemed guest creators have been invited to partake in creating harrowing new challenges for the realm's bravest adventurers.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class NexMachinaHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'nex-machina'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Nex Machina',
                                        'pic' : 'https://media.playstation.com/is/image/SCEA/nex-machina-screen-03-ps4-us-03dec16?$MediaCarousel_Original$',
                                        'synopsis': "Nex Machina is a shoot 'em up video game developed and published by Housemarque. The game was released in June 2017 for the PlayStation 4 video game console and Windows-based personal computers.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class GetEvenHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'get-even'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Get Even',
                                        'pic' : 'http://cdn.mos.cms.futurecdn.net/JZsnFaFsJjFDBhQa9MbuDc.jpg',
                                        'synopsis': "Get Even is a first-person shooter video game developed by The Farm 51 and published by Bandai Namco Entertainment for Microsoft Windows, PlayStation 4 and Xbox One.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class DanganronpaHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'danganronpa'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Danganronpa: Ultra Despair Girls',
                                        'pic' : 'https://cdn.destructoid.com//ul/307925-2811075-trailer_danganronpaultra_despairgirls_20150220.jpg',
                                        'synopsis': "Danganronpa Another Episode: Ultra Despair Girls is an action-adventure video game developed by Spike Chunsoft for PlayStation Vita.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class EliteHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'elite'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Elite: Dangerous',
                                        'pic' : 'https://static.gamespot.com/uploads/original/1197/11970954/2823045-starport_anaconda.jpg',
                                        'synopsis': "lite: Dangerous is a space adventure, trading, and combat simulation video game developed and published by Frontier Developments.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class GolfClub2Handler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'the-golf-club-2'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'The Golf Club 2',
                                        'pic' : 'https://i.ytimg.com/vi/GpyT0XC4bv0/maxresdefault.jpg',
                                        'synopsis': "Rise to fame and fortune in the largest, most dynamic golf game ever created. Assemble and join online Societies with friends, compete in tournaments, and earn money to climb the ranks in golf's largest gaming community.",
                                        'review': results,
                                        'game': name_url ,
                                        'rating': rating,
                                        'alert': alert}))

class ValkyriaHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'valkyria-revolution'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Valkyria Revolution',
                                        'pic' : 'https://cdn.vox-cdn.com/thumbor/yuU5RA7yAATMWZ2vd8h8jU6m6Eo=/0x0:1600x900/1200x800/filters:focal(672x322:928x578)/cdn.vox-cdn.com/uploads/chorus_image/image/50889561/valkyria_azure_revolution.0.jpg',
                                        'synopsis': "Valkyria Revolution, known in Japan as Valkyria: Azure Revolution, is an action role-playing video game developed by Media.Vision for PlayStation 4, PlayStation Vita and Xbox One.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))


class CBNSHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'cbns-trilogy'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Crash Bandicoot N. Sane Trilogy',
                                        'pic' : 'https://media.playstation.com/is/image/SCEA/crash-bandicoot-n-sane-trilogy-screen-04-us-03dec16?$MediaCarousel_Original$',
                                        'synopsis': "Crash Bandicoot N. Sane Trilogy is a platform video game compilation developed by Vicarious Visions and published by Activision for PlayStation 4.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class ThatsYouHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'thats-you'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "That's You!",
                                        'pic' : 'https://static.gamespot.com/uploads/screen_kubrick/1570/15709614/3256358-site_gameplay_thatsyou_20170703.jpg',
                                        'synopsis': "Get hilariously personal in this audacious social quiz from the PlayLink range, exclusive to PS4.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class MetalSlugHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'metal-slug-2'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Metal Slug 2 (re-release)",
                                        'pic' : 'http://cdn-static.denofgeek.com/sites/denofgeek/files/styles/article_width/public/2017/03/metal-slug-3.jpg?itok=TEoyTJ2s',
                                        'synopsis': "Metal Slug 2: Super Vehicle-001/II, more commonly known as simply Metal Slug 2, is a run and gun video game developed by SNK. It was originally released in 1998 for the Neo-Geo MVS arcade platform as the sequel to the popular 1996 game Metal Slug.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class WorldvsSwordHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'accel-world-vs-sword-art'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Accel World VS. Sword Art Online",
                                        'pic' : 'http://www.psu.com/media/articles/image/accelworld1.jpg',
                                        'synopsis': "Svart Alfheim and the Accelerated World have begun to merge. In the midst of the chaos, Yui has gone missing. Kirito must challenge the Seven Kings of pure color from the Accelerated World to gain access to her location. Players from both groups come together in a war of the worlds where the strongest Burst Linkers and ALO Players are on a mission to save Yui from the hands of Personna Babel.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class FableFortuneHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'fable-fortune'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Fable Fortune",
                                        'pic' : 'https://i.ytimg.com/vi/Lnw499IdZQM/maxresdefault.jpg',
                                        'synopsis': "Timeless heroes, despicable villains, countless chickens and a number of vaguely confused peasants will be on standby to welcome you back to this unforgettable CCG experience set in the iconic land of Albion.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class ZodiacHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'the-zodiac-age'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "FF XII: The Zodiac Age",
                                        'pic' : 'http://www.finalfantasyxii.com/img/home/final-fantasy-xii-character-group-shot.jpg',
                                        'synopsis': "Enter an era of war within the world of Ivalice. The small kingdom of Dalmasca, conquered by the Archadian Empire, is left in ruin and uncertainty. Princess Ashe, the one and only heir to the throne, devotes herself to the resistance to liberate her country. Vaan, a young man who lost his family in the war, dreams of flying freely in the skies. In a fight for freedom and fallen royalty, join these unlikely allies and their companions as they embark on a heroic adventure to free their homeland.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class MinecraftHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'minecraft'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Minecraft: Story Mode Season 2",
                                        'pic' : 'https://cdn2.vox-cdn.com/uploads/chorus_asset/file/8645163/MC201_SeaTempleExterior_1920x1080.jpg',
                                        'synopsis': "Now that Jesse and the gang have vanquished the Wither Storm, saved the world, and become totally super famous heroes, life has gotten a bit more...complicated. With more responsibilities and less time for adventure, old friendships have started to fade -- at least until Jesse's hand gets stuck in a creepy gauntlet that belongs to an ancient underwater temple. Together with old pals and new comrades alike, Jesse embarks on a brand new journey filled with tough choices, good times, and at least one temperamental llama.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class YonderHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'yonder'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Yonder: The Cloud Catcher Chronicles",
                                        'pic' : 'https://static1.squarespace.com/static/581d5d8220099e9ace514235/590dac0ecd0f684a2947bda3/590dac162e69cf3d4b372644/1494738229692/Bambex.jpg',
                                        'synopsis': "Gemea maintains the appearance of a paradise, yet an evil murk has enshrouded the land and its people in despair... As the hero of Yonder you will explore Gemea and uncover the islands secrets and mysteries within yourself.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class MoonHuntersHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'moon-hunters'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Moon Hunters",
                                        'pic' : 'https://cdn.cultofmac.com/wp-content/uploads/2014/09/Moon-Hunters.jpg',
                                        'synopsis': "Moon Hunters is an action role-playing video game developed and published by Kitfox Games.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class CODHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'COD'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "COD: Mondern Warfare Remastered",
                                        'pic' : 'https://charlieintel.com/wp-content/uploads/2017/06/mwrimage.jpeg',
                                        'synopsis': "Call of Duty: Modern Warfare Remastered is a first-person shooter video game developed by Raven Software and published by Activision.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class Splatton2Handler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'splatton2'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Splatton 2",
                                        'pic' : 'http://ll-c.ooyala.com/e1/trdG92YjE6CHZOtl9h_Y5M-87LyNMK46/promo324080340',
                                        'synopsis': "Splatoon 2 is a team-based third-person shooter video game developed and published by Nintendo for the Nintendo Switch. It is the sequel to the 2015 Wii U title Splatoon, and is playable by up to eight players in online four-versus-four matches.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class AvenColonyHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'aven-colony'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Aven Colony",
                                        'pic' : 'http://avencolony.com/wp-content/uploads/2016/08/promo1600x900.png?x16986',
                                        'synopsis': "Aven Colony is a city-building, Sci-fi, strategy video game developed by Mothership Entertainment and published by Itch.io. The Beta was released on September 8, 2016 on Microsoft Windows.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class FateExtellaHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'fate-extella'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Fate/Extella:The Umbral Star",
                                        'pic' : 'https://www.gamecrate.com/sites/default/files/Fate%20Extella%20The%20Umbral%20Star%20-%201.jpg',
                                        'synopsis': "Fate/Extella: The Umbral Star is an action video game developed and published by Marvelous. The game is the third installment in the universe that began with Fate/Extra and the second one to be released outside of Japan.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class FortniteHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'fortnite'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), stars=self.request.get('stars'),user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Fortnite",
                                        'pic' : 'https://static1.gamespot.com/uploads/original/1406/14063904/2880204-laststand_final_1080p+copy.png',
                                        'synopsis': "Fortnite is a co-op sandbox survival video game developed by People Can Fly and Epic Games, the latter of which also serves as publisher for the game.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class PyreHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'pyre'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Pyre",
                                        'pic' : 'https://cdn.vox-cdn.com/uploads/chorus_asset/file/8903015/Pyre_May_2017_01.jpg',
                                        'synopsis': "Pyre is an action role-playing video game developed by Supergiant Games for Microsoft Windows and PlayStation 4, released on July 25, 2017.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class DanganronpaPCHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'danganronpaPC'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Danganronpa: Ultra Despair Girls (PC)",
                                        'pic' : 'https://cdn.destructoid.com//ul/307925-2811075-trailer_danganronpaultra_despairgirls_20150220.jpg',
                                        'synopsis': "Danganronpa Another Episode: Ultra Despair Girls is an action-adventure video game developed by Spike Chunsoft for PlayStation Vita.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class TacomaHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'tacoma'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Tacoma",
                                        'pic' : 'http://gameranx.com/wp-content/uploads/2016/03/tacoma-1.jpg',
                                        'synopsis': "Tacoma is a video game by Fullbright. It is scheduled for release on Linux, Microsoft Windows, OS X, and Xbox One consoles in August 2017.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class HellbladeHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'hellblade'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Hellblade:Senua's Sacrifice",
                                        'pic' : 'https://i.ytimg.com/vi/WOSDW_wxH3Y/maxresdefault.jpg',
                                        'synopsis': "Hellblade: Senua's Sacrifice is an upcoming action-adventure video game developed and published by the British developer Ninja Theory.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class LawbreakersHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'lawbreakers'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Lawbreakers",
                                        'pic' : 'https://static.gamespot.com/uploads/original/536/5360430/3106269-lawbreakers_vangaurd_vs_titan.jpg',
                                        'synopsis': "LawBreakers, previously known under the code-name BlueStreak, is an upcoming first-person shooter video game developed by Boss Key Productions and published by Nexon.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class MegaManHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'mega-man'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Mega Man Legacy Collection 2",
                                        'pic' : 'https://c.slashgear.com/wp-content/uploads/2017/04/mega-man-legacy-collection-980x420.png',
                                        'synopsis': "4-in-1 Timeless Adventures - Experience the legacy of long-time video game icon Mega Man with these four most recent classics from the core series",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class SonicManiaHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'sonic-mania'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), stars=self.request.get('stars'),user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Sonic Mania",
                                        'pic' : 'https://i.ytimg.com/vi/OiL3fqk5yRo/maxresdefault.jpg',
                                        'synopsis': "Sonic Mania is an upcoming side-scrolling platform game developed by Headcannon and PagodaWest Games and published by Sega for Microsoft Windows, Nintendo Switch, PlayStation 4 and Xbox One.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class UnchartedHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'uncharted'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Uncharted: The Lost Legacy",
                                        'pic' : 'https://apollo2.dl.playstation.net/cdn/UP9000/CUSA07737_00/FREE_CONTENT0SZAeSQd9jFnHHvJmvDm/PREVIEW_SCREENSHOT2_146393.jpg',
                                        'synopsis': "Uncharted: The Lost Legacy is an action-adventure video game developed by Naughty Dog and published by Sony Interactive Entertainment.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class MaddenHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'madden-nfl-18'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Madden NFL 18",
                                        'pic' : 'http://www.sportsgamersonline.com/wp-content/uploads/2017/02/tom-brady-madden-25-13-1200x630-c.jpg',
                                        'synopsis': "Madden NFL 18 is an upcoming American football video game based on the NFL that is being developed by EA Tiburon and published by EA.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class AbsolverHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'absolver'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Absolver",
                                        'pic' : 'https://static.gamespot.com/uploads/original/536/5360430/3068853-absolver+-+screen+4.png',
                                        'synopsis': "Absolver is an upcoming martial arts-focused action role-playing video game developed by Sloclap, a Parisian indie game developer composed of former Ubisoft Paris employees.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class WarriorsHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'warriors-all-stars'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Warriors All-Stars",
                                        'pic' : 'https://cdn1.vox-cdn.com/uploads/chorus_asset/file/8323817/WarriorsAllStars_Screenshot06.jpg',
                                        'synopsis': "Warriors All-Stars, is a hack and slash game by Koei Tecmo. It is a crossover based on the long-running Warriors series, featuring an array of cast taken from various titles owned by the company, similar to the Warriors Orochi series.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class GolfHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'everybodys-golf'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Everybody's Golf",
                                        'pic' : 'https://c1.staticflickr.com/3/2845/33305050694_de7e749473_b.jpg',
                                        'synopsis': "Everybody's Golf, formerly known in North America as Hot Shots Golf, is a series of golf games published by Sony throughout the history of the PlayStation series of video game consoles.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class MarioRabidsHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'mario-rabids'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Mario + Rabbids: Kingdom Battle",
                                        'pic' : 'http://gematsu.com/wp-content/uploads/2017/06/Mario-Rabbids-Kingdom-Battle-Announced-Init.jpg',
                                            'synopsis': "Mario + Rabbids Kingdom Battle is an upcoming turn-based tactical role-playing video game developed and published by Ubisoft.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class YakuzaKiwamiHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'yakuza-kiwami'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'),stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;
        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Yakuza Kiwami",
                                        'pic' : 'https://www.bleedingcool.com/wp-content/uploads/2017/04/Yakuza-Kiwami.png',
                                        'synopsis': "It was developed by Sega for the PlayStation 3 and PlayStation 4",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))

class LifeIsStrangeHandler(webapp2.RequestHandler):
    def get(self):
        alert = ''
        name_url = 'life-is-strange'
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        one = GameData(review=self.request.get('review'), stars=self.request.get('stars'), user_name = cssi_user.first_name, game = name_url)
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                if int(one.stars) >5:
                    alert = ("Please give this game a rating between one and five.")
                elif int(one.stars) <1:
                    alert = ("Please give this game a rating between one and five.")
                else:
                    one.put()
        query = GameData.query()
        query = query.filter(ndb.GenericProperty('game') == name_url)
        query = query.order(GameData.review)
        results = query.fetch()
        rating = 0;
        count = 0;

        for para in results:
            rating += float(para.stars)
            count= count +1
        if count > 0:
            rating = rating / count
        rating = round(rating, 2)
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Life is Strange: Before the Storm",
                                        'pic' : 'https://cdn.vox-cdn.com/uploads/chorus_asset/file/8696367/e327ba76bf878c05dd80de3ff0361f35_1920_KR.jpg',
                                        'synopsis': "Life Is Strange 2 is an upcoming episodic graphic adventure video game developed by Dontnod Entertainment and published by Square Enix.",
                                        'review': results,
                                        'game': name_url,
                                        'rating': rating,
                                        'alert': alert }))




app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/homepage', GameHandler),
  ('/gaming-reviews', ReviewHandler),
  ('/history-of-gaming', HistoryHandler),
  ('/console-battle-arena', BattleHandler),
  ('/profile', ProfileHandler),
  ('/pollresults', ResultsHandler),
    #game handlers
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
  ('/thats-you', ThatsYouHandler),
  ('/metal-slug-2', MetalSlugHandler),
  ('/accel-world-vs-sword-art', WorldvsSwordHandler),
  ('/fable-fortune', FableFortuneHandler),
  ('/the-zodiac-age', ZodiacHandler),
  ('/minecraft', MinecraftHandler),
  ('/yonder', YonderHandler),
  ('/moon-hunters', MoonHuntersHandler),
  ('/COD', CODHandler),
  ('/splatton2', Splatton2Handler),
  ('/aven-colony', AvenColonyHandler),
  ('/fate-extella', FateExtellaHandler),
  ('/fortnite', FortniteHandler),
  ('/pyre', PyreHandler),
  ('/danganronpaPC', DanganronpaPCHandler),
  ('/tacoma', TacomaHandler),
  ('/hellblade', HellbladeHandler),
  ('/lawbreakers', LawbreakersHandler),
  ('/mega-man', MegaManHandler),
  ('/sonic-mania', SonicManiaHandler),
  ('/uncharted', UnchartedHandler),
  ('/madden-nfl-18', MaddenHandler),
  ('/absolver', AbsolverHandler),
  ('/warriors-all-stars', WarriorsHandler),
  ('/everybodys-golf', GolfHandler),
  ('/mario-rabids', MarioRabidsHandler),
  ('/yakuza-kiwami', YakuzaKiwamiHandler),
  ('/life-is-strange', LifeIsStrangeHandler),

], debug=True)
