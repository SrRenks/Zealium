(function() {
    const getFloatFrequencyData = AnalyserNode.prototype.getFloatFrequencyData;
    AnalyserNode.prototype.getFloatFrequencyData = function(array) {
        const variation = Math.random() * 0.0001;
        for (let i = 0; i < array.length; i++) {
            array[i] = array[i] + variation;
        }
        return getFloatFrequencyData.call(this, array);
    };
})();