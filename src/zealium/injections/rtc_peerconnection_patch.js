(() => {
    Object.defineProperty(window, 'RTCPeerConnection', {
        get: () => undefined
    });
})();