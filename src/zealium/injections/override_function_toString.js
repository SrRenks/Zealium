(function() {
    const nativeToString = Function.prototype.toString;
    const toStringProxy = new Proxy(nativeToString, {
        apply: function(target, thisArg, args) {
            if (thisArg.name === 'getParameter') {
                return 'function getParameter() { [native code] }';
            }
            return Reflect.apply(...arguments);
        }
    });
    Function.prototype.toString = toStringProxy;
})();