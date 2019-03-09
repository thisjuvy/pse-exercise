const rp = require('request-promise');

//reference your access token (developer token) here
const ACCESS_TOKEN = '';

//map to store the long poll url and stream position as they are captured.
let SESSION_INFO = {};

//GET request to store next_stream_position
getStreamPosition = () => {
  let uri = 'https://api.box.com/2.0/events?stream_position=now';
  makeRequest(uri).then(response => {
    SESSION_INFO.STREAM_POSITION = response.next_stream_position;
    //use the same long poll url if we already have one
    if (!SESSION_INFO.LPURL) {
      optionsCall();
    } else {
      longPollCall();
    }
  });
};

//OPTIONS request to store the long poll url
optionsCall = () => {
  let uri = 'https://api.box.com/2.0/events';
  makeRequest(uri, 'OPTIONS').then(response => {

    let entries = response.entries || [];

    if (entries.length > 0) {
      SESSION_INFO.LPURL = entries[0].url;
      console.log(`realtime url: ${SESSION_INFO.LPURL}`);
      longPollCall();
    }
  });
};

//GET request to listen for any incoming notications
longPollCall = () => {
  let uri = `${SESSION_INFO.LPURL}&stream_position=${SESSION_INFO.STREAM_POSITION}`;
  console.log('long polling...');
  makeRequest(uri).then(response => {
    console.log(`${response.message}`);
    if (response.message === 'new_change') {
      //react to the new change notification and request the latest event details
      getNewChange();
    } else {
      //react to the reconnect notification and re open the long poll connection
      console.log(`realtime url: ${SESSION_INFO.LPURL}`);
      longPollCall();
    }
  });
};

//GET request to display the most recent event info
getNewChange = () => {
  let uri = `https://api.box.com/2.0/events?stream_position=${SESSION_INFO.STREAM_POSITION}`;
  console.log('fetching events');
  makeRequest(uri).then(response => {
    let entries = response.entries || [];
    if (entries.length > 0) {
      let entry = entries[0];
      //#5
      console.log(`${entry.event_id} | ${entry.event_type}`);
      getStreamPosition();
    }
  });
};

/**
 * Makes an HTTP request with the provided uri and method.
 *
 * @param {number} uri The endpoint uri
 * @param {string} method The method type (defaults to GET)
 * @return The json response
 */
makeRequest = (uri, method = 'GET') => {
  return new Promise((resolve) => {
    let options = {
      uri,
      method,
      headers: {
        'Authorization': `Bearer ${ACCESS_TOKEN}`
      },
      json: true
    };

    rp(options).then(response => {
      resolve(response);
    }).catch(err => {
      //any HTTP exceptions will cause the script to exit
      console.log(`${err.message}`);
      process.exit()
    });
  });
};

//start the script
getStreamPosition();