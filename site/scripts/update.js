async function update() {
    try {
        const r = await fetch('/state.json', { cache: 'no-store' });
        const data = await r.json();
        document.getElementById('grocery').innerHTML = data.grocery;
        document.getElementById('daysold').innerHTML = data.daysold;
        document.getElementById('martin').innerHTML = data.martin;
        document.getElementById('izzy').innerHTML = data.izzy;
        document.getElementById('upcoming').innerHTML = data.upcoming;
    } catch { }
}

update();
setInterval(update, 10000);