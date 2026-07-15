if (history.scrollRestoration) {
    history.scrollRestoration = "manual";
}
window.scrollTo(0, 0);
window.addEventListener("beforeunload", () => {
    window.scrollTo(0, 0);
});
let currentWidth = window.innerWidth;

window.addEventListener("resize", () => {
    if (window.innerWidth !== currentWidth) {
        window.scrollTo(0, 0);
        location.reload();
    }
});

// Raindrops on Glass Effect for the first banner (Perfect Rainyscope Physics)
document.addEventListener("DOMContentLoaded", () => {
    const bannerOverlay = document.querySelector(".banner-blur-overlay");
    const videoElement =
        window.innerWidth <= 992
            ? document.querySelector(".banner_video_mobile") ||
            document.querySelector(".banner_image")
            : document.querySelector(".banner_video_desktop") ||
            document.querySelector(".banner_image");

    if (bannerOverlay && videoElement) {
        // Clear any old canvas if there was one
        bannerOverlay.innerHTML = "";

        // Dynamically inject rainyday.js from cdnjs, so we don't need to modify index.html at all!
        const script = document.createElement("script");
        script.src = '/static/js/rainyday.min.js';
        script.onload = () => {
            // Wait for video metadata to have exact crop dimensions
            const tryInitRain = setInterval(() => {
                if (videoElement.readyState >= 1 || videoElement.videoWidth > 0) {
                    clearInterval(tryInitRain);

                    videoElement.setAttribute("crossorigin", "anonymous");

                    let engine = new RainyDay({
                        image: videoElement,
                        parentElement: bannerOverlay,
                        // Provide crop explicitly so it bounds correctly on HTML5 Video
                        crop: [
                            0,
                            0,
                            videoElement.videoWidth || 1920,
                            videoElement.videoHeight || 1080,
                        ],
                        width: bannerOverlay.clientWidth,
                        height: bannerOverlay.clientHeight,
                        fps: 45,
                        blur: 0,
                        opacity: 1,
                    });

                    // Enable heavy non-linear gravity and distinct trails for realistic drop sliding
                    engine.gravity = engine.GRAVITY_NON_LINEAR;
                    engine.trail = engine.TRAIL_DROPS;

                    // Trick rainyday into drawing a transparent background
                    // This allows the live video underneath to show perfectly without being covered by a static frame!
                    try {
                        if (engine.background) {
                            engine.background
                                .getContext("2d")
                                .clearRect(0, 0, engine.canvas.width, engine.canvas.height);
                        }
                    } catch (e) { }

                    // Phase 1: Initial sparse drops (Random places par thodi-thodi boondein)
                    engine.rain(
                        [
                            [4, 6, 0.15], // Medium boondein random jagah par
                            [6, 8, 0.1], // Badi sliding boondein door-door girenge
                        ],
                        250,
                    );

                    // Phase 2: 1.5 seconds ke baad poori screen heavy boondon se bhar jayegi
                    setTimeout(() => {
                        // Ek baar me glass par bhari choti boondein dal dena
                        engine.rain([[1, 2, 2000]]);

                        // Bahut tezz aur bhari slide hone wale raindrops
                        engine.rain(
                            [
                                [2, 4, 0.6],
                                [5, 7, 0.4],
                                [7, 9, 0.2],
                                [9, 11, 0.1],
                            ],
                            50,
                        );
                    }, 1500);
                }
            }, 100);
        };
        document.head.appendChild(script);
    }
});

// Card Marquee (Clone logic)
document.addEventListener("DOMContentLoaded", () => {
    if (typeof gsap === "undefined") {
        return;
    }
    gsap.registerPlugin(ScrollTrigger);
    ScrollTrigger.config({ ignoreMobileResize: true });
    // ==========================================
    // ANIMATION 1: Premium Banner Section
    // ==========================================
    const banners = gsap.utils.toArray(".banner");
    const bannerSection = document.querySelector(".premium_banner_section");

    if (banners.length > 0 && bannerSection) {
        const total = banners.length;

        banners.forEach((banner, index) => {
            gsap.set(banner, {
                clipPath: "inset(0% 0% 0% 0%)",
                zIndex: total - index,
                visibility: "visible",
                opacity: 1,
            });
        });

        // Initial transparent state and navlink states are handled via classes
        const navLinks = document.querySelectorAll(".bhavin");

        const bannerTl = gsap.timeline({
            scrollTrigger: {
                trigger: bannerSection,
                start: "top top",
                end: () => `+=${(banners.length - 1) * 100}%`,
                pin: true,
                scrub: 1,
                invalidateOnRefresh: true,
                anticipatePin: 1,
                onUpdate: (self) => {
                    const navLinks = document.querySelectorAll(".bhavin");
                    // Navbar background logic: transparent only at the start
                    if (self.progress >= 0.99) {
                        document.documentElement.classList.remove("is-transparent-navbar");
                    } else {
                        document.documentElement.classList.add("is-transparent-navbar");
                    }

                    // Nav links text color and logo logic
                    if (self.progress >= 0.99) {
                        document.documentElement.classList.remove("is-white-navlinks");
                    } else {
                        const totalScroll = self.progress * (banners.length - 1);
                        const currentIndex = Math.floor(totalScroll);
                        const p = totalScroll - currentIndex;

                        let headerActiveBannerIndex = currentIndex;

                        if (
                            (1 - p) * window.innerHeight <= 60 &&
                            currentIndex < banners.length - 1
                        ) {
                            headerActiveBannerIndex = currentIndex + 1;
                        }

                        if (
                            headerActiveBannerIndex === 0 ||
                            headerActiveBannerIndex === 2 ||
                            headerActiveBannerIndex === 4
                        ) {
                            document.documentElement.classList.add("is-white-navlinks");
                        } else {
                            document.documentElement.classList.remove("is-white-navlinks");
                        }
                    }
                },
                // markers: true // Debug lines
            },
        });

        banners.forEach((banner, index) => {
            if (index === 0) return;
            bannerTl.fromTo(
                banners[index - 1],
                { clipPath: "inset(0% 0% 0% 0%)" },
                {
                    clipPath: "inset(0% 0% 100% 0%)",
                    ease: "none",
                    duration: 1,
                },
                index - 1,
            );
        });
    }
    // ==========================================
    // ANIMATION 2: Enhance Your Smile Bubbles
    // ==========================================
    const bubbleOrder = [
        ".bubble-3",
        ".bubble-5",
        ".bubble-1",
        ".bubble-4",
        ".bubble-6",
        ".bubble-2",
    ];
    const bubbleContainer = document.querySelector(
        ".enhance_your_smile_small_screen",
    );

    if (bubbleContainer) {
        gsap.set(bubbleOrder, {
            y: -1200,
            opacity: 0,
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
                        overwrite: "auto",
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
                        overwrite: "auto",
                    });
                });
            },
        });
    }

    // ==========================================
    // ANIMATION 3: Clientele Section
    // ==========================================

    const items = gsap.utils.toArray(".clientele_item");
    const list = document.querySelector(".clientele_list");

    if (items.length >= 6 && list) {
        items.forEach((item, index) => {
            const wrapper = item.querySelector(".clientele_vector_wrapper");
            const svg = item.querySelector(".clientele_vector");
            if (
                svg &&
                wrapper &&
                !wrapper.querySelector(".clientele_vector_inactive")
            ) {
                const inactiveSvg = svg.cloneNode(true);
                inactiveSvg.classList.remove("clientele_vector");
                inactiveSvg.classList.add("clientele_vector_inactive");
                wrapper.appendChild(inactiveSvg);
                gsap.set(svg, {
                    clipPath: index === 0 ? "inset(0% 0% 0% 0%)" : "inset(0% 0% 0% 0%)",
                });
            }
        });

        let currentActiveIndex = 0;

        const initialWrapper = items[0]?.querySelector(".clientele_vector_wrapper");
        if (initialWrapper) {
            gsap.to(initialWrapper, {
                y: -12,
                duration: 2,
                repeat: -1,
                yoyo: true,
                ease: "sine.inOut",
            });
        }

        let clienteleTl = gsap.timeline({
            scrollTrigger: {
                trigger: ".clientele_section",
                pin: true,
                start: "top 10%",
                end: () => "+=" + items[4].offsetTop,
                scrub: 1,
                invalidateOnRefresh: true,
                onUpdate: (self) => {
                    let newActiveIndex = Math.floor(self.progress * 5);
                    if (self.progress >= 0.999) newActiveIndex = 5;
                    if (newActiveIndex > 5) newActiveIndex = 5;
                    if (newActiveIndex < 0) newActiveIndex = 0;

                    if (newActiveIndex !== currentActiveIndex) {
                        const oldSvg =
                            items[currentActiveIndex]?.querySelector(".clientele_vector");
                        const newSvg =
                            items[newActiveIndex]?.querySelector(".clientele_vector");
                        const oldWrapper = items[currentActiveIndex]?.querySelector(
                            ".clientele_vector_wrapper",
                        );
                        const newWrapper = items[newActiveIndex]?.querySelector(
                            ".clientele_vector_wrapper",
                        );

                        if (oldSvg) {
                            gsap.to(oldSvg, {
                                clipPath: "inset(0% 0% 0% 0%)",
                                duration: 0.8,
                                overwrite: "auto",
                            });
                        }
                        if (oldWrapper) {
                            gsap.killTweensOf(oldWrapper);
                            gsap.to(oldWrapper, { y: 0, duration: 0.5, overwrite: "auto" });
                        }

                        if (newSvg) {
                            gsap.fromTo(
                                newSvg,
                                { clipPath: "inset(0% 0% 0% 0%)" },
                                {
                                    clipPath: "inset(0% 0% 0% 0%)",
                                    duration: 1,
                                    overwrite: "auto",
                                },
                            );
                        }
                        if (newWrapper) {
                            gsap.to(newWrapper, {
                                y: -12,
                                duration: 2,
                                repeat: -1,
                                yoyo: true,
                                ease: "sine.inOut",
                                overwrite: "auto",
                            });
                        }

                        items.forEach((item, i) =>
                            i === newActiveIndex
                                ? item.classList.add("active")
                                : item.classList.remove("active"),
                        );
                        currentActiveIndex = newActiveIndex;
                    }
                },
            },
        });

        clienteleTl.to(list, {
            y: () => -items[4].offsetTop,
            ease: "none",
        });
    }
});

window.addEventListener("load", () => {
    if (typeof ScrollTrigger !== "undefined") {
        ScrollTrigger.refresh();
    }
    setTimeout(() => {
        window.scrollTo(0, 0);
    }, 10);
});
