(function() {
    const toDataURL = HTMLCanvasElement.prototype.toDataURL;
    HTMLCanvasElement.prototype.toDataURL = function() {
        const ctx = this.getContext('2d');
        ctx.fillStyle = 'rgb(' + [Math.floor(Math.random()*255), Math.floor(Math.random()*255), Math.floor(Math.random()*255)].join(',') + ')';
        ctx.fillRect(0, 0, 10, 10);
        return toDataURL.apply(this, arguments);
    };
})();