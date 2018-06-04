var newShell = null;
$(document).ready(function () {
	$('#sidebarCollapse').on('click', function () {
		$('#sidebar').toggleClass('active');
	});
 
	$('#buttonClickActiv').on('click',function(){
		$('#startButton').css('opacity', '0.5');
		$('#startButton').addClass('disabled');
		$('#stopButton').css('opacity', '0.5');
		$('#stopButton').addClass('disabled');
		$('#statusButton').css('opacity', '0.5');
		$('#statusButton').addClass('disabled');
		$("#pText").show();
	});

	$('#buttonClickDeactiv').on('click',function(){
		$('#startButton').css('opacity', '0.5');
		$('#startButton').addClass('disabled');
		$('#stopButton').css('opacity', '0.5');
		$('#stopButton').addClass('disabled');
		$('#statusButton').css('opacity', '0.5');
		$('#statusButton').addClass('disabled');
		$("#pText").show();
	});

	$('#content-textarea').focusout(function(){
		$('#content-textarea').css("border-color","red");
	});

	


});