//alert('If you see this alert, then your custom JavaScript script has run!')


	TESTER = document.getElementById('tester');
	Plotly.plot( TESTER, [{
	x: [1, 2, 3, 4, 5],
	y: [1, 2, 4, 8, 16] }], {
	margin: { t: 0 } } );

alert(event.data);

window.addEventListener('message', function(event) {
  alert("Here I am");
  alert(event.data);
});
