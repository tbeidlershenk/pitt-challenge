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

