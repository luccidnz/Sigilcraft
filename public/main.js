
// ===== SIGILCRAFT ULTRA-REVOLUTIONARY FRONTEND =====

// Global error handler
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
});

// Prevent duplicate declarations
if (typeof window.SigilcraftApp !== 'undefined') {
    console.log('🔄 Reloading SigilcraftApp...');
    delete window.SigilcraftApp;
}

// Main Sigilcraft Application Class
window.SigilcraftApp = class SigilcraftApp {
    constructor() {
        this.isGenerating = false;
        this.currentCooldown = 0;
        this.cooldownTimer = null;
        this.isPro = this.checkProStatus();
        this.apiBaseUrl = window.location.origin;
        
        console.log('🎨 Initializing Sigilcraft Ultra...');
        this.init();
    }

    async init() {
        try {
            this.bindEvents();
            this.updateUI();
            await this.loadVibes();
            this.setMobileViewHeight();
            console.log('🎨 Sigilcraft Ultra initialized successfully!');
        } catch (error) {
            console.error('❌ Initialization failed:', error);
            this.showError('Failed to initialize application');
        }
    }

    checkProStatus() {
        const localPro = localStorage.getItem('sigilcraft_pro') === 'true';
        const cookiePro = document.cookie.includes('sigilcraft_pro=true');
        return localPro || cookiePro;
    }

    bindEvents() {
        // Generate button
        const generateBtn = document.getElementById('generateBtn');
        if (generateBtn) {
            generateBtn.addEventListener('click', () => this.generateSigil());
        }

        // Enter key in text input
        const phraseInput = document.getElementById('phraseInput');
        if (phraseInput) {
            phraseInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !this.isGenerating && this.currentCooldown === 0) {
                    this.generateSigil();
                }
            });
        }

        // Pro key modal
        const proKeyBtn = document.getElementById('proKeyBtn');
        const proKeyModal = document.getElementById('proKeyModal');
        const closeModal = document.getElementById('closeModal');
        const submitProKey = document.getElementById('submitProKey');

        if (proKeyBtn) {
            proKeyBtn.addEventListener('click', () => {
                if (proKeyModal) proKeyModal.style.display = 'flex';
            });
        }

        if (closeModal) {
            closeModal.addEventListener('click', () => {
                if (proKeyModal) proKeyModal.style.display = 'none';
            });
        }

        if (submitProKey) {
            submitProKey.addEventListener('click', () => this.submitProKey());
        }

        // Mobile viewport height adjustment
        window.addEventListener('resize', () => this.setMobileViewHeight());
    }

    setMobileViewHeight() {
        const vh = window.innerHeight * 0.01;
        document.documentElement.style.setProperty('--vh', `${vh}px`);
        
        if (window.innerWidth <= 768) {
            document.body.classList.add('mobile');
        } else {
            document.body.classList.remove('mobile');
        }
    }

    async loadVibes() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/api/vibes`);
            const data = await response.json();
            
            if (data.success) {
                this.populateVibeSelect(data.vibes, data.descriptions);
            }
        } catch (error) {
            console.error('❌ Failed to load vibes:', error);
        }
    }

    populateVibeSelect(vibes, descriptions) {
        const vibeSelect = document.getElementById('vibeSelect');
        if (!vibeSelect) return;

        vibeSelect.innerHTML = '';
        
        const freeVibes = this.isPro ? vibes : vibes.slice(0, 3);
        
        freeVibes.forEach(vibe => {
            const option = document.createElement('option');
            option.value = vibe;
            option.textContent = `${vibe.charAt(0).toUpperCase() + vibe.slice(1)} - ${descriptions[vibe] || 'Mystical energy'}`;
            vibeSelect.appendChild(option);
        });

        if (!this.isPro && vibes.length > 3) {
            const proOption = document.createElement('option');
            proOption.value = 'pro';
            proOption.textContent = '✨ Upgrade to Pro for all vibes';
            proOption.disabled = true;
            vibeSelect.appendChild(proOption);
        }
    }

    async generateSigil() {
        if (this.isGenerating || this.currentCooldown > 0) return;

        const phraseInput = document.getElementById('phraseInput');
        const vibeSelect = document.getElementById('vibeSelect');
        const generateBtn = document.getElementById('generateBtn');
        const resultSection = document.getElementById('resultSection');
        const sigilImage = document.getElementById('sigilImage');
        const errorMessage = document.getElementById('errorMessage');

        if (!phraseInput || !vibeSelect) {
            this.showError('Required elements not found');
            return;
        }

        const phrase = phraseInput.value.trim();
        if (!phrase) {
            this.showError('Please enter a phrase or intention');
            return;
        }

        if (phrase.length < 2) {
            this.showError('Phrase must be at least 2 characters long');
            return;
        }

        if (phrase.length > 500) {
            this.showError('Phrase is too long (max 500 characters)');
            return;
        }

        const vibe = vibeSelect.value;
        if (vibe === 'pro') {
            this.showError('Please upgrade to Pro to access all vibes');
            return;
        }

        this.isGenerating = true;
        this.updateUI();

        try {
            const response = await fetch(`${this.apiBaseUrl}/api/generate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    phrase: phrase,
                    vibe: vibe,
                    advanced: this.isPro
                })
            });

            const data = await response.json();

            if (data.success) {
                if (sigilImage) {
                    sigilImage.src = `data:image/png;base64,${data.image}`;
                    sigilImage.style.display = 'block';
                }
                
                if (resultSection) {
                    resultSection.style.display = 'block';
                    resultSection.scrollIntoView({ behavior: 'smooth' });
                }

                if (errorMessage) {
                    errorMessage.style.display = 'none';
                }

                console.log('✅ Sigil generated successfully');
                
                // Start cooldown for free users
                if (!this.isPro) {
                    this.startCooldown(10);
                }
            } else {
                this.showError(data.error || 'Failed to generate sigil');
            }
        } catch (error) {
            console.error('❌ Generation error:', error);
            this.showError('Network error. Please check your connection and try again.');
        } finally {
            this.isGenerating = false;
            this.updateUI();
        }
    }

    showError(message) {
        const errorMessage = document.getElementById('errorMessage');
        if (errorMessage) {
            errorMessage.textContent = message;
            errorMessage.style.display = 'block';
            setTimeout(() => {
                errorMessage.style.display = 'none';
            }, 5000);
        }
        console.error('❌ Error:', message);
    }

    startCooldown(seconds) {
        this.currentCooldown = seconds;
        this.updateUI();
        
        this.cooldownTimer = setInterval(() => {
            this.currentCooldown--;
            this.updateUI();
            
            if (this.currentCooldown <= 0) {
                clearInterval(this.cooldownTimer);
                this.cooldownTimer = null;
            }
        }, 1000);
    }

    updateUI() {
        const generateBtn = document.getElementById('generateBtn');
        const loadingSpinner = document.querySelector('.loading-spinner');
        
        if (generateBtn) {
            if (this.isGenerating) {
                generateBtn.textContent = 'Generating...';
                generateBtn.disabled = true;
            } else if (this.currentCooldown > 0) {
                generateBtn.textContent = `Wait ${this.currentCooldown}s`;
                generateBtn.disabled = true;
            } else {
                generateBtn.textContent = '✨ Generate Sigil';
                generateBtn.disabled = false;
            }
        }

        if (loadingSpinner) {
            loadingSpinner.style.display = this.isGenerating ? 'block' : 'none';
        }

        // Update Pro status display
        this.updateProStatus();
    }

    updateProStatus() {
        const proStatus = document.getElementById('proStatus');
        const proKeyBtn = document.getElementById('proKeyBtn');
        
        if (this.isPro) {
            if (proStatus) {
                proStatus.innerHTML = '<i class="fas fa-crown"></i> Pro Active';
                proStatus.className = 'pro-badge';
                proStatus.style.display = 'inline-flex';
            }
            if (proKeyBtn) {
                proKeyBtn.style.display = 'none';
            }
        } else {
            if (proStatus) {
                proStatus.style.display = 'none';
            }
            if (proKeyBtn) {
                proKeyBtn.style.display = 'inline-block';
            }
        }
    }

    async submitProKey() {
        const proKeyInput = document.getElementById('proKeyInput');
        const proKeyModal = document.getElementById('proKeyModal');
        
        if (!proKeyInput) return;
        
        const key = proKeyInput.value.trim();
        if (!key) {
            alert('Please enter a Pro key');
            return;
        }

        try {
            const response = await fetch(`${this.apiBaseUrl}/api/validate-pro-key`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ key: key })
            });

            const data = await response.json();

            if (data.success) {
                localStorage.setItem('sigilcraft_pro', 'true');
                this.isPro = true;
                this.updateUI();
                await this.loadVibes();
                
                if (proKeyModal) {
                    proKeyModal.style.display = 'none';
                }
                
                alert('🎉 Pro activated successfully!');
            } else {
                alert('❌ Invalid Pro key. Please check and try again.');
            }
        } catch (error) {
            console.error('❌ Pro key validation error:', error);
            alert('❌ Network error. Please try again.');
        }
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    if (!window.sigilcraftAppInstance) {
        window.sigilcraftAppInstance = new window.SigilcraftApp();
    }
});

// Expose app globally for debugging
if (typeof module !== 'undefined' && module.exports) {
    module.exports = window.SigilcraftApp;
}
