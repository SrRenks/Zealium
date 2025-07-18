(function() {
    const original = WebGLRenderingContext.prototype.getShaderPrecisionFormat;
    WebGLRenderingContext.prototype.getShaderPrecisionFormat = function() {
        return {
            rangeMin: 127,
            rangeMax: 127,
            precision: Math.floor(Math.random() * 23 + 8)
        };
    };
})();
