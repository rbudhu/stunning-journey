$("#id_image").change(function(event) {
    var fileTypes = ['jpg', 'jpeg', 'png', 'gif'];  //acceptable file types
    
    if (event.target.files && event.target.files[0]) {
        var extension = event.target.files[0].name.split('.').pop().toLowerCase(),  
	    isSuccess = fileTypes.indexOf(extension) > -1;  //is extension in acceptable types

        if (isSuccess) {
	    if ($( '#img-preview-div' ).hasClass('hidden')) {
		$( '#img-preview-div' ).removeClass('hidden');
	    }
	    if (!$( '#img-upload-warning' ).hasClass('hidden')) {
		$( '#img-upload-warning' ).addClass('hidden');
	    }

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
	}
	else {
	    if ($( '#img-upload-warning' ).hasClass('hidden')) {
		$( '#img-upload-warning' ).removeClass('hidden');
	    }
	}
    }
});
