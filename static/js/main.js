$(document).ready(function(){
	events();
});
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
}