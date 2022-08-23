#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
# Populating genres and Standout tasks

from distutils.log import error
from enum import unique
from errno import WSAEBADF
import json
import dateutil.parser
import babel
import datetime
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
# from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_migrate import Migrate
from flask_wtf import Form
from forms import *
from models import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app) # Instantiating SQLAlchemy from models.py
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# The Models can be found in the Models.py file


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #num_upcoming_shows should be aggregated based on number of upcoming shows per venue.

  data = []

  # Getting venues base on its city and state
  query = Venue.query.distinct(Venue.city, Venue.state).all()

  for da in query:
    obj = {}
    obj['city'] = da.city
    obj['state'] = da.state
    new_query = Venue.query.filter(Venue.city == da.city, Venue.state == da.state).all()
    venues = []
    for new in new_query:
      new_ven = {}
      new_ven['id'] = new.id
      new_ven['name'] = new.name

      # Getting the number of upcoming shows
      # Only the venue row which show's time is in the future will be returned in the filter method.
      new_ven["num_upcoming_shows"] = len(list(filter(lambda show: show.start_time > datetime.now(),new.shows)))

      venues.append(new_ven)
    obj['venues'] = venues
    data.append(obj)
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form['search_term']
  responses = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()
  count = len(responses)
  data = []
  for res in responses:
    obj = {}
    obj['id'] = res.id
    obj['name'] = res.name
    data.append(obj)

  response = {
    "count": count,
    "data": data
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # TODO: replace with real venue data from the venues table, using venue_id
 
  # shows the venue page with the given venue_id
  venue = Venue.query.filter_by(id=venue_id).first()

  # Getting past shows
  past_shows_query = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time<datetime.now()).all()   
  past_shows = []
  for show in past_shows_query:
    artistDetails = Artist.query.filter_by(id=show.artist_id).one()
    timeDate = show.start_time
    past_shows.append({
    'artist_id': show.artist_id,
    'artist_name': artistDetails.name,
    'artist_image_link': artistDetails.image_link,
    'start_time': timeDate.strftime("%m/%d/%Y %H:%M:%S"),
    })

  # GEtting upcoming post
  upcoming_shows_query = db.session.query(Show).join(Artist).filter(Show.venue_id==venue_id).filter(Show.start_time>datetime.now()).all()   
  upcoming_shows = [] 
  for show in upcoming_shows_query:
     obj = {}
     artistDetails = Artist.query.filter_by(id=show.artist_id).one()
     obj['artist_id'] = show.artist_id
     obj['artist_name'] = artistDetails.name
     obj['artist_image_link'] = artistDetails.image_link
     timeDate = show.start_time
     obj['start_time'] = timeDate.strftime("%m/%d/%Y %H:%M:%S")
     upcoming_shows.append(obj)

    
  data = {
    "id": venue.id,
    "name": venue.name,
    "genres": venue.genres.split(','),
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website_link,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  } 
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():  
  # # TODO: insert form data as a new Venue record in the db, instead
  # # TODO: modify data to be the data object returned from db insertion
  # # on successful db insert, flash success
  # flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # # TODO: on unsuccessful db insert, flash an error instead.
  # # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  # return render_template('pages/home.html')
  form = VenueForm(request.form)
  error=False
  try:
    name = form.name.data
    city = form.city.data
    state = form.state.data
    phone = form.phone.data
    address = form.address.data
    image_link = form.image_link.data
    genresList = form.genres.data # This returns a list of selected genres
    genres =  ",".join(genresList) # Converting genres list  to string
    facebook_link = form.facebook_link.data
    website_link = form.website_link.data
    seeking_description = form.seeking_description.data
    seeking_talent = form.seeking_talent.data # This returns True or False
    
    venue = Venue(name=name, city=city, address=address, phone=phone, state=state, image_link=image_link, facebook_link=facebook_link, website_link=website_link, seeking_talent=seeking_talent, seeking_description=seeking_description, genres=genres)
    db.session.add(venue)
    db.session.commit()
  except:
    error=True
    db.session.rollback()
  finally:
    db.session.close()
    if error:
      flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    else:
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error=False
  try:
    venue = Venue.query.filter_by(id=venue_id).first()
    db.session.delete(venue)
    db.session.commit()
  except:
    error=True
    db.session.rollback()
  finally:
    db.session.close()
  return render_template('pages/home.html')

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  datas = Artist.query.all()
  data = []
  for dat in datas:
    obj = {}
    obj['id'] = dat.id
    obj['name'] = dat.name
    data.append(obj)

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form['search_term']
  responses = Artist.query.filter(Artist.name.ilike(f'%{search_term}%')).all()
  count = len(responses)
  data = []
  for res in responses:
    obj = {}
    obj['id'] = res.id
    obj['name'] = res.name
    # Correction
    length = len(list(filter(lambda show: show.start_time > datetime.now(), res.shows)))
    obj['no_upcoming_posts'] = length
    data.append(obj)

  response = {
    "count": count,
    "data": data
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  artist = Artist.query.filter_by(id=artist_id).one()
  past_shows_query = db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time<datetime.now()).all()   
  past_shows = []
  for show in past_shows_query:
    venueDetails = Venue.query.filter_by(id=show.venue_id).one()
    timeDate = show.start_time
    past_shows.append({
    'venue_id': show.venue_id,
    'venue_name': venueDetails.name,
    'venue_image_link': venueDetails.image_link,
    'start_time': timeDate.strftime("%m/%d/%Y %H:%M:%S"),
    })


  upcoming_shows_query = db.session.query(Show).join(Venue).filter(Show.artist_id==artist_id).filter(Show.start_time>datetime.now()).all()   
  upcoming_shows = [] 
  for show in upcoming_shows_query:
     obj = {}
     venueDetails = Venue.query.filter_by(id=show.venue_id).one()
     obj['venue_id'] = show.venue_id
     obj['venue_name'] = venueDetails.name
     obj['venue_image_link'] = venueDetails.image_link
     timeDate = show.start_time
     obj['start_time'] = timeDate.strftime("%m/%d/%Y %H:%M:%S")
     upcoming_shows.append(obj)


  dataToBeSent = {
    "id": artist.id,
    "name": artist.name,
    "genres": artist.genres.split(','),
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website_link,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": past_shows,
    "upcoming_shows": upcoming_shows,
    "past_shows_count": len(past_shows),
    "upcoming_shows_count": len(upcoming_shows),
  }

  return render_template('pages/show_artist.html', artist=dataToBeSent)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm(request.form)

  # TODO: populate form with fields from artist with ID <artist_id>
  artistObject = Artist.query.filter_by(id=artist_id).first()

  # Populating the select fields
  form.state.data = artistObject.state
  form.genres.data =  artistObject.genres.split(',')

  #  Populating other fields
  artist = {
    "id": artistObject.id,
    "name": artistObject.name,
    "genres": artistObject.genres.split(','),
    "city": artistObject.city,
    "state": artistObject.state,
    "phone": artistObject.phone,
    "website": artistObject.website_link,
    "facebook_link": artistObject.facebook_link,
    "seeking_venue": artistObject.seeking_venue,
    "seeking_description":artistObject.seeking_description,
    "image_link": artistObject.image_link,
    "website_link": artistObject.website_link
  }
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm(request.form)
  # Getting the newly filled data
  error=False
  try:
    name = form.name.data
    city = form.city.data
    state = form.state.data
    phone = form.phone.data
    image_link = form.image_link.data

    genresList = form.genres.data # This returns a list of selected genres
    genres =  ",".join(genresList) # Converting genres list  to string
    facebook_link = form.facebook_link.data
    website_link = form.website_link.data
    seeking_description = form.seeking_description.data
    seeking_venue = form.seeking_venue.data # This returns True or False

    # Querying the database for the artist datas
    artistObject = Artist.query.filter_by(id=artist_id).one()

    # Updating the artist datas
    artistObject.name = name
    artistObject.city = city
    artistObject.state = state
    artistObject.phone = phone
    artistObject.image_link = image_link
    artistObject.genres = genres
    artistObject.facebook_link = facebook_link
    artistObject.website_link = website_link
    artistObject.website_link = website_link
    artistObject.seeking_description = seeking_description
    artistObject.seeking_description = seeking_description
    artistObject.seeking_venue = seeking_venue
    db.session.commit()
  except:
    error = True
    db.session.rollback()
  finally:
    db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm(request.form)
  # TODO: populate form with values from venue with ID <venue_id>
  venueObject = Venue.query.filter_by(id=venue_id).first()

  # Populating the select fields
  form.state.data = venueObject.state
  form.genres.data =  venueObject.genres.split(',')

  # Populating other fields
  venue = {
    "id": venueObject.id,
    "name": venueObject.name,
    # "genres": form.genres.data,
    "city": venueObject.city,
    "address": venueObject.address,
    # 'state': venueObject.state,
    "phone": venueObject.phone,
    "website": venueObject.website_link,
    "facebook_link": venueObject.facebook_link,
    "seeking_talent": venueObject.seeking_talent,
    "seeking_description":venueObject.seeking_description,
    "image_link": venueObject.image_link,
    "website_link": venueObject.website_link
  }
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  form = VenueForm(request.form)
  try:
    # Taking the Datas from the form
    name = form.name.data
    city = form.city.data
    state = form.state.data
    phone = form.phone.data
    address = form.address.data
    image_link = form.image_link.data
    genresList = form.genres.data # This returns a list of selected genres
    genres =  ",".join(genresList) # Converting genres list  to string
    facebook_link = form.facebook_link.data
    website_link = form.website_link.data
    seeking_description = form.seeking_description.data
    seeking_talent = form.seeking_talent.data 

    # Getting the venue row
    venueObject = Venue.query.filter_by(id=venue_id).first()

    # Updating the row
    venueObject.name = name
    venueObject.city = city
    venueObject.state = state
    venueObject.phone = phone
    venueObject.address = address
    venueObject.image_link = image_link
    venueObject.genres = genres
    venueObject.facebook_link = facebook_link
    venueObject.website_link = website_link
    venueObject.website_link = website_link
    venueObject.seeking_description = seeking_description
    venueObject.seeking_description = seeking_description
    venueObject.seeking_talent = seeking_talent
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
   # on successful db insert, flash success
  # flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # # TODO: on unsuccessful db insert, flash an error instead.
  # # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  # return render_template('pages/home.html')
  form = ArtistForm(request.form)
  error=False
  try:
    name = form.name.data
    city = form.city.data
    state = form.state.data
    phone = form.phone.data
    image_link = form.image_link.data
    genresList = form.genres.data # This returns a list
    genres =  ",".join(genresList) # Converting genres list  to string.
    facebook_link = form.facebook_link.data
    website_link = form.website_link.data
    seeking_description = form.seeking_description.data
    seeking_venue = form.seeking_venue.data
    artist = Artist(name=name, city=city, phone=phone, state=state, image_link=image_link, facebook_link=facebook_link, website_link=website_link, seeking_venue=seeking_venue, seeking_description=seeking_description, genres=genres)
    db.session.add(artist)
    db.session.commit()
  except:
    db.session.rollback()
    error=True
  finally:
    db.session.close()
    if error:
      flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    else:
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
    return render_template('pages/home.html')
  

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  datas = Show.query.all()
  dataToBeSent = []
  for show in datas:
    obj = {}
    obj['venue_id'] = show.venue_id
    obj['artist_id'] = show.artist_id
    obj['artist_name'] = Artist.query.filter_by(id=show.artist_id).one().name
    obj['venue_name'] = Venue.query.filter_by(id=show.venue_id).one().name
    obj['artist_image_link'] = Artist.query.filter_by(id=show.artist_id).one().image_link
    timeDate = show.start_time
    obj['start_time'] = timeDate.strftime("%m/%d/%Y %H:%M:%S")
    dataToBeSent.append(obj)
  return render_template('pages/shows.html', shows=dataToBeSent)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error=False
  try:
    form = ShowForm(request.form)
    artist_id = form.artist_id.data
    venue_id = form.venue_id.data
    start_time = form.start_time.data
    show = Show(artist_id=artist_id,venue_id=venue_id,start_time=start_time)
    db.session.add(show)
    db.session.commit()  
  except:
    error=True
    db.session.rollback()
  finally:
    db.session.close()
    if not error:
      flash('Show was successfully listed!')
    else:
      flash('An error occurred. Show could not be listed.')
    return render_template('pages/home.html')
  # on successful db insert, flash success
  # flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  #  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0')

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
