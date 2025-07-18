(() => {
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
})();
