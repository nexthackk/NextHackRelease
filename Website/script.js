// ============================================
// Email Collection & Form Handling
// ============================================

const API_BASE_URL = 'https://nexthackrelease-production.up.railway.app/api'; // Backend API URL

// DOM Elements
const emailForm = document.getElementById('emailForm');
const emailInput = document.getElementById('emailInput');
const submitBtn = document.getElementById('submitBtn');
const formMessage = document.getElementById('formMessage');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeForm();
    animateOnScroll();
});

// ============================================
// Form Initialization
// ============================================
function initializeForm() {
    emailForm.addEventListener('submit', handleFormSubmit);
    emailInput.addEventListener('input', clearMessage);
    emailInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            emailForm.dispatchEvent(new Event('submit'));
        }
    });
}

// ============================================
// Form Submission Handler
// ============================================
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const email = emailInput.value.trim();
    
    // Validate email
    if (!isValidEmail(email)) {
        showMessage('Please enter a valid email address', 'error');
        emailInput.focus();
        return;
    }
    
    // Disable form during submission
    setFormLoading(true);
    clearMessage();
    
    try {
        const response = await submitEmail(email);
        
        if (response.success) {
            // Show the message from backend (includes email status)
            showMessage(response.message || '🎉 Success! We\'ll notify you when we launch. Check your email for a welcome message!', 'success');
            emailInput.value = '';
            
            // Log to console for debugging
            console.log('Subscription successful:', response);
        } else {
            showMessage(response.message || 'Something went wrong. Please try again.', 'error');
        }
    } catch (error) {
        console.error('Form submission error:', error);
        showMessage('Unable to connect. Please check your connection and try again.', 'error');
    } finally {
        setFormLoading(false);
    }
}

// ============================================
// Email Validation
// ============================================
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// ============================================
// API Call to Submit Email
// ============================================
async function submitEmail(email) {
    try {
        const response = await fetch(`${API_BASE_URL}/subscribe`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email }),
        });
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        // If backend is not available, store locally as fallback
        if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
            return storeEmailLocally(email);
        }
        throw error;
    }
}

// ============================================
// Local Storage Fallback
// ============================================
function storeEmailLocally(email) {
    try {
        const storedEmails = JSON.parse(localStorage.getItem('sectool_subscribers') || '[]');
        
        // Check if email already exists
        if (storedEmails.includes(email)) {
            return {
                success: true,
                message: 'You\'re already subscribed! We\'ll notify you when we launch.',
            };
        }
        
        // Add email to local storage
        storedEmails.push(email);
        localStorage.setItem('sectool_subscribers', JSON.stringify(storedEmails));
        
        return {
            success: true,
            message: '🎉 Success! We\'ll notify you when we launch.',
        };
    } catch (error) {
        console.error('Local storage error:', error);
        return {
            success: false,
            message: 'Unable to save your email. Please try again later.',
        };
    }
}

// ============================================
// Form Loading State
// ============================================
function setFormLoading(loading) {
    submitBtn.disabled = loading;
    emailInput.disabled = loading;
    
    if (loading) {
        submitBtn.classList.add('loading');
        submitBtn.querySelector('.btn-text').textContent = 'Submitting...';
    } else {
        submitBtn.classList.remove('loading');
        submitBtn.querySelector('.btn-text').textContent = 'Notify Me';
    }
}

// ============================================
// Message Display
// ============================================
function showMessage(message, type = 'success') {
    if (!formMessage) return;
    
    formMessage.textContent = message;
    formMessage.className = `form-message ${type} show`;
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        clearMessage();
    }, 5000);
}

function clearMessage() {
    if (!formMessage) return;
    formMessage.classList.remove('show');
    formMessage.textContent = '';
}

// ============================================
// Scroll Animations
// ============================================
function animateOnScroll() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px',
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe feature cards
    document.querySelectorAll('.feature-card').forEach((card) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease-out, transform 0.6s ease-out';
        observer.observe(card);
    });
}

// ============================================
// Smooth Scroll for Navigation Links
// ============================================
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start',
            });
        }
    });
});

// ============================================
// Console Welcome Message
// ============================================
console.log(
    '%c🚀 SecTool - Coming Soon',
    'color: #6366F1; font-size: 20px; font-weight: bold;'
);
console.log(
    '%cWe\'re building something amazing. Stay tuned!',
    'color: #8B5CF6; font-size: 14px;'
);

