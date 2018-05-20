var newShell = null;
$(document).ready(function () {
	$('#sidebarCollapse').on('click', function () {
		$('#sidebar').toggleClass('active');
	});

	$('#buttonClick').on('click',function(){
		$('#startButton').css('opacity', '0.5');
		$('#startButton').addClass('disabled');
		$('#stopButton').css('opacity', '0.5');
		$('#stopButton').addClass('disabled');
		$('#statusButton').css('opacity', '0.5');
		$('#statusButton').addClass('disabled');
		$("#pText").show();
	});

});