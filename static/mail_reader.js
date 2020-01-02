
let v = document.getElementById("myVideo");
//create a canvas to grab an image for upload
let imageCanvas = document.createElement('canvas');
let imageCtx = imageCanvas.getContext("2d");
firstClick = false
//Add file blob to a form and post
function postFile(file) {
	let formdata = new FormData();
	formdata.append("image", file);
	let xhr = new XMLHttpRequest();
	xhr.open('POST', './', true);
	xhr.send(formdata);
	xhr.onload = function () {
	if (this.status === 200){
		options = this.response;
		if (options == "no_text")
			return sendImagefromCanvas();
		location.href = options;
		firstClick = false;
	}
	else
		console.error(xhr);
	};
}

//Get the image from the canvas
function sendImagefromCanvas() {
	//Make sure the canvas is set to the current video size
	imageCanvas.width = v.videoWidth;
	imageCanvas.height = v.videoHeight;
	imageCtx.drawImage(v, 0, 0, v.videoWidth, v.videoHeight);
	//Convert the canvas to blob and post the file
	imageCanvas.toBlob(postFile, 'image/jpeg');
}

//Take a picture on click
function getImagefromCanvas() {
	if (firstClick === true)
		return;
	firstClick = true ;
	document.getElementById("loader").style.display="block";
	document.getElementById("take-pic").style.display="none";
	sendImagefromCanvas();
};

window.onload = function () {
	//Get camera video
	navigator.mediaDevices.getUserMedia(

		{video: {width: 800, height: 400}, audio: false}
		)
	.then(stream => {
		v.srcObject = stream;
	})
	.catch(err => {
		console.log('navigator.getUserMedia error: ', err)
	});
};
