if (history.scrollRestoration) {
    history.scrollRestoration = 'manual';
}
window.scrollTo(0, 0);
let currentWidth = window.innerWidth;

window.addEventListener('resize', () => {
    if (window.innerWidth !== currentWidth) {
        window.scrollTo(0, 0);
        location.reload();
    }
});

 // Card Marquee (Clone logic)
document.addEventListener("DOMContentLoaded", () => {
   
    const cardSection = document.querySelector('.card_section');
    if (cardSection && !cardSection.querySelector('.marquee-content')) {
        const cardsHTML = cardSection.innerHTML;
        cardSection.innerHTML =
        `<div class="marquee-content">${cardsHTML}</div>
         <div class="marquee-content clone" aria-hidden="true">${cardsHTML}</div>`;
    }

    if (typeof gsap === 'undefined') {
        return;
    }

    gsap.registerPlugin(ScrollTrigger);
    // ==========================================
    // ANIMATION 1: Premium Banner Section
    // ==========================================
    const banners = gsap.utils.toArray('.banner');
    const bannerSection = document.querySelector('.premium_banner_section');

    if (banners.length > 0 && bannerSection) {
        const total = banners.length;

        banners.forEach((banner, index) => {
            gsap.set(banner, {
                clipPath: 'inset(0% 0% 0% 0%)',
                zIndex: total - index,
                visibility: 'visible',
                opacity: 1
            });
        });

        const bannerTl = gsap.timeline({
            scrollTrigger: {
                trigger: bannerSection,
                start: 'top 60px',
                end: () => `+=${(banners.length - 1) * 100}%`,
                pin: true,
                scrub: 2.5,
                invalidateOnRefresh: true,
                anticipatePin: 1,
                // markers: true // Debug lines
            }
        });

        banners.forEach((banner, index) => {
            if (index === 0) return;
            bannerTl.fromTo(banners[index - 1],
                { clipPath: 'inset(0% 0% 0% 0%)' },
                { clipPath: 'inset(0% 0% 100% 0%)',
                  ease: 'none',
                  duration: 1 },
                  index - 1
            );
        });
    }
    // ==========================================
    // ANIMATION 2: Enhance Your Smile Bubbles
    // ==========================================
    const bubbleOrder = [".bubble-3", ".bubble-5", ".bubble-1", ".bubble-4", ".bubble-6", ".bubble-2"];
    const bubbleContainer = document.querySelector(".enhance_your_smile_small_screen");

    if (bubbleContainer) {
        gsap.set(bubbleOrder, {
            y: -1200,
            opacity: 0
        });

        ScrollTrigger.create({
            trigger: bubbleContainer,
            start: "top 30%",
            onEnter: () => {
                bubbleOrder.forEach((selector, index) => {
                    gsap.to(selector, {
                        y: 0,
                        opacity: 1,
                        duration: 1.5,
                        ease: "bounce.out",
                        delay: index * 0.2,
                        overwrite: "auto"
                    });
                });
            },
            onLeaveBack: () => {
                bubbleOrder.forEach((selector, index) => {
                    gsap.to(selector, {
                        y: -1200,
                        opacity: 0,
                        duration: 0.8,
                        ease: "power2.in",
                        delay: index * 0.1,
                        overwrite: "auto"
                    });
                });
            }
        });
    }

    // ==========================================
    // ANIMATION 3: Clientele Section
    // ==========================================

    // const items = gsap.utils.toArray('.clientele_item');
    // const list = document.querySelector('.clientele_list');

    // if (items.length > 0 && list) {
    //     items.forEach((item, index) => {
    //         const wrapper = item.querySelector('.clientele_vector_wrapper');
    //         const svg = item.querySelector('.clientele_vector');
    //         if (svg && wrapper && !wrapper.querySelector('.clientele_vector_inactive')) {
    //             const inactiveSvg = svg.cloneNode(true);
    //             inactiveSvg.classList.remove('clientele_vector');
    //             inactiveSvg.classList.add('clientele_vector_inactive');
    //             wrapper.appendChild(inactiveSvg);
    //             gsap.set(svg, { clipPath: index === 0 ? 'inset(0% 0% 0% 0%)' : 'inset(0% 100% 0% 0%)' });
    //         }
    //     });

    //     let currentActiveIndex = 0;
    //     let clienteleTl = gsap.timeline({
    //         scrollTrigger: {
    //             trigger: '.clientele_section',
    //             pin: true,
    //             start: 'top 10%',
    //             end: '+=150%',
    //             scrub: 1,
    //             invalidateOnRefresh: true,
    //             onUpdate: (self) => {
    //                 const newActiveIndex = Math.min(items.length - 1, Math.floor(self.progress * items.length));
    //                 if (newActiveIndex !== currentActiveIndex) {
    //                     const oldSvg = items[currentActiveIndex]?.querySelector('.clientele_vector');
    //                     const newSvg = items[newActiveIndex]?.querySelector('.clientele_vector');
    //                     if (oldSvg) gsap.to(oldSvg, { clipPath: 'inset(0% 0% 0% 100%)', duration: 0.8, overwrite: 'auto' });
    //                     if (newSvg) gsap.fromTo(newSvg, { clipPath: 'inset(0% 100% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1.5, overwrite: 'auto' });
    //                     items.forEach((item, i) => i === newActiveIndex ? item.classList.add('active') : item.classList.remove('active'));
    //                     currentActiveIndex = newActiveIndex;
    //                 }
    //             }
    //         }
    //     });

    //     clienteleTl.to(list, {
    //         y: () => -(items[items.length - 1].offsetTop),
    //         ease: 'none'
    //     });
    // }

    // gsap.to('.clientele_vector_wrapper', {
    //     y: -12, duration: 2, repeat: -1, yoyo: true, ease: 'sine.inOut',
    // });
    
    const items = gsap.utils.toArray('.clientele_item');
    const list = document.querySelector('.clientele_list');

    if (items.length > 0 && list) {
        items.forEach((item, index) => {
            const wrapper = item.querySelector('.clientele_vector_wrapper');
            const svg = item.querySelector('.clientele_vector');

            if (svg && wrapper && !wrapper.querySelector('.clientele_vector_inactive')) {
                const inactiveSvg = svg.cloneNode(true);
                inactiveSvg.classList.remove('clientele_vector');
                inactiveSvg.classList.add('clientele_vector_inactive');
                wrapper.appendChild(inactiveSvg);

                // gsap.set(svg, {
                //     clipPath: index === 0
                //         ? 'inset(0% 0% 0% 0%)'
                //         : 'inset(0% 100% 0% 0%)'
                // });
            }
            // Ensure videos don't loop
            const video = item.querySelector('video');
            if (video) {
                gsap.set(video, {
                    opacity: index === 0 ? 1 : 0.5
                });
                video.pause();
                video.currentTime = 0;
                video.removeAttribute('loop');
            }
        });

        let currentActiveIndex = 0;

        //Play first video initially
        const firstVideo = items[0]?.querySelector('video');
        if (firstVideo) {
            firstVideo.play().catch(() => { });
        }

        let clienteleTl = gsap.timeline({
            scrollTrigger: {
                trigger: '.clientele_section',
                pin: true,
                start: 'top 10%',
                end: '+=150%',
                scrub: 1,
                invalidateOnRefresh: true,

                onUpdate: (self) => {
                    const newActiveIndex = Math.min(
                        items.length - 1,
                        Math.floor(self.progress * items.length)
                    );

                    if (newActiveIndex !== currentActiveIndex) {
                        const oldItem = items[currentActiveIndex];
                        const newItem = items[newActiveIndex];
                        const oldVideo = oldItem?.querySelector('video');
                        const newVideo = newItem?.querySelector('video');
                        //Stop & reset old video
                        if (oldVideo) {
                            oldVideo.pause();
                            oldVideo.currentTime = 0;
                            gsap.to(oldVideo, {
                                opacity: 0.1,
                                // duration: 0.5
                            });
                        }
                        // Play new video once
                        if (newVideo) {
                            newVideo.currentTime = 0;
                            newVideo.play().catch(() => { });
                            gsap.to(newVideo, {
                                opacity: 1,
                                // duration: 0.5
                            });
                        }
                        //SVG / clip animation
                        const oldSvg = oldItem?.querySelector('.clientele_vector');
                        const newSvg = newItem?.querySelector('.clientele_vector');
                        // if (oldSvg) {
                        //     gsap.to(oldSvg, {
                        //         clipPath: 'inset(0% 0% 0% 100%)',
                        //         duration: 0.8,
                        //         overwrite: 'auto'
                        //     });
                        // }

                        // if (newSvg) {
                        //     gsap.fromTo(newSvg,
                        //         { clipPath: 'inset(0% 100% 0% 0%)' },
                        //         { clipPath: 'inset(0% 0% 0% 0%)',
                        //           duration: 1.5,
                        //           overwrite: 'auto'
                        //         }
                        //     );
                        // }
                        // Active class update
                        items.forEach((item, i) => {
                            item.classList.toggle('active', i === newActiveIndex);
                        });
                        currentActiveIndex = newActiveIndex;
                    }
                }
            }
        });

        // Scroll movement
        clienteleTl.to(list, {
            y: () => {
                let maxScroll = list.scrollHeight - list.parentElement.clientHeight;
                return maxScroll > 0 ? -maxScroll : 0;
            },
            ease: 'none'
        });
    }
});

window.addEventListener("load", () => {
    if (typeof ScrollTrigger !== 'undefined') {
        ScrollTrigger.refresh();
    }
});