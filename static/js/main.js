$(document).ready(function(){
	events();
	autoStyling();
});

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

		var obj = $(this);

		$.getJSON('/api/pat/'+pattern.toLowerCase(), function(data){

			// var number = 0;

			// console.log(data.length);

			if(data.length == 0) {
				// cannot find pattern score
				// set to unable-to-click
				obj.addClass('lock').removeClass('open');
				return false;
			}
			draw(data);
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

