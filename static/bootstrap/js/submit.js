function submitSugg() {
  var suggestion = document.getElementById("suggestion").value;
  window.location.replace("submit.html?suggestion=" + suggestion);
}
