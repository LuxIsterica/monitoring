
$(document).ready(function () {
	$('#sidebarCollapse').on('click', function () {
		$('#sidebar').toggleClass('active');
		$('#content').toggleClass('opacity-content');
	});
 
 	if(document.getElementById('buttonSClickDeactiv') != null){
		document.getElementById("buttonSClickDeactiv").addEventListener("click", manage, false);
 	}
 	if(document.getElementById('buttonSClickActiv') != null){
 		document.getElementById('buttonSClickActiv').addEventListener("click", manage, false);
 	}
 	if(document.getElementById('buttonMClickDeactiv') != null){
		document.getElementById("buttonMClickDeactiv").addEventListener("click", manage, false);
 	}
 	if(document.getElementById('buttonMClickActiv') != null){
 		document.getElementById('buttonMClickActiv').addEventListener("click", manage, false);
 	}
 	if(document.getElementById('buttonCClickDeactiv') != null){
		document.getElementById("buttonCClickDeactiv").addEventListener("click", manage, false);
 	}
 	if(document.getElementById('buttonCClickActiv') != null){
 		document.getElementById('buttonCClickActiv').addEventListener("click", manage, false);
 	}

	function manage(){
			$('#startButton').css('opacity', '0.5');
			$('#startButton').addClass('disabled');
			$('#stopButton').css('opacity', '0.5');
			$('#stopButton').addClass('disabled');
			$('#statusButton').css('opacity', '0.5');
			$('#statusButton').addClass('disabled');
			$("#pText").show();
	};

	$('#contentTextarea').change(function(){
		$('#contentTextarea').css("border-color","red");
		$('#modificaTextarea').prop('disabled',false);
	});

});