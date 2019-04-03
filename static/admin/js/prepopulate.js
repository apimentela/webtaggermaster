(function($) {
    'use strict';
    $.fn.prepopulate = function(dependencies, maxLength, allowUnicode) {
        return this.each(function() {
            var prepopulatedField = $(this);
            var populate = function() {
                if (prepopulatedField.data('_changed')) {
                    return;
                }
                var values = [];
                $.each(dependencies, function(i, field) {
                    field = $(field);
                    if (field.val().length > 0) {
                        values.push(field.val());
                    }
                });
                prepopulatedField.val(URLify(values.join(' '), maxLength, allowUnicode));
            };
            prepopulatedField.data('_changed', false);
            prepopulatedField.change(function() {
                prepopulatedField.data('_changed', true);
            });
            if (!prepopulatedField.val()) {
                $(dependencies.join(',')).keyup(populate).change(populate).focus(populate);
            }
        });
    };
})(django.jQuery);
