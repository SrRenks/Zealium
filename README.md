# Zealium

**Zealium** is a stealthy Chromium remote-control toolkit leveraging the Chrome DevTools Protocol with dynamic JavaScript injection to evade bot detection. It provides multi-layered anti-fingerprinting patches, human-like interaction simulation, and robust stealth capabilities for advanced browser automation.

---

## Features

- **Stealth Browser Automation:**  
  Control Chromium-based browsers (Chrome, Edge) remotely with powerful stealth techniques to bypass modern bot detection systems and CAPTCHAs.

- **Dynamic JS Injection:**  
  Inject custom JavaScript patches at runtime to spoof browser fingerprints, including canvas, WebGL, audio, navigator properties, media devices, WebRTC, permissions, and more.

- **Human Behavior Simulation:**  
  Simulate natural mouse movements, clicks, scrolling, and typing with randomized, non-linear patterns, hesitations, and noise to mimic real user interactions.

- **Cross-Platform Support:**  
  Compatible with Windows, macOS, and Linux environments, detecting browser executables and managing user profiles seamlessly.

- **Customizable Stealth Levels:**  
  Choose from multiple preset stealth configurations (`low`, `normal`, `strict`), or supply your own patch methods for tailored stealth strategies.

---

## Installation

Requires Python 3.11+ and a Chromium-based browser installed.

```bash
pip install zealium
````

Or install dependencies manually with Poetry:

```bash
poetry install
```

---

## Usage Example

```python
from zealium import Zealium

# Launch browser with stealth
zealium = Zealium(browser="chrome", stealth_level="normal")
zealium.launch()

# Use human behavior simulator to type text
zealium.human.type_text("Hello, Zealium!")

# Interact stealthily via DevTools Protocol...

# Clean up
zealium.close()
```

---

## Stealth Toolkit

Zealium includes a collection of JavaScript patches injected into the browser context to evade detection, such as:

* Spoofing `navigator.webdriver` and other common bot signals
* Canvas fingerprint noise and spoofing
* WebGL precision spoofing
* Overriding `Function.prototype.toString`
* Mocking `navigator.plugins` and `navigator.mimeTypes`
* Faking `chrome.runtime`
* Neutralizing WebRTC IP leaks
* Audio context fingerprint mitigation
* Mocking media devices and permissions queries
* Spoofing screen properties and Intl DateTime formatting

Stealth levels control which patches are applied:

* `low`: Basic evasion
* `normal`: Moderate stealth
* `strict`: Comprehensive patching

### JS Injection Scripts for Stealth Patching

The `injections/` folder contains multiple JavaScript scripts injected dynamically to spoof and patch browser APIs, avoiding detection by anti-bot and fingerprinting systems.

| File                                    | Purpose                                                                                          |
|-----------------------------------------|------------------------------------------------------------------------------------------------|
| **audio_oscillator_patch.js**            | Patches `AudioContext.createOscillator` to add random jitter, avoiding audio fingerprinting.    |
| **canvas_noise.js**                      | Adds subtle noise to canvas pixel data to avoid canvas fingerprint consistency.                  |
| **intl_datetime_patch.js**               | Overrides `Intl.DateTimeFormat.prototype.resolvedOptions` to spoof locale and timezone data.    |
| **mock_audio_fingerprint.js**            | Adds small variations in audio frequency data to mask audio fingerprint patterns.              |
| **mock_chrome_runtime.js**                | Creates a fake `chrome.runtime` object to prevent detection errors in Chrome environment checks.|
| **mock_media_devices.js**                 | Mocks `navigator.mediaDevices.enumerateDevices` to simulate camera and microphone devices.     |
| **mock_navigator_connection.js**         | Spoofs `navigator.connection` properties like `downlink`, `effectiveType`, and `rtt`.          |
| **mock_navigator_plugins_and_mimetypes.js** | Fakes `navigator.plugins` and `navigator.mimeTypes` to simulate common browser plugins.          |
| **mock_webrtc.js**                       | Disables or spoofs WebRTC APIs like `RTCPeerConnection` to prevent IP leaks and fingerprinting. |
| **navigator_properties.js**               | Spoofs multiple `navigator` properties (webdriver, plugins, languages, platform, etc.)          |
| **override_function_toString.js**         | Overrides `Function.prototype.toString` to return legitimate source code for spoofed functions. |
| **permissions_query_patch.js**            | Patches `navigator.permissions.query` to avoid errors and spoof notification permission state. |
| **rtc_peerconnection_patch.js**           | Intercepts WebRTC ICE candidates to hide local IP addresses and prevent leaks.                  |
| **screen_properties.js**                  | Spoofs screen and window size properties to mask headless or virtual environment detection.    |
| **spoof_canvas_fingerprint.js**           | Alters Canvas API methods to return noisy or altered pixel data to defeat canvas fingerprinting.|
| **spoof_webgl_precision.js**              | Modifies WebGL precision parameters to match real hardware profiles.                            |
| **webgl_spoof.js**                        | Spoofs WebGL vendor and renderer strings to appear as common GPUs (e.g., NVIDIA).               |


Injecting these scripts selectively or all together via the `StealthToolkit` module allows fine-grained control over stealth level and evasion techniques.


---

## Human Behavior Simulation

The `HumanBehaviorSimulator` mimics real user input with:

* Natural mouse movement with Bezier curves and noise
* Randomized pauses and hesitations
* Realistic typing with variable delays and error simulation
* Scrolling with randomized deltas

These features reduce detection by behavior analysis systems.

---

## Project Structure

```
zealium/
├── core.py          # Main controller for browser launch, stealth, human simulation
├── human.py         # Human input simulation (mouse, keyboard)
├── stealth.py       # JS stealth injection toolkit
└── injections/      # JS patches for fingerprint spoofing
```

---

## Future Improvements

We plan to replace the `pychrome` dependency with a custom, lightweight CDP client built from scratch. This tool will directly interact with the Chromium DevTools Protocol, offering greater control, stability, and performance, tailored specifically for stealth automation use cases.

---

## Disclaimer

Zealium is intended for educational and ethical automation use only. Misuse to violate terms of service or conduct unauthorized scraping may be illegal. Use responsibly.
