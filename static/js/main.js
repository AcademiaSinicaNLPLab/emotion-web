$(document).ready(function(){
	events();
	autoStyling();
});

var current = '';
var prev = '';
var data = [];

var colors = ['#428bca', '#5cb85c', '#f0ad4e'];
var colorsDark = ['#3276b1', '#47a347', '#ed9c28'];

function autoStyling() {
	var len = $('.info-block').length;

	// max z-index

	$('.info-block').each(function(i, obj){

		var infotext = $(this).find('.info-text');
		var infotri = $(this).find('.info-tri');

		infotext.css('background', colors[i]);
		infotri.css('border-left-color', colors[i]);

		$(this).mouseenter(function(){
			infotext.css('background', colorsDark[i]);
			infotri.css('border-left-color', colorsDark[i]);
		}).mouseleave(function(){
			infotext.css('background', colors[i]);
			infotri.css('border-left-color', colors[i]);			
		});

		$(this).find('.info-element').css('z-index', len*2-i*2);
		$(this).find('.info-tri-shadow').css('z-index', len*2-i*2-1);
	});
}

function events(){

	/*
	$('.emotion-button').click(function(){
		location.href = "../" + $(this).text();
	});
	
	$('.docID-button').click(function(){
		location.href = $(this).text();
	});

	$('.sent').hover(function(){
		$(this).siblings('.pat').toggleClass('hide');
	});	
	*/
	var prev = '';
	var current = '';

	$('.pat').click(function(){
		var pattern = $(this).text();

		$('#chart-container').find('.pattern').text(pattern);

		current = encodeURIComponent( pattern.toLowerCase() );

		// click the same pattern, just show
		if( current == prev )
		{
			$('#chart-container').removeClass('hide');
			$('.mask').removeClass('hide');
		}
		// click different patterns, send ajax req
		else
		{
			prev = current;

			var obj = $(this);
			
			$.getJSON('../../api/pat_distribution/'+current, function(data){
		    	if(data.length == 0)
		    	{
		    		obj.addClass('lock').removeClass('open');
		    		return false;
		    	}
		    	else {
		    		draw(data);
					$('#chart-container').removeClass('hide');
					$('.mask').removeClass('hide');		    		
		    	}
			}).error(function(){
				obj.addClass('lock').removeClass('open');
				console.log('ajax error');
			});

		}

	});
	$('.close').click(function(){
		$(this).parents('.container').addClass('hide');
		$('.mask').addClass('hide');
	});
	$('.mask').click(function(){
		$('.close').click();
	});
	$(document).keyup(function(e){
		if(e.which == 27 || e.keyCode == 27)
		{
			if( !$('#chart-container').hasClass('hide') )
			{
				$('.close').click();
			}
		}
	});
}

