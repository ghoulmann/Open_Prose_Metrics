// postRequest('http://localhost:5000/docs_api', thisPage.toJson())
//   .then(data => console.log(data)) // Result from the `response.json()` call
//   .catch(error => console.error(error))
//
// function postRequest(url, data) {
//   return fetch(url, {
//     //credentials: 'same-origin', // 'include', default: 'omit'
//     method: 'POST', // 'GET', 'PUT', 'DELETE', etc.
//     //body: JSON.stringify(data), // Coordinate the body type with 'Content-Type'
//     body: JSON.stringify(data),
//     headers: new Headers({
//       'Content-Type': 'application/json'
//     }),
//     mode: 'no-cors'
//   })
//   .then(response => response.json())
// }


fetch('http://localhost:5000/docs_api', {
    //credentials: 'same-origin', // 'include', default: 'omit'
    method: 'post', // 'GET', 'PUT', 'DELETE', etc.
    //body: JSON.stringify(data), // Coordinate the body type with 'Content-Type'
    body: JSON.stringify(data),
    headers: new Headers({
      'Content-Type': 'application/json'
  })//,
    //mode: 'no-cors'
  })
  .then(function(response) {
  response.status     //=> number 100–599
  response.statusText //=> String
  response.headers    //=> Headers
  response.url        //=> String

  return response.text().then(function(text) {console.log(text)})
  }, function(error) {
    error.message //=> String
})

//function version
function extraeyes(data) {
    return fetch('http://localhost:5000/docs_api', {
        //credentials: 'same-origin', // 'include', default: 'omit'
        method: 'post', // 'GET', 'PUT', 'DELETE', etc.
        //body: JSON.stringify(data), // Coordinate the body type with 'Content-Type'
        body: JSON.stringify(data),
        headers: new Headers({
          'Content-Type': 'application/json'
      })//,
        //mode: 'no-cors'
      })
      .then(function(response) {
      response.status     //=> number 100–599
      response.statusText //=> String
      response.headers    //=> Headers
      response.url        //=> String

      return response.text().then(function(text) {console.log(text)})
      }, function(error) {
        error.message //=> String
    })
}
