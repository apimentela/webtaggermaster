jQuery(function($){
    $.timepicker.regional['de'] = {
                hourText: 'Stunde',
                minuteText: 'Minuten',
                amPmText: ['AM', 'PM'] ,
                closeButtonText: 'Beenden',
                nowButtonText: 'Aktuelle Zeit',
                deselectButtonText: 'Wischen' }
    $.timepicker.setDefaults($.timepicker.regional['de']);
});
