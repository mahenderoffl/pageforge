// PageForge - Premium Digital Bookstore JavaScript
// Developed by Mahender Banoth (IIT Patna)
// Instagram: @mahender_hustles | LinkedIn: Mahender Hustles

document.addEventListener("DOMContentLoaded", () => {
  console.log("🚀 PageForge loaded");
  console.log("📚 Developed by Mahender Banoth (IIT Patna)");
  console.log("📱 Follow: @mahender_hustles");
  
  // Initialize all interactive features
  initializeNavbar();
  initializeSearch();
  initializeBookCards();
  initializeCategoryCards();
  initializeAnimations();
  initializeFooter();
});

// Navbar functionality
function initializeNavbar() {
  const navbar = document.querySelector('.navbar');
  const menuToggle = document.querySelector('.menu-toggle');
  const navLinks = document.querySelector('.nav-links');
  
  // Navbar scroll effect
  window.addEventListener('scroll', () => {
    if (window.scrollY > 100) {
      navbar.style.background = 'rgba(0, 0, 0, 0.95)';
    } else {
      navbar.style.background = 'rgba(0, 0, 0, 0.8)';
    }
  });
  
  // Mobile menu toggle
  if (menuToggle && navLinks) {
    menuToggle.addEventListener('click', () => {
      navLinks.classList.toggle('active');
      menuToggle.classList.toggle('active');
    });
  }
}

// Search functionality
function initializeSearch() {
  const searchInput = document.querySelector('.search-input');
  const searchBtn = document.querySelector('.search-btn');
  
  if (searchInput && searchBtn) {
    // Search on Enter key
    searchInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        performSearch(searchInput.value);
      }
    });
    
    // Search on button click
    searchBtn.addEventListener('click', () => {
      performSearch(searchInput.value);
    });
  }
}

function performSearch(query) {
  if (query.trim()) {
    console.log('Searching for:', query);
    // Here you can add actual search functionality
    // For now, we'll just show an alert
    alert(`Searching for: "${query}"`);
  }
}

// Book card interactions
function initializeBookCards() {
  const bookCards = document.querySelectorAll('.book-card');
  
  bookCards.forEach(card => {
    const previewBtn = card.querySelector('.preview-btn');
    const addBtn = card.querySelector('.add-btn');
    
    if (previewBtn) {
      previewBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        const bookTitle = card.querySelector('.book-title').textContent;
        showBookPreview(bookTitle);
      });
    }
    
    if (addBtn) {
      addBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        const bookTitle = card.querySelector('.book-title').textContent;
        addToLibrary(bookTitle);
      });
    }
  });
}

function showBookPreview(title) {
  console.log('Previewing book:', title);
  alert(`Preview for "${title}" - Feature coming soon!`);
}

function addToLibrary(title) {
  console.log('Adding to library:', title);
  
  // Update cart count
  const cartCount = document.querySelector('.cart-count');
  if (cartCount) {
    let count = parseInt(cartCount.textContent) || 0;
    cartCount.textContent = count + 1;
    
    // Add animation
    cartCount.style.transform = 'scale(1.3)';
    setTimeout(() => {
      cartCount.style.transform = 'scale(1)';
    }, 200);
  }
  
  // Show success message
  showNotification(`"${title}" added to your library!`);
}

// Category card interactions
function initializeCategoryCards() {
  const categoryCards = document.querySelectorAll('.category-card');
  
  categoryCards.forEach(card => {
    card.addEventListener('click', () => {
      const categoryTitle = card.querySelector('h3').textContent;
      navigateToCategory(categoryTitle);
    });
  });
}

function navigateToCategory(category) {
  console.log('Navigating to category:', category);
  alert(`Browsing ${category} - Feature coming soon!`);
}

// Animation observers
function initializeAnimations() {
  // Intersection Observer for scroll animations
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      }
    });
  }, observerOptions);
  
  // Observe all animatable elements
  const animatableElements = document.querySelectorAll('.book-card, .category-card, .section-header');
  animatableElements.forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
  });
}

// Footer functionality
function initializeFooter() {
  const newsletterForm = document.querySelector('.newsletter-form');
  
  if (newsletterForm) {
    newsletterForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const email = newsletterForm.querySelector('input[type="email"]').value;
      handleNewsletterSignup(email);
    });
  }
  
  // Animate footer stats on scroll
  const footerStats = document.querySelectorAll('.footer-stats .stat-number');
  const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateNumber(entry.target);
        statsObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });
  
  footerStats.forEach(stat => statsObserver.observe(stat));
}

function handleNewsletterSignup(email) {
  if (email && isValidEmail(email)) {
    // Simulate newsletter signup
    showNotification('Successfully subscribed to our newsletter!');
    
    // Clear the input
    const input = document.querySelector('.newsletter-input input');
    if (input) {
      input.value = '';
    }
    
    // Add success state
    const button = document.querySelector('.newsletter-input button');
    if (button) {
      const originalHTML = button.innerHTML;
      button.innerHTML = '<i class="fas fa-check"></i>';
      button.style.background = '#28a745';
      
      setTimeout(() => {
        button.innerHTML = originalHTML;
        button.style.background = '';
      }, 2000);
    }
  } else {
    showNotification('Please enter a valid email address.', 'error');
  }
}

function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

function animateNumber(element) {
  const finalNumber = element.textContent;
  const numericValue = parseInt(finalNumber.replace(/[^\d]/g, ''));
  const suffix = finalNumber.replace(/[\d]/g, '');
  const duration = 2000;
  const stepTime = 50;
  const steps = duration / stepTime;
  const increment = numericValue / steps;
  
  let current = 0;
  const timer = setInterval(() => {
    current += increment;
    if (current >= numericValue) {
      current = numericValue;
      clearInterval(timer);
    }
    
    if (numericValue >= 1000) {
      element.textContent = Math.floor(current / 1000) + 'K' + suffix.replace('K', '');
    } else {
      element.textContent = Math.floor(current) + suffix;
    }
  }, stepTime);
}

// Utility function for notifications
function showNotification(message, type = 'success') {
  // Create notification element
  const notification = document.createElement('div');
  notification.className = 'notification';
  notification.textContent = message;
  
  // Style the notification
  const bgColor = type === 'error' ? 
    'linear-gradient(135deg, #ff3b30 0%, #ff6b6b 100%)' : 
    'linear-gradient(135deg, #007aff 0%, #5856d6 100%)';
    
  Object.assign(notification.style, {
    position: 'fixed',
    top: '100px',
    right: '20px',
    background: bgColor,
    color: 'white',
    padding: '1rem 2rem',
    borderRadius: '12px',
    boxShadow: '0 8px 32px rgba(0, 0, 0, 0.2)',
    zIndex: '10000',
    transform: 'translateX(400px)',
    transition: 'transform 0.3s ease',
    fontSize: '0.9rem',
    fontWeight: '500'
  });
  
  document.body.appendChild(notification);
  
  // Animate in
  setTimeout(() => {
    notification.style.transform = 'translateX(0)';
  }, 100);
  
  // Animate out and remove
  setTimeout(() => {
    notification.style.transform = 'translateX(400px)';
    setTimeout(() => {
      document.body.removeChild(notification);
    }, 300);
  }, 3000);
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      target.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  });
});

// Performance optimization: Lazy loading for images
function initializeLazyLoading() {
  const images = document.querySelectorAll('img[data-src]');
  const imageObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        img.src = img.dataset.src;
        img.removeAttribute('data-src');
        imageObserver.unobserve(img);
      }
    });
  });
  
  images.forEach(img => imageObserver.observe(img));
}

// Initialize lazy loading
initializeLazyLoading();

// Authentication and User Menu Functions
function toggleUserMenu() {
  const dropdown = document.getElementById('userDropdown');
  if (dropdown) {
    dropdown.classList.toggle('show');
  }
}

function toggleSearch() {
  const searchOverlay = document.getElementById('searchOverlay');
  const searchInput = document.getElementById('searchInput');
  
  if (searchOverlay) {
    searchOverlay.classList.toggle('show');
    if (searchOverlay.classList.contains('show') && searchInput) {
      setTimeout(() => searchInput.focus(), 100);
    }
  }
}

function toggleMobileMenu() {
  const navLinks = document.querySelector('.nav-links');
  const menuToggle = document.querySelector('.menu-toggle');
  
  if (navLinks && menuToggle) {
    navLinks.classList.toggle('active');
    menuToggle.classList.toggle('active');
  }
}

// Cart Management Functions
async function updateCartQuantity(bookId, quantity) {
  try {
    const response = await fetch('/update_cart', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        book_id: bookId,
        quantity: quantity
      })
    });
    
    const data = await response.json();
    
    if (data.success) {
      updateCartCount(data.cart_count);
      showNotification(data.message, 'success');
      
      // Update cart UI if on cart page
      if (window.location.pathname.includes('/cart')) {
        location.reload();
      }
    } else {
      showNotification(data.message, 'error');
    }
  } catch (error) {
    console.error('Error updating cart:', error);
    showNotification('Failed to update cart', 'error');
  }
}

async function removeFromCart(bookId) {
  try {
    const response = await fetch('/remove_from_cart', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        book_id: bookId
      })
    });
    
    const data = await response.json();
    
    if (data.success) {
      updateCartCount(data.cart_count);
      showNotification(data.message, 'success');
      
      // Remove item from cart UI
      const cartItem = document.querySelector(`[data-book-id="${bookId}"]`);
      if (cartItem) {
        cartItem.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => {
          cartItem.remove();
          updateCartTotal();
        }, 300);
      }
    } else {
      showNotification(data.message, 'error');
    }
  } catch (error) {
    console.error('Error removing from cart:', error);
    showNotification('Failed to remove item', 'error');
  }
}

function updateCartCount(count) {
  const cartCountElement = document.getElementById('cartCount');
  if (cartCountElement) {
    cartCountElement.textContent = count;
    
    // Add bounce animation
    cartCountElement.style.animation = 'bounce 0.3s ease';
    setTimeout(() => {
      cartCountElement.style.animation = '';
    }, 300);
  }
}

function updateCartTotal() {
  const cartItems = document.querySelectorAll('.cart-item');
  let total = 0;
  
  cartItems.forEach(item => {
    const price = parseFloat(item.querySelector('.item-price').dataset.price);
    const quantity = parseInt(item.querySelector('.quantity-input').value);
    total += price * quantity;
  });
  
  const totalElement = document.querySelector('.cart-total');
  if (totalElement) {
    totalElement.textContent = `$${total.toFixed(2)}`;
  }
}

// Admin Dashboard Functions
function confirmDelete(type, id, name) {
  return confirm(`Are you sure you want to delete this ${type}: "${name}"? This action cannot be undone.`);
}

// Form Validation Functions
function validateBookForm() {
  const form = document.getElementById('bookForm');
  if (!form) return true;
  
  const requiredFields = form.querySelectorAll('[required]');
  let isValid = true;
  
  requiredFields.forEach(field => {
    if (!field.value.trim()) {
      field.classList.add('error');
      isValid = false;
    } else {
      field.classList.remove('error');
    }
  });
  
  // Validate price
  const priceField = document.getElementById('price');
  if (priceField && parseFloat(priceField.value) < 0) {
    priceField.classList.add('error');
    isValid = false;
  }
  
  // Validate stock
  const stockField = document.getElementById('stock');
  if (stockField && parseInt(stockField.value) < 0) {
    stockField.classList.add('error');
    isValid = false;
  }
  
  return isValid;
}

// Enhanced Book Card Interactions
function initializeBookCardInteractions() {
  const bookCards = document.querySelectorAll('.book-card, .library-book-card');
  
  bookCards.forEach(card => {
    // Add to cart button
    const addToCartBtn = card.querySelector('.add-to-cart');
    if (addToCartBtn) {
      addToCartBtn.addEventListener('click', (e) => {
        e.preventDefault();
        const bookId = card.dataset.bookId || addToCartBtn.dataset.bookId;
        if (bookId) {
          addToCart(bookId);
        }
      });
    }
    
    // Quantity controls
    const quantityControls = card.querySelectorAll('.quantity-btn');
    quantityControls.forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const input = card.querySelector('.quantity-input');
        const bookId = card.dataset.bookId;
        const action = btn.dataset.action;
        
        if (input && bookId) {
          let quantity = parseInt(input.value);
          
          if (action === 'increase') {
            quantity++;
          } else if (action === 'decrease' && quantity > 1) {
            quantity--;
          }
          
          input.value = quantity;
          updateCartQuantity(bookId, quantity);
        }
      });
    });
    
    // Remove from cart button
    const removeBtn = card.querySelector('.remove-item');
    if (removeBtn) {
      removeBtn.addEventListener('click', (e) => {
        e.preventDefault();
        const bookId = card.dataset.bookId;
        if (bookId && confirm('Remove this item from cart?')) {
          removeFromCart(bookId);
        }
      });
    }
  });
}

// Close dropdowns when clicking outside
document.addEventListener('click', (e) => {
  const userMenu = document.querySelector('.user-menu');
  const searchOverlay = document.getElementById('searchOverlay');
  
  // Close user dropdown
  if (userMenu && !userMenu.contains(e.target)) {
    const dropdown = document.getElementById('userDropdown');
    if (dropdown) {
      dropdown.classList.remove('show');
    }
  }
  
  // Close search overlay when clicking outside search container
  if (searchOverlay && e.target === searchOverlay) {
    searchOverlay.classList.remove('show');
  }
});

// Initialize cart functionality on page load
document.addEventListener('DOMContentLoaded', () => {
  initializeBookCardInteractions();
  
  // Load cart count on page load
  fetch('/get_cart_count')
    .then(response => response.json())
    .then(data => updateCartCount(data.cart_count))
    .catch(error => console.error('Error loading cart count:', error));
});

// CSS animations for cart actions
const style = document.createElement('style');
style.textContent = `
  @keyframes fadeOut {
    from { opacity: 1; transform: translateX(0); }
    to { opacity: 0; transform: translateX(-100%); }
  }
  
  @keyframes bounce {
    0%, 20%, 50%, 80%, 100% { transform: scale(1); }
    40% { transform: scale(1.2); }
    60% { transform: scale(1.1); }
  }
  
  .cart-item {
    transition: all 0.3s ease;
  }
  
  .error {
    border-color: #ff453a !important;
    box-shadow: 0 0 0 3px rgba(255, 69, 58, 0.1) !important;
  }
`;
document.head.appendChild(style);

// Auto-hide flash messages
document.addEventListener('DOMContentLoaded', () => {
  const flashMessages = document.querySelectorAll('.flash-message');
  
  flashMessages.forEach(message => {
    // Auto-hide after 5 seconds
    setTimeout(() => {
      if (message.parentElement) {
        message.style.animation = 'fadeOut 0.3s ease';
        setTimeout(() => {
          message.remove();
        }, 300);
      }
    }, 5000);
  });
});

// ===== GLOBAL POLICY MODAL FUNCTIONALITY =====
// Policy modal function - available site-wide
function showPolicy(policyType) {
    const policies = {
        privacy: {
            title: 'Privacy Policy',
            icon: 'fas fa-shield-alt',
            content: `
                <h3>📍 Information We Collect</h3>
                <p>We collect information you provide directly, such as account details and purchase history. This includes your name, email address, payment information, and reading preferences.</p>
                
                <h3>🔒 How We Use Information</h3>
                <p>Your information is used to provide services, process transactions, improve user experience, and send you relevant book recommendations. We never sell your personal data to third parties.</p>
                
                <h3>🛡️ Data Protection</h3>
                <p>We implement industry-standard security measures including encryption, secure servers, and regular security audits to protect your personal information.</p>
                
                <h3>🍪 Cookies & Tracking</h3>
                <p>We use cookies to enhance your browsing experience, remember your preferences, and analyze site usage. You can manage cookie preferences in your browser settings.</p>
                
                <h3>📧 Contact</h3>
                <p>For privacy concerns or data requests, contact us at <strong>privacy@pageforge.com</strong> or through our support center.</p>
                
                <h3>📅 Last Updated</h3>
                <p>This policy was last updated on June 27, 2025. We will notify users of any significant changes.</p>
            `
        },
        terms: {
            title: 'Terms of Service',
            icon: 'fas fa-file-contract',
            content: `
                <h3>📋 Service Agreement</h3>
                <p>By using PageForge, you agree to these terms and our acceptable use policy. These terms govern your access to and use of our digital bookstore services.</p>
                
                <h3>📚 Digital Content</h3>
                <p>Books purchased are licensed for personal use only. Sharing, redistribution, or commercial use is prohibited. You retain access to purchased content as long as the service operates.</p>
                
                <h3>💳 Payment Terms</h3>
                <p>All prices are in Indian Rupees (₹) including applicable GST. All sales are final unless covered by our refund policy. Payment processing is secured through trusted providers.</p>
                
                <h3>👤 Account Responsibility</h3>
                <p>You are responsible for maintaining account security, including password protection. Notify us immediately of any unauthorized access.</p>
                
                <h3>⚖️ Limitation of Liability</h3>
                <p>Service is provided "as is" with standard limitations on liability. We strive for 99.9% uptime but cannot guarantee uninterrupted service.</p>
                
                <h3>📞 Termination</h3>
                <p>Either party may terminate the agreement. Upon termination, access to purchased content may be limited based on licensing agreements.</p>
            `
        },
        cookies: {
            title: 'Cookie Policy',
            icon: 'fas fa-cookie-bite',
            content: `
                <h3>🍪 What Are Cookies</h3>
                <p>Cookies are small text files stored on your device to enhance your browsing experience, remember preferences, and provide personalized content.</p>
                
                <h3>📊 Types We Use</h3>
                <p><strong>Essential Cookies:</strong> Required for basic site functionality like shopping cart and user authentication.<br>
                <strong>Analytics Cookies:</strong> Help us understand how visitors use our site to improve performance.<br>
                <strong>Preference Cookies:</strong> Remember your settings like theme, language, and reading preferences.<br>
                <strong>Marketing Cookies:</strong> Used to show relevant book recommendations and promotions.</p>
                
                <h3>⚙️ Managing Cookies</h3>
                <p>You can control cookies through your browser settings. Note that disabling certain cookies may limit website functionality, particularly for user accounts and personalization.</p>
                
                <h3>🔄 Cookie Retention</h3>
                <p>Session cookies are deleted when you close your browser. Persistent cookies remain for specific periods based on their purpose, typically 30 days to 2 years.</p>
                
                <h3>🌐 Third-Party Cookies</h3>
                <p>We may use trusted third-party services for analytics and payment processing, which may set their own cookies subject to their privacy policies.</p>
            `
        },
        support: {
            title: 'Accessibility Statement',
            icon: 'fas fa-universal-access',
            content: `
                <h3>♿ Our Commitment</h3>
                <p>PageForge is committed to providing an accessible digital reading experience for all users, including those with disabilities. We strive to meet WCAG 2.1 AA standards.</p>
                
                <h3>🔧 Accessibility Features</h3>
                <p><strong>Screen Reader Support:</strong> Compatible with popular screen readers like NVDA, JAWS, and VoiceOver.<br>
                <strong>Keyboard Navigation:</strong> Full site navigation without a mouse.<br>
                <strong>High Contrast:</strong> Enhanced visual contrast for better readability.<br>
                <strong>Text Scaling:</strong> Support for browser zoom up to 200%.<br>
                <strong>Alt Text:</strong> Descriptive text for all images and graphics.</p>
                
                <h3>📱 Reading Accessibility</h3>
                <p>Our reading app includes adjustable font sizes, dyslexia-friendly fonts, dark mode for light sensitivity, and customizable line spacing and margins.</p>
                
                <h3>🆘 Need Help?</h3>
                <p>If you encounter accessibility barriers, please contact our support team at <strong>accessibility@pageforge.com</strong>. We're committed to resolving issues promptly.</p>
                
                <h3>🔄 Ongoing Improvements</h3>
                <p>We regularly audit our platform and implement improvements based on user feedback and accessibility guidelines.</p>
            `
        },
        dmca: {
            title: 'DMCA Policy',
            icon: 'fas fa-copyright',
            content: `
                <h3>©️ Copyright Protection</h3>
                <p>PageForge respects intellectual property rights and complies with the Digital Millennium Copyright Act (DMCA). We promptly address copyright infringement claims.</p>
                
                <h3>📝 Filing a DMCA Notice</h3>
                <p>To file a copyright infringement claim, send a written notice to <strong>dmca@pageforge.com</strong> including:</p>
                <p>• Your contact information and electronic signature<br>
                • Identification of the copyrighted work<br>
                • Location of the infringing material on our site<br>
                • Good faith statement that use is unauthorized<br>
                • Statement of accuracy under penalty of perjury</p>
                
                <h3>🔍 Review Process</h3>
                <p>We investigate all valid DMCA claims within 24-48 hours and take appropriate action, including content removal when necessary. Rights holders will be notified of actions taken.</p>
                
                <h3>⚖️ Counter-Notices</h3>
                <p>Users may file counter-notices if they believe content was removed in error. Counter-notices must include similar information and be sent to the same email address.</p>
                
                <h3>📚 Repeat Infringers</h3>
                <p>We maintain a policy of terminating accounts of repeat copyright infringers in accordance with DMCA requirements.</p>
            `
        }
    };

    const policy = policies[policyType];
    if (!policy) {
        console.warn(`Policy type "${policyType}" not found`);
        return;
    }

    // Create modal
    const modal = document.createElement('div');
    modal.className = 'policy-modal';
    modal.innerHTML = `
        <div class="policy-modal-content">
            <div class="policy-modal-header">
                <h2><i class="${policy.icon}"></i> ${policy.title}</h2>
                <button class="policy-close" onclick="closePolicy()" aria-label="Close policy modal">&times;</button>
            </div>
            <div class="policy-modal-body">
                ${policy.content}
            </div>
            <div class="policy-modal-footer">
                <button class="btn-close" onclick="closePolicy()">
                    <i class="fas fa-times"></i>
                    Close
                </button>
            </div>
        </div>
    `;

    // Add modal styles if not already added
    if (!document.getElementById('policy-modal-styles')) {
        const styleSheet = document.createElement('style');
        styleSheet.id = 'policy-modal-styles';
        styleSheet.textContent = `
            .policy-modal {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.85);
                z-index: 10000;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 1rem;
                backdrop-filter: blur(8px);
                -webkit-backdrop-filter: blur(8px);
                animation: modalFadeIn 0.3s ease;
            }
            
            @keyframes modalFadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            
            .policy-modal-content {
                background: var(--background-secondary, #1a1a1a);
                border: 1px solid var(--border-color, rgba(255, 255, 255, 0.1));
                border-radius: var(--radius-lg, 20px);
                max-width: 700px;
                width: 100%;
                max-height: 85vh;
                overflow-y: auto;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
                animation: modalSlideIn 0.3s ease;
            }
            
            @keyframes modalSlideIn {
                from { 
                    opacity: 0; 
                    transform: translateY(-20px) scale(0.95); 
                }
                to { 
                    opacity: 1; 
                    transform: translateY(0) scale(1); 
                }
            }
            
            .policy-modal-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 2rem;
                border-bottom: 1px solid var(--border-color, rgba(255, 255, 255, 0.1));
                background: rgba(0, 122, 255, 0.05);
            }
            
            .policy-modal-header h2 {
                margin: 0;
                color: var(--text-primary, #ffffff);
                display: flex;
                align-items: center;
                gap: 0.75rem;
                font-size: 1.4rem;
                font-weight: 600;
            }
            
            .policy-modal-header i {
                color: var(--accent-color, #007aff);
                font-size: 1.2rem;
            }
            
            .policy-close {
                background: none;
                border: none;
                font-size: 2rem;
                color: var(--text-secondary, #a0a0a0);
                cursor: pointer;
                padding: 0.5rem;
                line-height: 1;
                border-radius: 50%;
                transition: all 0.2s ease;
                display: flex;
                align-items: center;
                justify-content: center;
                width: 44px;
                height: 44px;
            }
            
            .policy-close:hover {
                color: var(--text-primary, #ffffff);
                background: rgba(255, 255, 255, 0.1);
                transform: scale(1.1);
            }
            
            .policy-modal-body {
                padding: 2rem;
                color: var(--text-secondary, #a0a0a0);
                line-height: 1.7;
                font-size: 0.95rem;
            }
            
            .policy-modal-body h3 {
                color: var(--text-primary, #ffffff);
                margin: 2rem 0 1rem 0;
                font-size: 1.15rem;
                font-weight: 600;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            }
            
            .policy-modal-body h3:first-child {
                margin-top: 0;
            }
            
            .policy-modal-body p {
                margin: 0.75rem 0;
                line-height: 1.6;
            }
            
            .policy-modal-body strong {
                color: var(--accent-color, #007aff);
                font-weight: 600;
            }
            
            .policy-modal-footer {
                padding: 1.5rem 2rem;
                border-top: 1px solid var(--border-color, rgba(255, 255, 255, 0.1));
                text-align: right;
                background: rgba(0, 0, 0, 0.2);
            }
            
            .btn-close {
                background: var(--accent-gradient, linear-gradient(135deg, #007aff 0%, #5856d6 100%));
                color: white;
                border: none;
                padding: 0.875rem 1.5rem;
                border-radius: var(--radius-md, 12px);
                cursor: pointer;
                font-weight: 600;
                font-size: 0.95rem;
                transition: all 0.3s ease;
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
                box-shadow: 0 4px 15px rgba(0, 122, 255, 0.3);
            }
            
            .btn-close:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0, 122, 255, 0.4);
            }
            
            .btn-close:active {
                transform: translateY(0);
            }
            
            /* Mobile responsive */
            @media (max-width: 768px) {
                .policy-modal {
                    padding: 0.5rem;
                    align-items: flex-start;
                    padding-top: 2rem;
                }
                
                .policy-modal-content {
                    max-height: 90vh;
                    border-radius: var(--radius-md, 12px);
                }
                
                .policy-modal-header,
                .policy-modal-body,
                .policy-modal-footer {
                    padding: 1.5rem;
                }
                
                .policy-modal-header h2 {
                    font-size: 1.2rem;
                }
                
                .policy-modal-body {
                    font-size: 0.9rem;
                }
            }
        `;
        document.head.appendChild(styleSheet);
    }

    // Add modal to page
    document.body.appendChild(modal);
    
    // Prevent background scrolling
    document.body.style.overflow = 'hidden';
    
    // Animate in
    modal.style.opacity = '0';
    setTimeout(() => {
        modal.style.transition = 'opacity 0.3s ease';
        modal.style.opacity = '1';
    }, 10);

    // Close on escape key
    const handleEscape = (e) => {
        if (e.key === 'Escape') {
            closePolicy();
            document.removeEventListener('keydown', handleEscape);
        }
    };
    document.addEventListener('keydown', handleEscape);

    // Close on background click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closePolicy();
        }
    });
}

// Close policy modal function
function closePolicy() {
    const modal = document.querySelector('.policy-modal');
    if (modal) {
        modal.style.opacity = '0';
        setTimeout(() => {
            if (modal.parentNode) {
                modal.parentNode.removeChild(modal);
            }
            // Restore background scrolling
            document.body.style.overflow = '';
        }, 300);
    }
}

// ===== SUPPORT MODAL FUNCTIONALITY =====
// Support modal function - available site-wide
function showSupportModal(supportType) {
    const supportModals = {
        help: {
            title: 'Help Center',
            icon: 'fas fa-question-circle',
            content: `
                <h3>🆘 Frequently Asked Questions</h3>
                <p><strong>How do I download my purchased books?</strong><br>
                Visit your library, hover over any book, and click the "Download" button. Books will be available in PDF and EPUB formats.</p>
                
                <p><strong>Can I read books offline?</strong><br>
                Yes! Once downloaded, you can read your books anytime without an internet connection using our mobile apps or any compatible reader.</p>
                
                <p><strong>How many devices can I use?</strong><br>
                Your account supports up to 6 devices simultaneously. You can manage your devices in Account Settings.</p>
                
                <h3>📚 Reading Issues</h3>
                <p><strong>Book won't open:</strong> Try refreshing the page or clearing your browser cache. For mobile apps, restart the application.</p>
                
                <p><strong>Missing books:</strong> Check your library and ensure you're logged into the correct account. Contact support if books are still missing.</p>
                
                <h3>💳 Payment & Billing</h3>
                <p><strong>Payment failed:</strong> Verify your payment details and try again. We accept all major credit cards and UPI payments.</p>
                
                <p><strong>Refund requests:</strong> Visit our Refund Policy or contact support within 7 days of purchase.</p>
                
                <h3>📞 Still Need Help?</h3>
                <p>Contact our support team at <strong>support@pageforge.com</strong> or use the live chat feature (9 AM - 6 PM IST).</p>
            `
        },
        contact: {
            title: 'Contact Us',
            icon: 'fas fa-envelope',
            content: `
                <h3>📞 Get in Touch</h3>
                <p>Our dedicated support team is here to help you with any questions or issues you may have.</p>
                
                <h3>📧 Email Support</h3>
                <p><strong>General Support:</strong> support@pageforge.com<br>
                <strong>Technical Issues:</strong> tech@pageforge.com<br>
                <strong>Billing Questions:</strong> billing@pageforge.com<br>
                <strong>Partnership Inquiries:</strong> partnerships@pageforge.com</p>
                
                <h3>💬 Live Chat</h3>
                <p><strong>Available:</strong> Monday - Friday, 9:00 AM - 6:00 PM IST<br>
                <strong>Average Response:</strong> Under 2 minutes<br>
                <strong>Languages:</strong> English, Hindi</p>
                
                <h3>📱 Social Media</h3>
                <p>Follow us for updates and quick responses:<br>
                <strong>Instagram:</strong> @mahender_hustles<br>
                <strong>LinkedIn:</strong> Mahender Hustles<br>
                <strong>GitHub:</strong> mahenderoffl</p>
                
                <h3>⏰ Response Times</h3>
                <p><strong>Email:</strong> Within 24 hours<br>
                <strong>Technical Issues:</strong> Within 4 hours<br>
                <strong>Billing Queries:</strong> Within 12 hours</p>
                
                <div style="margin-top: 1.5rem; padding: 1rem; background: rgba(0, 122, 255, 0.1); border-radius: 8px;">
                    <p><strong>🚀 Quick Tip:</strong> Include your account email and order details for faster assistance!</p>
                </div>
            `
        },
        apps: {
            title: 'Reading Apps',
            icon: 'fas fa-mobile-alt',
            content: `
                <h3>📱 PageForge Mobile Apps</h3>
                <p>Enjoy your digital library anywhere with our premium reading apps designed for the best reading experience.</p>
                
                <h3>🍎 iOS App Features</h3>
                <p><strong>• Seamless Sync:</strong> Your library, bookmarks, and reading progress sync across all devices<br>
                <strong>• Dark Mode:</strong> Comfortable reading in any lighting condition<br>
                <strong>• Offline Reading:</strong> Download books for offline access<br>
                <strong>• Customizable:</strong> Adjust fonts, spacing, and background colors<br>
                <strong>• Voice Narration:</strong> Text-to-speech functionality</p>
                
                <h3>🤖 Android App Features</h3>
                <p><strong>• Material Design:</strong> Beautiful, intuitive interface<br>
                <strong>• Smart Recommendations:</strong> Discover new books based on your preferences<br>
                <strong>• Multiple Formats:</strong> Support for EPUB, PDF, and more<br>
                <strong>• Parental Controls:</strong> Safe reading environment for all ages<br>
                <strong>• Cloud Backup:</strong> Your data is always secure</p>
                
                <h3>💻 Desktop Readers</h3>
                <p><strong>• Web Reader:</strong> Full-featured reading directly in your browser<br>
                <strong>• Windows App:</strong> Native application for Windows 10/11<br>
                <strong>• macOS App:</strong> Optimized for Mac users<br>
                <strong>• Linux Support:</strong> Compatible with major Linux distributions</p>
                
                <h3>🔗 Download Links</h3>
                <div style="margin-top: 1rem; padding: 1rem; background: rgba(0, 122, 255, 0.05); border-radius: 8px;">
                    <p><strong>📱 Mobile Apps Coming Soon!</strong><br>
                    We're currently developing our mobile applications. Sign up for notifications to be the first to know when they're available!</p>
                    
                    <p><strong>🌐 Web Reader:</strong> Available now in your browser at pageforge.com</p>
                </div>
            `
        },
        devices: {
            title: 'Device Support',
            icon: 'fas fa-laptop',
            content: `
                <h3>📱 Supported Devices</h3>
                <p>PageForge works seamlessly across all your favorite devices for the ultimate reading experience.</p>
                
                <h3>💻 Computer & Laptop</h3>
                <p><strong>• Windows:</strong> Windows 10 or later, any modern browser<br>
                <strong>• macOS:</strong> macOS 10.14 or later, Safari/Chrome/Firefox<br>
                <strong>• Linux:</strong> Ubuntu 18.04+, Fedora 30+, any Chromium-based browser<br>
                <strong>• Chromebook:</strong> Chrome OS with Google Play Store access</p>
                
                <h3>📱 Mobile Devices</h3>
                <p><strong>• iPhone/iPad:</strong> iOS 13.0 or later<br>
                <strong>• Android:</strong> Android 8.0 (API level 26) or later<br>
                <strong>• Android Tablets:</strong> Full tablet optimization<br>
                <strong>• Amazon Fire Tablet:</strong> Fire OS 6.0 or later</p>
                
                <h3>📖 E-Readers</h3>
                <p><strong>• Kindle:</strong> Download EPUB files and convert using Calibre<br>
                <strong>• Kobo:</strong> Direct EPUB support<br>
                <strong>• Other E-Readers:</strong> Most EPUB-compatible devices</p>
                
                <h3>📺 Smart Devices</h3>
                <p><strong>• Smart TVs:</strong> Android TV, Apple TV (web browser)<br>
                <strong>• Gaming Consoles:</strong> PlayStation, Xbox (web browser)<br>
                <strong>• Streaming Devices:</strong> Chrome, Roku (via mobile app)</p>
                
                <h3>⚙️ System Requirements</h3>
                <p><strong>• Internet:</strong> Required for initial download and sync<br>
                <strong>• Storage:</strong> 100MB minimum, varies by library size<br>
                <strong>• RAM:</strong> 2GB minimum for smooth performance<br>
                <strong>• Browser:</strong> Latest version of Chrome, Firefox, Safari, or Edge</p>
                
                <h3>🔧 Troubleshooting</h3>
                <p>Having issues? Try these quick fixes:<br>
                • Clear browser cache and cookies<br>
                • Update your browser to the latest version<br>
                • Disable ad blockers temporarily<br>
                • Check your internet connection</p>
            `
        },
        account: {
            title: 'Account Settings',
            icon: 'fas fa-user-cog',
            content: `
                <h3>👤 Manage Your Account</h3>
                <p>Take control of your PageForge experience with these account management options.</p>
                
                <h3>🔐 Security Settings</h3>
                <p><strong>• Change Password:</strong> Update your password for enhanced security<br>
                <strong>• Two-Factor Authentication:</strong> Add an extra layer of protection<br>
                <strong>• Login History:</strong> Monitor recent account activity<br>
                <strong>• Device Management:</strong> View and manage authorized devices<br>
                <strong>• Privacy Controls:</strong> Manage data sharing preferences</p>
                
                <h3>📧 Communication Preferences</h3>
                <p><strong>• Email Notifications:</strong> Control when we contact you<br>
                <strong>• Newsletter:</strong> Stay updated with new releases and offers<br>
                <strong>• Reading Reminders:</strong> Get notified about unfinished books<br>
                <strong>• Recommendations:</strong> Personalized book suggestions<br>
                <strong>• Promotional Offers:</strong> Special deals and discounts</p>
                
                <h3>📱 Reading Preferences</h3>
                <p><strong>• Default Format:</strong> Choose EPUB or PDF as default<br>
                <strong>• Auto-Download:</strong> Automatically download purchased books<br>
                <strong>• Cloud Sync:</strong> Sync reading progress across devices<br>
                <strong>• Parental Controls:</strong> Restrict access to age-appropriate content<br>
                <strong>• Language:</strong> Set your preferred interface language</p>
                
                <h3>💳 Payment & Billing</h3>
                <p><strong>• Payment Methods:</strong> Manage your saved payment options<br>
                <strong>• Purchase History:</strong> View all your transactions<br>
                <strong>• Billing Address:</strong> Update your billing information<br>
                <strong>• Subscription:</strong> Manage premium subscriptions<br>
                <strong>• Auto-Renewal:</strong> Control automatic payments</p>
                
                <h3>📊 Privacy & Data</h3>
                <p><strong>• Data Export:</strong> Download your account data<br>
                <strong>• Reading Analytics:</strong> View your reading statistics<br>
                <strong>• Data Deletion:</strong> Request account data removal<br>
                <strong>• Cookie Preferences:</strong> Manage tracking preferences</p>
                
                <div style="margin-top: 1.5rem; padding: 1rem; background: rgba(255, 193, 7, 0.1); border-radius: 8px;">
                    <p><strong>⚠️ Account Access:</strong> Log into your account to access these settings. Need help? Contact our support team!</p>
                </div>
            `
        },
        gifts: {
            title: 'Gift Cards',
            icon: 'fas fa-gift',
            content: `
                <h3>🎁 PageForge Gift Cards</h3>
                <p>Share the joy of reading with digital gift cards! Perfect for book lovers, students, and anyone who enjoys great literature.</p>
                
                <h3>💝 Why Choose Gift Cards?</h3>
                <p><strong>• Instant Delivery:</strong> Delivered via email within minutes<br>
                <strong>• Flexible Amounts:</strong> Choose from ₹500 to ₹10,000<br>
                <strong>• No Expiry:</strong> Gift cards never expire<br>
                <strong>• Personal Touch:</strong> Add custom messages<br>
                <strong>• Easy Redemption:</strong> Simple one-click activation</p>
                
                <h3>🛒 Available Denominations</h3>
                <p><strong>• ₹500</strong> - Perfect for a few premium books<br>
                <strong>• ₹1,000</strong> - Great for building a small library<br>
                <strong>• ₹2,500</strong> - Ideal for academic collections<br>
                <strong>• ₹5,000</strong> - Perfect for avid readers<br>
                <strong>• ₹10,000</strong> - Ultimate book lover's package<br>
                <strong>• Custom Amount</strong> - Choose any amount between ₹100-₹10,000</p>
                
                <h3>🎯 Perfect Occasions</h3>
                <p><strong>• Birthdays & Anniversaries</strong><br>
                <strong>• Graduation & Academic Achievements</strong><br>
                <strong>• Festival Celebrations</strong><br>
                <strong>• Corporate Rewards</strong><br>
                <strong>• Teacher Appreciation</strong><br>
                <strong>• Holiday Gifts</strong></p>
                
                <h3>📝 How to Purchase</h3>
                <p>1. <strong>Choose Amount:</strong> Select or enter your desired value<br>
                2. <strong>Personalize:</strong> Add recipient details and custom message<br>
                3. <strong>Payment:</strong> Complete purchase with secure payment<br>
                4. <strong>Delivery:</strong> Gift card sent instantly via email<br>
                5. <strong>Redemption:</strong> Recipient enters code at checkout</p>
                
                <h3>🔧 Gift Card Management</h3>
                <p><strong>• Check Balance:</strong> View remaining credit anytime<br>
                <strong>• Transaction History:</strong> Track gift card usage<br>
                <strong>• Multiple Cards:</strong> Combine balances for larger purchases<br>
                <strong>• Partial Use:</strong> Use gift cards for partial payments<br>
                <strong>• Account Credit:</strong> Add gift card value to account wallet</p>
                
                <h3>❓ Frequently Asked Questions</h3>
                <p><strong>Q: Do gift cards expire?</strong><br>
                A: No, PageForge gift cards never expire!</p>
                
                <p><strong>Q: Can I use multiple gift cards?</strong><br>
                A: Yes, you can combine multiple gift cards for a single purchase.</p>
                
                <p><strong>Q: Are gift cards refundable?</strong><br>
                A: Gift cards are non-refundable, but they never expire.</p>
                
                <div style="margin-top: 1.5rem; padding: 1rem; background: rgba(40, 167, 69, 0.1); border-radius: 8px;">
                    <p><strong>🎉 Special Offer:</strong> Purchase gift cards worth ₹2,000 or more and get an additional 10% bonus value!</p>
                </div>
            `
        }
    };

    const support = supportModals[supportType];
    if (!support) {
        console.warn(`Support type "${supportType}" not found`);
        return;
    }

    // Create modal using the same structure as policy modals
    const modal = document.createElement('div');
    modal.className = 'policy-modal'; // Reuse policy modal styles
    modal.innerHTML = `
        <div class="policy-modal-content">
            <div class="policy-modal-header">
                <h2><i class="${support.icon}"></i> ${support.title}</h2>
                <button class="policy-close" onclick="closeSupportModal()" aria-label="Close support modal">&times;</button>
            </div>
            <div class="policy-modal-body">
                ${support.content}
            </div>
            <div class="policy-modal-footer">
                <button class="btn-close" onclick="closeSupportModal()">
                    <i class="fas fa-times"></i>
                    Close
                </button>
            </div>
        </div>
    `;

    // Add modal to page
    document.body.appendChild(modal);
    
    // Prevent background scrolling
    document.body.style.overflow = 'hidden';
    
    // Animate in
    modal.style.opacity = '0';
    setTimeout(() => {
        modal.style.transition = 'opacity 0.3s ease';
        modal.style.opacity = '1';
    }, 10);

    // Close on escape key
    const handleEscape = (e) => {
        if (e.key === 'Escape') {
            closeSupportModal();
            document.removeEventListener('keydown', handleEscape);
        }
    };
    document.addEventListener('keydown', handleEscape);

    // Close on background click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeSupportModal();
        }
    });
}

// Close support modal function
function closeSupportModal() {
    const modal = document.querySelector('.policy-modal');
    if (modal) {
        modal.style.opacity = '0';
        setTimeout(() => {
            if (modal.parentNode) {
                modal.parentNode.removeChild(modal);
            }
            // Restore background scrolling
            document.body.style.overflow = '';
        }, 300);
    }
}

// ===== ABOUT MODAL FUNCTIONALITY =====
// About modal function - available site-wide
function showAboutModal(aboutType) {
    const aboutModals = {
        pageforge: {
            title: 'About PageForge',
            icon: 'fas fa-book-open',
            content: `
                <h3>📚 Welcome to PageForge</h3>
                <p>PageForge is your premier digital bookstore, designed to provide an exceptional reading experience for book lovers worldwide. We believe that great literature should be accessible, affordable, and enjoyable for everyone.</p>
                
                <h3>🌟 What Makes Us Special</h3>
                <p><strong>• Curated Collection:</strong> Handpicked books from renowned authors and emerging talents<br>
                <strong>• Premium Experience:</strong> Beautiful, intuitive interface designed for readers<br>
                <strong>• Multi-Platform:</strong> Read seamlessly across all your devices<br>
                <strong>• Instant Access:</strong> Download and start reading immediately after purchase<br>
                <strong>• Fair Pricing:</strong> Competitive prices with regular discounts and offers</p>
                
                <h3>🎯 Our Vision</h3>
                <p>To create the world's most loved digital reading platform where literature thrives, readers discover new worlds, and authors connect with their audience in meaningful ways.</p>
                
                <h3>📈 Our Journey</h3>
                <p>Founded in 2025, PageForge was born from a passion for books and technology. We started with a simple idea: make digital reading as enjoyable as holding a physical book, while adding the convenience and features that only digital platforms can provide.</p>
                
                <h3>🌍 Global Reach, Local Touch</h3>
                <p>While we serve readers globally, we understand local preferences. Our platform supports multiple languages, local payment methods, and features content that resonates with diverse cultures and communities.</p>
                
                <h3>🤝 Community First</h3>
                <p>PageForge is more than a bookstore—it's a community of readers, writers, and book enthusiasts. We foster discussions, support independent authors, and create spaces where literary minds can connect and grow.</p>
                
                <div style="margin-top: 1.5rem; padding: 1rem; background: rgba(0, 122, 255, 0.1); border-radius: 8px;">
                    <p><strong>🚀 Join Our Story:</strong> Become part of the PageForge community and discover your next great read today!</p>
                </div>
            `
        },
        mission: {
            title: 'Our Mission',
            icon: 'fas fa-bullseye',
            content: `
                <h3>🎯 Our Core Mission</h3>
                <p>To democratize access to quality literature and make reading a delightful, accessible experience for everyone, regardless of their location, device, or background.</p>
                
                <h3>🌟 Our Values</h3>
                <p><strong>📖 Accessibility:</strong> Making books available to readers everywhere<br>
                <strong>🎨 Quality:</strong> Curating only the finest literary works<br>
                <strong>💡 Innovation:</strong> Constantly improving the digital reading experience<br>
                <strong>🤝 Community:</strong> Building connections between readers and authors<br>
                <strong>🌱 Sustainability:</strong> Promoting eco-friendly digital alternatives</p>
                
                <h3>🚀 What We're Building</h3>
                <p><strong>• Universal Library:</strong> A comprehensive collection spanning all genres and languages<br>
                <strong>• Smart Recommendations:</strong> AI-powered suggestions tailored to your taste<br>
                <strong>• Interactive Features:</strong> Social reading with notes, highlights, and discussions<br>
                <strong>• Author Platform:</strong> Tools for writers to publish and connect with readers<br>
                <strong>• Educational Tools:</strong> Resources for students, teachers, and researchers</p>
                
                <h3>🌍 Social Impact</h3>
                <p>We believe in the transformative power of reading. Through our platform, we:</p>
                <p>• Support independent authors and diverse voices<br>
                • Provide affordable access to educational content<br>
                • Reduce paper consumption through digital alternatives<br>
                • Foster global literacy and cultural exchange<br>
                • Create opportunities for literary discovery</p>
                
                <h3>📊 Measuring Success</h3>
                <p>Our success isn't just measured in sales, but in:</p>
                <p>• Number of readers discovering new authors<br>
                • Authors reaching wider audiences<br>
                • Books read and knowledge shared<br>
                • Communities formed around shared literary interests<br>
                • Positive impact on reading habits globally</p>
                
                <div style="margin-top: 1.5rem; padding: 1rem; background: rgba(40, 167, 69, 0.1); border-radius: 8px;">
                    <p><strong>💚 Join Our Mission:</strong> Every book you read on PageForge contributes to a more literate, connected, and enlightened world.</p>
                </div>
            `
        },
        developer: {
            title: 'Meet the Developer',
            icon: 'fas fa-user-tie',
            content: `
                <h3>👨‍💻 Mahender Banoth</h3>
                <p><strong>Student at Indian Institute of Technology (IIT) Patna</strong></p>
                
                <h3>🎓 Background</h3>
                <p>Mahender is a passionate student at IIT Patna, driven by curiosity and a vision to shape the tech-driven future. With a strong foundation in computer science and a love for literature, he envisioned PageForge as the perfect intersection of technology and reading.</p>
                
                <h3>💡 The Vision Behind PageForge</h3>
                <p>As an avid reader and tech enthusiast, Mahender noticed the gap between traditional reading experiences and modern digital capabilities. PageForge was born from his desire to create a platform that honors the literary tradition while embracing technological innovation.</p>
                
                <h3>🛠️ Technical Expertise</h3>
                <p><strong>• Full-Stack Development:</strong> Python, Flask, JavaScript, HTML/CSS<br>
                <strong>• Database Design:</strong> SQLite, PostgreSQL<br>
                <strong>• UI/UX Design:</strong> Modern, responsive web design<br>
                <strong>• Problem Solving:</strong> Analytical thinking and creative solutions<br>
                <strong>• Project Management:</strong> End-to-end product development</p>
                
                <h3>📚 Philosophy</h3>
                <p>"Technology should enhance human experiences, not replace them. With PageForge, I wanted to create a digital reading experience that feels as natural and enjoyable as reading a physical book, while adding features that make discovering and enjoying literature even better."</p>
                
                <h3>🌟 Future Goals</h3>
                <p>• Expand PageForge to serve millions of readers globally<br>
                • Develop innovative reading technologies and features<br>
                • Support emerging authors and diverse literary voices<br>
                • Contribute to the advancement of digital publishing<br>
                • Build sustainable, impactful technology solutions</p>
                
                <h3>📱 Connect with Mahender</h3>
                <p><strong>Instagram:</strong> @mahender_hustles<br>
                <strong>LinkedIn:</strong> Mahender Hustles<br>
                <strong>GitHub:</strong> mahenderoffl</p>
                
                <div style="margin-top: 1.5rem; padding: 1rem; background: rgba(0, 122, 255, 0.1); border-radius: 8px;">
                    <p><strong>🚀 Message from Mahender:</strong> "Thank you for being part of the PageForge journey. Your support motivates me to keep improving and building features that enhance your reading experience!"</p>
                </div>
            `
        },
        careers: {
            title: 'Careers at PageForge',
            icon: 'fas fa-briefcase',
            content: `
                <h3>🚀 Join the PageForge Team</h3>
                <p>While PageForge is currently in its growth phase as a solo project, we're always interested in connecting with talented individuals who share our passion for literature and technology.</p>
                
                <h3>🌟 What We Look For</h3>
                <p><strong>• Passion for Reading:</strong> Love for books and literature<br>
                <strong>• Technical Skills:</strong> Web development, mobile apps, or design<br>
                <strong>• Innovation Mindset:</strong> Creative problem-solving abilities<br>
                <strong>• User Focus:</strong> Understanding of user experience and design<br>
                <strong>• Growth Attitude:</strong> Willingness to learn and adapt</p>
                
                <h3>💼 Future Opportunities</h3>
                <p>As PageForge grows, we anticipate opportunities in:</p>
                <p><strong>• Frontend Development:</strong> React, Vue.js, modern JavaScript<br>
                <strong>• Backend Development:</strong> Python, Node.js, database optimization<br>
                <strong>• Mobile Development:</strong> iOS and Android native apps<br>
                <strong>• UI/UX Design:</strong> User interface and experience design<br>
                <strong>• Content Curation:</strong> Literary expertise and book selection<br>
                <strong>• Marketing & Community:</strong> Building reader communities</p>
                
                <h3>🎯 Our Work Culture</h3>
                <p><strong>• Remote-First:</strong> Flexible work arrangements<br>
                <strong>• Learning-Focused:</strong> Continuous skill development<br>
                <strong>• Impact-Driven:</strong> Meaningful work that affects readers globally<br>
                <strong>• Creative Freedom:</strong> Autonomy in solving problems<br>
                <strong>• Work-Life Balance:</strong> Sustainable and healthy work practices</p>
                
                <h3>🎓 Internship Opportunities</h3>
                <p>We're particularly interested in connecting with students and recent graduates who want to gain real-world experience in:</p>
                <p>• Full-stack web development<br>
                • Digital product design<br>
                • Content strategy and curation<br>
                • User research and testing<br>
                • Digital marketing and SEO</p>
                
                <h3>📧 Get in Touch</h3>
                <p>Interested in joining our mission? We'd love to hear from you!</p>
                <p><strong>Email:</strong> careers@pageforge.com<br>
                <strong>Subject Line:</strong> [Your Interest Area] - [Your Name]<br>
                <strong>Include:</strong> Brief introduction, relevant experience, and why you're excited about PageForge</p>
                
                <div style="margin-top: 1.5rem; padding: 1rem; background: rgba(255, 193, 7, 0.1); border-radius: 8px;">
                    <p><strong>📝 Note:</strong> While we may not have immediate openings, we're building a network of talented individuals interested in the future of digital reading. Let's connect!</p>
                </div>
            `
        },
        press: {
            title: 'Press & Media',
            icon: 'fas fa-newspaper',
            content: `
                <h3>📰 Press Information</h3>
                <p>PageForge is an innovative digital bookstore platform developed by Mahender Banoth, a student at IIT Patna. We're passionate about making quality literature accessible through modern technology.</p>
                
                <h3>📊 Key Facts</h3>
                <p><strong>• Founded:</strong> 2025<br>
                <strong>• Founder:</strong> Mahender Banoth (IIT Patna)<br>
                <strong>• Platform:</strong> Web-based digital bookstore<br>
                <strong>• Focus:</strong> Premium reading experience with modern UI/UX<br>
                <strong>• Mission:</strong> Democratizing access to quality literature</p>
                
                <h3>🎯 What Makes PageForge Newsworthy</h3>
                <p><strong>• Student Innovation:</strong> Developed by an IIT student showcasing technical excellence<br>
                <strong>• User Experience:</strong> Premium design rivaling major platforms<br>
                <strong>• Technology Stack:</strong> Modern web technologies and responsive design<br>
                <strong>• Literary Focus:</strong> Emphasis on quality content and reading experience<br>
                <strong>• Indian Market:</strong> Localized pricing and payment options</p>
                
                <h3>🖼️ Media Assets</h3>
                <p>For press coverage, we can provide:</p>
                <p>• High-resolution screenshots of the platform<br>
                • Founder photos and biographical information<br>
                • Platform statistics and user metrics<br>
                • Technical specifications and development details<br>
                • Vision and mission statements</p>
                
                <h3>📝 Press Releases</h3>
                <p><strong>Recent News:</strong></p>
                <p>• PageForge Launch: New Digital Bookstore Enters Market<br>
                • IIT Student Develops Premium Reading Platform<br>
                • Local Innovation in Digital Publishing Space<br>
                • Technology Meets Literature: The PageForge Story</p>
                
                <h3>🎤 Interview Opportunities</h3>
                <p>Mahender Banoth is available for interviews on topics including:</p>
                <p>• Student entrepreneurship and innovation<br>
                • Digital transformation in publishing<br>
                • Technology development and user experience<br>
                • The future of digital reading platforms<br>
                • Balancing studies with product development</p>
                
                <h3>📧 Media Contact</h3>
                <p><strong>Press Inquiries:</strong> press@pageforge.com<br>
                <strong>Response Time:</strong> Within 24 hours<br>
                <strong>Available For:</strong> Interviews, demos, technical discussions<br>
                <strong>Best Contact Times:</strong> 9 AM - 6 PM IST</p>
                
                <h3>🔗 Quick Links</h3>
                <p>• Platform Demo: pageforge.com<br>
                • Developer Profile: LinkedIn - Mahender Hustles<br>
                • Social Media: @mahender_hustles<br>
                • GitHub: mahenderoffl</p>
                
                <div style="margin-top: 1.5rem; padding: 1rem; background: rgba(0, 122, 255, 0.1); border-radius: 8px;">
                    <p><strong>📢 Story Ideas:</strong> We're always happy to discuss the intersection of education, technology, and literature. Contact us for unique perspectives on digital innovation!</p>
                </div>
            `
        }
    };

    const about = aboutModals[aboutType];
    if (!about) {
        console.warn(`About type "${aboutType}" not found`);
        return;
    }

    // Create modal using the same structure as policy modals
    const modal = document.createElement('div');
    modal.className = 'policy-modal'; // Reuse policy modal styles
    modal.innerHTML = `
        <div class="policy-modal-content">
            <div class="policy-modal-header">
                <h2><i class="${about.icon}"></i> ${about.title}</h2>
                <button class="policy-close" onclick="closeAboutModal()" aria-label="Close about modal">&times;</button>
            </div>
            <div class="policy-modal-body">
                ${about.content}
            </div>
            <div class="policy-modal-footer">
                <button class="btn-close" onclick="closeAboutModal()">
                    <i class="fas fa-times"></i>
                    Close
                </button>
            </div>
        </div>
    `;

    // Add modal to page
    document.body.appendChild(modal);
    
    // Prevent background scrolling
    document.body.style.overflow = 'hidden';
    
    // Animate in
    modal.style.opacity = '0';
    setTimeout(() => {
        modal.style.transition = 'opacity 0.3s ease';
        modal.style.opacity = '1';
    }, 10);

    // Close on escape key
    const handleEscape = (e) => {
        if (e.key === 'Escape') {
            closeAboutModal();
            document.removeEventListener('keydown', handleEscape);
        }
    };
    document.addEventListener('keydown', handleEscape);

    // Close on background click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeAboutModal();
        }
    });
}

// Close about modal function
function closeAboutModal() {
    const modal = document.querySelector('.policy-modal');
    if (modal) {
        modal.style.opacity = '0';
        setTimeout(() => {
            if (modal.parentNode) {
                modal.parentNode.removeChild(modal);
            }
            // Restore background scrolling
            document.body.style.overflow = '';
        }, 300);
    }
}

// Make functions globally available
window.showPolicy = showPolicy;
window.closePolicy = closePolicy;
window.showNotification = showNotification;
window.showSupportModal = showSupportModal;
window.closeSupportModal = closeSupportModal;
window.showAboutModal = showAboutModal;
window.closeAboutModal = closeAboutModal;
