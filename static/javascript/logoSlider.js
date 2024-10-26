document.addEventListener("DOMContentLoaded", function() {
    function initializeSlider(sliderId, prevBtnId, nextBtnId) {
      const slider = document.getElementById(sliderId);
      const items = slider.querySelectorAll('.logoItem');
      let currentIndex = 0;
      let autoSlideInterval;
  
      // Function to update the slider
      function updateSlider() {
        items.forEach((item, index) => {
          const totalItems = items.length;
          let distance = (index - currentIndex + totalItems) % totalItems;
  
          if (distance === 0) {
            item.style.transform = 'translateX(0) scale(1.1)';
            item.style.zIndex = 5;
            item.style.opacity = '1';
            item.style.filter = 'blur(0)';
          } else if (distance === 1 || distance === totalItems - 1) {
            const offset = distance === 1 ? 200 : -200;
            item.style.transform = `translateX(${offset}px) scale(0.9)`;
            item.style.zIndex = 4;
            item.style.opacity = '0.85';
            item.style.filter = 'blur(0.5px)';
          } else if (distance === 2 || distance === totalItems - 2) {
            const offset = distance === 2 ? 400 : -400;
            item.style.transform = `translateX(${offset}px) scale(0.8)`;
            item.style.zIndex = 3;
            item.style.opacity = '0.7';
            item.style.filter = 'blur(1px)';
          } else if (distance === 3 || distance === totalItems - 3) {
            const offset = distance === 3 ? 600 : -600;
            item.style.transform = `translateX(${offset}px) scale(0.7)`;
            item.style.zIndex = 2;
            item.style.opacity = '0.6';
            item.style.filter = 'blur(2px)';
          } else if (distance === 4 || distance === totalItems - 4) {
            const offset = distance === 4 ? 800 : -800;
            item.style.transform = `translateX(${offset}px) scale(0.6)`;
            item.style.zIndex = 1;
            item.style.opacity = '0.5';
            item.style.filter = 'blur(3px)';
          } else {
            item.style.transform = 'translateX(-1000px)';
            item.style.opacity = '0';
            item.style.filter = 'blur(5px)';
          }
        });
      }
  
      // Function to go to the next slide
      function goToNextSlide() {
        currentIndex = (currentIndex + 1) % items.length;
        updateSlider();
      }
  
      // Set an interval for automatic sliding (2 seconds)
      function startAutoSlide() {
        autoSlideInterval = setInterval(goToNextSlide, 2000); 
      }
  
      // Function to stop the automatic slider
      function stopAutoSlide() {
        clearInterval(autoSlideInterval);
      }
  
      // Next button click handler
      document.getElementById(nextBtnId).addEventListener('click', () => {
        stopAutoSlide(); 
        goToNextSlide();
        startAutoSlide(); 
      });
  
      // Previous button click handler
      document.getElementById(prevBtnId).addEventListener('click', () => {
        stopAutoSlide();  
        currentIndex = (currentIndex - 1 + items.length) % items.length;
        updateSlider();
        startAutoSlide();  
      });
  
      // Initialise the slider and start the automatic sliding
      updateSlider();
      startAutoSlide();
    }
  
    // Initialize both sliders
    initializeSlider('sponsorSlider', 'logoPrevSponsor', 'logoNextSponsor');
    initializeSlider('collabSlider', 'logoPrevCollab', 'logoNextCollab');
});