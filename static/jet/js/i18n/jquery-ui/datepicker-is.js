(function( factory ) {
	if ( typeof define === "function" && define.amd ) {
		define([ "../datepicker" ], factory );
	} else {
		factory( jQuery.datepicker );
	}
}(function( datepicker ) {
datepicker.regional['is'] = {
	closeText: 'Loka',
	prevText: '&#x3C; Fyrri',
	nextText: 'Næsti &#x3E;',
	currentText: 'Í dag',
	monthNames: ['Janúar','Febrúar','Mars','Apríl','Maí','Júní',
	'Júlí','Ágúst','September','Október','Nóvember','Desember'],
	monthNamesShort: ['Jan','Feb','Mar','Apr','Maí','Jún',
	'Júl','Ágú','Sep','Okt','Nóv','Des'],
	dayNames: ['Sunnudagur','Mánudagur','Þriðjudagur','Miðvikudagur','Fimmtudagur','Föstudagur','Laugardagur'],
	dayNamesShort: ['Sun','Mán','Þri','Mið','Fim','Fös','Lau'],
	dayNamesMin: ['Su','Má','Þr','Mi','Fi','Fö','La'],
	weekHeader: 'Vika',
	dateFormat: 'dd.mm.yy',
	firstDay: 0,
	isRTL: false,
	showMonthAfterYear: false,
	yearSuffix: ''};
datepicker.setDefaults(datepicker.regional['is']);
return datepicker.regional['is'];
}));
