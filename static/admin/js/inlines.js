(function($) {
    'use strict';
    $.fn.formset = function(opts) {
        var options = $.extend({}, $.fn.formset.defaults, opts);
        var $this = $(this);
        var $parent = $this.parent();
        var updateElementIndex = function(el, prefix, ndx) {
            var id_regex = new RegExp("(" + prefix + "-(\\d+|__prefix__))");
            var replacement = prefix + "-" + ndx;
            if ($(el).prop("for")) {
                $(el).prop("for", $(el).prop("for").replace(id_regex, replacement));
            }
            if (el.id) {
                el.id = el.id.replace(id_regex, replacement);
            }
            if (el.name) {
                el.name = el.name.replace(id_regex, replacement);
            }
        };
        var totalForms = $("#id_" + options.prefix + "-TOTAL_FORMS").prop("autocomplete", "off");
        var nextIndex = parseInt(totalForms.val(), 10);
        var maxForms = $("#id_" + options.prefix + "-MAX_NUM_FORMS").prop("autocomplete", "off");
        var showAddButton = maxForms.val() === '' || (maxForms.val() - totalForms.val()) > 0;
        $this.each(function(i) {
            $(this).not("." + options.emptyCssClass).addClass(options.formCssClass);
        });
        if ($this.length && showAddButton) {
            var addButton;
            if ($this.prop("tagName") === "TR") {
                var numCols = this.eq(-1).children().length;
                $parent.append('<tr class="' + options.addCssClass + '"><td colspan="' + numCols + '"><a href="javascript:void(0)">' + options.addText + "</a></tr>");
                addButton = $parent.find("tr:last a");
            } else {
                $this.filter(":last").after('<div class="' + options.addCssClass + '"><a href="javascript:void(0)">' + options.addText + "</a></div>");
                addButton = $this.filter(":last").next().find("a");
            }
            addButton.click(function(e) {
                e.preventDefault();
                var template = $("#" + options.prefix + "-empty");
                var row = template.clone(true);
                row.removeClass(options.emptyCssClass)
                .addClass(options.formCssClass)
                .attr("id", options.prefix + "-" + nextIndex);
                if (row.is("tr")) {
                    row.children(":last").append('<div><a class="' + options.deleteCssClass + '" href="javascript:void(0)">' + options.deleteText + "</a></div>");
                } else if (row.is("ul") || row.is("ol")) {
                    row.append('<li><a class="' + options.deleteCssClass + '" href="javascript:void(0)">' + options.deleteText + "</a></li>");
                } else {
                    row.children(":first").append('<span><a class="' + options.deleteCssClass + '" href="javascript:void(0)">' + options.deleteText + "</a></span>");
                }
                row.find("*").each(function() {
                    updateElementIndex(this, options.prefix, totalForms.val());
                });
                row.insertBefore($(template));
                $(totalForms).val(parseInt(totalForms.val(), 10) + 1);
                nextIndex += 1;
                if ((maxForms.val() !== '') && (maxForms.val() - totalForms.val()) <= 0) {
                    addButton.parent().hide();
                }
                row.find("a." + options.deleteCssClass).click(function(e1) {
                    e1.preventDefault();
                    row.remove();
                    nextIndex -= 1;
                    if (options.removed) {
                        options.removed(row);
                    }
                    $(document).trigger('formset:removed', [row, options.prefix]);
                    var forms = $("." + options.formCssClass);
                    $("#id_" + options.prefix + "-TOTAL_FORMS").val(forms.length);
                    if ((maxForms.val() === '') || (maxForms.val() - forms.length) > 0) {
                        addButton.parent().show();
                    }
                    var i, formCount;
                    var updateElementCallback = function() {
                        updateElementIndex(this, options.prefix, i);
                    };
                    for (i = 0, formCount = forms.length; i < formCount; i++) {
                        updateElementIndex($(forms).get(i), options.prefix, i);
                        $(forms.get(i)).find("*").each(updateElementCallback);
                    }
                });
                if (options.added) {
                    options.added(row);
                }
                $(document).trigger('formset:added', [row, options.prefix]);
            });
        }
        return this;
    };
    $.fn.formset.defaults = {
        prefix: "form",          // The form prefix for your django formset
        addText: "add another",      // Text for the add link
        deleteText: "remove",      // Text for the delete link
        addCssClass: "add-row",      // CSS class applied to the add link
        deleteCssClass: "delete-row",  // CSS class applied to the delete link
        emptyCssClass: "empty-row",    // CSS class applied to the empty row
        formCssClass: "dynamic-form",  // CSS class applied to each form in a formset
        added: null,          // Function called each time a new form is added
        removed: null          // Function called each time a form is deleted
    };
    $.fn.tabularFormset = function(options) {
        var $rows = $(this);
        var alternatingRows = function(row) {
            $($rows.selector).not(".add-row").removeClass("row1 row2")
            .filter(":even").addClass("row1").end()
            .filter(":odd").addClass("row2");
        };
        var reinitDateTimeShortCuts = function() {
            if (typeof DateTimeShortcuts !== "undefined") {
                $(".datetimeshortcuts").remove();
                DateTimeShortcuts.init();
            }
        };
        var updateSelectFilter = function() {
            if (typeof SelectFilter !== 'undefined') {
                $('.selectfilter').each(function(index, value) {
                    var namearr = value.name.split('-');
                    SelectFilter.init(value.id, namearr[namearr.length - 1], false);
                });
                $('.selectfilterstacked').each(function(index, value) {
                    var namearr = value.name.split('-');
                    SelectFilter.init(value.id, namearr[namearr.length - 1], true);
                });
            }
        };
        var initPrepopulatedFields = function(row) {
            row.find('.prepopulated_field').each(function() {
                var field = $(this),
                    input = field.find('input, select, textarea'),
                    dependency_list = input.data('dependency_list') || [],
                    dependencies = [];
                $.each(dependency_list, function(i, field_name) {
                    dependencies.push('#' + row.find('.field-' + field_name).find('input, select, textarea').attr('id'));
                });
                if (dependencies.length) {
                    input.prepopulate(dependencies, input.attr('maxlength'));
                }
            });
        };
        $rows.formset({
            prefix: options.prefix,
            addText: options.addText,
            formCssClass: "dynamic-" + options.prefix,
            deleteCssClass: "inline-deletelink",
            deleteText: options.deleteText,
            emptyCssClass: "empty-form",
            removed: alternatingRows,
            added: function(row) {
                initPrepopulatedFields(row);
                reinitDateTimeShortCuts();
                updateSelectFilter();
                alternatingRows(row);
            }
        });
        return $rows;
    };
    $.fn.stackedFormset = function(options) {
        var $rows = $(this);
        var updateInlineLabel = function(row) {
            $($rows.selector).find(".inline_label").each(function(i) {
                var count = i + 1;
                $(this).html($(this).html().replace(/(#\d+)/g, "#" + count));
            });
        };
        var reinitDateTimeShortCuts = function() {
            if (typeof DateTimeShortcuts !== "undefined") {
                $(".datetimeshortcuts").remove();
                DateTimeShortcuts.init();
            }
        };
        var updateSelectFilter = function() {
            if (typeof SelectFilter !== "undefined") {
                $(".selectfilter").each(function(index, value) {
                    var namearr = value.name.split('-');
                    SelectFilter.init(value.id, namearr[namearr.length - 1], false);
                });
                $(".selectfilterstacked").each(function(index, value) {
                    var namearr = value.name.split('-');
                    SelectFilter.init(value.id, namearr[namearr.length - 1], true);
                });
            }
        };
        var initPrepopulatedFields = function(row) {
            row.find('.prepopulated_field').each(function() {
                var field = $(this),
                    input = field.find('input, select, textarea'),
                    dependency_list = input.data('dependency_list') || [],
                    dependencies = [];
                $.each(dependency_list, function(i, field_name) {
                    dependencies.push('#' + row.find('.form-row .field-' + field_name).find('input, select, textarea').attr('id'));
                });
                if (dependencies.length) {
                    input.prepopulate(dependencies, input.attr('maxlength'));
                }
            });
        };
        $rows.formset({
            prefix: options.prefix,
            addText: options.addText,
            formCssClass: "dynamic-" + options.prefix,
            deleteCssClass: "inline-deletelink",
            deleteText: options.deleteText,
            emptyCssClass: "empty-form",
            removed: updateInlineLabel,
            added: function(row) {
                initPrepopulatedFields(row);
                reinitDateTimeShortCuts();
                updateSelectFilter();
                updateInlineLabel(row);
            }
        });
        return $rows;
    };
})(django.jQuery);
