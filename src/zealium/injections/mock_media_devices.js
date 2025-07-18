(function() {
    navigator.mediaDevices.enumerateDevices = function() {
        return Promise.resolve([
            {
                kind: 'audioinput',
                label: 'Microphone',
                deviceId: 'audio-1',
                groupId: 'group-1'
            },
            {
                kind: 'videoinput',
                label: 'Camera',
                deviceId: 'video-1',
                groupId: 'group-1'
            }
        ]);
    };
})();