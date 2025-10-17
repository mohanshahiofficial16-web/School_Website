document.addEventListener('DOMContentLoaded', function () {
    // -------- DOM ELEMENTS --------
    const dom = {
        mobileToggle: document.querySelector('.mobile-menu-toggle'),
        navMenu: document.querySelector('.nav-menu'),
        navOverlay: document.querySelector('.nav-overlay'),
        dropdownToggles: document.querySelectorAll('.dropdown-toggle'),
        header: document.querySelector('.site-header'),
        nav: document.querySelector('.main-nav'),
        backToTop: document.querySelector('.back-to-top'),
        fab: document.querySelector('.fab'),
        closeBtns: document.querySelectorAll('.close-btn'),
        alerts: document.querySelectorAll('.alert'),
        preloader: document.querySelector('.preloader'),
        mainContent: document.querySelector('.main-content')
    };

    // -------- STATE --------
    const state = {
        isMobileMenuOpen: false,
        resizeTimeout: null
    };

    // -------- INITIALIZATION --------
    function init() {
        setupMobileMenu();
        setupDropdowns();
        setupScrollEffects();
        setupBackToTop();
        setupFAB();
        setupAnimations();
        setupAlerts();
        setupResizeHandler();
        setupAccessibility();
        adjustContentMargin();
        setupPreloader();
    }

    // ==================== MOBILE MENU ====================
    function setupMobileMenu() {
        if (!dom.mobileToggle || !dom.navMenu) return;

        dom.mobileToggle.style.position = 'fixed';
        dom.mobileToggle.style.top = '25px';
        dom.mobileToggle.style.right = '25px';
        dom.mobileToggle.style.zIndex = '1002';

        dom.mobileToggle.addEventListener('click', e => {
            e.stopPropagation();
            toggleMobileMenu();
        });

        dom.navMenu.querySelectorAll('.nav-link:not(.dropdown-toggle)').forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth < 993) closeMobileMenu();
            });
        });

        if (dom.navOverlay) dom.navOverlay.addEventListener('click', closeMobileMenu);
    }

    function toggleMobileMenu() {
        state.isMobileMenuOpen = !state.isMobileMenuOpen;
        dom.navMenu.classList.toggle('active', state.isMobileMenuOpen);
        dom.navOverlay?.classList.toggle('active', state.isMobileMenuOpen);
        dom.mobileToggle.classList.toggle('active', state.isMobileMenuOpen);
        document.body.style.overflow = state.isMobileMenuOpen ? 'hidden' : '';
        dom.mobileToggle.setAttribute('aria-expanded', state.isMobileMenuOpen);
        if (!state.isMobileMenuOpen) closeAllDropdowns();
    }

    function closeMobileMenu() {
        state.isMobileMenuOpen = false;
        dom.navMenu.classList.remove('active');
        dom.navOverlay?.classList.remove('active');
        dom.mobileToggle.classList.remove('active');
        document.body.style.overflow = '';
        dom.mobileToggle.setAttribute('aria-expanded', 'false');
        closeAllDropdowns();
    }

    // ==================== DROPDOWNS ====================
    function setupDropdowns() {
        dom.dropdownToggles.forEach(toggle => {
            if (toggle.dataset.listenerAdded) return;
            toggle.dataset.listenerAdded = true;

            const dropdown = toggle.closest('.dropdown');
            if (!dropdown) return;

            const dropdownMenu = dropdown.querySelector('.dropdown-menu');
            if (dropdownMenu) {
                toggle.setAttribute('aria-haspopup', 'true');
                toggle.setAttribute('aria-expanded', 'false');
                const toggleId = toggle.id || (toggle.textContent.trim().toLowerCase().replace(/\s+/g, '-') + '-dropdown');
                toggle.id = toggleId;
                dropdownMenu.setAttribute('aria-labelledby', toggleId);
            }

            toggle.addEventListener('click', function (e) {
                if (window.innerWidth < 993) e.preventDefault();
                e.stopPropagation();
                const isActive = dropdown.classList.contains('active');

                if (window.innerWidth < 993) closeAllDropdownsExcept(dropdown);
                dropdown.classList.toggle('active', !isActive);
                toggle.setAttribute('aria-expanded', !isActive ? 'true' : 'false');

                if (window.innerWidth >= 993 && !state.isMobileMenuOpen) {
                    const link = dropdown.querySelector('.nav-link');
                    if (link && link.getAttribute('href') && link.getAttribute('href') !== '#') {
                        window.location.href = link.getAttribute('href');
                    }
                }
            });
        });

        // Click outside closes dropdowns
        document.addEventListener('click', e => {
            if (!e.target.closest('.dropdown')) closeAllDropdowns();
        });

        // Escape key closes all
        document.addEventListener('keydown', e => {
            if (e.key === 'Escape') {
                closeAllDropdowns();
                if (state.isMobileMenuOpen) closeMobileMenu();
            }
        });

        // Desktop hover
        document.querySelectorAll('.dropdown').forEach(dropdown => {
            if (dropdown.dataset.hoverListener) return;
            dropdown.dataset.hoverListener = true;

            dropdown.addEventListener('mouseenter', () => {
                if (window.innerWidth >= 993) {
                    closeAllDropdownsExcept(dropdown);
                    dropdown.classList.add('active');
                    const toggle = dropdown.querySelector('.dropdown-toggle');
                    if (toggle) toggle.setAttribute('aria-expanded', 'true');
                }
            });

            dropdown.addEventListener('mouseleave', () => {
                if (window.innerWidth >= 993) {
                    setTimeout(() => {
                        if (!dropdown.matches(':hover')) {
                            dropdown.classList.remove('active');
                            const toggle = dropdown.querySelector('.dropdown-toggle');
                            if (toggle) toggle.setAttribute('aria-expanded', 'false');
                        }
                    }, 100);
                }
            });
        });
    }

    function closeAllDropdownsExcept(except = null) {
        document.querySelectorAll('.dropdown').forEach(item => {
            if (item !== except) {
                item.classList.remove('active');
                const toggle = item.querySelector('.dropdown-toggle');
                if (toggle) toggle.setAttribute('aria-expanded', 'false');
            }
        });
    }

    function closeAllDropdowns() {
        closeAllDropdownsExcept();
    }

    // ==================== SCROLL EFFECTS ====================
    function setupScrollEffects() {
        if (!dom.header || !dom.nav) return;

        let lastScrollTop = 0;
        window.addEventListener('scroll', throttle(() => {
            const currentScroll = window.scrollY || window.pageYOffset;
            if (currentScroll > lastScrollTop) {
                dom.header.classList.add('hidden');
                dom.nav.classList.add('sticky');
            } else {
                dom.header.classList.remove('hidden');
                dom.nav.classList.remove('sticky');
            }
            lastScrollTop = Math.max(currentScroll, 0);
        }, 100));
    }

    // ==================== BACK TO TOP ====================
    function setupBackToTop() {
        if (!dom.backToTop) return;

        window.addEventListener('scroll', throttle(() => {
            const isVisible = window.scrollY > 300;
            dom.backToTop.classList.toggle('visible', isVisible);
            dom.backToTop.setAttribute('aria-hidden', !isVisible);
        }, 150));

        dom.backToTop.addEventListener('click', e => {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // ==================== FAB ====================
    function setupFAB() {
        if (!dom.fab) return;

        dom.fab.addEventListener('click', e => {
            e.preventDefault();
            const contact = document.getElementById('contact');
            if (contact) contact.scrollIntoView({ behavior: 'smooth' });
        });
    }

    // ==================== ANIMATIONS ====================
    function setupAnimations() {
        const animated = document.querySelectorAll('.animate-on-scroll');
        if (!animated.length) return;

        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animated');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

        animated.forEach(el => observer.observe(el));
    }

    // ==================== ALERTS ====================
    function setupAlerts() {
        dom.closeBtns.forEach(btn => {
            if (!btn.getAttribute('aria-label')) btn.setAttribute('aria-label', 'Close notification');
            btn.addEventListener('click', () => {
                const alert = btn.closest('.alert');
                if (alert) {
                    alert.style.opacity = '0';
                    setTimeout(() => alert.remove(), 300);
                }
            });
        });

        dom.alerts.forEach(alert => {
            setTimeout(() => {
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 300);
            }, 5000);
        });
    }

    // ==================== RESIZE ====================
    function setupResizeHandler() {
        window.addEventListener('resize', () => {
            clearTimeout(state.resizeTimeout);
            state.resizeTimeout = setTimeout(() => {
                if (window.innerWidth >= 993 && state.isMobileMenuOpen) closeMobileMenu();
                setupAnimations();
                adjustContentMargin();
            }, 250);
        });
    }

    // ==================== ACCESSIBILITY ====================
    function setupAccessibility() {
        const skipLink = document.querySelector('.skip-link');
        if (skipLink) {
            skipLink.addEventListener('click', e => {
                e.preventDefault();
                const target = document.querySelector(skipLink.getAttribute('href'));
                if (target) {
                    target.setAttribute('tabindex', '-1');
                    target.focus();
                    setTimeout(() => target.removeAttribute('tabindex'), 1000);
                }
            });
        }
    }

    // ==================== PRELOADER ====================
    function setupPreloader() {
        if (!dom.preloader) return;

        window.addEventListener('load', () => {
            setTimeout(() => {
                dom.preloader.classList.add('preloader--hidden');
                setTimeout(() => dom.preloader.remove(), 500);
            }, 500);
        });

        setTimeout(() => {
            if (!dom.preloader.classList.contains('preloader--hidden')) {
                dom.preloader.classList.add('preloader--hidden');
                setTimeout(() => dom.preloader.remove(), 500);
            }
        }, 3000);
    }

    // ==================== UTILS ====================
    function throttle(func, limit) {
        let inThrottle;
        return function (...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    init();
});
