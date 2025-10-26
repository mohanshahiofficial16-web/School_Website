document.addEventListener("DOMContentLoaded", () => {
    const counters = document.querySelectorAll(".counter");

    counters.forEach(counter => {
        const updateCount = () => {
            const target = +counter.getAttribute("data-target");
            let current = +counter.innerText.replace(/,/g, "");
            const increment = target / 200; // smaller divisor = faster

            if(current < target) {
                counter.innerText = Math.ceil(current + increment).toLocaleString();
                requestAnimationFrame(updateCount);
            } else {
                counter.innerText = target.toLocaleString();
            }
        };

        // Optional: animate only when visible
        const observer = new IntersectionObserver(entries => {
            if(entries[0].isIntersecting) {
                updateCount();
                observer.unobserve(counter);
            }
        }, { threshold: 0.5 });

        observer.observe(counter);
    });
});
