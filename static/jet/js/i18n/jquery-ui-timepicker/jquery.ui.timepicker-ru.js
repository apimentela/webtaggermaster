jQuery(function($){
    $.timepicker.regional['ru'] = {
                hourText: 'Часы',
                minuteText: 'Минуты',
                amPmText: ['AM', 'PM'],
                closeButtonText: 'Готово',
                nowButtonText: 'Сейчас',
                deselectButtonText: 'Снять выделение' }
    $.timepicker.setDefaults($.timepicker.regional['ru']);
});
