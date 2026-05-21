function applyHeadingOverrides() {
    const style = getComputedStyle(document.documentElement);
    const sections = ['grocery', 'daysold', 'martin', 'izzy', 'upcoming'];
    for (const id of sections) {
        const val = style.getPropertyValue(`--heading-${id}`).trim().replace(/^["']|["']$/g, '');
        if (!val) continue;
        const el = document.getElementById(id);
        const h1 = el?.querySelector('h1');
        if (h1) h1.textContent = val;
    }
}

async function update() {
    try {
        const r = await fetch('/state.json', { cache: 'no-store' });
        const data = await r.json();
        document.getElementById('grocery').innerHTML = data.grocery;
        document.getElementById('daysold').innerHTML = data.daysold;
        document.getElementById('martin').innerHTML = data.martin;
        document.getElementById('izzy').innerHTML = data.izzy;
        document.getElementById('upcoming').innerHTML = data.upcoming;
        applyHeadingOverrides();
    } catch { }
}

update();
setInterval(update, 10000);
