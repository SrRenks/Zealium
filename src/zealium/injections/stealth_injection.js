(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => false });
    Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
    Object.defineProperty(navigator, 'languages', { get: () => ['pt-BR', 'pt', 'en-US', 'en'] });
    Object.defineProperty(navigator, 'platform', { get: () => 'Win32' });
    Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 8 });
    Object.defineProperty(navigator, 'deviceMemory', { get: () => 8 });
    Object.defineProperty(navigator, 'maxTouchPoints', { get: () => 1 });

    Object.defineProperty(navigator, 'userAgent', {
        get: () => 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    });

    Object.defineProperty(window.screen, 'width', { get: () => 1920 });
    Object.defineProperty(window.screen, 'height', { get: () => 1080 });
    Object.defineProperty(window.screen, 'availWidth', { get: () => 1920 });
    Object.defineProperty(window.screen, 'availHeight', { get: () => 1040 });

    const getParameter = WebGLRenderingContext.prototype.getParameter;
    WebGLRenderingContext.prototype.getParameter = function(parameter) {
        if (parameter === 37445) return "Intel Inc.";
        if (parameter === 37446) return "Intel Iris OpenGL Engine";
        return getParameter.call(this, parameter);
    };

    const toDataURL = HTMLCanvasElement.prototype.toDataURL;
    HTMLCanvasElement.prototype.toDataURL = function(...args) {
        const ctx = this.getContext('2d');
        ctx.fillStyle = 'rgba(255,255,255,0.01)';
        ctx.fillRect(0, 0, this.width, this.height);
        return toDataURL.apply(this, args);
    };

    const getImageData = CanvasRenderingContext2D.prototype.getImageData;
    CanvasRenderingContext2D.prototype.getImageData = function(x, y, w, h) {
        const imageData = getImageData.call(this, x, y, w, h);
        for (let i = 0; i < imageData.data.length; i += 4) {
            imageData.data[i] ^= 1;
            imageData.data[i+1] ^= 1;
            imageData.data[i+2] ^= 1;
        }
        return imageData;
    };

    const AudioContextPrototype = window.AudioContext && window.AudioContext.prototype;
    if (AudioContextPrototype) {
        const createOscillator = AudioContextPrototype.createOscillator;
        AudioContextPrototype.createOscillator = function() {
            const osc = createOscillator.call(this);
            const originalStart = osc.start;
            osc.start = function(when) {
                originalStart.call(this, when + Math.random() * 0.001);
            };
            return osc;
        };
    }

    const originalQuery = navigator.permissions.query;
    navigator.permissions.query = function(parameters) {
        if (parameters.name === 'notifications') {
            return Promise.resolve({ state: Notification.permission });
        }
        return originalQuery(parameters);
    };

    Object.defineProperty(window, 'RTCPeerConnection', {
        get: () => undefined
    });

    Object.defineProperty(window, 'outerWidth', { get: () => window.innerWidth + 100 });
    Object.defineProperty(window, 'outerHeight', { get: () => window.innerHeight + 100 });

    Object.defineProperty(Intl.DateTimeFormat.prototype, 'resolvedOptions', {
        value: function() {
            return {
                locale: 'pt-BR',
                calendar: 'gregory',
                numberingSystem: 'latn',
                timeZone: 'America/Sao_Paulo'
            };
        }
    });
})();
