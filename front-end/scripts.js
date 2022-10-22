document.getElementById('image').addEventListener('click', openDialog);

function openDialog() {
  document.getElementById('fileid').click();
}

const image_input = document.querySelector("#fileid");

image_input.addEventListener("change", function() {
        const reader = new FileReader();
        reader.addEventListener("load", () => {
        const uploaded_image = reader.result;
        document.querySelector("#picture").style.backgroundImage = `url(${uploaded_image})`;
        image.src = readerEvent.target.result;
    });
    reader.readAsDataURL(this.files[0]);
  });


let request = new XMLHttpRequest()
request.open('GET', "https://jsonplaceholder.typicode.com/users", true)
request.onload = () => {
    let result = JSON.parse(request.responseText)
    let pill1 = result[0]
    /*document.getElementById("pill1").textContent = pill1.name + "    " + pill1.username;*/
    console.log(result[0]);
}
request.send()

