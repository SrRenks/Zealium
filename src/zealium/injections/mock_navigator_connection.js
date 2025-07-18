(function() {
    Object.defineProperty(navigator, 'connection', {
        get: () => ({
            downlink: 10,
            effectiveType: '4g',
            rtt: 50,
            saveData: false
        })
    });
})();