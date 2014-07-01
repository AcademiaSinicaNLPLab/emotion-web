function fill_colors(pat, colors)
{
	// var emotions = $.map(colors, function(key,value) {return key})

	// console.log(emotions)
	// var color_cell = $('<div/>')
	var color_cell = $('<tr/>')
							.addClass('color-row')
							.attr('pattern', pat)
							.appendTo('.color-levels-wrap');

	$.each(colors, function(i, color_obj){
		var emotion = color_obj[0];
		var color = color_obj[1] == 'none' ? false : color_obj[1];
		var status = color_obj[1] == 'none' ? 'off' : 'on';
		// console.log(emotion, '-->', color)

		// var color_block = $('<div/>')
		var color_block = $('<td/>')
								.text('O')
								.addClass('color-cell')
								.attr('emotion', emotion)
								.attr('status', status)
								.css({'background': color})
								.appendTo(color_cell);
	});
	
}

function bind_hover_event()
{
	
	// $( document ).on( "click", '.color-block', function(){ console.log($(this)); event.stopPropagation(); var pattern = $(this).attr('pattern'); console.log(pattern); });

	$( document ).on( "mouseover", '.color-cell', function(event){

		var status = $(this).attr('status');
		var color_info_wrap = $('.color-info-wrap');

		var color_emotion = color_info_wrap.find('.color-emotion');
		var color_pattern = color_info_wrap.find('.color-pattern');	



		if(status == 'on')
		{
			var emotion = $(this).attr('emotion'); 
			var pattern = $(this).parent().attr('pattern');

			color_info_wrap.offset({ top: event.clientY + $(document).scrollTop(), left: 16 + event.clientX});

			// color_info_wrap.offset({ top: 100, left: 100});

			// console.log( event.clientX );
			// var st = $(document).scrollTop();
			// console.log( )
			// console.log( 'clientY:',event.clientY );
			// console.log( 'pageY:',event.pageY );

			color_emotion.css({'background': $(this).css('background')});

			color_emotion.text(emotion);
			color_pattern.text(pattern);

			// color_info_wrap.removeClass('hide');
			// color_info_wrap.removeClass('hide');
			
		}else
		{
			color_info_wrap.offset({ top: 0, left: 0});
			color_emotion.text('');
			color_pattern.text('');
			color_emotion.css({'background': false});
			// color_info_wrap.addClass('hide');
		}
	}).on( "mouseleave", '.color-cell', function(){
		var color_info_wrap = $('.color-info-wrap');

		var color_emotion = color_info_wrap.find('.color-emotion');
		var color_pattern = color_info_wrap.find('.color-pattern');	
		color_info_wrap.offset({ top: 0, left: 0});		
		color_emotion.text('');
		color_pattern.text('');
		color_emotion.css({'background': false});		
		// var color_info_wrap = $('.color-info-wrap');
		// color_info_wrap.addClass('hide');
	});
}

function bind_switch_event()
{
	$('#feeling-platte').click(function(){
		$('.color-wrap').slideToggle();
	});
}

function bind_color_events()
{

	bind_hover_event();


	bind_switch_event();

	var pats = $('.pat');

	var total = pats.length;

	$.each(pats, function(i, obj){
		var pat = $(obj).text();

		var api_url = '../../../api/pat_color/'+pat;

		$.ajax({
			dataType: "json",
			url: api_url,
			type: "GET",
			statusCode: {
				200: function (data) {
					console.log('[200] get',data.length,'colors in "'+decodeURIComponent(pat)+'"' );
					// console.log(data);

					fill_colors(pat, data);
					// defined in chart.js
					// draw(data);

					// $('#chart-container').removeClass('hide');
					// $('.mask').removeClass('hide');
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
			// $('.pat-search-loading').toggleClass('hide');
		});		
		// return false;
	});
	
}