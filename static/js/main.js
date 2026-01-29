// Main JavaScript file for Virtual Career Counselor

// Dark Mode Toggle Functionality
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    // Update toggle button
    updateThemeToggle(newTheme);
}

function updateThemeToggle(theme) {
    const themeIcons = document.querySelectorAll('.theme-icon');
    const themeTexts = document.querySelectorAll('.theme-text');
    
    themeIcons.forEach(icon => {
        icon.textContent = theme === 'dark' ? '☀️' : '🌙';
    });
    
    themeTexts.forEach(text => {
        text.textContent = theme === 'dark' ? 'Light' : 'Dark';
    });
}

// Initialize theme on page load
function initializeTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeToggle(savedTheme);
}

// Initialize theme when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeTheme();
});

// Utility functions
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Form validation
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePassword(password) {
    return password.length >= 6;
}

// Auto-resize textareas
document.addEventListener('DOMContentLoaded', function() {
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    });
});

// Smooth scrolling for anchor links
document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});

// Loading states for buttons
function setButtonLoading(button, loading = true) {
    if (loading) {
        button.disabled = true;
        button.dataset.originalText = button.textContent;
        button.textContent = 'Loading...';
    } else {
        button.disabled = false;
        button.textContent = button.dataset.originalText || button.textContent;
    }
}

// API helper functions
async function apiRequest(url, data, method = 'POST') {
    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        return await response.json();
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

// Chat functionality
class ChatManager {
    constructor(chatMessagesId, chatFormId, messageInputId) {
        this.chatMessages = document.getElementById(chatMessagesId);
        this.chatForm = document.getElementById(chatFormId);
        this.messageInput = document.getElementById(messageInputId);
        
        if (this.chatForm) {
            this.init();
        }
    }
    
    init() {
        this.chatForm.addEventListener('submit', (e) => this.handleSubmit(e));
        this.setupAutoResize();
    }
    
    setupAutoResize() {
        if (this.messageInput) {
            this.messageInput.addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = this.scrollHeight + 'px';
            });
        }
    }
    
    addMessage(content, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = isUser ? 'user-message' : 'ai-message';
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        if (isUser) {
            messageContent.innerHTML = `<strong>You:</strong> ${this.escapeHtml(content)}`;
        } else {
            // Convert markdown-like formatting to HTML
            let formattedContent = content
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                .replace(/\n/g, '<br>')
                .replace(/• /g, '&bull; ');
            
            messageContent.innerHTML = `<strong>Career Counselor AI:</strong><br>${formattedContent}`;
        }
        
        messageDiv.appendChild(messageContent);
        this.chatMessages.appendChild(messageDiv);
        
        this.scrollToBottom();
    }
    
    showTyping() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'ai-message typing';
        typingDiv.id = 'typing-indicator';
        typingDiv.innerHTML = '<div class="message-content"><strong>Career Counselor AI:</strong> <em>Thinking...</em></div>';
        this.chatMessages.appendChild(typingDiv);
        this.scrollToBottom();
        return typingDiv;
    }
    
    removeTyping() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    async handleSubmit(e) {
        e.preventDefault();
        
        const message = this.messageInput.value.trim();
        if (!message) return;
        
        // Add user message
        this.addMessage(message, true);
        
        // Clear input
        this.messageInput.value = '';
        this.messageInput.style.height = 'auto';
        
        // Show typing indicator
        const typingIndicator = this.showTyping();
        
        try {
            const result = await apiRequest('/api/chat', { message: message });
            
            this.removeTyping();
            
            if (result.success) {
                this.addMessage(result.response);
            } else {
                this.addMessage('Sorry, I encountered an error. Please try again.');
            }
        } catch (error) {
            this.removeTyping();
            this.addMessage('Sorry, I encountered a connection error. Please try again.');
        }
    }
}

// Initialize chat manager if on dashboard page
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('chatMessages')) {
        new ChatManager('chatMessages', 'chatForm', 'messageInput');
    }
});

// Admin dashboard functionality
class AdminDashboard {
    constructor() {
        if (document.querySelector('.admin-dashboard')) {
            this.init();
        }
    }
    
    init() {
        this.loadStats();
        this.setupEventListeners();
    }
    
    async loadStats() {
        try {
            const result = await apiRequest('/api/admin/stats', {}, 'GET');
            
            if (result.success) {
                document.getElementById('totalUsers').textContent = result.stats.total_users;
                document.getElementById('totalConversations').textContent = result.stats.total_conversations;
                document.getElementById('totalAdmins').textContent = result.stats.total_admins;
            }
        } catch (error) {
            console.error('Error loading stats:', error);
        }
    }
    
    setupEventListeners() {
        // Add event listeners for admin actions
        const refreshBtn = document.querySelector('[onclick="refreshStats()"]');
        if (refreshBtn) {
            refreshBtn.onclick = () => {
                this.loadStats();
                showNotification('Statistics refreshed successfully!');
            };
        }
        
        const exportBtn = document.querySelector('[onclick="exportData()"]');
        if (exportBtn) {
            exportBtn.onclick = () => {
                showNotification('Data export feature coming soon!', 'info');
            };
        }
    }
}

// Initialize admin dashboard
document.addEventListener('DOMContentLoaded', function() {
    new AdminDashboard();
});

// Form enhancement
document.addEventListener('DOMContentLoaded', function() {
    // Add form validation feedback
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input[required]');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                if (this.value.trim() === '') {
                    this.style.borderColor = '#dc3545';
                } else if (this.type === 'email' && !validateEmail(this.value)) {
                    this.style.borderColor = '#dc3545';
                } else if (this.type === 'password' && !validatePassword(this.value)) {
                    this.style.borderColor = '#dc3545';
                } else {
                    this.style.borderColor = '#28a745';
                }
            });
            
            input.addEventListener('input', function() {
                this.style.borderColor = '#e1e5e9';
            });
        });
    });
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to submit chat form
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const chatForm = document.getElementById('chatForm');
        if (chatForm && document.activeElement.tagName === 'TEXTAREA') {
            chatForm.dispatchEvent(new Event('submit'));
        }
    }
});

// Page visibility API for real-time updates
document.addEventListener('visibilitychange', function() {
    if (!document.hidden && document.querySelector('.admin-dashboard')) {
        // Refresh admin stats when page becomes visible
        const adminDash = new AdminDashboard();
    }
});

console.log('Virtual Career Counselor - JavaScript loaded successfully!');