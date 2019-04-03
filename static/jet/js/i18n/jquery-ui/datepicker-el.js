(function( factory ) {
	if ( typeof define === "function" && define.amd ) {
		define([ "../datepicker" ], factory );
	} else {
		factory( jQuery.datepicker );
	}
}(function( datepicker ) {
datepicker.regional['el'] = {
	closeText: 'Κλείσιμο',
	prevText: 'Προηγούμενος',
	nextText: 'Επόμενος',
	currentText: 'Σήμερα',
	monthNames: ['Ιανουάριος','Φεβρουάριος','Μάρτιος','Απρίλιος','Μάιος','Ιούνιος',
	'Ιούλιος','Αύγουστος','Σεπτέμβριος','Οκτώβριος','Νοέμβριος','Δεκέμβριος'],
	monthNamesShort: ['Ιαν','Φεβ','Μαρ','Απρ','Μαι','Ιουν',
	'Ιουλ','Αυγ','Σεπ','Οκτ','Νοε','Δεκ'],
	dayNames: ['Κυριακή','Δευτέρα','Τρίτη','Τετάρτη','Πέμπτη','Παρασκευή','Σάββατο'],
	dayNamesShort: ['Κυρ','Δευ','Τρι','Τετ','Πεμ','Παρ','Σαβ'],
	dayNamesMin: ['Κυ','Δε','Τρ','Τε','Πε','Πα','Σα'],
	weekHeader: 'Εβδ',
	dateFormat: 'dd/mm/yy',
	firstDay: 1,
	isRTL: false,
	showMonthAfterYear: false,
	yearSuffix: ''};
datepicker.setDefaults(datepicker.regional['el']);
return datepicker.regional['el'];
}));
