function update_stars() {
  let stars = document.querySelectorAll('div.rating-select input[name="rating"]');

  for (let star of stars) {
    star.previousElementSibling.innerHTML = "&#9734;";
  }

  let star_selected = document.querySelector('div.rating-select input[name="rating"]:checked');
  if (star_selected) {
    for (let star of stars) {
      star.previousElementSibling.innerHTML = "&#9733";
      if (star == star_selected) break;
    }
  }
}

document.addEventListener("DOMContentLoaded", function(event) {
  document.querySelector("div.rating-select").addEventListener("click", update_stars);
})
