(() => {
    const spoofed = {
        locale: 'en-US',
        calendar: 'gregory',
        numberingSystem: 'latn',
        timeZone: 'UTC'
    };

    Object.defineProperty(Intl.DateTimeFormat.prototype, 'resolvedOptions', {
        value: () => spoofed
    });
})();
