jQuery(function($){
    $.timepicker.regional['tr'] = {
                hourText: 'Saat',
                minuteText: 'Dakika',
                amPmText: ['AM', 'PM'],
                closeButtonText: 'Kapat',
                nowButtonText: 'Şu anda',
                deselectButtonText: 'Seçimi temizle' }
    $.timepicker.setDefaults($.timepicker.regional['tr']);
});
