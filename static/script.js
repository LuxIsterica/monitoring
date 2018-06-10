var newShell = null;
$(document).ready(function () {
	$('#sidebarCollapse').on('click', function () {
		$('#sidebar').toggleClass('active');
	});
 
	$('#buttonSitesClickActiv').on('click',function(){
		$('#startButton').css('opacity', '0.5');
		$('#startButton').addClass('disabled');
		$('#stopButton').css('opacity', '0.5');
		$('#stopButton').addClass('disabled');
		$('#statusButton').css('opacity', '0.5');
		$('#statusButton').addClass('disabled');
		$("#pText").show();
	});

	$('#buttonSitesClickDeactiv').on('click',function(){
		$('#startButton').css('opacity', '0.5');
		$('#startButton').addClass('disabled');
		$('#stopButton').css('opacity', '0.5');
		$('#stopButton').addClass('disabled');
		$('#statusButton').css('opacity', '0.5');
		$('#statusButton').addClass('disabled');
		$("#pText").show();
	});

	$('#buttonModsClickActiv').on('click',function(){
		$('#startButton').css('opacity', '0.5');
		$('#startButton').addClass('disabled');
		$('#stopButton').css('opacity', '0.5');
		$('#stopButton').addClass('disabled');
		$('#statusButton').css('opacity', '0.5');
		$('#statusButton').addClass('disabled');
		$("#pText").show();
	});

	$('#buttonModsClickDeactiv').on('click',function(){
		$('#startButton').css('opacity', '0.5');
		$('#startButton').addClass('disabled');
		$('#stopButton').css('opacity', '0.5');
		$('#stopButton').addClass('disabled');
		$('#statusButton').css('opacity', '0.5');
		$('#statusButton').addClass('disabled');
		$("#pText").show();
	});

	$('#buttonConfClickActiv').on('click',function(){
		$('#startButton').css('opacity', '0.5');
		$('#startButton').addClass('disabled');
		$('#stopButton').css('opacity', '0.5');
		$('#stopButton').addClass('disabled');
		$('#statusButton').css('opacity', '0.5');
		$('#statusButton').addClass('disabled');
		$("#pText").show();
	});

	$('#buttonConfClickDeactiv').on('click',function(){
		$('#startButton').css('opacity', '0.5');
		$('#startButton').addClass('disabled');
		$('#stopButton').css('opacity', '0.5');
		$('#stopButton').addClass('disabled');
		$('#statusButton').css('opacity', '0.5');
		$('#statusButton').addClass('disabled');
		$("#pText").show();
	});

	$('#contentTextarea').mouseleave(function(){
		$('#contentTextarea').css("border-color","red");
		$('#modificaCrontab').prop('disabled',false);
	});

});