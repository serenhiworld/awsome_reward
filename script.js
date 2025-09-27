// Mobile menu toggle
const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');

if (hamburger && navLinks) {
    hamburger.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        hamburger.classList.toggle('active');
    });
}

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const target = document.querySelector(this.getAttribute('href'));
        if (!target) {
            return;
        }
        e.preventDefault();
        target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
        navLinks?.classList.remove('active');
        hamburger?.classList.remove('active');
    });
});

// Header scroll effect
window.addEventListener('scroll', () => {
    const header = document.querySelector('.header');
    if (!header) return;
    if (window.scrollY > 80) {
        header.style.boxShadow = '0 12px 30px rgba(15, 23, 42, 0.08)';
    } else {
        header.style.boxShadow = 'none';
    }
});

// Intersection Observer animations
const observerOptions = {
    threshold: 0.15,
    rootMargin: '0px 0px -80px 0px'
};

const animatedElements = document.querySelectorAll('.product-card, .benefit-card, .testimonial-card, .referral-card, .step-card, .deal-card');

const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-in');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

animatedElements.forEach(el => observer.observe(el));

// Copy referral code helper
function showCopyToast(message) {
    const toast = document.createElement('div');
    toast.className = 'copy-toast';
    toast.textContent = message;
    document.body.appendChild(toast);
    requestAnimationFrame(() => toast.classList.add('visible'));
    setTimeout(() => {
        toast.classList.remove('visible');
        setTimeout(() => toast.remove(), 300);
    }, 1800);
}

async function copyText(text) {
    try {
        if (navigator.clipboard?.writeText) {
            await navigator.clipboard.writeText(text);
        } else {
            const tempInput = document.createElement('textarea');
            tempInput.value = text;
            document.body.appendChild(tempInput);
            tempInput.select();
            document.execCommand('copy');
            tempInput.remove();
        }
        showCopyToast('已复制推荐链接，快去领取奖励！');
    } catch (error) {
        console.error('复制失败', error);
        showCopyToast('复制失败，请手动复制链接');
    }
}

document.querySelectorAll('.copy-code-btn').forEach(button => {
    button.addEventListener('click', event => {
        const copyValue = event.currentTarget.getAttribute('data-copy') || event.currentTarget?.previousElementSibling?.textContent;
        if (copyValue) {
            copyText(copyValue.trim());
        }
    });
});

// Scroll-to-top button
const scrollToTop = document.createElement('button');
scrollToTop.innerHTML = '<i class="fas fa-arrow-up"></i>';
scrollToTop.className = 'scroll-to-top';
scrollToTop.setAttribute('aria-label', '返回顶部');
document.body.appendChild(scrollToTop);

scrollToTop.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

window.addEventListener('scroll', () => {
    if (window.scrollY > 400) {
        scrollToTop.classList.add('visible');
    } else {
        scrollToTop.classList.remove('visible');
    }
});

// Copy toast styles
const toastStyles = document.createElement('style');
toastStyles.textContent = `
    .copy-toast {
        position: fixed;
        bottom: 30px;
        left: 50%;
        transform: translate(-50%, 20px);
        background: rgba(15, 23, 42, 0.9);
        color: #fff;
        padding: 0.75rem 1.4rem;
        border-radius: 999px;
        font-weight: 500;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.2s ease, transform 0.2s ease;
        z-index: 999;
    }

    .copy-toast.visible {
        opacity: 1;
        transform: translate(-50%, 0);
    }
`;
document.head.appendChild(toastStyles);
