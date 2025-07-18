(function() {
    Object.defineProperty(navigator, 'plugins', {
        get: () => [1, 2, 3, 4, 5]
    });
    Object.defineProperty(navigator, 'mimeTypes', {
        get: () => [1, 2]
    });
})();