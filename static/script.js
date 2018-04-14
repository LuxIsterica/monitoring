var newShell = null;
$(document).ready(function () {
	$('#sidebarCollapse').on('click', function () {
		$('#sidebar').toggleClass('active');
	});

	function removeAll(){
		document.getElementById("pathFileFound").innerHTML = "";
	}
});