(function( factory ) {
	if ( typeof define === "function" && define.amd ) {
		define([ "../datepicker" ], factory );
	} else {
		factory( jQuery.datepicker );
	}
}(function( datepicker ) {
datepicker.regional['tj'] = {
	closeText: 'Идома',
	prevText: '&#x3c;Қафо',
	nextText: 'Пеш&#x3e;',
	currentText: 'Имрӯз',
	monthNames: ['Январ','Феврал','Март','Апрел','Май','Июн',
	'Июл','Август','Сентябр','Октябр','Ноябр','Декабр'],
	monthNamesShort: ['Янв','Фев','Мар','Апр','Май','Июн',
	'Июл','Авг','Сен','Окт','Ноя','Дек'],
	dayNames: ['якшанбе','душанбе','сешанбе','чоршанбе','панҷшанбе','ҷумъа','шанбе'],
	dayNamesShort: ['якш','душ','сеш','чор','пан','ҷум','шан'],
	dayNamesMin: ['Як','Дш','Сш','Чш','Пш','Ҷм','Шн'],
	weekHeader: 'Хф',
	dateFormat: 'dd.mm.yy',
	firstDay: 1,
	isRTL: false,
	showMonthAfterYear: false,
	yearSuffix: ''};
datepicker.setDefaults(datepicker.regional['tj']);
return datepicker.regional['tj'];
}));
