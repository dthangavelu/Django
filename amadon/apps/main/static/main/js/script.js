
$(document).ready(function(){
	$(function(){
		var select = '';
		for (var i=1;i<=100;i++){
			select += '<option val=' + i + '>' + i + '</option>';
		}
		$('#select_qty').html(select);
		}
	});​
});

