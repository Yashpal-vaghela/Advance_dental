document.addEventListener("DOMContentLoaded", function () {
    var smileStorySwiper = new Swiper(".smile-story-swiper", {
        loop: true, 
        speed: 4000,
        slidesPerView: "auto", 
        spaceBetween: 20,
        autoplay: {
            delay: 0, 
            disableOnInteraction: false,
        },
        grabCursor: true,
        freeMode: {
            enabled: true,
            momentum: false,
        },
        allowTouchMove: true,
        breakpoints: {
            0: {
                spaceBetween: 20,
            },
            576: {
                spaceBetween: 20,
            },
            993: {
                spaceBetween: 20,
            },
        },
        on: {
            touchEnd: function (swiper) {
                setTimeout(function () {
                    if (swiper && swiper.autoplay) {
                        swiper.autoplay.start();
                    }
                }, 0);
            },
        },
    }); 
});