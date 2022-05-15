let slide_n = 0;
let images = document.querySelectorAll(".image img");

function previous_slide(){
  images[slide_n].style.display = "none";
  slide_n = ((slide_n - 1) % images.length + images.length) % images.length;
  images[slide_n].style.display = "block";
}

function next_slide() {
  images[slide_n].style.display = "none";
  slide_n = ((slide_n + 1) % images.length + images.length) % images.length;
  images[slide_n].style.display = "block";
}


document.addEventListener("DOMContentLoaded", function(event) {
  images[slide_n].style.display = "block";
  document.querySelector(".previous").addEventListener("click", previous_slide);
  document.querySelector(".next").addEventListener("click", next_slide);
})
