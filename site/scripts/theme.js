(function () {
    const themes = [
        'amleth',
        'houston',
        'muthur',
        'yeolde',
    ];

    const theme = themes[Math.floor(Math.random() * themes.length)];

    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = `./style/${theme}.css`;
    document.head.appendChild(link);
})();
