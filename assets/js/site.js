const search = document.querySelector('#schedule-search');

if (search) {
    const cards = [...document.querySelectorAll('.searchable')];
    search.addEventListener('input', () => {
        const q = search.value.trim().toLowerCase();
        for (const card of cards) {
            card.classList.toggle('is-hidden', q && !card.textContent.toLowerCase().includes(q));
        }
        for (const week of document.querySelectorAll('.week')) {
            const visible = week.querySelector('.searchable:not(.is-hidden)');
            week.classList.toggle('is-hidden', q && !visible);
        }
    });
}

for (const a of document.querySelectorAll('a[target="_blank"]')) {
    a.title = a.title || 'Opens in a new tab';
}
