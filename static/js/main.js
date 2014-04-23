$(document).ready(function(){
	events();
});

var data = [];

function events(){
	$('.emotion-button').click(function(){
		location.href = "../" + $(this)[0].innerText;
	});
	
	$('.docID-button').click(function(){
		location.href = $(this)[0].innerText;
	});

	$('.sent').hover(function(){
		$(this).siblings('.pat').toggleClass('hide');
	});	

	$('.pat').click(function(){
		var pattern = $(this).text();
		$('#chart-container').find('.pattern').text(pattern);


		$.getJSON('/api/pat/'+pattern.toLowerCase(), function(data){

			var number = 0;

			console.log(data.length);

			if(data.length == 0) {
				return false;
			}
			draw(data, data.length);
			$('#chart-container').toggleClass('hide');
			$('.mask').toggleClass('hide');
		});

		
	});
	$('.close').click(function(){
		$(this).parents('.container').toggleClass('hide');
		$('.mask').toggleClass('hide');
	});
	$('.mask').click(function(){
		$('.close').click();
	});
}

