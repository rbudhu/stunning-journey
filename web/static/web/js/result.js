$(document).ready(function() {
    $("#tenso-share-button").click(function() {
	    var pk = $(this).data('pk');
	    $.post(urls.share_tenso(), {
		'pk': pk
	    }, function() {
	    }).done(function() {
		$('#tenso-share-button').addClass('hidden');
		$('#tenso-shared-button').removeClass('hidden');
	    }).error(function() {
		$('#tenso-share-alert').removeClass('hidden');
	    });
    });
});
