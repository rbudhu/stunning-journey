$(document).ready(function() {
    $("#tenso-share-button").click(function() {
	    var pk = $(this).data('pk');
	    $.post(urls.share_tenso(), {
		'pk': pk
	    }, function() {
	    }).done(function() {
		location.reload();
	    }).error(function() {
		$('#tenso-share-alert').removeClass('hidden');
	    });
    });
});
