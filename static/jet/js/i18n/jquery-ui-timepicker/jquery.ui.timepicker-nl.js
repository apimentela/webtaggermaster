jQuery(function($){
    $.timepicker.regional['nl'] = {
                hourText: 'Uren',
                minuteText: 'Minuten',
                amPmText: ['AM', 'PM'],
				closeButtonText: 'Sluiten',
				nowButtonText: 'Actuele tijd',
				deselectButtonText: 'Wissen' }
    $.timepicker.setDefaults($.timepicker.regional['nl']);
});
