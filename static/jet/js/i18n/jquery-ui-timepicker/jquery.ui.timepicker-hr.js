jQuery(function($){
    $.timepicker.regional['hr'] = {
                hourText: 'Sat',
                minuteText: 'Minuta',
                amPmText: ['Prijepodne', 'Poslijepodne'],
                closeButtonText: 'Zatvoriti',
                nowButtonText: 'Sada',
                deselectButtonText: 'Poništite'}
    $.timepicker.setDefaults($.timepicker.regional['hr']);
});
