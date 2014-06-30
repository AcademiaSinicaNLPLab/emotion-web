
function bind_feature_options_event () 
{
	var features_chx = $('.feature-options').find('input:checkbox');
	var features_label = $('.feature-options').find('label');
	var features_weights = $('.feature-options').find('input:text');

	// features_label.click(function(e){ 
	// 	var chkbox = $(this).siblings('input:checkbox');

	// 	var tf = chkbox.attr("checked") == undefined ? false : true
	// 	console.log( tf );
	// 	chkbox.attr("checked", !tf);
	// });

	// $.each(chx, function(i, obj){

	// });


	// console.log(features_chx);
	// console.log(features_label);
	// console.log(features_weights);
}

function get_instant_feature_options()
{
	return "{ 'TFIDF':0.7, 'pattern':0.3 }"
}
function randomData (){
	var labels = color.domain();
	return labels.map(function(label){
		return { label: label, value: Math.random() }
	});
}
function bind_instant_predict_event () {
	$('#demo-submit-btn').click(function(){
		var text = $('#demo-textarea').val();
		

		// var feature_types = $('.feature-checkbox').map(function() { return $(this).val(); }).get();
		// console.log( feature_types );
		var api_url = '/feelit/api/predict/'
		$.ajax({
			url: api_url,
			type: "POST",
			data: {'article': text,  options: get_instant_feature_options() },
			statusCode: {
				200: function (data) {
					console.log('[200] get',data);

					var parsed = JSON.parse(data);

					// var seq = $.map( parsed, function(i, val){
						
					// 	return {label: val[0], value: val[1]}
					// } );

					// console.log( seq );
					// var data = data.map();
					var labels = parsed.map(function(obj){ return { label: obj[0], value: obj[1]}; });

					var d = randomData();

					change(labels);

					// d3.select(".randomize")
					// 	.on("click", function(){
					// 		change(randomData());
					// 	});
				},
				204: function (resp) {
					console.log('[204] no data for "'+decodeURIComponent(text)+'"');
				},
				500: function (resp) {
					console.log('[500] error to get info of "',decodeURIComponent(text)+'"');
				}
			}
		}).complete(function(){
			console.log('complete ajax');
			// close loading
			// $('.pat-search-loading').toggleClass('hide');
		});		
	});
}