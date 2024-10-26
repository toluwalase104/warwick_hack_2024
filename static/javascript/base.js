document.addEventListener('DOMContentLoaded', function () {
    AOS.init();

    function initVanta() {
        if (window.vantaEffect) {
            window.vantaEffect.destroy(); 
        }

        var fullPage = document.body; // Target the entire body or full-screen container

        // Ensure dimensions are accurate before initializing VANTA
        var width = window.innerWidth;
        var height = window.innerHeight;

        if (window.innerWidth > 576) {
            fullPage.style.backgroundColor = 'transparent';

            // Use requestAnimationFrame to ensure proper initialization
            window.requestAnimationFrame(function() {
                window.vantaEffect = VANTA.GLOBE({
                    el: fullPage,
                    mouseControls: true,
                    touchControls: true,
                    gyroControls: false,
                    minHeight: height,
                    minWidth: width,
                    scale: 1.00,
                    scaleMobile: 1.00,
                    color: 0x20dbdb,
                    color2: 0xededed,
                    size: 2.00,
                    backgroundColor: 0x5e7c4c
                });
            });
        } else {
            fullPage.style.backgroundColor = '#5e7c4c';
            if (window.vantaEffect) {
                window.vantaEffect.destroy();
            }
        }
    }

    initVanta();

    window.addEventListener('resize', function() {
        initVanta(); // Reinitialize VANTA effect on resize
    });

    // Initialize on window load to ensure all layout is complete
    window.addEventListener('load', function() {
        initVanta();
    });
});
