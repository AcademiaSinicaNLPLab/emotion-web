var emotions = [];

function getEmotions()
{
	// $('.predict-label').each(function(i, obj){
	// 	console.log( $(obj).attr('emotion') );
	// })
	var labels = $.map( $('.predict-label'), function( obj, i ) {
		return $(obj).attr('emotion');
	});
	labels.sort()
	return labels;
	// console.log( labels );
}


function restore()
{
	// clear previous select
	$('td').removeClass('highlight');

	$.each( $('.show_true_self'), function(i, obj){

		if( $(obj).hasClass('gold-label') )
		{
			var goldidx = parseInt($(obj).attr('goldidx')) + 1;
			$(obj).text( goldidx );
		}
		else if( $(obj).hasClass('predict-label') )
		{
			var predictidx = parseInt($(obj).attr('predictidx')) + 1;
			$(obj).text( predictidx );
		}
		$(obj).removeClass('show_true_self');

	});
}

function bind_label_hover_event () 
{

	var predict_label_type = $('#predict-label-wrap').find('.label-type');
	var predict_label_name = $('#predict-label-wrap').find('.label-name');

	var gold_label_type = $('#gold-label-wrap').find('.label-type');
	var gold_label_name = $('#gold-label-wrap').find('.label-name');

	var clear = function(){
		predict_label_type.text('');
		predict_label_name.text('');
		gold_label_type.text('');
		gold_label_name.text('');
	}

	// predict event
	$('.predict-label').mouseenter(function(){
		var predict_label = $(this).attr('emotion');
		predict_label_type.text('(predict)');
		predict_label_name.text(predict_label);
	}).mouseleave(function(){
		clear();
	}).click(function(){
		var predictidx = $(this).attr('predictidx');

		restore();
		
		// select row
		$('td[predictidx='+predictidx+']').addClass('highlight');	

		show_predict_label(predictidx);
	});

	// gold-label event
	$('.gold-label').mouseenter(function(){
		var gold_label = $(this).attr('emotion');
		gold_label_type.text('(gold)');
		gold_label_name.text(gold_label);
	}).mouseleave(function(){
		clear();
	}).click(function(){
		var goldidx = $(this).attr('goldidx');

		restore();

		// select row
		$('td[goldidx='+goldidx+']').addClass('highlight');

		show_gold_label(goldidx);	

	});


	/// count event
	$('.count').mouseenter(function(){
		var goldidx = parseInt($(this).attr('goldidx'));
		var predictidx = parseInt($(this).attr('predictidx'));

		// console.log( goldidx )
		// console.log( predictidx )

		gold_label_type.text('(gold)');
		gold_label_name.text(emotions[goldidx]);

		predict_label_type.text('(predict)');
		predict_label_name.text(emotions[predictidx]);

	}).mouseleave(function(){
		clear();
	}).click(function(){

		var goldidx = $(this).attr('goldidx');
		var predictidx = $(this).attr('predictidx');

		restore();

		// select row
		$('td[goldidx='+goldidx+']').addClass('highlight');

		// select col
		$('td[predictidx='+predictidx+']').addClass('highlight');

		show_gold_label(goldidx);
		show_predict_label(predictidx);
	});
}


function show_gold_label(goldidx)
{
	$('.gold-label[goldidx='+goldidx.toString()+']').addClass('show_true_self').text( emotions[parseInt(goldidx)] );
}
function show_predict_label(predictidx)
{
	$('.predict-label[predictidx='+predictidx.toString()+']').addClass('show_true_self').text( emotions[parseInt(predictidx)] );
}

function bind_init_events()
{
	emotions = getEmotions();
}

function bind_dev_events()
{
	$('#hitme').click(function(){
		emotions = getEmotions();
	});

}