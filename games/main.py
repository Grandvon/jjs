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
    review = ndb.StringProperty()



class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())
        email_address = user.nickname()
        var_user = {"first_name" : cssi_user.first_name,
        "last_name": cssi_user.last_name, "email_address" : email_address}

        main_template = env.get_template('profile.html')
        self.response.out.write(main_template.render(var_user))





#The following handlers each follow the template for the gaming review page.
class Tekken7Handler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '4.75')
        key = game.put()


        one = GameData(review=self.request.get('review'))
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()


        query = GameData.query()
        query = query.order(GameData.review)
        results = query.fetch()

        user = users.get_current_user()
        cssi_user = CssiUser.get_by_id(user.user_id())

        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Tekken 7',
                                        'pic' : 'https://i.ytimg.com/vi/7NyPT_o5aOs/maxresdefault.jpg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'user' : cssi_user.first_name + " " + cssi_user.last_name }))



class DriftingHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '3')
        key = game.put()

        one = GameData(review=self.request.get('review'))
        if not one:
            x=0
        else:
            if len(str(one.review)) > 0:
                one.put()


        query = GameData.query()
        query = query.order(GameData.review)
        results = query.fetch()

        user = users.get_current_user()

        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Drifting Lands',
                                        'pic' : 'https://steamdb.info/static/camo/apps/327240/header.jpg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum...",
                                        'review': results,
                                        'user' : first_name}))

class Dirt4Handler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Dirt 4',
                                        'pic' : 'http://blogcdn.codemasters.com/wp-content/uploads/2017/01/Fiesta_Aus_3.jpg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class ESHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'ESO: Morrowwind',
                                        'pic' : 'http://assets1.ignimgs.com/2017/01/31/esomorrowind-stills-naryu-1485890491125_1280w.jpg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class UnderPressureHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'GOTG Eps 2:Under Pressure',
                                        'pic' : "https://dontfeedthegamers.com/wp-content/uploads/2017/05/telltale-guardians-episode-2.jpg",
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class TownOfLightHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'The Town of Light',
                                        'pic' : 'https://i.ytimg.com/vi/RAI3B0K9HiU/maxresdefault.jpg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class WipeoutHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Wipeout Omega Collection',
                                        'pic' : 'https://media.playstation.com/is/image/SCEA/wipeout-omega-collection-screen-08-us-03dec16?$MediaCarousel_Original$',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class WonderBoyHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Wonder Boy',
                                        'pic' : 'https://i.ytimg.com/vi/ibKf66tVoFw/maxresdefault.jpg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class ArmsHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Arms',
                                        'pic' : 'http://content.newsinc.com/jpg/838/32428466/56430218.jpg?t=1495116180',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))


class DeadByDayLightHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Dead by Daylight',
                                        'pic' : 'https://images4.alphacoders.com/721/721397.jpg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class StormbloodHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Stormblood',
                                        'pic' : 'http://cdn.mos.cms.futurecdn.net/F8MCdkAPcjJSSyoTPnGoV.jpg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class NexMachinaHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Nex Machina',
                                        'pic' : 'https://media.playstation.com/is/image/SCEA/nex-machina-screen-03-ps4-us-03dec16?$MediaCarousel_Original$',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class GetEvenHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Get Even',
                                        'pic' : 'http://cdn.mos.cms.futurecdn.net/JZsnFaFsJjFDBhQa9MbuDc.jpg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class DanganronpaHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Danganronpa: Ultra Despair Girls',
                                        'pic' : 'https://cdn.destructoid.com//ul/307925-2811075-trailer_danganronpaultra_despairgirls_20150220.jpg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class EliteHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Elite: Dangerous',
                                        'pic' : 'https://static.gamespot.com/uploads/original/1197/11970954/2823045-starport_anaconda.jpg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class GolfClub2Handler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'The Golf Club 2',
                                        'pic' : 'https://i.ytimg.com/vi/GpyT0XC4bv0/maxresdefault.jpg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class ValkyriaHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Valkyria Revolution',
                                        'pic' : 'https://cdn.vox-cdn.com/thumbor/yuU5RA7yAATMWZ2vd8h8jU6m6Eo=/0x0:1600x900/1200x800/filters:focal(672x322:928x578)/cdn.vox-cdn.com/uploads/chorus_image/image/50889561/valkyria_azure_revolution.0.jpg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class CBNSHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': 'Crash Bandicoot N. Sane Trilogy',
                                        'pic' : 'https://media.playstation.com/is/image/SCEA/crash-bandicoot-n-sane-trilogy-screen-04-us-03dec16?$MediaCarousel_Original$',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class ThatsYouHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "That's You!",
                                        'pic' : 'https://static.gamespot.com/uploads/screen_kubrick/1570/15709614/3256358-site_gameplay_thatsyou_20170703.jpg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class MetalSlugHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Metal Slug 2 (re-release)",
                                        'pic' : 'http://cdn-static.denofgeek.com/sites/denofgeek/files/styles/article_width/public/2017/03/metal-slug-3.jpg?itok=TEoyTJ2s',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class WorldvsSwordHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Accel World VS. Sword Art Online",
                                        'pic' : 'http://www.psu.com/media/articles/image/accelworld1.jpg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class FableFortuneHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Fable Fortune",
                                        'pic' : 'https://i.ytimg.com/vi/Lnw499IdZQM/maxresdefault.jpg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class ZodiacHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "FF XII: The Zodiac Age",
                                        'pic' : 'http://www.finalfantasyxii.com/img/home/final-fantasy-xii-character-group-shot.jpg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class MinecraftHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Minecraft: Story Mode Season 2",
                                        'pic' : 'https://cdn2.vox-cdn.com/uploads/chorus_asset/file/8645163/MC201_SeaTempleExterior_1920x1080.jpg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class YonderHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Yonder: The Cloud Catcher Chronicles",
                                        'pic' : 'https://static1.squarespace.com/static/581d5d8220099e9ace514235/590dac0ecd0f684a2947bda3/590dac162e69cf3d4b372644/1494738229692/Bambex.jpg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class MoonHuntersHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = 'https://cdn.cultofmac.com/wp-content/uploads/2014/09/Moon-Hunters.jpg')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Moon Hunters",
                                        'pic' : '',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class CODHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "COD: Mondern Warfare Remastered",
                                        'pic' : 'https://charlieintel.com/wp-content/uploads/2017/06/mwrimage.jpeg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class Splatton2Handler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Splatton 2",
                                        'pic' : 'http://ll-c.ooyala.com/e1/trdG92YjE6CHZOtl9h_Y5M-87LyNMK46/promo324080340',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class AvenColonyHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Aven Colony",
                                        'pic' : 'http://avencolony.com/wp-content/uploads/2016/08/promo1600x900.png?x16986',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class FateExtellaHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Fate/Extella:The Umbral Star",
                                        'pic' : 'https://www.gamecrate.com/sites/default/files/Fate%20Extella%20The%20Umbral%20Star%20-%201.jpg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class FortniteHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Fortnite",
                                        'pic' : 'https://static1.gamespot.com/uploads/original/1406/14063904/2880204-laststand_final_1080p+copy.png',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class PyreHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Pyre",
                                        'pic' : 'https://cdn.vox-cdn.com/uploads/chorus_asset/file/8903015/Pyre_May_2017_01.jpg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class DanganronpaPCHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Danganronpa: Ultra Despair Girls (PC)",
                                        'pic' : 'https://cdn.destructoid.com//ul/307925-2811075-trailer_danganronpaultra_despairgirls_20150220.jpg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class TacomaHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Tacoma",
                                        'pic' : 'http://gameranx.com/wp-content/uploads/2016/03/tacoma-1.jpg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class HellbladeHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Hellblade:Senua's Sacrifice",
                                        'pic' : 'https://i.ytimg.com/vi/WOSDW_wxH3Y/maxresdefault.jpg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class LawbreakersHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Lawbreakers",
                                        'pic' : 'https://static.gamespot.com/uploads/original/536/5360430/3106269-lawbreakers_vangaurd_vs_titan.jpg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class MegaManHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Mega Man Legacy Collection 2",
                                        'pic' : 'https://c.slashgear.com/wp-content/uploads/2017/04/mega-man-legacy-collection-980x420.png',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class SonicManiaHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Sonic Mania",
                                        'pic' : 'https://i.ytimg.com/vi/OiL3fqk5yRo/maxresdefault.jpg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class UnchartedHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Uncharted: The Lost Legacy",
                                        'pic' : 'https://apollo2.dl.playstation.net/cdn/UP9000/CUSA07737_00/FREE_CONTENT0SZAeSQd9jFnHHvJmvDm/PREVIEW_SCREENSHOT2_146393.jpg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class MaddenHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Madden NFL 18",
                                        'pic' : 'http://www.sportsgamersonline.com/wp-content/uploads/2017/02/tom-brady-madden-25-13-1200x630-c.jpg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class AbsolverHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Absolver",
                                        'pic' : 'https://static.gamespot.com/uploads/original/536/5360430/3068853-absolver+-+screen+4.png',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class WarriorsHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Warriors All-Stars",
                                        'pic' : 'https://cdn1.vox-cdn.com/uploads/chorus_asset/file/8323817/WarriorsAllStars_Screenshot06.jpg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class GolfHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Everybody's Golf",
                                        'pic' : 'https://c1.staticflickr.com/3/2845/33305050694_de7e749473_b.jpg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class MarioRabidsHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Mario + Rabbids: Kingdom Battle",
                                        'pic' : 'http://gematsu.com/wp-content/uploads/2017/06/Mario-Rabbids-Kingdom-Battle-Announced-Init.jpg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class YakuzaKiwamiHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Yakuza Kiwami",
                                        'pic' : 'https://www.bleedingcool.com/wp-content/uploads/2017/04/Yakuza-Kiwami.png',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))

class LifeIsStrangeHandler(webapp2.RequestHandler):
    def get(self):
        game = GameData(stars = '')
        key = game.put()
        main_template = env.get_template('reviewtemplate.html')
        self.response.out.write(main_template.render({'name': "Life is Strange: Before the Storm",
                                        'pic' : 'https://cdn.vox-cdn.com/uploads/chorus_asset/file/8696367/e327ba76bf878c05dd80de3ff0361f35_1920_KR.jpg',
                                        'stars': key.get().stars,
                                        'synopsis': "lorem ipsum..."}))










app = webapp2.WSGIApplication([
  ('/', MainHandler),
  ('/homepage', GameHandler),
  ('/gaming-reviews', ReviewHandler),
  ('/history-of-gaming', HistoryHandler),
  ('/console-battle-arena', BattleHandler),
  ('/profile', ProfileHandler),
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
