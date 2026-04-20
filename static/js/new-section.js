document.addEventListener("DOMContentLoaded", () => {
    gsap.registerPlugin(ScrollTrigger);

    const cardSection = document.querySelector('.card_section');
    if (cardSection) {
        const cardsHTML = cardSection.innerHTML;
        cardSection.innerHTML = `
            <div class="marquee-content">${cardsHTML}</div>
            <div class="marquee-content clone" aria-hidden="true">${cardsHTML}</div>
        `;
    }

    // ==========================================
    // ANIMATION 1: Premium Banner Section (TOP)
    // ==========================================
    const banners = gsap.utils.toArray('.banner');
    if (banners.length > 0) {
        const total = banners.length;

        banners.forEach((banner, index) => {
            gsap.set(banner, {
                clipPath: 'inset(0% 0% 0% 0%)',
                zIndex: total - index
            });
        });

        const bannerTl = gsap.timeline({
            scrollTrigger: {
                trigger: '.premium_banner_section',
                start: 'top 60px',
                end: () => `+=${(banners.length - 1) * 100}%`,
                pin: true,
                scrub: 2.5,
            }
        });

        banners.forEach((banner, index) => {
            if (index === 0) return;
            const prevBanner = banners[index - 1];
            const startTime = index - 1;

            bannerTl.to(prevBanner, {
                clipPath: 'inset(0% 0% 100% 0%)',
                ease: 'none',
                duration: 1
            }, startTime);
        });
    }
    // ==========================================
    // ANIMATION 2: Enhance Your Smile Bubbles (MIDDLE)
    // ==========================================
    const bubbleOrder = [".bubble-3", ".bubble-5", ".bubble-1", ".bubble-4", ".bubble-6", ".bubble-2"];

    if (document.querySelector(".enhance_your_smile_small_screen")) {

        bubbleOrder.forEach(selector => {
            gsap.set(selector, { y: -1200, opacity: 0 });
        });

        ScrollTrigger.create({
            trigger: ".enhance_your_smile_small_screen",
            start: "top 30%",
            onEnter: () => {
                bubbleOrder.forEach((selector, index) => {
                    gsap.to(selector, {
                        y: 0,
                        opacity: 1,
                        duration: 1.5,
                        ease: "bounce.out",
                        delay: index * 0.2
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
                        delay: index * 0.1
                    });
                });
            }
        });
    }

    // ==========================================
    // ANIMATION 3: Clientele Section (BOTTOM)
    // ==========================================
    gsap.to('.clientele_vector_wrapper', {
        y: -12,
        duration: 2,
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut',
    });

    const items = gsap.utils.toArray('.clientele_item');
    const list = document.querySelector('.clientele_list');

    if (items.length > 0 && list) {
        items.forEach((item, index) => {
            const wrapper = item.querySelector('.clientele_vector_wrapper');
            const svg = item.querySelector('.clientele_vector');

            if (svg && wrapper) {
                const inactiveSvg = svg.cloneNode(true);
                inactiveSvg.classList.remove('clientele_vector');
                inactiveSvg.classList.add('clientele_vector_inactive');
                wrapper.appendChild(inactiveSvg);

                if (index !== 0) {
                    gsap.set(svg, { clipPath: 'inset(0% 100% 0% 0%)' });
                } else {
                    gsap.set(svg, { clipPath: 'inset(0% 0% 0% 0%)' });
                }
            }

            if (index === 0) item.classList.add('active');
            else item.classList.remove('active');
        });

        const lastItem = items[items.length - 1];
        const maxScroll = lastItem.offsetTop;
        let currentActiveIndex = 0;

        let clienteleTl = gsap.timeline({
            scrollTrigger: {
                trigger: '.clientele_section',
                pin: true,
                start: 'top 10%',
                end: '+=150%',
                scrub: 1,
                onUpdate: (self) => {
                    const progress = self.progress;
                    const newActiveIndex = Math.min(items.length - 1, Math.floor(progress * items.length));

                    if (newActiveIndex !== currentActiveIndex) {
                        const oldItem = items[currentActiveIndex];
                        if (oldItem) {
                            oldItem.classList.remove('active');
                            const oldSvg = oldItem.querySelector('.clientele_vector');
                            if (oldSvg) {
                                gsap.to(oldSvg, { clipPath: 'inset(0% 0% 0% 100%)', duration: 0.8, ease: 'power2.inOut', overwrite: 'auto' });
                            }
                        }

                        const newItem = items[newActiveIndex];
                        if (newItem) {
                            newItem.classList.add('active');
                            const newSvg = newItem.querySelector('.clientele_vector');
                            if (newSvg) {
                                gsap.fromTo(newSvg, { clipPath: 'inset(0% 100% 0% 0%)' }, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1.5, ease: 'power2.out', overwrite: 'auto' });
                            }
                        }
                        currentActiveIndex = newActiveIndex;
                    }
                },
            }
        });

        if (maxScroll > 0) {
            clienteleTl.to(list, {
                y: -maxScroll,
                ease: 'none',
            });
        }
    }
});

window.addEventListener("load", () => {
    ScrollTrigger.refresh();
});