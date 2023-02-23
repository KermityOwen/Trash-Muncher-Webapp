function sendLocation() {
  var name = document.getElementById("location_name");
  var radio = document.querySelector('input[name="location_size"]:checked').value;

  alert(name.value);
  alert(radio);

  return false;
}
