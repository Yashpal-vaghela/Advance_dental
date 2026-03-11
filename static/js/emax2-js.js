document.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll(".benefit-card");
    const timeline = document.querySelector(".timeline");
    const centerLine = document.querySelector(".center-line");
    console.log("emax2-js loaded");
    function updateOnScroll() {
        const viewportHeight = window.innerHeight;

        // 1. Animate Middle Line
        if (timeline && centerLine) {
            // We map the section's scroll from 0 (just entering bottom) to 1 (just leaving top)
            const timelineRect = timeline.getBoundingClientRect();
            const totalTravel = viewportHeight + timelineRect.height;
            const consumed = viewportHeight - timelineRect.top;

            let progress = consumed / totalTravel;
            progress = Math.max(0, Math.min(1, progress));

            // This calculation forces the 'needle' to glide from top to bottom
            // 0% progress -> center of needle is at 0%
            // 100% progress -> center of needle is at 100%
            centerLine.style.top = `${progress * 90}%`;
            // Keep the center of the gradient perfectly aligned with the percentage point
            centerLine.style.transform = `translate(-50%, -50%)`;
        }

        // 2. Animate Cards
        cards.forEach((card) => {
            const rect = card.getBoundingClientRect();
            const cardCenter = rect.top + rect.height / 2;

            const startY = viewportHeight * 0.90;
            const endY = viewportHeight * 0.50;

            let progress = (startY - cardCenter) / (startY - endY);
            progress = Math.max(0, Math.min(1, progress));

            // Interpolate values
            const opacity = 0.15 + (0.85 * progress);
            const scale = 0.85 + (0.15 * progress);

            card.style.opacity = opacity;
            card.style.transform = `scale(${scale})`;
        });
    }

    // Use requestAnimationFrame for completely smooth 60fps binding to scroll
    let ticking = false;
    window.addEventListener("scroll", () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                updateOnScroll();
                ticking = false;
            });
            ticking = true;
        }
    });

    // Initial trigger
    updateOnScroll();

    // 3. FAQ Accordion Logic
    const faqItems = document.querySelectorAll(".faq-item");

    faqItems.forEach(item => {
        const questionBtn = item.querySelector(".faq-question");
        const answer = item.querySelector(".faq-answer");

        // Initialize any items that are pre-set to active in HTML
        if (item.classList.contains("active")) {
            answer.style.maxHeight = answer.scrollHeight + "px";
        }

        questionBtn.addEventListener("click", () => {
            const isActive = item.classList.contains("active");

            // Close all other items for a clean single-open accordion feel
            faqItems.forEach(otherItem => {
                otherItem.classList.remove("active");
                const otherAnswer = otherItem.querySelector(".faq-answer");
                otherAnswer.style.maxHeight = null;
            });

            if (!isActive) {
                // Open this item
                item.classList.add("active");
                answer.style.maxHeight = answer.scrollHeight + "px";
            }
        });
    });
});
