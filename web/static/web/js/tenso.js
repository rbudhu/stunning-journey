$(document).ready(function() {
  $("#id_image").change(function(event) {
    var fileTypes = ['jpg', 'jpeg', 'png', 'gif'];  //acceptable file types
    
    if (event.target.files && event.target.files[0]) {
        var extension = event.target.files[0].name.split('.').pop();
	isSuccess = fileTypes.indexOf(extension.toLowerCase()) > -1;
	$( '#img-upload-warning' ).addClass('hidden');
        if (isSuccess) {
	    var reader = new FileReader();
	    reader.onload = function(){
		var output = document.getElementById('img-preview');
		output.src = reader.result;

		if (output.cropper) {
		    output.cropper.replace(output.src);
		}
		else {
		    var cropper = new Cropper(output, {
			background: false,
			zoomable: false,
			crop: function(e) {
			    var box = [e.detail.x, e.detail.y,
				       e.detail.x + e.detail.width,
				       e.detail.y + e.detail.height];
			    var box_json = JSON.stringify(box);
			    $("#id_box").val(box_json);
			}
		    });
		}
            };
	    reader.readAsDataURL(event.target.files[0]);
	    document.location.href = window.location.protocol +
		"//"  + 
		window.location.host +
		"/" +
		window.location.pathname.split("/")[1] +
		"#preview";
	}
	else {
	    $( '#img-upload-warning' ).removeClass('hidden');
	}
    }
  });
});
