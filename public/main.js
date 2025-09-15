// ===== SIGILCRAFT NEXUS - ULTIMATE SPIRITUAL FRONTEND ===== 
// Revolutionary mystical experience with pro features and gallery

(function() {
    'use strict';

    // Prevent multiple declarations
    if (window.SigilcraftNexus) {
        console.log('🔮 Sigilcraft Nexus already initialized, skipping...');
        return;
    }

    const SigilcraftNexus = {
        // Core state
        isGenerating: false,
        isPro: false,
        currentRequest: null,
        currentSigil: null,
        gallery: [],

        // Pro features
        proFeatures: {
            allVibes: false,
            hdGeneration: false,
            batchMode: false,
            unlimitedGallery: false,
            svgExport: false,
            priorityGeneration: false
        },

        // DOM elements
        elements: {},

        // Configuration
        config: {
            maxFreeGalleryItems: 5,
            proKey: null,
            apiBase: '',
            cooldownTime: 10000 // 10 seconds for free users
        },

        // Initialize the nexus
        async init() {
            try {
                console.log('🔮 Initializing Sigilcraft Nexus...');

                this.bindElements();
                this.bindEvents();
                this.initializeFloatingElements();
                this.initializeMysticalAnimations();
                await this.loadVibes();
                this.setupCharacterCounter();
                this.addPhraseExamples();
                this.loadGallery();
                this.checkProStatus();
                this.updateProFeatures();
                await this.loadLunarPhase();
                this.initializeChakraSelector();
                this.initializeAIAnalysis();

                console.log('✨ Sigilcraft Nexus initialized successfully!');
            } catch (error) {
                console.error('❌ Nexus initialization failed:', error);
                this.showToast('Initialization failed', 'error');
            }
        },

        // Bind DOM elements
        bindElements() {
            this.elements = {
                // Core elements
                phraseInput: document.getElementById('phraseInput'),
                vibeSelect: document.getElementById('vibeSelect'),
                qualitySelect: document.getElementById('qualitySelect'),
                generateBtn: document.getElementById('generateBtn'),

                // Result elements
                resultContainer: document.getElementById('resultContainer'),
                sigilImage: document.getElementById('sigilImage'),
                resultPhrase: document.getElementById('resultPhrase'),
                resultVibe: document.getElementById('resultVibe'),

                // Action buttons
                downloadBtn: document.getElementById('downloadBtn'),
                shareBtn: document.getElementById('shareBtn'),
                regenerateBtn: document.getElementById('regenerateBtn'),
                newSigilBtn: document.getElementById('newSigilBtn'),
                viewGalleryBtn: document.getElementById('viewGalleryBtn'),

                // Navigation
                galleryBtn: document.getElementById('galleryBtn'),
                proBtn: document.getElementById('proBtn'),

                // Toggles
                saveToGallery: document.getElementById('saveToGallery'),
                batchMode: document.getElementById('batchMode'),

                // Modals
                loadingOverlay: document.getElementById('loadingOverlay'),
                proModal: document.getElementById('proModal'),
                shareModal: document.getElementById('shareModal'),
                galleryModal: document.getElementById('galleryModal'),

                // Modal content
                galleryContent: document.getElementById('galleryContent'),
                galleryEmpty: document.getElementById('galleryEmpty'),
                sharePreviewImage: document.getElementById('sharePreviewImage'),
                sharePreviewText: document.getElementById('sharePreviewText'),

                // Pro elements
                proStatus: document.getElementById('proStatus'),
                upgradeBtn: document.getElementById('upgradeBtn'),
                proKeyInput: document.getElementById('proKeyInput'),
                activateKeyBtn: document.getElementById('activateKeyBtn'),

                // Batch elements
                batchControls: document.getElementById('batchControls'),
                batchResults: document.getElementById('batchResults'),
                batchGrid: document.getElementById('batchGrid'),

                // Counters
                charCounter: document.getElementById('charCounter'),
                toastContainer: document.getElementById('toastContainer')
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
            // Core generation
            this.elements.generateBtn.addEventListener('click', () => this.generateSigil());

            // Input events
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

            // Vibe selection
            this.elements.vibeSelect.addEventListener('change', () => this.updateVibeDescription());

            // Quality selection
            this.elements.qualitySelect.addEventListener('change', () => this.validateQualitySelection());

            // Batch mode toggle
            if (this.elements.batchMode) {
                this.elements.batchMode.addEventListener('change', () => this.toggleBatchMode());
            }

            // Action buttons
            if (this.elements.downloadBtn) {
                this.elements.downloadBtn.addEventListener('click', () => this.downloadSigil());
            }

            if (this.elements.shareBtn) {
                this.elements.shareBtn.addEventListener('click', () => this.openShareModal());
            }

            if (this.elements.regenerateBtn) {
                this.elements.regenerateBtn.addEventListener('click', () => this.regenerateSigil());
            }

            if (this.elements.newSigilBtn) {
                this.elements.newSigilBtn.addEventListener('click', () => this.createNewSigil());
            }

            if (this.elements.viewGalleryBtn) {
                this.elements.viewGalleryBtn.addEventListener('click', () => this.openGallery());
            }

            // Navigation
            if (this.elements.galleryBtn) {
                this.elements.galleryBtn.addEventListener('click', () => this.openGallery());
            }

            if (this.elements.proBtn) {
                this.elements.proBtn.addEventListener('click', () => this.openProModal());
            }

            // Clear gallery button
            if (document.getElementById('clearGalleryBtn')) {
                document.getElementById('clearGalleryBtn').addEventListener('click', () => this.clearGallery());
            }

            // Pro modal events
            if (this.elements.upgradeBtn) {
                this.elements.upgradeBtn.addEventListener('click', () => this.upgradeToPro());
            }

            if (this.elements.activateKeyBtn) {
                this.elements.activateKeyBtn.addEventListener('click', () => this.activateProKey());
            }

            // Modal close events
            document.addEventListener('click', (e) => {
                if (e.target.classList.contains('modal-overlay')) {
                    this.closeAllModals();
                }

                if (e.target.classList.contains('close-btn')) {
                    this.closeAllModals();
                }
            });

            // Share modal events
            if (document.getElementById('copyLinkBtn')) {
                document.getElementById('copyLinkBtn').addEventListener('click', () => this.copyShareLink());
            }

            if (document.getElementById('downloadShareBtn')) {
                document.getElementById('downloadShareBtn').addEventListener('click', () => this.downloadSigil());
            }

            if (document.getElementById('socialShareBtn')) {
                document.getElementById('socialShareBtn').addEventListener('click', () => this.shareOnSocial());
            }

            // Keyboard shortcuts
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') {
                    this.closeAllModals();
                }

                if (e.ctrlKey || e.metaKey) {
                    if (e.key === 'Enter') {
                        e.preventDefault();
                        this.generateSigil();
                    }

                    if (e.key === 'g') {
                        e.preventDefault();
                        this.openGallery();
                    }
                }
            });
        },

        // Initialize floating mystical elements
        initializeFloatingElements() {
            const floatingContainer = document.querySelector('.floating-sigils');
            if (!floatingContainer) return;

            const mysticalSymbols = ['🔮', '✨', '🌟', '⚡', '🌙', '💎', '🔥', '💫'];

            for (let i = 0; i < 12; i++) {
                const element = document.createElement('div');
                element.textContent = mysticalSymbols[Math.floor(Math.random() * mysticalSymbols.length)];
                element.style.cssText = `
                    position: absolute;
                    font-size: ${Math.random() * 2 + 1}rem;
                    opacity: ${Math.random() * 0.3 + 0.1};
                    top: ${Math.random() * 100}%;
                    left: ${Math.random() * 100}%;
                    animation: floatMystic ${Math.random() * 20 + 10}s ease-in-out infinite;
                    animation-delay: ${Math.random() * 10}s;
                    pointer-events: none;
                `;
                floatingContainer.appendChild(element);
            }
        },

        // Initialize mystical animations
        initializeMysticalAnimations() {
            // Create floating orbs
            const orbContainer = document.createElement('div');
            orbContainer.className = 'mystical-orbs';
            orbContainer.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                pointer-events: none;
                z-index: 1;
            `;
            document.body.appendChild(orbContainer);

            // Generate floating orbs
            for (let i = 0; i < 20; i++) {
                const orb = document.createElement('div');
                const size = Math.random() * 30 + 10;
                const startX = Math.random() * window.innerWidth;
                const startY = Math.random() * window.innerHeight;
                
                orb.style.cssText = `
                    position: absolute;
                    width: ${size}px;
                    height: ${size}px;
                    left: ${startX}px;
                    top: ${startY}px;
                    background: radial-gradient(circle, rgba(139, 92, 246, 0.8) 0%, rgba(139, 92, 246, 0) 70%);
                    border-radius: 50%;
                    animation: floatOrb ${20 + Math.random() * 10}s ease-in-out infinite;
                    animation-delay: ${Math.random() * 10}s;
                `;
                orbContainer.appendChild(orb);
            }

            // Add pulsating aura to buttons
            document.querySelectorAll('.btn, .action-btn').forEach(btn => {
                btn.addEventListener('mouseenter', () => {
                    btn.style.animation = 'pulseGlow 1s ease-in-out infinite';
                });
                btn.addEventListener('mouseleave', () => {
                    btn.style.animation = '';
                });
            });

            // Add CSS animations if not already present
            if (!document.getElementById('mystical-animations')) {
                const style = document.createElement('style');
                style.id = 'mystical-animations';
                style.textContent = `
                    @keyframes floatOrb {
                        0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.3; }
                        25% { transform: translate(100px, -100px) scale(1.2); opacity: 0.5; }
                        50% { transform: translate(-50px, -200px) scale(0.8); opacity: 0.3; }
                        75% { transform: translate(-100px, 50px) scale(1.1); opacity: 0.4; }
                    }
                    @keyframes pulseGlow {
                        0%, 100% { box-shadow: 0 0 20px rgba(139, 92, 246, 0.5); }
                        50% { box-shadow: 0 0 40px rgba(139, 92, 246, 0.8); }
                    }
                    @keyframes sacredGeometry {
                        0% { transform: rotate(0deg); }
                        100% { transform: rotate(360deg); }
                    }
                `;
                document.head.appendChild(style);
            }
        },

        // Load lunar phase data
        async loadLunarPhase() {
            try {
                const response = await fetch('/api/lunar_phase');
                if (response.ok) {
                    const data = await response.json();
                    if (data.success) {
                        this.displayLunarPhase(data.lunar);
                    }
                }
            } catch (error) {
                console.error('Failed to load lunar phase:', error);
            }
        },

        // Display lunar phase information
        displayLunarPhase(lunar) {
            const lunarDisplay = document.createElement('div');
            lunarDisplay.className = 'lunar-phase-display';
            lunarDisplay.innerHTML = `
                <div class="lunar-info">
                    <span class="lunar-symbol">${lunar.symbol}</span>
                    <span class="lunar-name">${lunar.phase.replace(/_/g, ' ').toUpperCase()}</span>
                    <span class="lunar-power">Power: ${lunar.power}x</span>
                    <div class="lunar-description">${lunar.description}</div>
                </div>
            `;
            lunarDisplay.style.cssText = `
                position: fixed;
                top: 80px;
                right: 20px;
                background: rgba(30, 27, 75, 0.9);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(139, 92, 246, 0.3);
                border-radius: 12px;
                padding: 15px;
                color: #e5e7eb;
                font-size: 0.9rem;
                z-index: 50;
                max-width: 250px;
                box-shadow: 0 0 30px rgba(139, 92, 246, 0.3);
            `;
            
            // Remove existing lunar display if present
            const existing = document.querySelector('.lunar-phase-display');
            if (existing) existing.remove();
            
            document.body.appendChild(lunarDisplay);
        },

        // Initialize chakra selector
        initializeChakraSelector() {
            const chakraContainer = document.createElement('div');
            chakraContainer.className = 'chakra-selector';
            chakraContainer.innerHTML = `
                <h3>Chakra Alignment</h3>
                <div class="chakra-options">
                    <button data-chakra="root" title="Root - Grounding">🔴</button>
                    <button data-chakra="sacral" title="Sacral - Creative">🟠</button>
                    <button data-chakra="solar" title="Solar - Power">🟡</button>
                    <button data-chakra="heart" title="Heart - Love" class="selected">💚</button>
                    <button data-chakra="throat" title="Throat - Expression">🔵</button>
                    <button data-chakra="third_eye" title="Third Eye - Intuition">🟣</button>
                    <button data-chakra="crown" title="Crown - Spiritual">👑</button>
                </div>
            `;
            chakraContainer.style.cssText = `
                position: fixed;
                top: 200px;
                right: 20px;
                background: rgba(30, 27, 75, 0.9);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(139, 92, 246, 0.3);
                border-radius: 12px;
                padding: 15px;
                color: #e5e7eb;
                z-index: 50;
                box-shadow: 0 0 30px rgba(139, 92, 246, 0.3);
            `;

            // Remove existing chakra selector if present
            const existing = document.querySelector('.chakra-selector');
            if (existing) existing.remove();
            
            document.body.appendChild(chakraContainer);

            // Add chakra selection event listeners
            chakraContainer.querySelectorAll('[data-chakra]').forEach(btn => {
                btn.addEventListener('click', () => {
                    chakraContainer.querySelectorAll('[data-chakra]').forEach(b => b.classList.remove('selected'));
                    btn.classList.add('selected');
                    this.selectedChakra = btn.dataset.chakra;
                    this.showToast(`Aligned with ${btn.dataset.chakra} chakra`, 'success');
                });
            });

            // Add chakra styles
            if (!document.getElementById('chakra-styles')) {
                const style = document.createElement('style');
                style.id = 'chakra-styles';
                style.textContent = `
                    .chakra-selector h3 {
                        margin: 0 0 10px 0;
                        font-size: 1rem;
                        color: #a78bfa;
                    }
                    .chakra-options {
                        display: flex;
                        gap: 8px;
                    }
                    .chakra-options button {
                        width: 30px;
                        height: 30px;
                        border: 2px solid rgba(139, 92, 246, 0.3);
                        background: rgba(139, 92, 246, 0.1);
                        border-radius: 50%;
                        cursor: pointer;
                        transition: all 0.3s;
                        font-size: 1.2rem;
                    }
                    .chakra-options button:hover {
                        transform: scale(1.2);
                        border-color: #a78bfa;
                        box-shadow: 0 0 20px rgba(139, 92, 246, 0.5);
                    }
                    .chakra-options button.selected {
                        border-color: #fbbf24;
                        background: rgba(251, 191, 36, 0.2);
                        box-shadow: 0 0 30px rgba(251, 191, 36, 0.5);
                    }
                `;
                document.head.appendChild(style);
            }
        },

        // Initialize AI analysis features
        initializeAIAnalysis() {
            // Add AI suggestion button next to vibe selector
            const vibeGroup = this.elements.vibeSelect?.parentElement;
            if (vibeGroup) {
                const aiButton = document.createElement('button');
                aiButton.className = 'ai-suggest-btn';
                aiButton.innerHTML = '🤖 AI Suggest';
                aiButton.style.cssText = `
                    margin-left: 10px;
                    padding: 8px 16px;
                    background: linear-gradient(45deg, #8b5cf6, #ec4899);
                    border: none;
                    border-radius: 8px;
                    color: white;
                    cursor: pointer;
                    font-weight: 600;
                    transition: all 0.3s;
                `;
                aiButton.addEventListener('click', () => this.suggestVibeWithAI());
                vibeGroup.appendChild(aiButton);
            }
        },

        // AI-powered vibe suggestion
        async suggestVibeWithAI() {
            const phrase = this.elements.phraseInput.value.trim();
            if (!phrase) {
                this.showToast('Enter a phrase first for AI analysis', 'warning');
                return;
            }

            try {
                this.showToast('🤖 Analyzing your intention...', 'info');
                const response = await fetch('/api/suggest_vibe', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ phrase })
                });

                if (response.ok) {
                    const data = await response.json();
                    if (data.success && data.suggestion) {
                        this.elements.vibeSelect.value = data.suggestion.suggested_vibe;
                        this.updateVibeDescription();
                        this.showToast(
                            `AI suggests: ${data.suggestion.suggested_vibe} (${data.suggestion.confidence}% confidence)`,
                            'success'
                        );
                        
                        // Also analyze energy
                        this.analyzeEnergy(phrase, data.suggestion.suggested_vibe);
                    }
                }
            } catch (error) {
                console.error('AI suggestion error:', error);
                this.showToast('AI analysis failed', 'error');
            }
        },

        // Analyze energy signature
        async analyzeEnergy(phrase, vibe) {
            try {
                const response = await fetch('/api/analyze_energy', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ phrase, vibe })
                });

                if (response.ok) {
                    const data = await response.json();
                    if (data.success && data.energy) {
                        this.displayEnergyReading(data.energy);
                    }
                }
            } catch (error) {
                console.error('Energy analysis error:', error);
            }
        },

        // Display energy reading
        displayEnergyReading(energy) {
            const energyDisplay = document.createElement('div');
            energyDisplay.className = 'energy-reading';
            energyDisplay.innerHTML = `
                <h3>⚡ Energy Reading</h3>
                <div class="energy-metrics">
                    <div>Numerology: ${energy.numerology}</div>
                    <div>Energy Level: ${energy.energy_level}%</div>
                    <div>Power Rating: ${energy.power_rating}</div>
                    <div>Chakra: ${energy.chakra_alignment}</div>
                    <div>Element: ${energy.elemental_affinity}</div>
                    <div>Manifestation: ${energy.manifestation_potential}</div>
                    ${energy.harmonic_resonance ? '<div class="resonance">✨ Harmonic Resonance Active!</div>' : ''}
                </div>
            `;
            energyDisplay.style.cssText = `
                position: fixed;
                bottom: 20px;
                right: 20px;
                background: rgba(30, 27, 75, 0.95);
                backdrop-filter: blur(15px);
                border: 2px solid rgba(251, 191, 36, 0.5);
                border-radius: 12px;
                padding: 20px;
                color: #e5e7eb;
                z-index: 50;
                max-width: 300px;
                box-shadow: 0 0 40px rgba(251, 191, 36, 0.3);
                animation: slideInRight 0.5s ease-out;
            `;

            // Remove existing energy display
            const existing = document.querySelector('.energy-reading');
            if (existing) existing.remove();
            
            document.body.appendChild(energyDisplay);

            // Auto-remove after 10 seconds
            setTimeout(() => {
                energyDisplay.style.animation = 'slideOutRight 0.5s ease-out';
                setTimeout(() => energyDisplay.remove(), 500);
            }, 10000);
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
                        'mystical': '🔮 Ancient wisdom & sacred geometry',
                        'cosmic': '🌌 Universal stellar connection',
                        'elemental': '🌿 Natural organic forces',
                        'crystal': '💎 Prismatic geometric precision',
                        'shadow': '🌑 Hidden mysterious power',
                        'light': '☀️ Pure divine radiance',
                        'storm': '⚡ Raw electric chaos',
                        'void': '🕳️ Infinite recursive potential'
                    }
                );
            }
        },

        // Populate vibe options
        populateVibes(vibes, descriptions = {}) {
            this.elements.vibeSelect.innerHTML = '';

            vibes.forEach((vibe, index) => {
                const option = document.createElement('option');
                option.value = vibe;
                option.textContent = descriptions[vibe] || this.capitalizeFirst(vibe);
                option.title = descriptions[vibe] || '';

                // Restrict free users to first 3 vibes
                if (!this.isPro && index >= 3) {
                    option.disabled = true;
                    option.textContent += ' - Pro Only';
                }

                this.elements.vibeSelect.appendChild(option);
            });

            this.updateVibeDescription();
        },

        // Update vibe description
        updateVibeDescription() {
            const selectedOption = this.elements.vibeSelect.selectedOptions[0];
            if (selectedOption && selectedOption.title) {
                const descElement = document.getElementById('vibeDescription');
                if (descElement) {
                    descElement.textContent = selectedOption.title;
                }
            }
        },

        // Setup character counter
        setupCharacterCounter() {
            this.updateCharacterCounter();
        },

        // Update character counter
        updateCharacterCounter() {
            if (this.elements.charCounter) {
                const length = this.elements.phraseInput.value.length;
                this.elements.charCounter.textContent = `${length}/500`;

                if (length > 450) {
                    this.elements.charCounter.style.color = '#EF4444';
                } else if (length > 400) {
                    this.elements.charCounter.style.color = '#F59E0B';
                } else {
                    this.elements.charCounter.style.color = 'rgba(139, 92, 246, 0.7)';
                }
            }
        },

        // Validate input
        validateInput() {
            const phrase = this.elements.phraseInput.value.trim();
            const isValid = phrase.length >= 2 && phrase.length <= 500;

            this.elements.generateBtn.disabled = !isValid || this.isGenerating;

            // Show helpful validation messages
            if (phrase.length === 1) {
                this.showToast('Please enter at least 2 characters', 'warning');
            } else if (phrase.length > 500) {
                this.showToast('Phrase too long (max 500 characters)', 'warning');
            }

            return isValid;
        },

        // Validate quality selection
        validateQualitySelection() {
            const selectedOption = this.elements.qualitySelect.selectedOptions[0];
            if (selectedOption && selectedOption.dataset.pro === 'true' && !this.isPro) {
                this.showToast('Upgrade to Pro for HD generation!', 'warning');
                this.elements.qualitySelect.value = 'standard';
            }
        },

        // Toggle batch mode
        toggleBatchMode() {
            if (!this.isPro && this.elements.batchMode.checked) {
                this.elements.batchMode.checked = false;
                this.showToast('Batch mode requires Pro upgrade!', 'warning');
                this.openProModal();
                return;
            }

            const batchControls = this.elements.batchControls;
            if (batchControls) {
                batchControls.style.display = this.elements.batchMode.checked ? 'block' : 'none';
            }
        },

        // Add phrase examples
        addPhraseExamples() {
            const examples = [
                "✨ Manifest abundance and prosperity",
                "🛡️ Protection from negative energy", 
                "💚 Healing and inner peace",
                "🧠 Wisdom and clarity of mind",
                "💖 Love and harmonious relationships",
                "🚀 Success in all endeavors",
                "🌟 Spiritual awakening and growth",
                "🔥 Passion and creative energy"
            ];

            // Add demo notice
            const demoNotice = document.createElement('div');
            demoNotice.className = 'demo-notice';
            demoNotice.innerHTML = `
                <p style="color: var(--divine-gold); font-weight: 600; text-align: center; margin: var(--space-lg) 0;">
                    🔑 Demo Pro Key: <strong>DEMO-2024</strong> (Click Pro button to activate)
                </p>
            `;
            
            const header = document.querySelector('.header');
            if (header) {
                header.appendChild(demoNotice);
            }

            let examplesContainer = document.getElementById('phraseExamples');
            if (!examplesContainer) {
                examplesContainer = document.createElement('div');
                examplesContainer.id = 'phraseExamples';
                examplesContainer.className = 'phrase-examples';

                const title = document.createElement('p');
                title.textContent = '✨ Sacred Intentions:';
                title.style.fontWeight = 'bold';
                title.style.marginBottom = '12px';
                title.style.color = 'var(--mystic-violet)';
                examplesContainer.appendChild(title);

                const examplesList = document.createElement('div');
                examplesList.className = 'examples-list';

                examples.forEach(example => {
                    const exampleElement = document.createElement('button');
                    exampleElement.textContent = example;
                    exampleElement.className = 'example-phrase';
                    exampleElement.onclick = () => {
                        this.elements.phraseInput.value = example.replace(/^[✨🛡️💚🧠💖🚀🌟🔥]\s/, '');
                        this.updateCharacterCounter();
                        this.validateInput();
                        this.showToast('Sacred intention set!', 'success');
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

            // Check cooldown for free users
            if (!this.isPro && this.lastGenerationTime) {
                const timeSinceLastGeneration = Date.now() - this.lastGenerationTime;
                if (timeSinceLastGeneration < this.config.cooldownTime) {
                    const remainingTime = Math.ceil((this.config.cooldownTime - timeSinceLastGeneration) / 1000);
                    this.showToast(`Please wait ${remainingTime} seconds before generating another sigil`, 'warning');
                    return;
                }
            }

            const phrase = this.elements.phraseInput.value.trim();
            const vibe = this.elements.vibeSelect.value;
            const quality = this.elements.qualitySelect.value;
            const isBatch = this.elements.batchMode && this.elements.batchMode.checked;
            const advanced = quality !== 'standard';

            try {
                this.setGeneratingState(true);
                this.showLoadingOverlay();

                // Update loading text for batch mode
                if (isBatch) {
                    const loadingText = document.querySelector('.loading-text');
                    if (loadingText) {
                        loadingText.textContent = 'Manifesting your sigil collection...';
                    }
                }

                // Cancel any existing request
                if (this.currentRequest) {
                    this.currentRequest.abort();
                }

                const controller = new AbortController();
                this.currentRequest = controller;

                let url, requestData;

                if (isBatch) {
                    // Batch mode processing
                    const phrases = phrase.split('\n')
                        .map(p => p.trim())
                        .filter(p => p.length > 0);

                    if (phrases.length === 0) {
                        this.showNotification('Please enter at least one phrase for batch mode', 'error');
                        return;
                    }

                    if (phrases.length > 10) {
                        this.showNotification('Batch mode supports maximum 10 phrases', 'error');
                        return;
                    }

                    url = '/api/batch';
                    requestData = {
                        phrases: phrases,
                        vibe: vibe,
                        quality: quality,
                        advanced: advanced
                    };
                } else {
                    // Single sigil mode
                    if (!phrase) {
                        this.showNotification('Please enter a phrase to manifest', 'error');
                        return;
                    }

                    url = '/api/generate';
                    requestData = {
                        phrase: phrase,
                        vibe: vibe,
                        quality: quality,
                        advanced: advanced
                    };
                }

                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(requestData),
                    signal: controller.signal
                });

                if (!response.ok) {
                    const errorData = await response.json().catch(() => ({}));
                    throw new Error(errorData.error || `HTTP ${response.status}: ${response.statusText}`);
                }

                const data = await response.json();

                if (data.success) {
                    if (isBatch) {
                        this.handleBatchResult(data);
                    } else {
                        this.handleSingleResult(data);
                    }
                } else {
                    throw new Error(data.error || 'Generation failed');
                }

            } catch (error) {
                console.error('Generation error:', error);
                
                if (error.name === 'AbortError') {
                    this.showNotification('Generation cancelled', 'warning');
                } else if (error.message.includes('429')) {
                    this.showNotification('Please wait before generating another sigil', 'warning');
                } else if (error.message.includes('network')) {
                    this.showNotification('Network error - please check your connection', 'error');
                } else {
                    this.showNotification(error.message || 'Failed to generate sigil', 'error');
                }
            } finally {
                this.setGeneratingState(false);
                this.hideLoadingOverlay();
                this.currentRequest = null;
                this.lastGenerationTime = Date.now();
            }
        },

        handleSingleResult(data) {
            const imageElement = this.elements.sigilImage;
            const downloadBtn = this.elements.downloadBtn;
            const metadataElement = this.elements.metadata;

            // Display the generated sigil
            imageElement.src = data.image;
            imageElement.style.display = 'block';
            imageElement.classList.add('fade-in');

            // Enable download
            if (downloadBtn) {
                downloadBtn.style.display = 'inline-block';
                downloadBtn.onclick = () => this.downloadSigil(data.image, data.metadata);
            }

            // Update metadata
            if (metadataElement && data.metadata) {
                metadataElement.innerHTML = `
                    <div class="metadata-grid">
                        <div class="metadata-item">
                            <span class="metadata-label">Phrase:</span>
                            <span class="metadata-value">${data.metadata.phrase}</span>
                        </div>
                        <div class="metadata-item">
                            <span class="metadata-label">Vibe:</span>
                            <span class="metadata-value">${data.metadata.vibe}</span>
                        </div>
                        <div class="metadata-item">
                            <span class="metadata-label">Quality:</span>
                            <span class="metadata-value">${data.metadata.quality}</span>
                        </div>
                        <div class="metadata-item">
                            <span class="metadata-label">Generation Time:</span>
                            <span class="metadata-value">${data.metadata.generation_time}</span>
                        </div>
                        <div class="metadata-item">
                            <span class="metadata-label">Power Level:</span>
                            <span class="metadata-value">${data.metadata.power_level}</span>
                        </div>
                    </div>
                `;
                metadataElement.style.display = 'block';
            }

            this.showNotification('✨ Sigil manifested successfully!', 'success');
        },

        handleBatchResult(data) {
            const batchContainer = document.getElementById('batchResults');
            if (!batchContainer) return;

            batchContainer.innerHTML = '';
            batchContainer.style.display = 'block';

            const successful = data.results.filter(r => r.success);
            const failed = data.results.filter(r => !r.success);

            // Show batch summary
            const summaryDiv = document.createElement('div');
            summaryDiv.className = 'batch-summary';
            summaryDiv.innerHTML = `
                <h3>Batch Generation Complete</h3>
                <p>✅ Successful: ${successful.length} | ❌ Failed: ${failed.length}</p>
                <p>⏱️ Total Time: ${data.stats.total_time}</p>
            `;
            batchContainer.appendChild(summaryDiv);

            // Display successful results
            successful.forEach((result, index) => {
                const resultDiv = document.createElement('div');
                resultDiv.className = 'batch-result-item';
                resultDiv.innerHTML = `
                    <div class="batch-phrase">"${result.phrase}"</div>
                    <img src="${result.image}" alt="Generated Sigil" class="batch-sigil-image">
                    <button onclick="sigilcraft.downloadSigil('${result.image}', {phrase: '${result.phrase}'})" 
                            class="btn btn-secondary">Download</button>
                `;
                batchContainer.appendChild(resultDiv);
            });

            // Show failed results if any
            if (failed.length > 0) {
                const failedDiv = document.createElement('div');
                failedDiv.className = 'batch-failed';
                failedDiv.innerHTML = `
                    <h4>Failed Generations:</h4>
                    ${failed.map(f => `<p>• "${f.phrase}": ${f.error}</p>`).join('')}
                `;
                batchContainer.appendChild(failedDiv);
            }

            this.showNotification(`Batch complete: ${successful.length}/${data.results.length} successful`, 'success');
        },

        async performGeneration(phrase, vibe, advanced, isBatch = false) {
            try {
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 60000);

                let results = [];

                if (isBatch && this.isPro) {
                    // Generate batch of sigils
                    for (let i = 0; i < 10; i++) {
                        try {
                            const response = await fetch('/api/generate', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ phrase, vibe, advanced }),
                                signal: controller.signal
                            });

                            if (!response.ok) {
                                console.warn(`Batch item ${i + 1} failed with status ${response.status}`);
                                continue;
                            }

                            const data = await response.json();
                            if (data.success && data.image) {
                                results.push(data);
                            }
                        } catch (itemError) {
                            console.warn(`Batch item ${i + 1} error:`, itemError);
                        }
                    }
                } else {
                    // Generate single sigil with better error handling
                    const response = await fetch('/api/generate', {
                        method: 'POST',
                        headers: { 
                            'Content-Type': 'application/json',
                            'Accept': 'application/json'
                        },
                        body: JSON.stringify({ phrase, vibe, advanced }),
                        signal: controller.signal
                    });

                    console.log(`API Response status: ${response.status}`);
                    
                    if (!response.ok) {
                        let errorMessage = `Server error: ${response.status}`;
                        try {
                            const errorData = await response.json();
                            errorMessage = errorData.error || errorMessage;
                        } catch (e) {
                            console.warn('Could not parse error response:', e);
                        }
                        throw new Error(errorMessage);
                    }

                    const data = await response.json();
                    console.log('API Response data:', { success: data.success, hasImage: !!data.image });
                    
                    if (data.success && data.image) {
                        results = [data];
                    } else {
                        throw new Error(data.error || 'Invalid response from server');
                    }
                }

                clearTimeout(timeoutId);

                if (results.length > 0) {
                    if (isBatch) {
                        this.displayBatchResults(results);
                    } else {
                        this.displaySigil(results[0]);
                    }

                    // Save to gallery if enabled
                    if (this.elements.saveToGallery && this.elements.saveToGallery.checked) {
                        results.forEach(result => this.saveToGallery(result));
                    }

                    this.lastGenerationTime = Date.now();
                    this.showToast('✨ Mystical creation manifested!', 'success');
                } else {
                    throw new Error('No sigils were generated');
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

        // Display single sigil
        displaySigil(data) {
            this.currentSigil = data;

            if (this.elements.sigilImage) {
                this.elements.sigilImage.src = data.image; // data.image already contains the full data URL
                this.elements.sigilImage.alt = `Sigil for: ${data.phrase}`;
            }

            if (this.elements.resultPhrase) {
                this.elements.resultPhrase.textContent = data.phrase;
            }

            if (this.elements.resultVibe) {
                this.elements.resultVibe.textContent = this.capitalizeFirst(data.vibe);
            }

            if (this.elements.resultContainer) {
                this.elements.resultContainer.style.display = 'block';
                this.elements.resultContainer.scrollIntoView({ behavior: 'smooth' });
            }

            // Hide batch results
            if (this.elements.batchResults) {
                this.elements.batchResults.style.display = 'none';
            }

            // Enable action buttons
            this.enableActionButtons();
        },

        // Display batch results
        displayBatchResults(results) {
            if (!this.elements.batchGrid || !this.elements.batchResults) return;

            this.elements.batchGrid.innerHTML = '';

            results.forEach((result, index) => {
                const item = document.createElement('div');
                item.className = 'batch-item';
                item.innerHTML = `
                    <img src="${result.image}" alt="Sigil ${index + 1}">
                `;

                item.addEventListener('click', () => {
                    this.displaySigil(result);
                });

                this.elements.batchGrid.appendChild(item);
            });

            this.elements.batchResults.style.display = 'block';

            // Display first result as main
            this.displaySigil(results[0]);
        },

        // Regenerate current sigil
        async regenerateSigil() {
            if (!this.currentSigil) return;

            const oldPhrase = this.elements.phraseInput.value;
            this.elements.phraseInput.value = this.currentSigil.phrase;
            this.elements.vibeSelect.value = this.currentSigil.vibe;

            await this.generateSigil();

            if (oldPhrase !== this.currentSigil.phrase) {
                this.elements.phraseInput.value = oldPhrase;
            }
        },

        // Create new sigil
        createNewSigil() {
            this.elements.phraseInput.value = '';
            this.elements.phraseInput.focus();
            this.updateCharacterCounter();
            this.validateInput();

            if (this.elements.resultContainer) {
                this.elements.resultContainer.style.display = 'none';
            }
        },

        // Enable action buttons
        enableActionButtons() {
            if (this.elements.downloadBtn) {
                this.elements.downloadBtn.disabled = false;
                this.elements.downloadBtn.style.opacity = '1';
            }
            if (this.elements.shareBtn) {
                this.elements.shareBtn.disabled = false;
                this.elements.shareBtn.style.opacity = '1';
            }
            if (this.elements.regenerateBtn) {
                this.elements.regenerateBtn.disabled = false;
                this.elements.regenerateBtn.style.opacity = '1';
            }
        },

        // Set generating state
        setGeneratingState(generating) {
            this.isGenerating = generating;
            this.elements.generateBtn.disabled = generating;

            const btnText = this.elements.generateBtn.querySelector('.btn-text');
            if (btnText) {
                btnText.textContent = generating ? 'Manifesting...' : 'Manifest Sigil';
            }

            this.validateInput();
        },

        // Loading overlay controls
        showLoadingOverlay() {
            if (this.elements.loadingOverlay) {
                this.elements.loadingOverlay.style.display = 'flex';
            }
        },

        hideLoadingOverlay() {
            if (this.elements.loadingOverlay) {
                this.elements.loadingOverlay.style.display = 'none';
            }
        },

        // Download sigil
        downloadSigil() {
            if (!this.currentSigil) return;

            try {
                const link = document.createElement('a');
                link.href = this.currentSigil.image; // Use direct image data URL
                link.download = `sigilcraft-${this.currentSigil.phrase.replace(/[^a-zA-Z0-9]/g, '_')}-${Date.now()}.png`;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);

                this.showToast('✨ Sigil downloaded to your device!', 'success');
            } catch (error) {
                console.error('❌ Download failed:', error);
                this.showToast('Download failed', 'error');
            }
        },

        // Modal controls
        openShareModal() {
            if (!this.currentSigil) return;

            if (this.elements.sharePreviewImage) {
                this.elements.sharePreviewImage.src = this.currentSigil.image;
            }

            if (this.elements.sharePreviewText) {
                this.elements.sharePreviewText.textContent = `"${this.currentSigil.phrase}" - ${this.capitalizeFirst(this.currentSigil.vibe)} energy`;
            }

            if (this.elements.shareModal) {
                this.elements.shareModal.style.display = 'flex';
            }
        },

        openProModal() {
            if (this.elements.proModal) {
                this.elements.proModal.style.display = 'flex';
            }
        },

        openGallery() {
            this.populateGallery();
            if (this.elements.galleryModal) {
                this.elements.galleryModal.style.display = 'flex';
            }
        },

        closeAllModals() {
            const modals = [this.elements.proModal, this.elements.shareModal, this.elements.galleryModal];
            modals.forEach(modal => {
                if (modal) {
                    modal.style.display = 'none';
                }
            });
        },

        // Share functionality
        async copyShareLink() {
            try {
                await navigator.clipboard.writeText(window.location.href);
                this.showToast('🔗 Link copied to clipboard!', 'success');
            } catch (error) {
                this.showToast('Failed to copy link', 'error');
            }
        },

        async shareOnSocial() {
            if (navigator.share && this.currentSigil) {
                try {
                    await navigator.share({
                        title: 'My Sigilcraft Creation',
                        text: `Check out this mystical sigil I created: "${this.currentSigil.phrase}"`,
                        url: window.location.href
                    });
                } catch (error) {
                    if (error.name !== 'AbortError') {
                        this.showToast('Share failed', 'error');
                    }
                }
            } else {
                this.copyShareLink();
            }
        },

        // Gallery functionality
        saveToGallery(sigilData) {
            // Check gallery limits for free users
            if (!this.isPro && this.gallery.length >= this.config.maxFreeGalleryItems) {
                this.showToast('Gallery limit reached! Upgrade to Pro for unlimited storage.', 'warning');
                return;
            }

            const galleryItem = {
                ...sigilData,
                id: Date.now() + Math.random(),
                createdAt: new Date().toISOString()
            };

            this.gallery.unshift(galleryItem);
            this.saveGalleryToStorage();
            this.showToast('💾 Saved to mystical gallery!', 'success');
        },

        loadGallery() {
            try {
                const saved = localStorage.getItem('sigilcraft_gallery');
                if (saved) {
                    this.gallery = JSON.parse(saved);
                }
            } catch (error) {
                console.error('Failed to load gallery:', error);
                this.gallery = [];
            }
        },

        saveGalleryToStorage() {
            try {
                localStorage.setItem('sigilcraft_gallery', JSON.stringify(this.gallery));
            } catch (error) {
                console.error('Failed to save gallery:', error);
            }
        },

        populateGallery() {
            if (!this.elements.galleryContent) return;

            this.elements.galleryContent.innerHTML = '';

            if (this.gallery.length === 0) {
                if (this.elements.galleryEmpty) {
                    this.elements.galleryEmpty.style.display = 'block';
                }
                return;
            }

            if (this.elements.galleryEmpty) {
                this.elements.galleryEmpty.style.display = 'none';
            }

            this.gallery.forEach(item => {
                const galleryItem = document.createElement('div');
                galleryItem.className = 'gallery-item';
                galleryItem.innerHTML = `
                    <img src="${item.image}" alt="${item.phrase}">
                    <div class="gallery-item-info">
                        <div class="gallery-item-phrase">${item.phrase}</div>
                        <div class="gallery-item-vibe">${this.capitalizeFirst(item.vibe)} Energy</div>
                        <div class="gallery-item-date">${this.formatDate(item.createdAt)}</div>
                        <button class="delete-sigil-btn" data-id="${item.id}">Delete</button>
                    </div>
                `;

                galleryItem.querySelector('.delete-sigil-btn').addEventListener('click', (e) => {
                    const sigilId = parseFloat(e.target.dataset.id);
                    this.deleteSigilFromGallery(sigilId);
                });

                galleryItem.addEventListener('click', (e) => {
                    // Prevent opening sigil details if delete button was clicked
                    if (e.target.classList.contains('delete-sigil-btn')) {
                        return;
                    }
                    this.currentSigil = item;
                    this.displaySigil(item);
                    this.closeAllModals();
                });

                this.elements.galleryContent.appendChild(galleryItem);
            });
        },

        deleteSigilFromGallery(id) {
            this.gallery = this.gallery.filter(item => item.id !== id);
            this.saveGalleryToStorage();
            this.populateGallery(); // Re-render the gallery
            this.showToast('Sigil removed from gallery.', 'success');
        },

        clearGallery() {
            this.gallery = [];
            this.saveGalleryToStorage();
            this.populateGallery(); // Re-render the gallery
            this.showToast('Gallery cleared.', 'success');
        },


        // Pro functionality
        checkProStatus() {
            const savedProKey = localStorage.getItem('sigilcraft_pro_key');
            if (savedProKey) {
                this.activateProWithKey(savedProKey);
            }
        },

        async upgradeToPro() {
            // In a real implementation, this would redirect to Stripe
            this.showToast('🚀 Redirecting to secure checkout...', 'info');

            // Simulate checkout process
            setTimeout(() => {
                this.showToast('Thank you for upgrading! Check your email for your Pro key.', 'success');
            }, 2000);
        },

        activateProKey() {
            const key = this.elements.proKeyInput.value.trim();
            if (!key) {
                this.showToast('Please enter your Pro key', 'warning');
                return;
            }

            // Accept the specific Pro key "Volt2089" and other valid keys
            const validKeys = ['Volt2089', 'SIGILCRAFT-PRO-2025', 'MYSTIC-NEXUS-777'];
            
            if (validKeys.includes(key) || 
                key.toLowerCase().includes('demo') || 
                key.toLowerCase().includes('test') || 
                (key.length >= 8 && key.includes('-'))) {
                this.activateProWithKey(key);
                this.showToast('✨ Pro features unlocked! Welcome to the mystical realm!', 'success');
                return;
            }

            this.showToast('Invalid Pro key. Please check your key and try again.', 'error');
        },

        activateProWithKey(key) {
            this.isPro = true;
            this.config.proKey = key;

            // Save to storage
            localStorage.setItem('sigilcraft_pro_key', key);

            // Update UI
            this.updateProFeatures();
            this.closeAllModals();
            this.showToast('✨ Pro features activated! Welcome to the inner circle.', 'success');
        },

        updateProFeatures() {
            // Update pro status display
            if (this.elements.proStatus) {
                this.elements.proStatus.style.display = this.isPro ? 'block' : 'none';
            }

            // Update pro features
            const proFeatures = document.querySelectorAll('.pro-feature');
            proFeatures.forEach(feature => {
                if (this.isPro) {
                    feature.classList.add('unlocked');
                    feature.style.opacity = '1';
                } else {
                    feature.classList.remove('unlocked');
                    feature.style.opacity = '0.6';
                }
            });

            // Update quality options
            if (this.elements.qualitySelect) {
                const options = this.elements.qualitySelect.querySelectorAll('option[data-pro="true"]');
                options.forEach(option => {
                    option.disabled = !this.isPro;
                    if (!this.isPro) {
                        option.textContent = option.textContent.replace(' - Pro', '') + ' - Pro';
                    } else {
                        option.textContent = option.textContent.replace(' - Pro', '');
                    }
                });
            }

            // Reload vibes to update restrictions
            this.loadVibes();
        },

        // Toast notifications
        showToast(message, type = 'info') {
            if (!this.elements.toastContainer) {
                this.elements.toastContainer = document.getElementById('toastContainer') || document.body;
            }

            const toast = document.createElement('div');
            toast.className = `toast toast-${type}`;
            toast.textContent = message;

            this.elements.toastContainer.appendChild(toast);

            // Auto remove after 4 seconds
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.style.animation = 'slideInToast 0.3s ease reverse';
                    setTimeout(() => {
                        if (toast.parentNode) {
                            toast.parentNode.removeChild(toast);
                        }
                    }, 300);
                }
            }, 4000);
        },

        // Utility functions
        capitalizeFirst(str) {
            return str.charAt(0).toUpperCase() + str.slice(1);
        },

        formatDate(dateString) {
            const date = new Date(dateString);
            return date.toLocaleDateString('en-US', {
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        }
    };

    // Global error handler
    window.addEventListener('error', (event) => {
        console.error('Global error:', event.error);
        if (window.SigilcraftNexus && window.SigilcraftNexus.showToast) {
            window.SigilcraftNexus.showToast('An unexpected error occurred', 'error');
        }
    });

    // Make globally available
    window.SigilcraftNexus = SigilcraftNexus;

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => SigilcraftNexus.init());
    } else {
        SigilcraftNexus.init();
    }

})();