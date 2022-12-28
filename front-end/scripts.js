document.getElementById('image').addEventListener('click', openDialog);

function openDialog() {
  document.getElementById('fileid').click();
}

const image_input = document.querySelector("#fileid");

image_input.addEventListener("change", function () {
  const reader = new FileReader();
  reader.addEventListener("load", () => {
    const uploaded_image = reader.result;
    document.querySelector("#picture").style.backgroundImage = `url(${uploaded_image})`;
    document.querySelector("#picture").src = reader.result;
    console.log('RESULT: ', reader.result)

    fetch("https://pill-identifier.herokuapp.com/predict", {
      method: "POST",
      headers: { 'Content-Type': 'application/json', 
                  "Access-Control-Allow-Origin": "*", 
                  "Access-Control-Allow-Credentials": "true", 
                  "Access-Control-Allow-Methods": "GET,HEAD,OPTIONS,POST,PUT", 
                  'Access-Control-Allow-Headers': "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers" 
                },
  
      body: JSON.stringify(reader.result)
    })
      .then(res => res.json())
      .then(data => {
        console.log(data)
      })
  });

  reader.readAsDataURL(this.files[0]);
  //console.log('JSON String: ', JSON.stringify(reader.result))

  
})





/*let request = new XMLHttpRequest()
request.open('GET', "https://jsonplaceholder.typicode.com/users", true)
request.onload = () => {
    let result = JSON.parse(request.responseText)
    let pill1 = result[0]
    /*document.getElementById("pill1").textContent = pill1.name + "    " + pill1.username;
    console.log(result[0]);
}
request.send()*/

