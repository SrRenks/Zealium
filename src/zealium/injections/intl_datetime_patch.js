(() => {
    Object.defineProperty(Intl.DateTimeFormat.prototype, 'resolvedOptions', {
        value: function() {
            return {
                locale: 'pt-BR',
                calendar: 'gregory',
                numberingSystem: 'latn',
                timeZone: 'America/Sao_Paulo'
            };
        }
    });
})();
