
// ===== SIGILCRAFT ULTRA-REVOLUTIONARY FRONTEND V4.0 =====
// Maximum text-responsiveness with advanced features

(function() {
    'use strict';

    // Prevent multiple declarations
    if (window.SigilcraftApp) {
        console.log('🔄 Sigilcraft already initialized, skipping...');
        return;
    }

    const SigilcraftApp = {
        // Core state
        isGenerating: false,
        currentRequest: null,
        
        // DOM elements
        elements: {},

        // Initialize the application
        async init() {
            try {
                console.log('🎨 Initializing Sigilcraft Ultra...');
                
                this.bindElements();
                this.bindEvents();
                await this.loadVibes();
                this.setupCharacterCounter();
                this.addPhraseExamples();
                
                console.log('🎨 Sigilcraft Ultra initialized successfully!');
            } catch (error) {
                console.error('❌ Initialization failed:', error);
                this.showToast('Initialization failed', 'error');
            }
        },

        // Bind DOM elements
        bindElements() {
            this.elements = {
                phraseInput: document.getElementById('phraseInput'),
                vibeSelect: document.getElementById('vibeSelect'),
                advancedToggle: document.getElementById('advancedToggle'),
                generateBtn: document.getElementById('generateBtn'),
                resultContainer: document.getElementById('resultContainer'),
                sigilImage: document.getElementById('sigilImage'),
                downloadBtn: document.getElementById('downloadBtn'),
                shareBtn: document.getElementById('shareBtn'),
                loadingOverlay: document.getElementById('loadingOverlay'),
                charCounter: document.getElementById('charCounter'),
                analysisContainer: document.getElementById('analysisContainer')
            };

            // Validate required elements
            const required = ['phraseInput', 'vibeSelect', 'generateBtn'];
            for (const elementId of required) {
                if (!this.elements[elementId]) {
                    throw new Error(`Required element not found: ${elementId}`);
                }
            }
        },

        // Bind event listeners
        bindEvents() {
            // Generate button
            this.elements.generateBtn.addEventListener('click', () => this.generateSigil());

            // Phrase input events
            this.elements.phraseInput.addEventListener('input', () => {
                this.updateCharacterCounter();
                this.validateInput();
            });

            this.elements.phraseInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.generateSigil();
                }
            });

            // Download button
            if (this.elements.downloadBtn) {
                this.elements.downloadBtn.addEventListener('click', () => this.downloadSigil());
            }

            // Share button
            if (this.elements.shareBtn) {
                this.elements.shareBtn.addEventListener('click', () => this.shareSigil());
            }

            // Vibe selection change
            this.elements.vibeSelect.addEventListener('change', () => this.updateVibeDescription());
        },

        // Load available vibes
        async loadVibes() {
            try {
                const response = await fetch('/api/vibes');
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                
                const data = await response.json();
                if (data.success && data.vibes) {
                    this.populateVibes(data.vibes, data.descriptions);
                } else {
                    throw new Error('Invalid vibes data structure');
                }
            } catch (error) {
                console.warn('⚠️ Could not load vibes from server, using fallback');
                this.populateVibes(
                    ['mystical', 'cosmic', 'elemental', 'crystal', 'shadow', 'light', 'storm', 'void'],
                    {
                        'mystical': 'Ancient wisdom & sacred geometry',
                        'cosmic': 'Universal stellar connection',
                        'elemental': 'Natural organic forces',
                        'crystal': 'Prismatic geometric precision',
                        'shadow': 'Hidden mysterious power',
                        'light': 'Pure divine radiance',
                        'storm': 'Raw electric chaos',
                        'void': 'Infinite recursive potential'
                    }
                );
            }
        },

        // Populate vibe options
        populateVibes(vibes, descriptions = {}) {
            this.elements.vibeSelect.innerHTML = '';
            
            vibes.forEach(vibe => {
                const option = document.createElement('option');
                option.value = vibe;
                option.textContent = vibe.charAt(0).toUpperCase() + vibe.slice(1);
                option.title = descriptions[vibe] || '';
                this.elements.vibeSelect.appendChild(option);
            });

            this.updateVibeDescription();
        },

        // Update vibe description
        updateVibeDescription() {
            const selectedOption = this.elements.vibeSelect.selectedOptions[0];
            if (selectedOption && selectedOption.title) {
                // Find or create description element
                let descElement = document.getElementById('vibeDescription');
                if (!descElement) {
                    descElement = document.createElement('div');
                    descElement.id = 'vibeDescription';
                    descElement.className = 'vibe-description';
                    this.elements.vibeSelect.parentNode.appendChild(descElement);
                }
                descElement.textContent = selectedOption.title;
            }
        },

        // Setup character counter
        setupCharacterCounter() {
            if (!this.elements.charCounter) {
                const counterElement = document.createElement('div');
                counterElement.id = 'charCounter';
                counterElement.className = 'char-counter';
                this.elements.phraseInput.parentNode.appendChild(counterElement);
                this.elements.charCounter = counterElement;
            }
            this.updateCharacterCounter();
        },

        // Update character counter
        updateCharacterCounter() {
            if (this.elements.charCounter) {
                const length = this.elements.phraseInput.value.length;
                this.elements.charCounter.textContent = `${length}/500`;
                
                if (length > 450) {
                    this.elements.charCounter.style.color = '#f44336';
                } else if (length > 400) {
                    this.elements.charCounter.style.color = '#ff9800';
                } else {
                    this.elements.charCounter.style.color = '#666';
                }
            }
        },

        // Validate input
        validateInput() {
            const phrase = this.elements.phraseInput.value.trim();
            const isValid = phrase.length >= 2 && phrase.length <= 500;
            
            this.elements.generateBtn.disabled = !isValid || this.isGenerating;
            
            return isValid;
        },

        // Add phrase examples
        addPhraseExamples() {
            const examples = [
                "Manifest abundance and prosperity",
                "Protection from negative energy",
                "Healing and inner peace",
                "Wisdom and clarity of mind",
                "Love and harmonious relationships"
            ];

            // Create examples container if it doesn't exist
            let examplesContainer = document.getElementById('phraseExamples');
            if (!examplesContainer) {
                examplesContainer = document.createElement('div');
                examplesContainer.id = 'phraseExamples';
                examplesContainer.className = 'phrase-examples';
                
                const title = document.createElement('p');
                title.textContent = 'Example phrases:';
                title.style.fontWeight = 'bold';
                title.style.marginBottom = '8px';
                examplesContainer.appendChild(title);

                const examplesList = document.createElement('div');
                examplesList.className = 'examples-list';
                
                examples.forEach(example => {
                    const exampleElement = document.createElement('button');
                    exampleElement.textContent = example;
                    exampleElement.className = 'example-phrase';
                    exampleElement.onclick = () => {
                        this.elements.phraseInput.value = example;
                        this.updateCharacterCounter();
                        this.validateInput();
                    };
                    examplesList.appendChild(exampleElement);
                });

                examplesContainer.appendChild(examplesList);
                this.elements.phraseInput.parentNode.appendChild(examplesContainer);
            }
        },

        // Generate sigil
        async generateSigil() {
            if (this.isGenerating || !this.validateInput()) return;

            const phrase = this.elements.phraseInput.value.trim();
            const vibe = this.elements.vibeSelect.value;
            const advanced = this.elements.advancedToggle ? this.elements.advancedToggle.checked : false;

            try {
                this.setGeneratingState(true);
                this.showLoadingOverlay();

                // Cancel any existing request
                if (this.currentRequest) {
                    this.currentRequest.abort();
                }

                // Create new request with timeout
                const controller = new AbortController();
                this.currentRequest = controller;

                const timeoutId = setTimeout(() => controller.abort(), 60000); // 60 second timeout

                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ phrase, vibe, advanced }),
                    signal: controller.signal
                });

                clearTimeout(timeoutId);

                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({}));
                    throw new Error(errorData.error || `Server error: ${response.status}`);
                }

                const data = await response.json();

                if (data.success && data.image) {
                    this.displaySigil(data);
                    this.showToast('Revolutionary sigil manifested!', 'success');
                } else {
                    throw new Error(data.error || 'Invalid response from server');
                }

            } catch (error) {
                console.error('❌ Generation failed:', error);
                
                if (error.name === 'AbortError') {
                    this.showToast('Request timed out. Please try again.', 'warning');
                } else {
                    this.showToast(`Generation failed: ${error.message}`, 'error');
                }
            } finally {
                this.setGeneratingState(false);
                this.hideLoadingOverlay();
                this.currentRequest = null;
            }
        },

        // Display generated sigil
        displaySigil(data) {
            if (this.elements.sigilImage) {
                this.elements.sigilImage.src = `data:image/png;base64,${data.image}`;
                this.elements.sigilImage.alt = `Sigil for: ${data.phrase}`;
            }

            if (this.elements.resultContainer) {
                this.elements.resultContainer.style.display = 'block';
                this.elements.resultContainer.scrollIntoView({ behavior: 'smooth' });
            }

            // Store image data for download
            this.currentSigilData = data;

            // Enable download/share buttons
            if (this.elements.downloadBtn) this.elements.downloadBtn.disabled = false;
            if (this.elements.shareBtn) this.elements.shareBtn.disabled = false;
        },

        // Set generating state
        setGeneratingState(generating) {
            this.isGenerating = generating;
            this.elements.generateBtn.disabled = generating;
            this.elements.generateBtn.textContent = generating ? 'Manifesting...' : 'Generate Sigil';
            this.validateInput(); // Re-validate to update button state
        },

        // Show loading overlay
        showLoadingOverlay() {
            if (this.elements.loadingOverlay) {
                this.elements.loadingOverlay.style.display = 'flex';
            }
        },

        // Hide loading overlay
        hideLoadingOverlay() {
            if (this.elements.loadingOverlay) {
                this.elements.loadingOverlay.style.display = 'none';
            }
        },

        // Download sigil
        downloadSigil() {
            if (!this.currentSigilData) return;

            try {
                const link = document.createElement('a');
                link.href = `data:image/png;base64,${this.currentSigilData.image}`;
                link.download = `sigil-${this.currentSigilData.phrase.replace(/[^a-zA-Z0-9]/g, '_')}-${Date.now()}.png`;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                
                this.showToast('Sigil downloaded successfully!', 'success');
            } catch (error) {
                console.error('❌ Download failed:', error);
                this.showToast('Download failed', 'error');
            }
        },

        // Share sigil
        async shareSigil() {
            if (!this.currentSigilData) return;

            try {
                if (navigator.share) {
                    await navigator.share({
                        title: 'My Sigilcraft Creation',
                        text: `Check out this sigil I created for: "${this.currentSigilData.phrase}"`,
                        url: window.location.href
                    });
                } else {
                    // Fallback: copy URL to clipboard
                    await navigator.clipboard.writeText(window.location.href);
                    this.showToast('URL copied to clipboard!', 'success');
                }
            } catch (error) {
                console.error('❌ Share failed:', error);
                this.showToast('Share failed', 'error');
            }
        },

        // Show toast notification
        showToast(message, type = 'info') {
            const toast = document.createElement('div');
            toast.className = `toast toast-${type}`;
            toast.textContent = message;
            
            document.body.appendChild(toast);
            
            // Auto remove after 4 seconds
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 4000);
        }
    };

    // Global error handler
    window.addEventListener('error', (event) => {
        console.error('Global error:', event.error);
        if (window.SigilcraftApp && window.SigilcraftApp.showToast) {
            window.SigilcraftApp.showToast('An unexpected error occurred', 'error');
        }
    });

    // Make SigilcraftApp globally available
    window.SigilcraftApp = SigilcraftApp;

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => SigilcraftApp.init());
    } else {
        SigilcraftApp.init();
    }

})();
