const slider = document.querySelector('.slider');

function activate(e) {
  const items = document.querySelectorAll('.item');
  if (e.target.matches('.next')) {
    slider.append(items[0]);
  } else if (e.target.matches('.prev')) {
    slider.prepend(items[items.length - 1]);
  }
}

document.addEventListener('click', activate, false);

function autoSlide() {
  const items = document.querySelectorAll('.item');
  slider.append(items[0]);
}

// Set an interval to auto-slide every 5 seconds
setInterval(autoSlide, 5000);