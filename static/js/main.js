$(document).ready(function(){
	events();
});

var current = '';
var prev = '';
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
		// $('#chart-container').find('svg').html('');

		current = pattern.toLowerCase();
		if( current == prev ){
			$('#chart-container').removeClass('hide');
			$('.mask').removeClass('hide');
		}else{
			prev = current;

			// reset sort
			// truncate data
			// 
			$.getJSON('/api/pat/'+pattern.toLowerCase(), function(data){

				if(data.length == 0) { return false; }

		    	var checkbox_wrap = $('#chart-container').find('.checkbox-wrap');
		    	checkbox_wrap.removeClass('checked');

				draw(data);

				$('#chart-container').removeClass('hide');
				$('.mask').removeClass('hide');
			});

		}

	});
	$('.close').click(function(){
		$(this).parents('.container').addClass('hide');
		$('.mask').addClass('hide');

		// $('#chart-container').find('svg').html('');
	});
	$('.mask').click(function(){
		$('.close').click();
	});
    
}

