let form = document.querySelector("form");
let input_img = document.querySelector("input#id_images");
input_img.addEventListener("change", OnChange);

function OnChange() {
  // Remove div if already exists (to replace previous upload)
  let image_selection = document.querySelector("div.image_selection");
  if (image_selection) {
    image_selection.remove();
  }

  // Insert div for image selection
  const files = this.files;
  image_selection = document.createElement("div");
  image_selection.className = "image_selection";
  input_img.after(image_selection);

  // Insert images in image selection div
  if (files.length == 0) {
    image_selection.textContent = "No images selected";
  }
  else if (files.length <= 5) {
    for (const file of files){
      let img = document.createElement("img");
      img.src = URL.createObjectURL(file);
      image_selection.append(img);
    }
  }
  else {
    image_selection.textContent = "You can only upload a maximum of 5 images";
  }
}
