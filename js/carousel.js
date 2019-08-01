let slideIndex = 0;
let carousel = document.querySelector('.about_surround');
let slides = document.querySelectorAll('.item');
// let buttons = document.querySelectorAll('.about_surround button');
//
// const addButtonDisableListeners = (el, eventName, disabled) => {
//   el.addEventListener(eventName, () => {
//     for (let button of buttons) {
//       button.disabled = disabled;
//     }
//   });
// };

const showSlide = (delta=0) => {
  slideIndex += slides.length + delta;
  slideIndex %= slides.length;

  for (let slide of slides) {
    slide.classList.remove('left');
    slide.classList.remove('right');
    slide.classList.remove('active');
    slide.classList.add('inactive');
  }

  slides[slideIndex].classList.add('active');
  slides[slideIndex].classList.remove('inactive');

  let leftIndex = (slideIndex + slides.length - 1) % slides.length;
  let rightIndex = (slideIndex + slides.length + 1) % slides.length;
  slides[leftIndex].classList.add('left');
  slides[rightIndex].classList.add('right');
};

// for (let slide of slides) {
//   addButtonDisableListeners(slide, 'transitionrun', true);
//   addButtonDisableListeners(slide, 'transitionend', false);
// }

carousel.addEventListener('keydown', (e) => {
  if (e.key === "ArrowRight") {
    showSlide(1);
  } else if (e.key === "ArrowLeft") {
    showSlide(-1);
  }
});

showSlide();
