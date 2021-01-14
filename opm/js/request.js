function extraeyes(payload) {
  const URL = 'http://localhost:5000/docs_api';
  const MSG = payload;
  const OTHERPARAMS = {
    body: MSG,
    method: 'POST',
    Mode: 'no-cors',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'Body': MSG
    }
  }
  fetch(URL, OTHERPARAMS)
  .then(function(response) {
    console.log(response.type);
    console.log(response.url);
    console.log(response.useFinalURL);
    console.log(response.status);
    console.log(response.ok);
    console.log(response.statusText);
    console.log(response.headers);
    return response.blob();
  })
}


function postData(url = `http://localhost:5000/docs_api`, data) {
  // Default options are marked with *
    return fetch(url, {
        method: "POST", // *GET, POST, PUT, DELETE, etc.
        mode: "no-cors", // no-cors, cors, *same-origin
        cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
        credentials: "same-origin", // include, *same-origin, omit
        headers: {
            "Content-Type": "application/json; charset=utf-8",
            // "Content-Type": "application/x-www-form-urlencoded",
        },
        redirect: "follow", // manual, *follow, error
        referrer: "no-referrer", // no-referrer, *client
        //body: JSON.stringify(data) // body data type must match "Content-Type" header
        body: data
    })
    .then(res => res.json())
    .then(response => console.log('Success:', JSON.stringify(response)))
    .catch(error => console.error('Error:', error));
}


//--------------------------
function reqListener() {
  var data = JSON.parse(this.responseText);
  console.log(data);
}

function reqError(err) {
  console.log('Fetch Error :-S', err);
}
function reqListener() {
  var data = JSON.parse(this.responseText);
  console.log(data);
}
function reqError(err) {
  console.log('Fetch Error :-S', err);
}

var request = new Request('http://localhost:5000/docs_api', {
      method: 'POST',
      mode: 'no-cors',
      redirect: 'follow',
      headers: {
        'Content-Type': 'text/json'
      }
    });
fetch(request)
  .then(function (data) {
    console.log('Request succeeded with JSON response', data);
  })
  .catch(function (error) {
    console.log('Request failed', error);
  });
//-------------------------

$.ajax({
    url: serviceUrl,
    type: "POST",
    dataType: "json",
    data: jsonData,
    contentType: "application/json"
});

// see https://www.airpair.com/js/jquery-ajax-post-tutorial
