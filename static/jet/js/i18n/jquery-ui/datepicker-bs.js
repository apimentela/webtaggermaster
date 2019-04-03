(function( factory ) {
	if ( typeof define === "function" && define.amd ) {
		define([ "../datepicker" ], factory );
	} else {
		factory( jQuery.datepicker );
	}
}(function( datepicker ) {
datepicker.regional['bs'] = {
	closeText: 'Zatvori',
	prevText: '&#x3C;',
	nextText: '&#x3E;',
	currentText: 'Danas',
	monthNames: ['Januar','Februar','Mart','April','Maj','Juni',
	'Juli','August','Septembar','Oktobar','Novembar','Decembar'],
	monthNamesShort: ['Jan','Feb','Mar','Apr','Maj','Jun',
	'Jul','Aug','Sep','Okt','Nov','Dec'],
	dayNames: ['Nedelja','Ponedeljak','Utorak','Srijeda','Četvrtak','Petak','Subota'],
	dayNamesShort: ['Ned','Pon','Uto','Sri','Čet','Pet','Sub'],
	dayNamesMin: ['Ne','Po','Ut','Sr','Če','Pe','Su'],
	weekHeader: 'Wk',
	dateFormat: 'dd.mm.yy',
	firstDay: 1,
	isRTL: false,
	showMonthAfterYear: false,
	yearSuffix: ''};
datepicker.setDefaults(datepicker.regional['bs']);
return datepicker.regional['bs'];
}));
