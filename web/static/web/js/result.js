$(document).ready(function() {
    $("#tenso-share-checkbox").change(function() {
	if (this.checked) {
	    var pk = $(this).data('pk');
	    $.post(urls.share_tenso(), {
		'pk': pk
	    }, function() {
		
	    }).done(function() {
		$('.tenso-share-checkbox').addClass('hidden');
	    }).error(function() {
		$('#tenso-share-alert').removeClass('hidden');
	    });
	}
    });
});
