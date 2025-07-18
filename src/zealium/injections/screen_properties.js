(() => {
    Object.defineProperty(window.screen, 'width', { get: () => 1920 });
    Object.defineProperty(window.screen, 'height', { get: () => 1080 });
    Object.defineProperty(window.screen, 'availWidth', { get: () => 1920 });
    Object.defineProperty(window.screen, 'availHeight', { get: () => 1040 });
    
    Object.defineProperty(window, 'outerWidth', { get: () => window.innerWidth + 100 });
    Object.defineProperty(window, 'outerHeight', { get: () => window.innerHeight + 100 });
})();
