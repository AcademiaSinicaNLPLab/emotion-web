
function search_event()
{
	$('.pat').click(function(){
		var pat = $(this).text()
		pat = encodeURIComponent( pat.toLowerCase() );

		var api_url = window.location.pathname.indexOf('/feelit/') >= 0 ? '/feelit/api/pat_distribution/'+pat : '/api/pat_distribution/'+pat;

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
	});
	
}

function filter_event()
{
	var handler = function(){

		

		var filter_name = $.trim( $(this).parent().find('.filter-name').val() ).toLowerCase();
		var filter_option = $.trim( $(this).parent().find('.filter-option').val() );
		var filter_value = parseFloat( $.trim($(this).parent().find('.filter-value').val()) );

		console.log( filter_name, filter_option, filter_value );

		var targets = $('.data').find('tr.pat-wrap');

		var keep_cnt = 0;
		var total_cnt = 0;

		$.each(targets, function(i, obj){

			var target = $(obj);

			var target_value = parseFloat( target.find('td[vtype="'+filter_name+'"]').text() );

			var hide;

			if( filter_option == '>' )
			{
				hide = target_value > filter_value ? true : false;
			}else
			{
				hide = target_value < filter_value ? true : false;
			}
			if( hide )
			{
				if( !target.hasClass('fade') ){ target.addClass('fade') }
				
			}else
			{
				if( target.hasClass('fade') ){ target.removeClass('fade') }
				keep_cnt += 1;
			}
			total_cnt += 1;
		});

		$('.filter-info').find('.remain-value').text( Math.round(parseFloat(keep_cnt)/parseFloat(total_cnt)*100).toString() + '%')
	};
	$('.filters-wrap').find('input').click(handler).keyup(handler);
	$('.filters-wrap').find('select').change(handler);
}

$(document).ready(function(){

	filter_event();
	search_event();

	$('.filter-name').click();
});