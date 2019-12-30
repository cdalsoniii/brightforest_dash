//alert('If you see this alert, then your custom JavaScript script has run!')

alert(event.data);

window.addEventListener('message', function(event) {
  alert("Here I am");
  alert(event.data);
});
