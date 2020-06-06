$(document).ready(function(){
	AOS.init({ disable: 'mobile' });

	$('[data-bs-chart]').each(function(index, elem) {
		this.chart = new Chart($(elem), $(elem).data('bs-chart'));
	});

});