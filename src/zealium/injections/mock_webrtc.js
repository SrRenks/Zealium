(function() {
    Object.defineProperty(RTCIceCandidate.prototype, 'address', {
        get: () => '192.168.0.' + Math.floor(Math.random() * 100 + 1)
    });
})();