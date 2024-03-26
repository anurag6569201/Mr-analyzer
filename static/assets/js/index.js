const icons = document.querySelectorAll('.info-btn');
const infoData = document.querySelectorAll('.info-data');

icons.forEach(icon => {
    icon.addEventListener('click', () => {
        const infoToShow = document.querySelector(`.${icon.dataset.info}`);
        infoData.forEach(info => info.classList.remove('active'));
        icons.forEach(icon => icon.classList.remove('active-btn'));
        icon.classList.add('active-btn');
        infoToShow.classList.add('active');
    });
});