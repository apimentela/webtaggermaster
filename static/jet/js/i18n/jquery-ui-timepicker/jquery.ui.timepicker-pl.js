jQuery(function($){
    $.timepicker.regional['pl'] = {
                hourText: 'Godziny',
                minuteText: 'Minuty',
                amPmText: ['', ''],
				closeButtonText: 'Zamknij',
                nowButtonText: 'Teraz',
                deselectButtonText: 'Odznacz'}
    $.timepicker.setDefaults($.timepicker.regional['pl']);
});
