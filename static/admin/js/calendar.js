(function() {
    'use strict';
    var CalendarNamespace = {
        monthsOfYear: gettext('January February March April May June July August September October November December').split(' '),
        daysOfWeek: gettext('S M T W T F S').split(' '),
        firstDayOfWeek: parseInt(get_format('FIRST_DAY_OF_WEEK')),
        isLeapYear: function(year) {
            return (((year % 4) === 0) && ((year % 100) !== 0 ) || ((year % 400) === 0));
        },
        getDaysInMonth: function(month, year) {
            var days;
            if (month === 1 || month === 3 || month === 5 || month === 7 || month === 8 || month === 10 || month === 12) {
                days = 31;
            }
            else if (month === 4 || month === 6 || month === 9 || month === 11) {
                days = 30;
            }
            else if (month === 2 && CalendarNamespace.isLeapYear(year)) {
                days = 29;
            }
            else {
                days = 28;
            }
            return days;
        },
        draw: function(month, year, div_id, callback, selected) { // month = 1-12, year = 1-9999
            var today = new Date();
            var todayDay = today.getDate();
            var todayMonth = today.getMonth() + 1;
            var todayYear = today.getFullYear();
            var todayClass = '';
            var isSelectedMonth = false;
            if (typeof selected !== 'undefined') {
                isSelectedMonth = (selected.getUTCFullYear() === year && (selected.getUTCMonth() + 1) === month);
            }
            month = parseInt(month);
            year = parseInt(year);
            var calDiv = document.getElementById(div_id);
            removeChildren(calDiv);
            var calTable = document.createElement('table');
            quickElement('caption', calTable, CalendarNamespace.monthsOfYear[month - 1] + ' ' + year);
            var tableBody = quickElement('tbody', calTable);
            var tableRow = quickElement('tr', tableBody);
            for (var i = 0; i < 7; i++) {
                quickElement('th', tableRow, CalendarNamespace.daysOfWeek[(i + CalendarNamespace.firstDayOfWeek) % 7]);
            }
            var startingPos = new Date(year, month - 1, 1 - CalendarNamespace.firstDayOfWeek).getDay();
            var days = CalendarNamespace.getDaysInMonth(month, year);
            var nonDayCell;
            tableRow = quickElement('tr', tableBody);
            for (i = 0; i < startingPos; i++) {
                nonDayCell = quickElement('td', tableRow, ' ');
                nonDayCell.className = "nonday";
            }
            var currentDay = 1;
            for (i = startingPos; currentDay <= days; i++) {
                if (i % 7 === 0 && currentDay !== 1) {
                    tableRow = quickElement('tr', tableBody);
                }
                if ((currentDay === todayDay) && (month === todayMonth) && (year === todayYear)) {
                    todayClass = 'today';
                } else {
                    todayClass = '';
                }
                if (isSelectedMonth && currentDay === selected.getUTCDate()) {
                    if (todayClass !== '') {
                        todayClass += " ";
                    }
                    todayClass += "selected";
                }
                var cell = quickElement('td', tableRow, '', 'class', todayClass);
                quickElement('a', cell, currentDay, 'href', 'javascript:void(' + callback + '(' + year + ',' + month + ',' + currentDay + '));');
                currentDay++;
            }
            while (tableRow.childNodes.length < 7) {
                nonDayCell = quickElement('td', tableRow, ' ');
                nonDayCell.className = "nonday";
            }
            calDiv.appendChild(calTable);
        }
    };
    function Calendar(div_id, callback, selected) {
        this.div_id = div_id;
        this.callback = callback;
        this.today = new Date();
        this.currentMonth = this.today.getMonth() + 1;
        this.currentYear = this.today.getFullYear();
        if (typeof selected !== 'undefined') {
            this.selected = selected;
        }
    }
    Calendar.prototype = {
        drawCurrent: function() {
            CalendarNamespace.draw(this.currentMonth, this.currentYear, this.div_id, this.callback, this.selected);
        },
        drawDate: function(month, year, selected) {
            this.currentMonth = month;
            this.currentYear = year;
            if(selected) {
                this.selected = selected;
            }
            this.drawCurrent();
        },
        drawPreviousMonth: function() {
            if (this.currentMonth === 1) {
                this.currentMonth = 12;
                this.currentYear--;
            }
            else {
                this.currentMonth--;
            }
            this.drawCurrent();
        },
        drawNextMonth: function() {
            if (this.currentMonth === 12) {
                this.currentMonth = 1;
                this.currentYear++;
            }
            else {
                this.currentMonth++;
            }
            this.drawCurrent();
        },
        drawPreviousYear: function() {
            this.currentYear--;
            this.drawCurrent();
        },
        drawNextYear: function() {
            this.currentYear++;
            this.drawCurrent();
        }
    };
    window.Calendar = Calendar;
})();
