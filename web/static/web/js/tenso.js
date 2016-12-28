$("#id_image").change(function(event) {      
	var reader = new FileReader();
	reader.onload = function(){
	    var output = document.getElementById('img-preview');
	    output.src = reader.result;
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
	};
	reader.readAsDataURL(event.target.files[0]);	     
    });
