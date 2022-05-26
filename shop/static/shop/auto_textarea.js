function on_input() {
  this.style.height = "auto";
  this.style.height = this.scrollHeight + "px";
}

textarea = document.querySelector("form textarea");
textarea.style.overflowY = "hidden";
textarea.addEventListener("input", on_input);
