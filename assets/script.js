// Theme persistence
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
});

// Modern tab system
function createCustomTabs() {
    const containers = document.querySelectorAll('[data-custom-tabs]');
    
    containers.forEach(container => {
        const tabs = container.querySelectorAll('[role="button"]');
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                // Remove active class from all tabs
                tabs.forEach(t => t.classList.remove('active'));
                // Add active class to clicked tab
                tab.classList.add('active');
                // Trigger Streamlit rerun
                Streamlit.setComponentValue(tab.dataset.value);
            });
        });
    });
}

// Initialize components
document.addEventListener('DOMContentLoaded', () => {
    createCustomTabs();
    
    // Add parallax effect to cards
    const cards = document.querySelectorAll('.user-card');
    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = (e.clientX - rect.left) / card.offsetWidth;
            const y = (e.clientY - rect.top) / card.offsetHeight;
            
            card.style.transform = `
                perspective(1000px)
                rotateX(${(0.5 - y) * 10}deg)
                rotateY(${(x - 0.5) * 10}deg)
            `;
        });
        
        card.addEventListener('mouseleave', () => {
            card.style.transform = 'none';
        });
    });
});