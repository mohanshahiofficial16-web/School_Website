document.addEventListener('DOMContentLoaded', function() {
    // Initialize event filters
    const eventTypeFilter = document.getElementById('event-type');
    const monthFilter = document.getElementById('month');
    const eventCards = document.querySelectorAll('.event-card');
    const currentDate = new Date();

    // ========== 1. Preserve filter selections on page refresh ==========
    if (eventTypeFilter && monthFilter) {
        if (window.performance && window.performance.navigation.type === window.performance.navigation.TYPE_BACK_FORWARD) {
            const params = new URLSearchParams(window.location.search);
            if (params.has('event_type')) {
                eventTypeFilter.value = params.get('event_type');
            }
            if (params.has('month')) {
                monthFilter.value = params.get('month');
            }
        }
    }

    // ========== 2. Event RSVP functionality ==========
    const rsvpButtons = document.querySelectorAll('.btn-rsvp');
    rsvpButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const eventCard = this.closest('.event-card');
            const eventTitle = eventCard.querySelector('h2').textContent;
            
            alert(`Thank you for your interest in "${eventTitle}". RSVP functionality would be implemented here.`);
        });
    });

    // ========== 3. Past events styling ==========
    eventCards.forEach(card => {
        const dateElement = card.querySelector('.event-date');
        if (dateElement) {
            const day = dateElement.querySelector('.day').textContent;
            const month = dateElement.querySelector('.month').textContent;
            const year = dateElement.querySelector('.year').textContent;
            
            const eventDate = new Date(`${month} ${day}, ${year}`);
            
            if (eventDate < currentDate) {
                card.classList.add('past-event');
                const rsvpBtn = card.querySelector('.btn-rsvp');
                if (rsvpBtn) {
                    rsvpBtn.style.display = 'none';
                }
            }
        }
    });

    // ========== 4. Filtering Logic ==========
    function filterEvents() {
        const selectedType = eventTypeFilter.value;
        const selectedMonth = monthFilter.value;

        eventCards.forEach(card => {
            let matches = true;

            // Match by type
            if (selectedType && selectedType !== "all") {
                const cardType = card.dataset.type; // add data-type="seminar" etc. in HTML
                if (cardType !== selectedType) {
                    matches = false;
                }
            }

            // Match by month
            if (selectedMonth && selectedMonth !== "all") {
                const dateElement = card.querySelector('.event-date');
                if (dateElement) {
                    const cardMonth = dateElement.querySelector('.month').textContent.toLowerCase();
                    if (cardMonth !== selectedMonth.toLowerCase()) {
                        matches = false;
                    }
                }
            }

            // Show or hide
            card.style.display = matches ? "block" : "none";
        });
    }

    // Attach event listeners to filters
    if (eventTypeFilter) eventTypeFilter.addEventListener('change', filterEvents);
    if (monthFilter) monthFilter.addEventListener('change', filterEvents);

    // Run once on load (in case of refresh with filters applied)
    filterEvents();
});
