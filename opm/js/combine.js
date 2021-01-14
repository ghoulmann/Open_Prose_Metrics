(function () {
    class WritingSample {
        constructor(text) {
            this.plaintext = text;
            this.author = "anonymous";
            this.apis = "no";
        }
        toConsole() {
            console.log(this.text);
        }
        toAlert() {
            alert(this.text);
        }
        toJson() {
            return JSON.stringify(this);
        }
    }


    var plaintext = "";
    x = document.getElementsByTagName("P");
    for (i = 0; i <= x.length - 1; i++) {
        plaintext += x[i].innerText;
        plaintext += "\n\n";

    }
    //plainttext = plaintext.replace("undefined", "");
    console.log(plaintext);
    data = new WritingSample(plaintext)

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


})();
