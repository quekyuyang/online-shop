function update_stars() {
  let stars = document.querySelectorAll('div.rating-select input[name="rating"]');
  for (let star of stars) {
    star.previousElementSibling.innerHTML = "&#9733;";
  }
  let stars_after_selected = document.querySelectorAll(
    'div.rating-select input[name="rating"]:checked ~ input'
  );
  for (let star of stars_after_selected) {
    star.previousElementSibling.innerHTML = "&#9734;";
  }
}

document.addEventListener("DOMContentLoaded", function(event) {
  document.querySelector("div.rating-select").addEventListener("click", update_stars);
})
