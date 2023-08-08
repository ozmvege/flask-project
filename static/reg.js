/**
 *  Light Switch @version v0.1.4
 */

(function () {
    let lightSwitch = document.getElementById('lightSwitch');
    if (!lightSwitch) {
        return;
    }

    /**
     * @function darkMode
     * @summary: changes the theme to 'dark mode' and save settings to local storage.
     * Basically, replaces/toggles every CSS class that has '-light' class with '-dark'
     */
    function darkMode() {
        document.querySelectorAll('.bg-light').forEach((element) => {
            element.classList.replace('bg-light', 'bg-dark');
        });

        document.querySelectorAll('.text-dark').forEach((element) => {
            element.classList.replace('text-dark', 'text-light');
        });

        document.querySelectorAll('.card').forEach((element) => {
            element.classList.add('cg-dark');
            element.classList.remove('cg-light');
        });

        // Body
        document.body.classList.add('bg-dark');
        document.body.classList.remove('bg-light');
        if (document.body.classList.contains('text-dark')) {
            document.body.classList.replace('text-dark', 'text-light');
        } else {
            document.body.classList.add('text-light');
        }

        // Tables
        var tables = document.querySelectorAll('table');
        for (var i = 0; i < tables.length; i++) {
            // add table-dark class to each table
            tables[i].classList.add('table-dark');
        }

        // set light switch input to true
        if (!lightSwitch.checked) {
            lightSwitch.checked = true;
        }
        localStorage.setItem('lightSwitch', 'dark');
    }

    /**
     * @function lightMode
     * @summary: changes the theme to 'light mode' and save settings to local storage.
     */
    function lightMode() {
        document.querySelectorAll('.bg-dark').forEach((element) => {
            element.classList.replace('bg-dark', 'bg-light');
        });

        document.querySelectorAll('.text-light').forEach((element) => {
            element.classList.replace('text-light', 'text-dark');
        });

        document.querySelectorAll('.card').forEach((element) => {
            element.classList.add('cg-light');
            element.classList.remove('cg-dark');
        });

        // Body
        document.body.classList.add('bg-light');
        document.body.classList.remove('bg-dark');
        if (document.body.classList.contains('text-light')) {
            document.body.classList.replace('text-light', 'text-dark');
        } else {
            document.body.classList.add('text-dark');
        }

        // Tables
        var tables = document.querySelectorAll('table');
        for (var i = 0; i < tables.length; i++) {
            if (tables[i].classList.contains('table-dark')) {
                tables[i].classList.remove('table-dark');
            }
        }

        if (lightSwitch.checked) {
            lightSwitch.checked = false;
        }
        localStorage.setItem('lightSwitch', 'light');
    }

    /**
     * @function onToggleMode
     * @summary: the event handler attached to the switch. calling @darkMode or @lightMode depending on the checked state.
     */
    function onToggleMode() {
        if (lightSwitch.checked) {
            darkMode();
        } else {
            lightMode();
        }
    }

    /**
     * @function getSystemDefaultTheme
     * @summary: get system default theme by media query
     */
    function getSystemDefaultTheme() {
        const darkThemeMq = window.matchMedia('(prefers-color-scheme: dark)');
        if (darkThemeMq.matches) {
            return 'dark';
        }
        return 'light';
    }

    function setup() {
        var settings = localStorage.getItem('lightSwitch');
        if (settings == null) {
            settings = getSystemDefaultTheme();
        }

        if (settings == 'dark') {
            lightSwitch.checked = true;
        }

        lightSwitch.addEventListener('change', onToggleMode);
        onToggleMode();
    }

    setup();
})();
