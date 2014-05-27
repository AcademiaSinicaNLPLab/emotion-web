function results_events()
{
	$('.feature_name[type=fusion]').click(function(){
		var idx = $('.feature_name').index($(this));

		var sources = $('.detail').eq(idx).find('.sources').attr('sources').split(',');

		$('.col').removeClass('highlight');

		$.each(sources, function(i, src){
			var sid_idx = $('.sid').index( $('.sid[sid="'+src+'"]') );
			$('td.col').eq(sid_idx).addClass('highlight');
			$('.avg').eq(sid_idx).addClass('highlight');
			$('.param').eq(sid_idx).addClass('highlight');
			$('.detail').eq(sid_idx).addClass('highlight');
		});
	});
}