jQuery(function($){
    $.timepicker.regional['hu'] = {
                hourText: 'Óra',
                minuteText: 'Perc',
                amPmText: ['De.', 'Du.'] ,
                closeButtonText: 'Kész',
                nowButtonText: 'Most',
                deselectButtonText: 'Törlés' }
    $.timepicker.setDefaults($.timepicker.regional['hu']);
});
