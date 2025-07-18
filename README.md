Sure! Here's a professional README.md draft in English for your **zealium** project, focused on stealth Chromium automation, human behavior simulation, and anti-bot fingerprint evasion:

---


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

## 🚧 Future Improvements

We plan to replace the `pychrome` dependency with a custom, lightweight CDP client built from scratch. This tool will directly interact with the Chromium DevTools Protocol, offering greater control, stability, and performance, tailored specifically for stealth automation use cases.

---

## Disclaimer

Zealium is intended for educational and ethical automation use only. Misuse to violate terms of service or conduct unauthorized scraping may be illegal. Use responsibly.


