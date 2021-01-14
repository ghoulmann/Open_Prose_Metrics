// x = document.getElementsByTagName("P");
// for (i = 0; i < x.length; i++){
//     console.log(x[i].innerText);
// }
class WritingSample {
    constructor(text, person) {
        this.plaintext = text;
        this.author = person;
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

function paragraphText() {
    var plaintext = "";
    x = document.getElementsByTagName("P");
    for (i = 0; i <= x.length - 1; i++) {
        plaintext += x[i].innerText;
        plaintext += "\n\n";

    }
    plainttext = plaintext.replace("undefined", "");
    console.log(plaintext);
    return plaintext;
}

// function extraeyes(payload) {
//     const Url='http://localhost:5000/docs_api';
//     const Data=payload;
//     const otherParams={
//         body:Data,
//         method:"POST",
//         mode:"no-cors"
//     };
//     fetch(Url, otherParams)
//     .then(data=>{return data.json()})
//     .then(res=>{console.log(res)})
//     .catch(error=console.log(error));
// }

var allText = paragraphText();
thisPage = new WritingSample(allText, "anonymous");
console.log(thisPage.toJson());
//extraeyes(thisPage.toJson());

// function extraeyes(load) {
//
// }
// fetch('http://localhost:5000', {
//   method: 'POST',
//   headers: {
//     'Accept': 'application/json, text/plain, */*',
//     'Content-Type': 'application/json',
//     'Mode': 'no-cors',
//     'body': payload.toJson()}
//     .then(res=>res.json())
//     .then(res => console.log(res))
// })
