// Animate elements when they come into view
function animateOnScroll() {
    const elements = document.querySelectorAll('.feature-card, .stat-item, .testimonial-card');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    
    elements.forEach(element => {
        observer.observe(element);
        // Add random delay for staggered animation
        element.style.transitionDelay = `${Math.random() * 0.3}s`;
    });
}

// Counter animation for stats
function animateCounters() {
    const counters = document.querySelectorAll('.stat-number');
    const speed = 200;
    
    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-target') || 
            (counter.id === 'users-count' ? 10000 : 
             counter.id === 'transactions-count' ? 250000 : 
             counter.id === 'savings-count' ? 50000000 : 
             counter.id === 'rating-count' ? 4.9 : 0));
        
        const increment = target / speed;
        let current = 0;
        
        const updateCount = () => {
            current += increment;
            if (current < target) {
                if (counter.id === 'rating-count') {
                    counter.textContent = current.toFixed(1);
                } else {
                    counter.textContent = Math.floor(current).toLocaleString();
                }
                setTimeout(updateCount, 1);
            } else {
                if (counter.id === 'rating-count') {
                    counter.textContent = target.toFixed(1);
                } else {
                    counter.textContent = target.toLocaleString();
                }
            }
        };
        
        updateCount();
    });
}

// Initialize animations when page loads
document.addEventListener('DOMContentLoaded', () => {
    animateOnScroll();
    
    // Start counter animation when stats section is visible
    const statsObserver = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting) {
            animateCounters();
            statsObserver.disconnect();
        }
    });
    
    statsObserver.observe(document.querySelector('.stats'));
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});