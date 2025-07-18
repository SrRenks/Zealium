from pychrome.tab import Tab
import threading
import random
import time
import math


def cubic_bezier(p0, p1, p2, p3, t):
    u = 1 - t
    tt = t * t
    uu = u * u
    uuu = uu * u
    ttt = tt * t
    x = uuu * p0[0] + 3 * uu * t * p1[0] + 3 * u * tt * p2[0] + ttt * p3[0]
    y = uuu * p0[1] + 3 * uu * t * p1[1] + 3 * u * tt * p2[1] + ttt * p3[1]
    return (x, y)


def ease_in_out(t):
    return t * t * (3 - 2 * t)


def distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


class HumanMouseMover:
    def __init__(
        self,
        tab: Tab,
        move_area=((100, 100), (1400, 800)),
        min_curve_steps=30,
        max_curve_steps=50,
        pause_chance=0.02,
        pause_duration_range=(0.1, 0.4),
    ) -> None:
        self.tab = tab
        self.running = False
        self.paused = False
        self._lock = threading.Lock()
        self.thread = threading.Thread(target=self._move_loop, daemon=True)

        self.current_pos = (800, 400)
        self.target_pos = None
        self._curve_points = None
        self._curve_step = 0
        self._curve_steps = 0
        self._move_area = move_area
        self._min_curve_steps = min_curve_steps
        self._max_curve_steps = max_curve_steps
        self._pause_chance = pause_chance
        self._pause_duration_range = pause_duration_range

        self._multi_curve_queue = []

    def start(self) -> None:
        self.running = True
        self.thread.start()

    def stop(self) -> None:
        if self.running:
            self.running = False
            if self.thread.is_alive():
                self.thread.join(timeout=2)

    def pause(self) -> None:
        with self._lock:
            self.paused = True

    def resume(self) -> None:
        with self._lock:
            self.paused = False

    def _generate_next_target(self):
        x = random.uniform(self._move_area[0][0], self._move_area[1][0])
        y = random.uniform(self._move_area[0][1], self._move_area[1][1])
        return (x, y)

    def _generate_bezier_control_points(self, start, end):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        distance_val = max(distance(start, end), 1)
        norm_dx = dx / distance_val
        norm_dy = dy / distance_val

        cp1 = (
            start[0] + dx * random.uniform(0.25, 0.4) + norm_dy * random.uniform(-distance_val * 0.3, distance_val * 0.3),
            start[1] + dy * random.uniform(0.25, 0.4) - norm_dx * random.uniform(-distance_val * 0.3, distance_val * 0.3),
        )
        cp2 = (
            start[0] + dx * random.uniform(0.6, 0.75) + norm_dy * random.uniform(-distance_val * 0.3, distance_val * 0.3),
            start[1] + dy * random.uniform(0.6, 0.75) - norm_dx * random.uniform(-distance_val * 0.3, distance_val * 0.3),
        )
        return cp1, cp2

    def _enqueue_multi_curve(self, start, end, segments=2):
        points = [start]
        for i in range(1, segments):
            interp = i / segments
            inter_point = (start[0] + (end[0] - start[0]) * interp, start[1] + (end[1] - start[1]) * interp)
            points.append(inter_point)
        points.append(end)

        curves = []
        for i in range(len(points) - 1):
            cp1, cp2 = self._generate_bezier_control_points(points[i], points[i + 1])
            curves.append((points[i], cp1, cp2, points[i + 1]))
        self._multi_curve_queue.extend(curves)

    def _should_pause(self):
        return random.random() < self._pause_chance and len(self._multi_curve_queue) == 0

    def _move_loop(self) -> None:
        while self.running:
            with self._lock:
                if self.paused:
                    time.sleep(0.1)
                    continue

            if not self._multi_curve_queue and (self.target_pos is None or distance(self.current_pos, self.target_pos) < 5):
                self.target_pos = self._generate_next_target()
                dist = distance(self.current_pos, self.target_pos)

                segments = 3 if dist > 300 else 1
                self._enqueue_multi_curve(self.current_pos, self.target_pos, segments=segments)

                self._curve_step = 0
                self._curve_steps = random.randint(self._min_curve_steps, self._max_curve_steps)

            if self._multi_curve_queue:
                curve = self._multi_curve_queue[0]
                t_raw = self._curve_step / (self._curve_steps - 1)
                t = ease_in_out(t_raw)
                x, y = cubic_bezier(*curve, t)

                speed_factor = 1 - abs(t - ease_in_out(max(0, t_raw - 0.05)))
                noise_scale = 3 * speed_factor
                noise_x = random.uniform(-noise_scale, noise_scale)
                noise_y = random.uniform(-noise_scale, noise_scale)

                x_noisy = x + noise_x
                y_noisy = y + noise_y

                self.tab.call_method(
                    "Input.dispatchMouseEvent",
                    type="mouseMoved",
                    x=x_noisy,
                    y=y_noisy,
                    button="none",
                    buttons=0,
                    clickCount=0,
                )

                self.current_pos = (x, y)
                self._curve_step += 1

                if self._curve_step >= self._curve_steps:
                    self._multi_curve_queue.pop(0)
                    self._curve_step = 0
                    self._curve_steps = random.randint(self._min_curve_steps, self._max_curve_steps)

                if not self._multi_curve_queue and self._should_pause():
                    time.sleep(max(0, random.uniform(*self._pause_duration_range)))

                sleep_time = max(0.01, 0.03 - speed_factor * 0.02) + random.uniform(0, 0.01)
                time.sleep(sleep_time)
            else:
                time.sleep(0.05)


class HumanBehaviorSimulator:
    def __init__(self, tab: Tab, speed_factor: float = 1.0) -> None:
        self.tab = tab
        self.speed_factor = max(0.1, speed_factor)

    def _smooth_step(self, t: float) -> float:
        return t * t * (3 - 2 * t)

    def _sigmoid(self, x: float) -> float:
        return 1 / (1 + math.exp(-x))

    def _gaussian_noise(self, mean: float = 0, std_dev: float = 1) -> float:
        adjusted_std = std_dev * self.speed_factor
        return random.gauss(mean, adjusted_std)

    def _attention_curve(self, position: int, total_steps: int, base: float = 0.25, peak_delay: float = 0.5) -> float:
        normalized = position / max(total_steps - 1, 1)
        delay = base + (math.sin(normalized * math.pi) * peak_delay)
        noise = self._gaussian_noise(0, 0.02)
        result = max(0.05, delay + noise)
        return result * self.speed_factor

    def _hesitation_curve(self, time_passed: float, intensity: float = 1.0) -> float:
        base = 0.3
        decay = 0.4 * math.exp(-time_passed * intensity)
        result = base + decay
        return result * self.speed_factor

    def wait_for_pageload(self, timeout: int = 15) -> bool:
        start = time.time()
        while time.time() - start < timeout:
            result = self.tab.call_method("Runtime.evaluate", expression="document.readyState")
            if result["result"]["value"] == "complete":
                return True
            time.sleep(max(0, 0.3 * self.speed_factor))
        return False

    def scroll_page(self) -> None:
        for _ in range(random.randint(2, 6)):
            delta = random.randint(20, 60)
            x = random.randint(300, 600)
            y = random.randint(300, 600)

            self.tab.call_method("Input.dispatchMouseEvent",
                type="mouseWheel",
                x=x,
                y=y,
                deltaX=0,
                deltaY=delta,
                modifiers=0
            )

            time.sleep(max(0, (abs(math.sin(time.time())) * 0.2 + 0.1) * self.speed_factor))

    def type_text(self, text: str, typing_speed: float = 1.0) -> None:
        typed = ""
        digits = "0123456789"
        start_time = time.time()

        for i, char in enumerate(text):
            vk = ord(char)

            if random.random() < 0.05 and len(typed) > 1:
                wrong_digit = random.choice([d for d in digits if d != char])
                vk_wrong = ord(wrong_digit)

                self.tab.call_method("Input.dispatchKeyEvent", type="keyDown", windowsVirtualKeyCode=vk_wrong)
                time.sleep(max(0, 0.005 * typing_speed))
                self.tab.call_method("Input.dispatchKeyEvent", type="char", text=wrong_digit)
                time.sleep(max(0, 0.005 * typing_speed))
                self.tab.call_method("Input.dispatchKeyEvent", type="keyUp", windowsVirtualKeyCode=vk_wrong)
                time.sleep(max(0, 0.04 * typing_speed))

                self.tab.call_method("Input.dispatchKeyEvent", type="keyDown", windowsVirtualKeyCode=8)
                self.tab.call_method("Input.dispatchKeyEvent", type="keyUp", windowsVirtualKeyCode=8)
                time.sleep(max(0, 0.04 * typing_speed))

            self.tab.call_method("Input.dispatchKeyEvent", type="keyDown", windowsVirtualKeyCode=vk)
            time.sleep(max(0, 0.003 * typing_speed))
            self.tab.call_method("Input.dispatchKeyEvent", type="char", text=char)
            time.sleep(max(0, 0.003 * typing_speed))
            self.tab.call_method("Input.dispatchKeyEvent", type="keyUp", windowsVirtualKeyCode=vk)

            typed += char

            delay = self._attention_curve(i, len(text))
            time.sleep(max(0, delay * typing_speed))

        total_time = time.time() - start_time
        time.sleep(max(0, self._hesitation_curve(total_time) * typing_speed))

    def move_mouse(self, start_x: int, start_y: int, end_x: int, end_y: int, steps: int = 20):
        for i in range(steps):
            t = self._smooth_step(i / (steps - 1))
            x = start_x + (end_x - start_x) * t + self._gaussian_noise(0, 1.2)
            y = start_y + (end_y - start_y) * t + self._gaussian_noise(0, 1.2)

            self.tab.call_method("Input.dispatchMouseEvent", type="mouseMoved", x=x, y=y)
            time.sleep(max(0, (0.015 + self._gaussian_noise(0, 0.005)) * self.speed_factor))

    def click(self, x: int, y: int) -> None:
        origin_x = random.randint(0, 100)
        origin_y = random.randint(0, 100)
        self.move_mouse(origin_x, origin_y, x, y)

        self.tab.call_method("Input.dispatchMouseEvent", type="mousePressed", x=x, y=y, button="left", clickCount=1)
        time.sleep(max(0, (0.08 + self._gaussian_noise(0, 0.02)) * max(0.1, self.speed_factor / 2)))
        self.tab.call_method("Input.dispatchMouseEvent", type="mouseReleased", x=x, y=y, button="left", clickCount=1)
