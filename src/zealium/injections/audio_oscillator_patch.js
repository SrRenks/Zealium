(() => {
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
})();
