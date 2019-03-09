import requests
import sys
from pprint import pprint

# reference your access token (developer token) here
ACCESS_TOKEN = ''

# dictionary to store the long poll url and stream position as they are
# captured.
SESSION_INFO = {}


def get_stream_position():
  """GET request to store next_stream_position"""

  global SESSION_INFO
  uri = 'https://api.box.com/2.0/events?stream_position=now'
  response = make_request(uri)
  SESSION_INFO['STREAM_POSITION'] = response['next_stream_position']
  # use the same long poll url if we already have one
  if 'LPURL' in SESSION_INFO:
    long_poll_call()
  else:
    options_call()


def options_call():
  """OPTIONS request to store the long poll url"""

  global SESSION_INFO
  uri = 'https://api.box.com/2.0/events'
  response = make_request(uri, 'OPTIONS')
  entries = response['entries'] or []
  if len(entries) > 0:
    SESSION_INFO['LPURL'] = entries[0]['url']
    pprint('realtime url: ' + SESSION_INFO['LPURL'])
    long_poll_call()


def long_poll_call():
  """GET request to listen for any incoming notications"""

  if 'LPURL' in SESSION_INFO and 'STREAM_POSITION' in SESSION_INFO:
    uri = SESSION_INFO['LPURL'] + '&stream_position=' + \
        str(SESSION_INFO['STREAM_POSITION'])
    pprint('long polling...')
    response = make_request(uri)
    pprint(response['message'])
    if response['message'] == 'new_change':
      # react to the new change notification and request the latest event
      # details
      get_new_change()
    else:
      # react to the reconnect notification and re open the long poll
      # connection
      pprint('realtime url: ' + SESSION_INFO['LPURL'])
      long_poll_call()


def get_new_change():
  """GET request to display the most recent event info"""

  if 'STREAM_POSITION' in SESSION_INFO:
    uri = 'https://api.box.com/2.0/events?stream_position=' + \
        str(SESSION_INFO['STREAM_POSITION'])
    pprint('fetching events')
    response = make_request(uri)
    entries = response['entries'] or []
    if len(entries) > 0:
      entry = entries[0]
      pprint(entry['event_id'] + ' | ' + entry['event_type'])
      get_stream_position()


def make_request(uri, method='GET'):
  """Makes an HTTP request with the provided uri and method

Args:
  uri (string): The enpoint uri.
  method (string): The method type (defaults to GET)

Returns:
          The json response

"""

  headers = {'Authorization': 'Bearer ' + ACCESS_TOKEN}
  try:
    if method == 'OPTIONS':
      response = requests.options(uri, headers=headers)
      response.raise_for_status()
      return response.json()
    else:
      response = requests.get(uri, headers=headers)
      response.raise_for_status()
      return response.json()
  except requests.exceptions.HTTPError as e:
    # any HTTP exceptions will cause the script to exit
    pprint(e)
    sys.exit(1)

# start the script
get_stream_position()
