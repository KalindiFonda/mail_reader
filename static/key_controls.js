document.addEventListener('keydown', function(event) {
	console.log(event.code)
  if (event.code == 'Digit1') {
     document.getElementById("option1").click();
  } else if (event.code == 'Digit2') {
     document.getElementById("option2").click();
  } else if (event.code == 'Digit3') {
     document.getElementById("option3").click();
   }  else if (event.code == 'ShiftLeft' || event.code == 'Digit4' ){
     document.getElementById("take-pic").click();
   } else if (event.code == 'ShiftRight') {
     document.getElementById("last").click();
    }
});