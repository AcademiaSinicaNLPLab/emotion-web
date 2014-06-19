$(document).ready(function(){

	search_events();
	
	chart_events();
	chart_autoStyling();

	matrix_events();

	results_events();

	$('#tomatrix').click();
});

var current = '';
var prev = '';
var data = [];

var colors = ['#428bca', '#5cb85c', '#f0ad4e'];
var colorsDark = ['#3276b1', '#47a347', '#ed9c28'];

function pat_search(pat)
{

}

function search_events()
{
	$('.pat-search-btn').click(function(){
		var pat = $.trim( $(this).siblings('.pat-search-bar').val() );

		$('#chart-container').find('.pattern').text(pat);
		pat = encodeURIComponent( pat.toLowerCase() );

		var api_url = '/feelit/api/pat_distribution/'+pat;

		$('.pat-search-loading').toggleClass('hide');
		

			setTimeout(function(){
				$.ajax({
					url: api_url,
					type: "GET",
					statusCode: {
						200: function (data) {
							console.log('[200] get',data.length,'emotions in "'+decodeURIComponent(pat)+'"' );

							// defined in chart.js
							draw(data);

							$('#chart-container').removeClass('hide');
							$('.mask').removeClass('hide');
						},
						204: function (resp) {
							console.log('[204] no data for "'+decodeURIComponent(pat)+'"');

							// obj.addClass('lock').removeClass('open');
						},
						500: function (resp) {
							console.log('[500] error to get info of "',decodeURIComponent(pat)+'"');
						}
					}
				}).complete(function(){
					console.log('complete ajax');
					// close loading
					$('.pat-search-loading').toggleClass('hide');
				});	
			}, 250);


	});
	$('.pat-search-bar').keyup(function(e){
		if(e.keyCode == 13 || e.which == 13)
		{
			$('.pat-search-btn').click();
		}
	});	
}

function chart_autoStyling() {
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

function chart_events(){

	var prev = '';
	var current = '';

	$('.pat').click(function(){

		// if the pattern is already locked (in gray color)
		// just skip all operation
		if( $(this).hasClass('lock') ){
			return false;
		}

		var pattern = $(this).text();

		$('#chart-container').find('.pattern').text(pattern);

		current = encodeURIComponent( pattern.toLowerCase() );

		// click the same pattern
		// hide mask, show chart
		if( current == prev )
		{
			$('#chart-container').removeClass('hide');
			$('.mask').removeClass('hide');
		}
		// click different patterns, send ajax request
		else
		{
			prev = current;

			var obj = $(this);

			var api_url = '../../../api/pat_distribution/'+current; // change to automatically bind the url address? like "os.path.join" in python

			$.ajax({
				url: api_url,
				type: "GET",
				statusCode: {
					200: function (data) {
						console.log('[200] get',data.length,'emotions in "'+decodeURIComponent(current)+'"' );

						// defined in chart.js
						draw(data);

						$('#chart-container').removeClass('hide');
						$('.mask').removeClass('hide');
					},
					204: function (resp) {
						console.log('[204] no data for "'+decodeURIComponent(current)+'"');

						obj.addClass('lock').removeClass('open');
					},
					500: function (resp) {
						console.log('[500] error to get info of "',decodeURIComponent(current)+'"');
					}
				}
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

function matrix_events()
{
	bind_init_events();
	bind_label_hover_event();
	bind_dev_events();
	bind_filter_evnet();
}
