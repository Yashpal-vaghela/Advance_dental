gsap.registerPlugin(ScrollTrigger);

ScrollTrigger.config({
  ignoreMobileResize: true
});



if ("scrollRestoration" in history) {
  history.scrollRestoration = "manual";
}

let initialWidth = window.innerWidth;
let initialHeight = window.innerHeight;
let resizeTimer;

window.addEventListener("resize", () => {
  clearTimeout(resizeTimer);

  resizeTimer = setTimeout(() => {
    const widthChanged = window.innerWidth !== initialWidth;
    const heightChanged = Math.abs(window.innerHeight - initialHeight) > 80;

    if (widthChanged || heightChanged) {
      // Force disable scroll restoration
      if ("scrollRestoration" in history) {
        history.scrollRestoration = "manual";
      }

      // Scroll to top BEFORE reload
      document.documentElement.scrollTop = 0;
      document.body.scrollTop = 0;
      window.scrollTo({ top: 0, left: 0, behavior: "instant" });

      // Small delay ensures scroll is applied
      setTimeout(() => {
        window.location.reload();
      }, 100);
    }
  }, 300);
});


window.addEventListener("load", () => {
  if (window.innerWidth >= 992) {
    initHeroSection();
  } else {
    initMobileHeroAnimation();
    initMobileSections();
  }
  initEmaxMaterialHighlightReversible();
  initOfferingsSection();
  ScrollTrigger.refresh();
});

function initMobileHeroAnimation() {
  const hero = document.querySelector(".emax-smallscreen.emax-intro");
  if (!hero) return;

  // Safely inject the fixed background behind everything
  let mobileBg = document.querySelector(".mobile-fixed-bg");
  if (!mobileBg) {
    mobileBg = document.createElement("div");
    mobileBg.className = "mobile-fixed-bg is-active";
    document.body.prepend(mobileBg);
  } else {
    mobileBg.classList.add("is-active");
  }

  const bgText = hero.querySelector(".emax-bg-text");
  const leftCard = hero.querySelector(".emax-left");
  const centerCard = hero.querySelector(".emax-center");
  const rightCard = hero.querySelector(".emax-right");
  const subHeading = hero.querySelector(".emax-sub");
  const mainHeading = hero.querySelector(".emax-main");

  // Force GSAP to use xPercent instead of parsing the CSS matrix into exact pixels.
  // We add yPercent: 50 here so the center card starts lower down.
  gsap.set(centerCard, { x: 0, xPercent: -50, yPercent: 50, scale: 0.8, autoAlpha: 0 });
  gsap.set(leftCard, { x: 0, xPercent: -50, scale: 0.8, autoAlpha: 0 });
  gsap.set(rightCard, { x: 0, xPercent: -50, scale: 0.8, autoAlpha: 0 });

  gsap.set(bgText, { autoAlpha: 0, y: 50 });
  gsap.set([subHeading, mainHeading], { autoAlpha: 0, y: 30 });

  // 1) Entrance Animation Timeline (Plays automatically when section is reached)
  const enterTl = gsap.timeline({
    scrollTrigger: {
      trigger: hero,
      start: "top 80%",
    }
  });

  enterTl.to(bgText, { autoAlpha: 1, y: 0, duration: 1.2, ease: "power3.out" })
    .to(centerCard, { scale: 1, yPercent: 0, autoAlpha: 1, duration: 1.0, ease: "back.out(1.2)" }, "-=0.8")
    // Side cards start from the center (xPercent: -50) and move to their original CSS locations
    // We add a slight delay (e.g. +=0.2) so they don't immediately pop out before the eye adjusts
    .to(leftCard, { xPercent: -140, scale: 0.92, autoAlpha: 1, duration: 1.0, ease: "back.out(1.2)" }, "+=0.2")
    .to(rightCard, { xPercent: 40, scale: 0.92, autoAlpha: 1, duration: 1.0, ease: "back.out(1.2)" }, "<")
    .to([subHeading, mainHeading], { autoAlpha: 1, y: 0, stagger: 0.2, duration: 1.0, ease: "power2.out" }, "-=0.5")
    .eventCallback("onComplete", () => {
      // FORCE GSAP to clear any cached starting positions for the scroll timeline.
      // Now when you scroll backward to 0, it knows exactly what to revert to!
      scrollTl.invalidate();
    });

  // 2) Scroll Animation Timeline (Pins hero and folds cards back inside)
  const scrollTl = gsap.timeline({
    scrollTrigger: {
      trigger: hero,
      start: "top top",     // Start pinning when hero hits the top
      end: "+=80%",         // Keep pinned for 0.8x screen height to allow faster scrolling
      scrub: 1,             // Smooth scrub
      pin: true,
      anticipatePin: 1
    }
  });

  // Slowly retract cards behind center
  scrollTl.to(leftCard, { xPercent: -50, scale: 0.8, ease: "none" }, 0)
    .to(rightCard, { xPercent: -50, scale: 0.8, ease: "none" }, 0)
    // Simply slide texts naturally UPWARD out of the screen while fading out
    .to([subHeading, mainHeading, bgText], { autoAlpha: 0, y: -700, ease: "none", duration: 0.5 }, 0);
}


function initOfferingsSection() {
  const section = document.querySelector(".emax-offering");
  const card1 = section && section.querySelector(".emax-offer-card:not(.is-second)");
  const card2 = section && section.querySelector(".emax-offer-card.is-second");
  if (!section || !card1 || !card2) return;

  // Helper: get current navbar height (recalculated every time)
  function getNavH() {
    const navbar = document.querySelector(".navbar, nav, header");
    return navbar ? navbar.getBoundingClientRect().height : 70;
  }

  // Reset any previously applied transforms
  gsap.set([card1, card2], { clearProps: "all" });

  const tl = gsap.timeline({
    scrollTrigger: {
      trigger: section,
      // Always recalculate start based on current navbar height
      start: () => "top top+=" + getNavH(),
      end: () => "+=" + (window.innerHeight * 0.6),
      scrub: 1.2,
      pin: true,
      pinSpacing: false,
      anticipatePin: 1,
      invalidateOnRefresh: true,
    }
  });

  // Phase 1: Slide card2 up so it overlaps card1, stopping 20px below card1's top
  tl.to(card2, {
    y: () => {
      // Always recalculate at animation time for full responsiveness
      const c1top = card1.getBoundingClientRect().top;
      const c2top = card2.getBoundingClientRect().top;
      return -(c2top - c1top - 20);
    },
    ease: "none",
    duration: 1,
  }, 0);

  // Phase 2: Hold the stacked state so user can see it
  tl.to({}, { duration: 0.5 });
}

function initHeroSection() {
  const hero = document.querySelector(".desktop-hero");
  if (!hero) return;

  const stage = hero.querySelector(".emax-stage");
  const left = hero.querySelector(".emax-left");
  const right = hero.querySelector(".emax-right");
  const heading = hero.querySelector(".emax-heading");
  const bgText = hero.querySelector(".emax-bg-text");
  const crownLeft = hero.querySelector(".emax-crown-left");
  const crownRight = hero.querySelector(".emax-detail-right");
  const veneerLeft = hero.querySelector(".emax-veneer-left");
  const veneerRight = hero.querySelector(".emax-veneer-right");
  const veneerBg = hero.querySelector(".emax-veneer");

  if (!stage || !left || !right || !heading || !bgText ||
    !crownLeft || !crownRight || !veneerLeft || !veneerRight || !veneerBg) return;
  const phase1 = 0.62;
  let tl;

  function build(cfg) {

    if (tl) {
      tl.scrollTrigger && tl.scrollTrigger.kill(true);
      tl.kill();
      tl = null;
    }

    gsap.set([stage, left, right, heading, bgText, crownLeft, crownRight, veneerLeft, veneerRight], { clearProps: "all" });

    function getStageCenterY() {
      const r = stage.getBoundingClientRect();
      const centerTop = (window.innerHeight - r.height) / 2;
      return (centerTop - r.top) + cfg.stageTopGap;
    }
    function getOutOfViewY(el, extraGap = 60) {
      const r = el.getBoundingClientRect();
      return -(r.bottom + extraGap);
    }
    function getBesideStageY(el, extra = 0) {
      const s = stage.getBoundingClientRect();
      const e = el.getBoundingClientRect();
      const targetTop = (s.top + s.height / 2) - (e.height / 2) + extra;
      return (targetTop - e.top);
    }
    gsap.set([crownLeft, crownRight], { y: cfg.crownTextStartY, autoAlpha: 0 });
    gsap.set([veneerLeft, veneerRight], { y: cfg.veneerTextStartY, autoAlpha: 0 });
    tl = gsap.timeline({
      scrollTrigger: {
        trigger: hero,
        start: "top top",
        end: () => "+=" + (window.innerHeight * 1),
        scrub: true,
        pin: true,
        pinSpacing: true,
        anticipatePin: 1,
        invalidateOnRefresh: true,
      }
    });
    console.log(window.innerWidth < 1281 && window.innerHeight < 700);

    tl.to(left, { x: cfg.leftX, scale: cfg.sideScale, ease: "none", duration: phase1 }, 0);
    tl.to(right, { x: cfg.rightX, scale: cfg.sideScale, ease: "none", duration: phase1 }, 0);
    tl.to(heading, { y: () => getOutOfViewY(heading, 100), opacity: 0, ease: "none", duration: phase1 }, 0);
    tl.to(bgText, { y: cfg.bgTextY, ease: "none", duration: phase1 }, 0);
    tl.to(stage, { y: () => getStageCenterY(), duration: phase1, ease: "none" }, 0);
    tl.to(stage, { y: () => getStageCenterY(), ease: "none" }, 0);
    tl.addLabel("crownIn", cfg.crownInAt);
    tl.addLabel("crownOut", cfg.crownOutAt);
    tl.addLabel("veneerIn", cfg.veneerInAt);

    tl.to(right, {
      width: cfg.centerW,
      left: cfg.rightToLeft,
      top: "0%",
      x: cfg.rightPreX,
      xPercent: 100,
      scale: 1,
      zIndex: 4,
      ease: "none",
    }, "crownIn");

    tl.to(right, {
      left: "50%",
      xPercent: -50,
      x: 0,
      width: cfg.centerW,
      top: "0%",
      zIndex: 7,
      ease: "none"
    }, cfg.rightSettleAt);

    tl.to(hero, {
      onStart: () => hero.classList.add("hero-crown-on"),
      onReverseComplete: () => hero.classList.remove("hero-crown-on")
    }, cfg.crownBgAt);
    tl.to([crownLeft, crownRight], { autoAlpha: 1, y: 0, ease: "none", }, "crownIn");
    tl.to([crownLeft, crownRight], { y: () => getOutOfViewY(crownLeft, cfg.outGap), ease: "none", }, "crownOut");

    tl.to(left, {
      width: cfg.centerW,
      left: cfg.leftToLeft,
      top: "0%",
      x: cfg.leftPreX,
      xPercent: -100,
      scale: cfg.leftScale,
      zIndex: 9,
      ease: "none",
    }, cfg.leftInAt);

    tl.to(left, {
      left: "50%",
      xPercent: -50,
      x: 0,
      width: cfg.centerW,
      top: "0%",
      zIndex: 10,
      ease: "none"
    }, cfg.leftSettleAt);

    tl.to({}, {
      onStart: () => {
        hero.classList.remove("hero-crown-on");
        veneerBg.classList.add("veneer-bg-on");
      },
      onReverseComplete: () => {
        veneerBg.classList.remove("veneer-bg-on");
        hero.classList.add("hero-crown-on");
      }
    }, cfg.veneerBgAt);
    tl.to([veneerLeft, veneerRight], {
      autoAlpha: 1,
      y: () => getBesideStageY(veneerLeft, 0),
      ease: "none",
    }, "veneerIn");

    // Add extra duration at the end so the user can read the veneer text before it unpins
    tl.to({}, { duration: 0.1 });
    return tl;
  }

  const cfgDesktop = {
    scrollLen: 600,
    sideScale: 0.80,
    leftX: -130,
    rightX: -150,
    headingY: -710,
    bgTextY: -200,
    stageTopGap: -40,
    centerW: 300,
    rightToLeft: "29%",
    rightPreX: 90,
    leftToLeft: "71%",
    leftPreX: -90,
    leftScale: 1.1,
    crownTextStartY: 100,
    veneerTextStartY: 40,
    outGap: 60,
    crownInAt: 0.75,
    rightSettleAt: 1.05,
    crownBgAt: 0.72,
    crownOutAt: 1.55,
    leftInAt: 1.75,
    leftSettleAt: 2.10,
    veneerBgAt: 2.10,
    veneerInAt: 2.20,
  };

  const cfg1280 = {
    scrollLen: 600,
    sideScale: 0.80,
    leftX: -100,
    rightX: -120,
    headingY: -600,
    bgTextY: -150,
    stageTopGap: 0,
    centerW: 200,
    rightToLeft: "29%",
    rightPreX: 60,
    leftToLeft: "65%",
    leftPreX: -60,
    leftScale: 1.05,
    crownTextStartY: 40,
    veneerTextStartY: 40,
    outGap: 60,
    crownInAt: 0.75,
    rightSettleAt: 1.05,
    crownBgAt: 0.72,
    crownOutAt: 1.55,
    leftInAt: 1.75,
    leftSettleAt: 2.10,
    veneerBgAt: 2.10,
    veneerInAt: 2.20,
  };

  ScrollTrigger.matchMedia({
    "(min-width: 1281px)": () => build(cfgDesktop),
    "(max-width: 1280px) and (min-width: 992px)": () => build(cfg1280),


  });
}

function initEmaxMaterialHighlightReversible() {
  if (window.__emaxMaterialInited) return;
  window.__emaxMaterialInited = true;

  const SECTION_SEL = ".emax-material";

  const sections = document.querySelectorAll(SECTION_SEL);
  if (!sections.length) return;

  const mm = gsap.matchMedia();

  sections.forEach((section, index) => {
    const BODY_SEL = ".emax-material-body";
    const WORD_CLASS = "word";
    const ON_CLASS = "is-on";
    const TRIGGER_ID = `emax-material-pin-reversible-${index}`;

    const body = section.querySelector(BODY_SEL);
    if (!body) return;

    let materialTL = null;
    const paras = Array.from(body.querySelectorAll("p"));
    if (!paras.length) return;

    function tokenizePreserveSpaces(text) {
      return text.match(/(\s+|[^\s]+)/g) || [];
    }
    function wrapWordsInParagraph(p) {
      if (!p || p.dataset.emaxWrapped === "1") return;

      const walker = document.createTreeWalker(p, NodeFilter.SHOW_TEXT, {
        acceptNode: (node) => {
          if (!node.nodeValue || !node.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
          if (node.parentElement?.classList?.contains(WORD_CLASS)) return NodeFilter.FILTER_REJECT;
          return NodeFilter.FILTER_ACCEPT;
        }
      });

      const textNodes = [];
      while (walker.nextNode()) textNodes.push(walker.currentNode);

      textNodes.forEach((textNode) => {
        const tokens = tokenizePreserveSpaces(textNode.nodeValue);
        const frag = document.createDocumentFragment();

        tokens.forEach((t) => {
          if (/^\s+$/.test(t)) {
            frag.appendChild(document.createTextNode(t));
          } else {
            const span = document.createElement("span");
            span.className = WORD_CLASS;
            span.textContent = t;
            frag.appendChild(span);
          }
        });

        textNode.parentNode.replaceChild(frag, textNode);
      });

      p.dataset.emaxWrapped = "1";
    }
    function wrapAllParagraphs() {
      paras.forEach(wrapWordsInParagraph);
    }
    function killExisting() {
      const st = ScrollTrigger.getById(TRIGGER_ID);
      if (st) st.kill(true); // remove spacer properly
      if (materialTL) {
        materialTL.kill();
        materialTL = null;
      }
    }

    mm.add(
      {
        desktop: "(min-width: 992px)",
        mobile: "(max-width: 991px)",
        reduceMotion: "(prefers-reduced-motion: reduce)"
      },
      (context) => {
        killExisting();

        // If the section is hidden via CSS, ignore creating animations for it.
        if (window.getComputedStyle(section).display === "none") {
          return;
        }

        if (context.conditions.reduceMotion) {
          wrapAllParagraphs();
          const allWords = body.querySelectorAll(`.${WORD_CLASS}`);
          allWords.forEach((w) => w.classList.add(ON_CLASS));
          gsap.set(allWords, { opacity: 1 });
          return () => killExisting();
        }

        wrapAllParagraphs();

        const paragraphs = Array.from(body.querySelectorAll("p"));
        const paragraphWordLists = paragraphs.map((p) =>
          Array.from(p.querySelectorAll(`.${WORD_CLASS}`))
        );

        const allWords = Array.from(body.querySelectorAll(`.${WORD_CLASS}`));
        gsap.set(allWords, { opacity: 0.35 });
        allWords.forEach((w) => w.classList.remove(ON_CLASS));

        const isMobile = context.conditions.mobile;

        const PX_PER_UNIT = isMobile ? 7 :9;
        const GAP_UNITS = isMobile ? 6 : 8;

        materialTL = gsap.timeline({ paused: true });

        paragraphWordLists.forEach((words, idx) => {
          if (!words.length) return;

          materialTL.to(words, {
            opacity: 1,
            ease: "none",
            stagger: { each: 1, ease: "none" }
          });

          if (idx < paragraphs.length - 1) {
            materialTL.to({}, { duration: GAP_UNITS });
          }
        });
        const MIN_SCROLL = isMobile ? 350 : 500;
        const scrollLen = Math.max(MIN_SCROLL, materialTL.duration() * PX_PER_UNIT);

        function syncClassesFromProgress(p) {
          const total = allWords.length;
          const onCount = Math.round(p * total);
          for (let i = 0; i < total; i++) {
            allWords[i].classList.toggle(ON_CLASS, i < onCount);
          }
        }

        ScrollTrigger.create({
          id: TRIGGER_ID,
          trigger: section,
          start: "top top",
          end: () => `+=${scrollLen}`,
          scrub: true,
          pin: true,
          pinSpacing: true,
          anticipatePin: 1,
          invalidateOnRefresh: true,
          onUpdate: (self) => {
            const p = self.progress;
            materialTL.progress(p);
            syncClassesFromProgress(p);
          }
        });

        return () => killExisting();
      }
    );
  });
}

function initMobileSections() {
  const crownMobile = document.getElementById("emax-crown-mobile");
  if (crownMobile) {
    const crownCard = crownMobile.querySelector(".emax-card");
    const crownTexts = crownMobile.querySelectorAll(".emax-crown-left, .emax-detail-right");

    // Target precisely the mobile sections so the color does not bleed into the body globally
    const mobileSectionsTarget = ".emax-intro, #emax-crown-mobile, #emax-veneer-mobile";

    // 1) Full Screen Background transition
    ScrollTrigger.create({
      trigger: crownMobile,
      start: "top 60%", // Triggers precisely when section hits exactly 60% of viewport
      end: "bottom 60%", // Ends as its bottom passes 60%
      onEnter: () => gsap.to(":root", { "--emax-overlay-alpha": 0.4, duration: 0.4, overwrite: "auto" }),
      onEnterBack: () => gsap.to(":root", { "--emax-overlay-alpha": 0.4, duration: 0.4, overwrite: "auto" }),
      onLeaveBack: () => gsap.to(":root", { "--emax-overlay-alpha": 0, duration: 0.4, overwrite: "auto" })
    });

    // 2) Image and Text smoothly entering from the sides
    const crownTl = gsap.timeline({
      scrollTrigger: {
        trigger: crownMobile,
        start: "top 50%",
        toggleActions: "play none none reverse"
      }
    });

    crownTl.fromTo(crownCard, { y: 50, scale: 0.95, autoAlpha: 0 }, { y: 0, scale: 1, autoAlpha: 1, duration: 1.2, ease: "power3.out" }, 0)
      .fromTo(crownTexts, { y: 50, autoAlpha: 0 }, { y: 0, autoAlpha: 1, stagger: 0.2, duration: 1.0, ease: "power2.out" }, "-=0.8");
  }

  const veneerMobile = document.getElementById("emax-veneer-mobile");
  if (veneerMobile) {
    const veneerCard = veneerMobile.querySelector(".emax-card");
    const veneerTexts = veneerMobile.querySelectorAll(".emax-veneer-left, .emax-veneer-right");

    // Slightly different sky blue shade for the second section -> Now fades overlay back to 0 like desktop
    ScrollTrigger.create({
      trigger: veneerMobile,
      start: "top 60%",
      end: "bottom bottom",
      onEnter: () => {
        gsap.to(":root", { "--emax-overlay-alpha": 0, duration: 0.4, overwrite: "auto" });
        document.querySelector(".mobile-fixed-bg")?.classList.add("is-active");
      },
      onEnterBack: () => {
        gsap.to(":root", { "--emax-overlay-alpha": 0, duration: 0.4, overwrite: "auto" });
        document.querySelector(".mobile-fixed-bg")?.classList.add("is-active");
      },
      onLeave: () => {
        gsap.to(":root", { "--emax-overlay-alpha": 0, duration: 0.4, overwrite: "auto" });
        document.querySelector(".mobile-fixed-bg")?.classList.remove("is-active");
      }
    });

    const veneerTl = gsap.timeline({
      scrollTrigger: {
        trigger: veneerMobile,
        start: "top 50%",
        toggleActions: "play none none reverse"
      }
    });

    veneerTl.fromTo(veneerCard, { y: 50, scale: 0.95, autoAlpha: 0 }, { y: 0, scale: 1, autoAlpha: 1, duration: 1.2, ease: "power3.out" }, 0)
      .fromTo(veneerTexts, { y: 50, autoAlpha: 0 }, { y: 0, autoAlpha: 1, stagger: 0.2, duration: 1.0, ease: "power2.out" }, "-=0.8");
  }
}
