jQuery(function($){
    $.timepicker.regional['fr'] = {
                hourText: 'Heures',
                minuteText: 'Minutes',
                amPmText: ['AM', 'PM'],
                closeButtonText: 'Fermer',
                nowButtonText: 'Maintenant',
                deselectButtonText: 'Désélectionner' }
    $.timepicker.setDefaults($.timepicker.regional['fr']);
});
