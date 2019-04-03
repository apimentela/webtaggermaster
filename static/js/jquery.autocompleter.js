;(function ($, window) {
    'use strict';
    var guid = 0,
        ignoredKeyCode = [9, 13, 17, 19, 20, 27, 33, 34, 35, 36, 37, 39, 44, 92, 113, 114, 115, 118, 119, 120, 122, 123, 144, 145],
        allowOptions = [
            'source',
            'empty',
            'limit',
            'cache',
            'cacheExpires',
            'focusOpen',
            'selectFirst',
            'changeWhenSelect',
            'highlightMatches',
            'ignoredKeyCode',
            'customLabel',
            'customValue',
            'template',
            'offset',
            'combine',
            'callback',
            'minLength',
            'delay'
        ],
        userAgent = (window.navigator.userAgent||window.navigator.vendor||window.opera),
        isFirefox = /Firefox/i.test(userAgent),
        isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(userAgent),
        isFirefoxMobile = (isFirefox && isMobile),
        $body = null,
        delayTimeout = null,
        localStorageKey = 'autocompleterCache',
        supportLocalStorage = (function () {
            var supported = typeof window.localStorage !== 'undefined';
            if (supported) {
                try {
                    localStorage.setItem('autocompleter', 'autocompleter');
                    localStorage.removeItem('autocompleter');
                } catch (e) {
                    supported = false;
                }
            }
            return supported;
        })();
    var options = {
        source: null,
        asLocal: false,
        empty: true,
        limit: 10,
        minLength: 0,
        delay: 0,
        customClass: [],
        cache: true,
        cacheExpires: 86400,
        focusOpen: true,
        hint: false,
        selectFirst: false,
        changeWhenSelect: true,
        highlightMatches: false,
        ignoredKeyCode: [],
        customLabel: false,
        customValue: false,
        template: false,
        offset: false,
        combine: $.noop,
        callback: $.noop
    };
    var publics = {
        defaults: function (opts) {
            console.log("defaults!!");
            options = $.extend(options, opts || {});
            return (typeof this === 'object') ? $(this) : true;
        },
        option: function (properties) {
            console.log("options!!");
            return $(this).each(function (i, input) {
                var data = $(input).next('.autocompleter').data('autocompleter');
                for (var property in properties) {
                    if ($.inArray(property, allowOptions) !== -1) {
                        data[property] = properties[property];
                    }
                }
            });
        },
        open: function () {
            return $(this).each(function (i, input) {
                var data = $(input).next('.autocompleter').data('autocompleter');
                if (data) {
                    _open(null, data);
                }
            });
        },
        close: function () {
            return $(this).each(function (i, input) {
                var data = $(input).next('.autocompleter').data('autocompleter');
                if (data) {
                    _close(null, data);
                }
            });
        },
        clearCache: function () {
            _deleteCache();
        },
        destroy: function () {
            return $(this).each(function (i, input) {
                var data = $(input).next('.autocompleter').data('autocompleter');
                if (data) {
                    if (data.jqxhr) {
                        data.jqxhr.abort();
                    }
                    if (data.$autocompleter.hasClass('open')) {
                        data.$autocompleter.find('.autocompleter-selected')
                                           .trigger('click.autocompleter');
                    }
                    if (!data.originalAutocomplete) {
                        data.$node.removeAttr('autocomplete');
                    } else {
                        data.$node.attr('autocomplete', data.originalAutocomplete);
                    }
                    data.$node.off('.autocompleter')
                               .removeClass('autocompleter-node');
                    data.$autocompleter.off('.autocompleter')
                                         .remove();
                }
            });
        }
    };
    function _init(opts) {
        opts = $.extend({}, options, opts || {});
        if ($body === null) {
            $body = $('body');
        }
        var $items = $(this);
        for (var i = 0, count = $items.length; i < count; i++) {
            _build($items.eq(i), opts);
        }
        return $items;
    }
    function _build($node, opts) {
        if (!$node.hasClass('autocompleter-node')) {
            opts = $.extend({}, opts, $node.data('autocompleter-options'));
            if (typeof opts.source === 'string' && (opts.source.slice(-5) === '.json' || opts.asLocal === true)) {
                $.ajax({
                    url: opts.source,
                    type: 'GET',
                    dataType: 'json',
                    async: false
                }).done(function (response) {
                    opts.source = response;
                });
            }
            var html = '<div class="autocompleter ' + opts.customClass.join(' ') + '" id="autocompleter-' + (guid + 1) + '">';
            if (opts.hint) {
                html += '<div class="autocompleter-hint"></div>';
            }
            html += '<ul class="autocompleter-list"></ul>';
            html += '</div>';
            $node.addClass('autocompleter-node')
                 .after(html);
            var $autocompleter = $node.next('.autocompleter').eq(0);
            var originalAutocomplete = $node.attr('autocomplete');
            $node.attr('autocomplete', 'off');
            var data = $.extend({
                $node: $node,
                $autocompleter: $autocompleter,
                $selected: null,
                $list: null,
                index: -1,
                hintText: false,
                source: false,
                jqxhr: false,
                response: null,
                focused: false,
                query: '',
                originalAutocomplete: originalAutocomplete,
                guid: guid++
            }, opts);
            data.$autocompleter.on('mousedown.autocompleter', '.autocompleter-item', data, _select)
                               .data('autocompleter', data);
            data.$node.on('keyup.autocompleter', data, _onKeyup)
                      .on('keydown.autocompleter', data, _onKeydown)
                      .on('focus.autocompleter', data, _onFocus)
                      .on('blur.autocompleter', data, _onBlur)
                      .on('mousedown.autocompleter', data, _onMousedown);
        }
    }
    function _search(query, source, data) {
        console.log("_search");
        var response = [];
        query = query.toUpperCase();
        if (source.length) {
            for (var i = 0; i < 2; i++) {
                for (var item in source) {
                    if (response.length < data.limit) {
                        var label = (data.customLabel && source[item][data.customLabel]) ? source[item][data.customLabel] : source[item].label;
                        switch (i) {
                        case 0:
                            if (label.toUpperCase().search(query) === 0) {
                                response.push(source[item]);
                                delete source[item];
                            }
                            break;
                        case 1:
                            if (label.toUpperCase().search(query) !== -1) {
                                response.push(source[item]);
                                delete source[item];
                            }
                            break;
                        }
                    }
                }
            }
        }
        return response;
    }
    function _launch(data) {
        clearTimeout(delayTimeout);
        data.query = $.trim(data.$node.val());
        if ((!data.empty && data.query.length === 0) || (data.minLength && (data.query.length < data.minLength))) {
            _clear(data);
            return;
        }
        if (data.delay) {
            delayTimeout = setTimeout(function () { _xhr(data); }, data.delay);
        } else {
            _xhr(data);
        }
    }
    function _xhr(data) {
        if (typeof data.source === 'object') {
            _clear(data);
            var search = _search(data.query, _clone(data.source), data);
            if (search.length) {
                _response(search, data);
            }
        } else {
            if (data.jqxhr) {
                data.jqxhr.abort();
            }
            var ajaxData = $.extend({
                limit: data.limit,
                query: data.query
            }, data.combine(data.query));
            data.jqxhr = $.ajax({
                url:        data.source,
                dataType:   'json',
                crossDomain: true,
                data:       ajaxData,
                beforeSend: function (xhr) {
                    data.$autocompleter.addClass('autocompleter-ajax');
                    _clear(data);
                    if (data.cache) {
                        var stored = _getCache(this.url, data.cacheExpires);
                        if (stored) {
                            xhr.abort();
                            _response(stored, data);
                        }
                    }
                }
            })
            .done(function (response) {
                if (data.offset) {
                    response = _grab(response, data.offset);
                }
                if (data.cache) {
                    _setCache(this.url, response);
                }
                _response(response, data);
            })
            .always(function () {
                data.$autocompleter.removeClass('autocompleter-ajax');
            });
        }
    }
    function _clear(data) {
        data.response = null;
        data.$list = null;
        data.$selected = null;
        data.index = 0;
        data.$autocompleter.find('.autocompleter-list').empty();
        data.$autocompleter.find('.autocompleter-hint').removeClass('autocompleter-hint-show').empty();
        data.hintText = false;
        _close(null, data);
    }
    function _response(response, data) {
        _buildList(response, data);
        if (data.$autocompleter.hasClass('autocompleter-focus')) {
            _open(null, data);
        }
    }
    function _buildList(list, data) {
        console.log("_buildList");
        console.log(list);
        console.log(data);
        var menu = '';
        for (var item = 0, count = list.length; item < count; item++) {
            var classes = ['autocompleter-item'],
                highlightReg = new RegExp(data.query, 'gi');
            if (data.selectFirst && item === 0 && !data.changeWhenSelect) {
                classes.push('autocompleter-item-selected');
            }
            var label = (data.customLabel && list[item][data.customLabel]) ? list[item][data.customLabel] : list[item].label,
                clear = label;
            label = data.highlightMatches ? label.replace(highlightReg, '<strong>$&</strong>') : label;
            var value = (data.customValue && list[item][data.customValue]) ? list[item][data.customValue] : list[item].value;
            if (data.template) {
                var template = data.template.replace(/({{ label }})/gi, label);
                for (var property in list[item]) {
                    if (list[item].hasOwnProperty(property)) {
                        var regex = new RegExp('{{ ' + property + ' }}', 'gi');
                        template = template.replace(regex, list[item][property]);
                    }
                }
                label = template;
            }
            if (value) {
                console.log("existe value");
                console.log(value);
                menu += '<li data-value="' + value + '" data-label="' + clear + '" class="' + classes.join(' ') + '">' + label + '</li>';
            } else {
                console.log("no existio value");
                menu += '<li data-label="' + clear + '" class="' + classes.join(' ') + '">' + label + '</li>';
            }
        }
        if (list.length && data.hint) {
            var hintLabel = (data.customLabel && list[0][data.customLabel]) ? list[0][data.customLabel] : list[0].label,
                hint = ( hintLabel.substr(0, data.query.length).toUpperCase() === data.query.toUpperCase() ) ? hintLabel : false;
            if (hint && (data.query !== hintLabel)) {
                var hintReg = new RegExp(data.query, 'i');
                var hintText = hint.replace(hintReg, '<span>' + data.query + '</span>');
                data.$autocompleter.find('.autocompleter-hint').addClass('autocompleter-hint-show').html(hintText);
                data.hintText = hintText;
            }
        }
        data.response = list;
        data.$autocompleter.find('.autocompleter-list').html(menu);
        data.$selected = (data.$autocompleter.find('.autocompleter-item-selected').length) ? data.$autocompleter.find('.autocompleter-item-selected') : null;
        data.$list = (list.length) ? data.$autocompleter.find('.autocompleter-item') : null;
        data.index = data.$selected ? data.$list.index(data.$selected) : -1;
        data.$autocompleter.find('.autocompleter-item').each(function (i, j) {
            $(j).data(data.response[i]);
        });
    }
    function _onKeyup(e) {
        var data = e.data,
            code = e.keyCode ? e.keyCode : e.which;
        if ( (code === 40 || code === 38) && data.$autocompleter.hasClass('autocompleter-show') ) {
            var len = data.$list.length,
                next,
                prev;
            if (len) {
                if (len > 1) {
                    if (data.index === len - 1) {
                        next = data.changeWhenSelect ? -1 : 0;
                        prev = data.index - 1;
                    } else if (data.index === 0) {
                        next = data.index + 1;
                        prev = data.changeWhenSelect ? -1 : len - 1;
                    } else if (data.index === -1) {
                        next = 0;
                        prev = len - 1;
                    } else {
                        next = data.index + 1;
                        prev = data.index - 1;
                    }
                } else if (data.index === -1) {
                    next = 0;
                    prev = 0;
                } else {
                    prev = -1;
                    next = -1;
                }
                data.index = (code === 40) ? next : prev;
                data.$list.removeClass('autocompleter-item-selected');
                if (data.index !== -1) {
                    data.$list.eq(data.index).addClass('autocompleter-item-selected');
                }
                data.$selected = data.$autocompleter.find('.autocompleter-item-selected').length ? data.$autocompleter.find('.autocompleter-item-selected') : null;
                if (data.changeWhenSelect) {
                    _setValue(data);
                }
            }
        } else if ($.inArray(code, ignoredKeyCode) === -1 && $.inArray(code, data.ignoredKeyCode) === -1) {
            _launch(data);
        }
    }
    function _onKeydown(e) {
        var data = e.data,
            code = e.keyCode ? e.keyCode : e.which;
        if (code === 40 || code === 38 ) {
            e.preventDefault();
            e.stopPropagation();
        } else if (code === 39) {
            if (data.hint && data.hintText && data.$autocompleter.find('.autocompleter-hint').hasClass('autocompleter-hint-show')) {
                e.preventDefault();
                e.stopPropagation();
                var hintOrigin = data.$autocompleter.find('.autocompleter-item').length ? data.$autocompleter.find('.autocompleter-item').eq(0).attr('data-label') : false;
                if (hintOrigin) {
                    data.query = hintOrigin;
                    _setHint(data);
                }
            }
        } else if (code === 13) {
            if (data.$autocompleter.hasClass('autocompleter-show') && data.$selected) {
                _select(e);
            }
        }
    }
    function _onFocus(e, internal) {
        if (!internal) {
            var data = e.data;
            data.$autocompleter.addClass('autocompleter-focus');
            if (!data.$node.prop('disabled') && !data.$autocompleter.hasClass('autocompleter-show')) {
                if (data.focusOpen) {
                    _launch(data);
                    data.focused = true;
                    setTimeout(function () {
                        data.focused = false;
                    }, 500);
                }
            }
        }
    }
    function _onBlur(e, internal) {
        e.preventDefault();
        e.stopPropagation();
        var data = e.data;
        if (!internal) {
            data.$autocompleter.removeClass('autocompleter-focus');
            _close(e);
        }
    }
    function _onMousedown(e) {
        if (e.type === 'mousedown' && $.inArray(e.which, [2, 3]) !== -1) { return; }
        var data = e.data;
        if (data.$list && !data.focused) {
            if (!data.$node.is(':disabled')) {
                if (isMobile && !isFirefoxMobile) {
                    var el = data.$select[0];
                    if (window.document.createEvent) { // All
                        var evt = window.document.createEvent('MouseEvents');
                        evt.initMouseEvent('mousedown', false, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
                        el.dispatchEvent(evt);
                    } else if (el.fireEvent) { // IE
                        el.fireEvent('onmousedown');
                    }
                } else {
                    if (data.$autocompleter.hasClass('autocompleter-closed')) {
                        _open(e);
                    } else if (data.$autocompleter.hasClass('autocompleter-show')) {
                        _close(e);
                    }
                }
            }
        }
    }
    function _open(e, instanceData) {
        var data = e ? e.data : instanceData;
        if (!data.$node.prop('disabled') && !data.$autocompleter.hasClass('autocompleter-show') && data.$list && data.$list.length) {
            data.$autocompleter.removeClass('autocompleter-closed').addClass('autocompleter-show');
            $body.on('click.autocompleter-' + data.guid, ':not(.autocompleter-item)', data, _closeHelper);
        }
    }
    function _closeHelper(e) {
        if ( $(e.target).hasClass('autocompleter-node') ) {
            return;
        }
        if ($(e.currentTarget).parents('.autocompleter').length === 0) {
            _close(e);
        }
    }
    function _close(e, instanceData) {
        var data = e ? e.data : instanceData;
        if (data.$autocompleter.hasClass('autocompleter-show')) {
            data.$autocompleter.removeClass('autocompleter-show').addClass('autocompleter-closed');
            $body.off('.autocompleter-' + data.guid);
        }
    }
    function _select(e) {
        if (e.type === 'mousedown' && $.inArray(e.which, [2, 3]) !== -1) {
            return;
        }
        var data = e.data;
        e.preventDefault();
        e.stopPropagation();
        if (e.type === 'mousedown' && $(this).length) {
            data.$selected = $(this);
            data.index = data.$list.index(data.$selected);
        }
        if (!data.$node.prop('disabled')) {
            _close(e);
            _update(data);
            if (e.type === 'click') {
                data.$node.trigger('focus', [ true ]);
            }
        }
    }
    function _setHint(data) {
        _setValue(data);
        _handleChange(data);
        _launch(data);
    }
    function _setValue(data) {
        if (data.$selected) {
            if (data.hintText && data.$autocompleter.find('.autocompleter-hint').hasClass('autocompleter-hint-show')) {
                data.$autocompleter.find('.autocompleter-hint').removeClass('autocompleter-hint-show');
            }
            data.$node.val(data.$selected.attr('data-value') ? data.$selected.attr('data-value') : data.$selected.attr('data-label'));
        } else {
            if (data.hintText && !data.$autocompleter.find('.autocompleter-hint').hasClass('autocompleter-hint-show')) {
                data.$autocompleter.find('.autocompleter-hint').addClass('autocompleter-hint-show');
            }
            data.$node.val(data.query);
        }
    }
    function _update(data) {
        _setValue(data);
        _handleChange(data);
        _clear(data);
    }
    function _handleChange(data) {
        console.log("_handleChange");
        data.callback.call(data.$autocompleter, data.$node.val(), data.index, data.response[data.index]);
        data.$node.trigger('change');
    }
    function _grab(response, offset) {
        offset = offset.split('.');
        while (response && offset.length) {
            response = response[offset.shift()];
        }
        return response;
    }
    function _setCache(url, data) {
        if (!supportLocalStorage) {
            return;
        }
        if (url && data) {
            cache[url] = {
                value: data,
                timestamp: +new Date()
            };
            try {
                localStorage.setItem(localStorageKey, JSON.stringify(cache));
            } catch (e) {
                var code = e.code || e.number || e.message;
                if (code === 22) {
                    _deleteCache();
                } else {
                    throw(e);
                }
            }
        }
    }
    function _getCache(url, expires) {
        var response = false,
            item;
        expires = expires || false;
        if (!url) {
            return false;
        }
        item = cache[url];
        if (item && item.value) {
            response = item.value;
            if (item.timestamp && expires && (+new Date() - item.timestamp > expires * 1000)) {
                return false;
            } else {
                return response;
            }
        } else {
            return false;
        }
    }
    function _loadCache() {
        if (!supportLocalStorage) {
            return;
        }
        return JSON.parse(localStorage.getItem(localStorageKey) || '{}');
    }
    function _deleteCache() {
        try {
            localStorage.removeItem(localStorageKey);
            cache = _loadCache();
        } catch (e) {
            throw(e);
        }
    }
    function _clone(obj) {
        var copy;
        if (null === obj || 'object' !== typeof obj) {
            return obj;
        }
        copy = obj.constructor();
        for (var attr in obj) {
            if (obj.hasOwnProperty(attr)) {
                copy[attr] = obj[attr];
            }
        }
        return copy;
    }
    var cache = _loadCache();
    $.fn.autocompleter = function (method) {
        if (publics[method]) {
            return publics[method].apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (typeof method === 'object' || !method) {
            return _init.apply(this, arguments);
        }
        return this;
    };
    $.autocompleter = function (method) {
        if (method === 'defaults') {
            publics.defaults.apply(this, Array.prototype.slice.call(arguments, 1));
        } else if (method === 'clearCache') {
            publics.clearCache.apply(this, null);
        }
    };
})(jQuery, window);
