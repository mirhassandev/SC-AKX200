import asyncio
import queue
import threading
import serial
from serial.tools import list_ports
import json
from pathlib import Path
from datetime import datetime
import os

import flet as ft

# Store config in user's AppData folder (writable location) instead of Program Files
CONFIG_FILE = Path(os.path.expanduser("~")) / "AppData" / "Local" / "SC-AKX200" / "panasonic_config.json"
CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)

# Named alignment constants (ft.alignment.center, .center_left, etc.) are not
# consistently present across Flet versions/builds. Building directly from
# the Alignment primitive sidesteps that entirely.
ALIGN_CENTER = ft.alignment.Alignment(0, 0)
ALIGN_CENTER_LEFT = ft.alignment.Alignment(-1, 0)


def _safe(obj, **kwargs):
    """Set attributes only if they exist on this Flet build — avoids
    AttributeError crashes from cosmetic properties that vary by version."""
    for k, v in kwargs.items():
        try:
            setattr(obj, k, v)
        except Exception:
            pass


class RemoconProtocol:
    """SPP Protocol handler for Panasonic audio systems"""

    CMD_REMOCON_IR = 0x07
    CMD_VOLUME_CONTROL = 0x28
    CMD_SOUND_SET = 0x0A
    MAGIC_START = 0xAA

    @staticmethod
    def calc_checksum(data: bytes) -> int:
        total = sum(data) & 0xFF
        return ((total ^ 0xFF) + 1) & 0xFF

    @staticmethod
    def build_frame(cmd_id: int, payload: list) -> bytes:
        payload_bytes = bytes([b & 0xFF for b in payload])
        payload_len = len(payload_bytes)

        frame = bytearray([
            RemoconProtocol.MAGIC_START,
            cmd_id & 0xFF,
            (payload_len >> 8) & 0xFF,
            payload_len & 0xFF,
        ])
        frame.extend(payload_bytes)
        frame.append(RemoconProtocol.calc_checksum(bytes(frame)))
        return bytes(frame)


class SerialWorker(threading.Thread):
    def __init__(self, command_queue, log_callback):
        super().__init__()
        self.command_queue = command_queue
        self.log_callback = log_callback
        self.daemon = True
        self.ser = None
        self.connected = False
        self.running = True
        self.port = "COM4"

    def log(self, msg: str):
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.log_callback(f"[{timestamp}] {msg}\n")

    def run(self):
        while self.running:
            try:
                if self.connected and self.ser and self.ser.is_open:
                    if self.ser.in_waiting > 0:
                        incoming = self.ser.read(self.ser.in_waiting)
                        hex_str = " ".join([f"{b:02X}" for b in incoming])
                        self.log(f"RECV  {hex_str}")

                try:
                    task = self.command_queue.get(timeout=0.05)
                except queue.Empty:
                    continue

                action = task.get("action")

                if action == "connect":
                    self.port = task.get("port", "COM4")
                    try:
                        if self.ser and self.ser.is_open:
                            self.ser.close()
                        self.ser = serial.Serial(
                            port=self.port,
                            baudrate=9600,
                            bytesize=serial.EIGHTBITS,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            timeout=1,
                            write_timeout=1,
                            rtscts=False,
                            dsrdtr=False,
                        )
                        self.connected = True
                        self.log(f"Connected to {self.port} @ 9600 baud")
                        if callable(task.get("callback")):
                            task["callback"](True, f"Connected ({self.port})")
                    except Exception as e:
                        self.connected = False
                        self.log(f"Connection failed: {e}")
                        if callable(task.get("callback")):
                            task["callback"](False, f"Failed: {e}")

                elif action == "disconnect":
                    if self.ser and self.ser.is_open:
                        self.ser.close()
                    self.connected = False
                    self.log("Disconnected")
                    if callable(task.get("callback")):
                        task["callback"](False, "Disconnected")

                elif action == "send_remocon":
                    if self.connected and self.ser and self.ser.is_open:
                        payload = task["payload"]
                        frame = RemoconProtocol.build_frame(RemoconProtocol.CMD_REMOCON_IR, payload)
                        try:
                            self.ser.write(frame)
                            self.ser.flush()
                            payload_hex = " ".join([f"{b:02X}" for b in payload])
                            frame_hex = " ".join([f"{b:02X}" for b in frame])
                            self.log(f"SEND  payload=[{payload_hex}] frame=[{frame_hex}]")
                        except Exception as e:
                            self.log(f"Send error: {e}")
                    else:
                        self.log("Not connected - payload dropped")

                self.command_queue.task_done()
            except Exception as e:
                self.log(f"Worker error: {e}")

    def stop(self):
        self.running = False


class PanasonicSCAKX200App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "SC-AKX200"
        self.page.padding = 0
        self.page.bgcolor = "#000000"
        self.page.vertical_alignment = "start"

        # A dark bgcolor alone doesn't stop Flet's built-in Material chrome
        # (dropdown menus, hover/ripple surfaces, tab indicators) from using
        # the default *light* theme underneath — that mismatch is what was
        # showing up as a big grey slab and washed-out hover states.
        _safe(self.page, theme_mode=ft.ThemeMode.DARK)

        # ---- palette: minimal / dark / Apple-adjacent ----
        self.BG_DARK = "#000000"
        self.CARD_GLASS = "#111113"
        self.CARD_BORDER = "#232326"
        self.INPUT_BG = "#17171A"
        self.INPUT_BG_HOVER = "#232327"
        self.ACCENT_BLUE = "#0A84FF"
        self.RED_ALERT = "#FF453A"
        self.ORANGE_WARN = "#FF9F0A"
        self.GREEN_OK = "#30D158"
        self.TEXT_MUTED = "#86868B"
        self.TEXT_PRIMARY = "#F5F5F7"

        self._configure_window()

        self.log_lines = []
        self.current_port = self.load_config().get("last_port", "COM4")
        self.cmd_queue = queue.Queue()
        self.worker = SerialWorker(self.cmd_queue, self.log_message)
        self.worker.start()

        self.preset_buttons = {}
        self.selected_preset = None
        self.dbass_buttons = {}
        self.selected_dbass = "off"
        self.beat_buttons = {}
        self.selected_beat = "off"

        # Double-click detection for title bar
        self._title_bar_last_click_time = 0
        self._title_bar_double_click_threshold = 0.3  # 300ms window for double-click

        self.page.on_keyboard_event = self.on_keyboard
        self.debug_visible = False

        self.build_ui()

    # ------------------------------------------------------------------
    # window chrome helpers (kept version-agnostic: try the nested
    # `page.window.*` API first, fall back to the older flat
    # `page.window_*` attributes if unavailable)
    # ------------------------------------------------------------------
    def _configure_window(self):
        w = getattr(self.page, "window", None)
        if w is not None:
            _safe(
                w,
                width=1200, height=800,
                min_width=980, min_height=680,
                frameless=True, title_bar_hidden=True,
                bgcolor=ft.Colors.TRANSPARENT,
                icon="D:\\Workspace\\Projects\\SC-AKX200\\Guillendesign-Variations-3-Music.ico",
            )
            # Intercept the native close signal too (Alt+F4, taskbar "Close
            # window", etc.) so cleanup still runs even when it wasn't our
            # custom close button that triggered the close.
            _safe(w, prevent_close=True, on_event=self._on_window_event)
        else:
            _safe(
                self.page,
                window_width=1200, window_height=800,
                window_min_width=980, window_min_height=680,
                window_frameless=True, window_title_bar_hidden=True,
                window_icon="D:\\Workspace\\Projects\\SC-AKX200\\Guillendesign-Variations-3-Music.ico",
            )

    def _win_minimize(self, e=None):
        if getattr(self, "_win_minimizing", False):
            return
        self._win_minimizing = True
        try:
            w = getattr(self.page, "window", None)
            if w is not None:
                w.minimized = True
            else:
                self.page.window_minimized = True
            self.page.update()
        except Exception as ex:
            self.log_message(f"Minimize error: {ex}\n")
        finally:
            self._win_minimizing = False

    def _win_toggle_maximize(self, e=None):
        if getattr(self, "_win_maximizing", False):
            return
        self._win_maximizing = True
        try:
            w = getattr(self.page, "window", None)
            if w is not None:
                w.maximized = not getattr(w, "maximized", False)
            else:
                self.page.window_maximized = not getattr(self.page, "window_maximized", False)
            self.page.update()
        except Exception as ex:
            self.log_message(f"Maximize error: {ex}\n")
        finally:
            self._win_maximizing = False

    def _on_title_bar_click(self, e):
        """Detect double-click on title bar for maximize/minimize.
        Uses timing-based detection: if clicks happen within 300ms, it's a double-click."""
        import time
        now = time.time()
        
        # Check if this is the second click within the threshold
        if now - self._title_bar_last_click_time < self._title_bar_double_click_threshold:
            # Double-click detected
            self._win_toggle_maximize()
            self._title_bar_last_click_time = 0  # Reset to prevent triple-clicks
        else:
            # Single click - record the time
            self._title_bar_last_click_time = now

    def _run_cleanup_once(self):
        # save_config / worker.stop / serial close must only happen once, but
        # up to three different paths can all try to trigger it (the close
        # button, a native close signal, and page.on_close as a fallback) —
        # this makes calling it more than once harmless.
        if getattr(self, "_cleanup_done", False):
            return
        self._cleanup_done = True
        self.on_closing()

    async def _on_window_event(self, e):
        # Fires for native window state changes; only act on the close
        # request (e.g. Alt+F4) since prevent_close=True stops it from
        # closing the app on its own.
        try:
            if getattr(e, "type", None) == ft.WindowEventType.CLOSE:
                self._run_cleanup_once()
                w = getattr(self.page, "window", None)
                if w is not None:
                    await w.destroy()
        except Exception as ex:
            self.log_message(f"Window event error: {ex}\n")

    def _win_close_sync(self, e=None):
        # Synchronous wrapper to properly invoke the async close coroutine.
        # run_task schedules the coroutine on the event loop instead of
        # trying to await it from a non-async context.
        self.page.run_task(self._win_close)

    async def _win_close(self, e=None):
        # Window.close()/destroy() are coroutines in current Flet — calling
        # one without awaiting it just creates a coroutine object that's
        # immediately discarded, which is why the close button used to do
        # nothing at all.
        self._run_cleanup_once()
        w = getattr(self.page, "window", None)
        try:
            if w is not None:
                await w.close()
            else:
                self.page.window_close()
        except Exception as ex:
            self.log_message(f"Window close error: {ex}\n")

    # ------------------------------------------------------------------
    def load_config(self):
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_config(self):
        config = {"last_port": self.current_port}
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)

    def get_available_ports(self):
        ports = [port.device for port in list_ports.comports()]
        return ports if ports else ["COM4"]

    # ------------------------------------------------------------------
    # small reusable UI atoms — no Material ripple (ink) anywhere, just
    # smooth hover/selection colour transitions for a flatter, calmer feel
    # ------------------------------------------------------------------
    def _hover_bg(self, container, base, hover, hover_border=None, base_border=None,
                  skip_if_selected=False):
        def handler(e):
            if skip_if_selected and container.data:
                return
            # Handle both string "true"/"false" and boolean True/False across Flet versions
            hovering = str(e.data).lower() == "true" if e.data is not None else False
            container.bgcolor = hover if hovering else base
            if hover_border is not None and base_border is not None:
                # A thicker, accent-tinted border reads as a soft "glow ring"
                # and is a plain, universally-supported Container property —
                # unlike a BoxShadow, it can't silently fail to reach the
                # client and take the whole hover update down with it.
                container.border = ft.Border.all(2 if hovering else 1, hover_border if hovering else base_border)
            container.update()
        return handler

    def _with_bounce(self, container, handler):
        """Wrap a click handler with a quick, physical-feeling scale bounce
        so a click/tap always reads as a distinct, momentary event — clearly
        different from the steady hover highlight, and from a persistent
        'selected' pill state, which is untouched by this."""
        def wrapped(e):
            if handler:
                handler(e)
            self.page.run_task(self._press_bounce, container)
        return wrapped

    async def _press_bounce(self, container):
        try:
            container.scale = 0.96
            container.update()
            await asyncio.sleep(0.09)
            container.scale = 1.0
            container.update()
        except Exception:
            pass

    def _hover_style(self, accent_color=None, strength=1.0):
        """Standard hover border tuple, tinted with the given accent colour
        (or the app's default accent blue) so every control's hover state
        matches the same theme instead of a generic grey highlight."""
        color = accent_color or self.ACCENT_BLUE
        return {
            "hover_border": ft.Colors.with_opacity(min(0.9, 0.7 * strength), color),
            "base_border": self.CARD_BORDER,
        }

    def _remote_button(self, label, icon, payload, accent=None, on_click=None):
        color = {
            "danger": self.RED_ALERT,
            "accent": self.ACCENT_BLUE,
            "warning": self.ORANGE_WARN,
        }.get(accent, self.TEXT_PRIMARY)
        label_color = color if accent else self.TEXT_MUTED
        handler = on_click if on_click else (lambda e, p=payload: self.send_remocon(p))
        # Accent-coloured buttons (power/bluetooth/mute/sound) glow in their
        # own colour on hover; plain buttons glow in the app's accent blue.
        hover_accent = color if accent else self.ACCENT_BLUE

        c = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(icon, size=32, color=color),
                    ft.Text(label.upper(), size=13, color=label_color, weight=ft.FontWeight.W_600),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
            ),
            expand=True,
            bgcolor=self.INPUT_BG,
            border=ft.Border.all(1, self.CARD_BORDER),
            border_radius=14,
            alignment=ALIGN_CENTER,
            animate=180,
        )
        _safe(c, scale=1, animate_scale=100)
        c.on_click = self._with_bounce(c, handler)
        c.on_hover = self._hover_bg(
            c, self.INPUT_BG, self.INPUT_BG_HOVER,
            **self._hover_style(hover_accent),
        )
        return c

    def _pill(self, text_value, selected, expand=False, width=None):
        text = ft.Text(text_value, size=15, weight=ft.FontWeight.W_600,
                        color=self.TEXT_PRIMARY if selected else self.TEXT_MUTED)
        c = ft.Container(
            content=text,
            padding=18,
            bgcolor=self.ACCENT_BLUE if selected else self.INPUT_BG,
            border=ft.Border.all(1, self.ACCENT_BLUE if selected else self.CARD_BORDER),
            border_radius=10,
            alignment=ALIGN_CENTER,
            animate=150,
            data=selected,
        )
        if width:
            c.width = width
        if expand:
            c.expand = True
        _safe(c, scale=1, animate_scale=100)
        # skip_if_selected keeps the solid accent-blue "selected" look fully
        # intact on hover, so selected vs. hovered vs. idle stay visually
        # distinct at a glance.
        c.on_hover = self._hover_bg(
            c, self.INPUT_BG, self.INPUT_BG_HOVER,
            skip_if_selected=True,
            **self._hover_style(strength=0.85),
        )
        return c, text

    def _flat_button(self, label_text, accent=False, on_click=None, expand=False):
        text = ft.Text(label_text, size=13, weight=ft.FontWeight.W_600, color=self.TEXT_PRIMARY)
        base = self.ACCENT_BLUE if accent else self.INPUT_BG
        c = ft.Container(
            content=text,
            padding=ft.Padding(20, 10, 20, 10) if hasattr(ft, "Padding") else 14,
            bgcolor=base,
            border=ft.Border.all(1, self.CARD_BORDER if not accent else self.ACCENT_BLUE),
            border_radius=10,
            alignment=ALIGN_CENTER,
            on_click=on_click,
            animate=150,
        )
        if expand:
            c.expand = True
        hover_color = "#0970DE" if accent else self.INPUT_BG_HOVER
        c.on_hover = self._hover_bg(c, base, hover_color)
        return c, text

    def section_label(self, text: str):
        return ft.Text(text.upper(), size=11, weight=ft.FontWeight.W_600, color=self.TEXT_MUTED)

    def tab_content(self, controls):
        return ft.Container(
            content=ft.Column(
                controls,
                spacing=18,
                expand=True,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            ),
            padding=22,
            bgcolor=self.BG_DARK,
            expand=True,
        )

    # ------------------------------------------------------------------
    # main layout
    # ------------------------------------------------------------------
    def build_ui(self):
        self.page.controls.clear()

        title_bar = self._build_title_bar()
        control_bar = self._build_control_bar()

        # As of Flet 0.86, Tab no longer carries `text`/`content` and Tabs no
        # longer takes `tabs=` directly. The headers (TabBar) and the pages
        # (TabBarView) are now separate controls that Tabs.content wraps.
        tab_bar = ft.TabBar(
            tabs=[
                ft.Tab(label="Remote"),
                ft.Tab(label="Preset EQ"),
                ft.Tab(label="Manual EQ"),
                ft.Tab(label="D.Bass"),
            ],
        )
        _safe(
            tab_bar,
            indicator_color=self.ACCENT_BLUE,
            label_color=self.TEXT_PRIMARY,
            unselected_label_color=self.TEXT_MUTED,
            divider_color=self.CARD_BORDER,
        )

        tab_bar_view = ft.TabBarView(
            expand=True,
            controls=[
                self.tab_content([self.build_remote_view()]),
                self.tab_content([self.build_preset_view()]),
                self.tab_content([self.build_manual_eq_view()]),
                self.tab_content([self.build_dbass_view()]),
            ],
        )

        tabs = ft.Tabs(
            selected_index=0,
            length=4,
            animation_duration=ft.Duration(milliseconds=200),
            expand=True,
            content=ft.Column(expand=True, spacing=0, controls=[tab_bar, tab_bar_view]),
        )

        left_content = ft.Container(
            content=ft.Column(
                [control_bar, ft.Container(content=tabs, expand=True, bgcolor=self.CARD_GLASS,
                                            border=ft.Border.all(1, self.CARD_BORDER), border_radius=16)],
                spacing=14,
                expand=True,
            ),
            expand=True,
            padding=ft.Padding(20, 16, 8, 16) if hasattr(ft, "Padding") else 16,
            bgcolor=self.BG_DARK,
        )

        self.debug_panel = self._build_debug_panel()
        self.debug_panel.visible = self.debug_visible

        body = ft.Row(
            [left_content, self.debug_panel],
            expand=True,
            spacing=0,
        )

        self.page.add(
            ft.Column([title_bar, body], expand=True, spacing=0)
        )
        self.page.update()

    def _build_control_bar(self):
        self.port_combo = ft.Dropdown(
            width=140,
            options=[ft.DropdownOption(key=p, text=p) for p in self.get_available_ports()],
            value=self.current_port,
            bgcolor=self.INPUT_BG,
            border_color=self.CARD_BORDER,
            text_style=ft.TextStyle(size=12, color=self.TEXT_PRIMARY),
            on_select=self.on_port_select,
        )
        self.status_badge = ft.Text("OFFLINE", color=self.TEXT_MUTED, size=12, weight=ft.FontWeight.W_600)
        self.status_dot = ft.Container(width=7, height=7, border_radius=4, bgcolor=self.TEXT_MUTED)

        self.connect_btn, self.connect_btn_text = self._flat_button("Connect", accent=True, on_click=self.toggle_connection)

        refresh_btn = ft.Container(
            content=ft.Icon(ft.Icons.REFRESH, size=16, color=self.TEXT_MUTED),
            width=40,
            height=40,
            bgcolor=self.INPUT_BG,
            border=ft.Border.all(1, self.CARD_BORDER),
            border_radius=10,
            alignment=ALIGN_CENTER,
            on_click=self.refresh_ports,
            animate=150,
        )
        refresh_btn.on_hover = self._hover_bg(refresh_btn, self.INPUT_BG, self.INPUT_BG_HOVER)

        return ft.Container(
            content=ft.Row(
                [
                    ft.Text("PORT", color=self.TEXT_MUTED, weight=ft.FontWeight.W_600, size=11),
                    self.port_combo,
                    refresh_btn,
                    self.connect_btn,
                    ft.Row([self.status_dot, self.status_badge], spacing=8,
                           vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ],
                spacing=12,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                wrap=False,
            ),
            padding=16,
            bgcolor=self.CARD_GLASS,
            border=ft.Border.all(1, self.CARD_BORDER),
            border_radius=16,
        )

    # ------------------------------------------------------------------
    # custom frameless title bar
    # ------------------------------------------------------------------
    def _window_button(self, icon, on_click, danger=False):
        icon_ctrl = ft.Icon(icon, size=13, color=self.TEXT_MUTED)
        c = ft.Container(
            content=icon_ctrl,
            width=46,
            height=44,
            alignment=ALIGN_CENTER,
            bgcolor=self.CARD_GLASS,
            on_click=on_click,
            animate=120,
            border_radius=4,
        )
        _safe(c, scale=1, animate_scale=80)

        def hover(e):
            # Handle both string "true"/"false" and boolean True/False across Flet versions
            is_hovering = str(e.data).lower() == "true" if e.data is not None else False
            if is_hovering:
                c.bgcolor = self.RED_ALERT if danger else "#1C1C1E"
                icon_ctrl.color = "#FFFFFF" if danger else self.ACCENT_BLUE
                c.scale = 1.1
            else:
                c.bgcolor = self.CARD_GLASS
                icon_ctrl.color = self.TEXT_MUTED
                c.scale = 1.0
            c.update()

        c.on_hover = hover
        return c

    def _build_title_bar(self):
        brand = ft.Row(
            [
                ft.Image(
                    src="D:\\Workspace\\Projects\\SC-AKX200\\Guillendesign-Variations-3-Music.ico",
                    width=20,
                    height=20,
                ),
                ft.Text("SC-AKX200", size=13, weight=ft.FontWeight.W_600, color=self.TEXT_PRIMARY),
                ft.Text("Control Panel", size=12, color=self.TEXT_MUTED),
            ],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        drag_area_cls = getattr(ft, "WindowDragArea", None)
        left = ft.Container(
            content=(drag_area_cls(content=brand, expand=True) if drag_area_cls else brand),
            expand=True,
            padding=ft.Padding(16, 0, 0, 0) if hasattr(ft, "Padding") else 16,
            alignment=ALIGN_CENTER_LEFT,
            bgcolor=self.CARD_GLASS,
            on_click=self._on_title_bar_click,
        )

        window_controls = ft.Row(
            [
                self._window_button(ft.Icons.REMOVE, self._win_minimize),
                self._window_button(ft.Icons.CROP_SQUARE, self._win_toggle_maximize),
                self._window_button(ft.Icons.CLOSE, self._win_close_sync, danger=True),
            ],
            spacing=0,
        )

        return ft.Container(
            content=ft.Row(
                [left, window_controls],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            height=44,
            bgcolor=self.CARD_GLASS,
            border=ft.Border(bottom=ft.BorderSide(1, self.CARD_BORDER)) if hasattr(ft, "BorderSide") else ft.Border.all(1, self.CARD_BORDER),
        )

    # ------------------------------------------------------------------
    # debug panel (hidden by default — Ctrl+Shift+I toggles it)
    # ------------------------------------------------------------------
    def _build_debug_panel(self):
        self.log_text = ft.Text(
            color=self.TEXT_MUTED,
            size=12,
            font_family="monospace",
            selectable=True,
        )

        close_btn = ft.Container(
            content=ft.Icon(ft.Icons.CLOSE, size=14, color=self.TEXT_MUTED),
            width=28, height=28, border_radius=8, alignment=ALIGN_CENTER,
            on_click=lambda e: self.set_debug_visible(False),
            bgcolor=self.INPUT_BG,
            border=ft.Border.all(1, self.CARD_BORDER),
            animate=120,
        )
        close_btn.on_hover = self._hover_bg(close_btn, self.INPUT_BG, self.INPUT_BG_HOVER)

        shortcut_chip = ft.Container(
            content=ft.Text("CTRL+SHIFT+I", size=10, weight=ft.FontWeight.W_600, color=self.TEXT_MUTED),
            padding=ft.Padding(8, 5, 8, 5) if hasattr(ft, "Padding") else 6,
            bgcolor=self.INPUT_BG,
            border=ft.Border.all(1, self.CARD_BORDER),
            border_radius=6,
        )

        header = ft.Row(
            [
                ft.Row(
                    [
                        ft.Container(width=7, height=7, border_radius=4, bgcolor=self.GREEN_OK),
                        ft.Text("DEBUG LOG", size=12, weight=ft.FontWeight.W_700, color=self.TEXT_PRIMARY),
                    ],
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Row(
                    [shortcut_chip, close_btn],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # ListView (rather than a scrolling Column) so `auto_scroll` keeps
        # the newest lines pinned in view as they stream in, like a real
        # terminal, instead of the user having to scroll down manually.
        log_list = ft.ListView(
            controls=[self.log_text],
            expand=True,
            auto_scroll=True,
            spacing=0,
            padding=0,
        )

        log_scroll = ft.Container(
            content=log_list,
            expand=True,
            bgcolor="#0A0A0C",
            border=ft.Border.all(1, self.CARD_BORDER),
            border_radius=12,
            padding=14,
        )

        # manual frame tester — handy for confirming / discovering remocon
        # codes by hand against the real hardware instead of guessing in code
        self.test_ch = ft.TextField(
            label="CH", value="0", expand=True, height=48,
            bgcolor=self.INPUT_BG, color=self.TEXT_PRIMARY,
            border_color=self.CARD_BORDER, text_size=13,
        )
        _safe(
            self.test_ch,
            border_radius=10,
            focused_border_color=self.ACCENT_BLUE,
            content_padding=ft.Padding(12, 4, 12, 4) if hasattr(ft, "Padding") else 12,
            label_style=ft.TextStyle(size=10.5, color=self.TEXT_MUTED, weight=ft.FontWeight.W_600),
        )
        self.test_code = ft.TextField(
            label="CODE", value="0", expand=True, height=48,
            bgcolor=self.INPUT_BG, color=self.TEXT_PRIMARY,
            border_color=self.CARD_BORDER, text_size=13,
        )
        _safe(
            self.test_code,
            border_radius=10,
            focused_border_color=self.ACCENT_BLUE,
            content_padding=ft.Padding(12, 4, 12, 4) if hasattr(ft, "Padding") else 12,
            label_style=ft.TextStyle(size=10.5, color=self.TEXT_MUTED, weight=ft.FontWeight.W_600),
        )
        test_send, _ = self._flat_button("Send", accent=True, on_click=self.send_test_frame)
        test_send.height = 48
        test_send.width = 88

        tester = ft.Container(
            content=ft.Column(
                [
                    ft.Text("FRAME TESTER", size=10.5, weight=ft.FontWeight.W_700, color=self.TEXT_MUTED),
                    ft.Row(
                        [self.test_ch, self.test_code, test_send],
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.END,
                    ),
                ],
                spacing=10,
            ),
            padding=14,
            bgcolor=self.CARD_GLASS,
            border=ft.Border.all(1, self.CARD_BORDER),
            border_radius=12,
        )

        clear_btn, _ = self._flat_button("Clear Log", accent=False, on_click=self.clear_log, expand=True)

        return ft.Container(
            content=ft.Column([header, log_scroll, tester, clear_btn], spacing=14, expand=True),
            padding=18,
            bgcolor=self.CARD_GLASS,
            border=ft.Border(left=ft.BorderSide(1, self.CARD_BORDER)) if hasattr(ft, "BorderSide") else ft.Border.all(1, self.CARD_BORDER),
            width=380,
        )

    def send_test_frame(self, e=None):
        try:
            ch = int(self.test_ch.value)
            code = int(self.test_code.value)
        except (TypeError, ValueError):
            self.log_message("Invalid test values - use plain integers\n")
            return
        self.log_message(f"TEST  manual payload=[{ch}, {code}]\n")
        self.send_remocon([ch, code])

    def set_debug_visible(self, value: bool):
        self.debug_visible = value
        self.debug_panel.visible = value
        self.page.update()

    def on_keyboard(self, e):
        if (getattr(e, "key", "") or "").upper() == "I" and getattr(e, "ctrl", False) and getattr(e, "shift", False):
            self.set_debug_visible(not self.debug_visible)

    # ------------------------------------------------------------------
    # sections
    # ------------------------------------------------------------------
    def build_remote_view(self):
        remote_defs = [
            ("Power", ft.Icons.POWER_SETTINGS_NEW, [28, 61], "danger", None),
            ("Dimmer", ft.Icons.BRIGHTNESS_6, [28, -105], None, None),
            ("Eject", ft.Icons.EJECT, [28, 1], None, None),
            ("Bluetooth", ft.Icons.BLUETOOTH, [0, -91], "accent", None),
            ("USB / CD", ft.Icons.ALBUM, [0, -124], None, None),
            ("Aux", ft.Icons.HEADPHONES, [4, -92], None, None),
            ("Rewind", ft.Icons.FAST_REWIND, [28, 73], None, None),
            ("Play", ft.Icons.PLAY_ARROW, [28, 6], None, None),
            ("Forward", ft.Icons.FAST_FORWARD, [28, 74], None, None),
            ("Stop", ft.Icons.STOP, [28, 0], None, None),
            ("Vol −", ft.Icons.VOLUME_DOWN, [0, 33], None, None),
            ("Vol +", ft.Icons.VOLUME_UP, [0, 32], None, None),
            ("Setup", ft.Icons.TUNE, [28, -75], None, None),
            ("Mute", ft.Icons.VOLUME_OFF, [0, 50], "warning", None),
            ("Display", ft.Icons.DESKTOP_WINDOWS, [28, 85], None, None),
            ("Sound", ft.Icons.GRAPHIC_EQ, [20, -80], "accent", None),
            ("Menu", ft.Icons.MENU, [28, -69], None, self.send_play_menu),
            ("Left", ft.Icons.CHEVRON_LEFT, [28, -3], None, None),
            ("OK", ft.Icons.CHECK, [28, -5], None, None),
            ("Right", ft.Icons.CHEVRON_RIGHT, [28, -4], None, None),
        ]

        buttons = [
            self._remote_button(label, icon, payload, accent, on_click)
            for label, icon, payload, accent, on_click in remote_defs
        ]

        # Laid out as fixed rows (10 per row, matching the two visual rows
        # in the reference UI) rather than a wrapping Row, so every button
        # can carry expand=True and stretch to fill the available cell
        # instead of sitting at a fixed 112x84 size.
        row_size = 10
        rows = [
            ft.Row(
                buttons[i:i + row_size],
                spacing=10,
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.STRETCH,
            )
            for i in range(0, len(buttons), row_size)
        ]
        return ft.Column(
            rows,
            spacing=10,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

    def build_preset_view(self):
        presets = [
            ("ROCK", [1, 29]), ("POP", [1, 30]), ("ELECTRONICA", [1, 31]), ("REGGAETON", [1, 32]),
            ("CUMBIA", [1, 33]), ("SALSA", [1, 34]), ("FORRO", [1, 35]), ("FUNK", [1, 36]),
            ("SAMBA", [1, 37]), ("SERTANEJO", [1, 38]), ("AXE", [1, 39]), ("MPB", [1, 40]),
            ("FOOTBALL", [1, 41]), ("FLAT", [1, 52]),
        ]
        row_size = 7
        rows = []
        for start in range(0, len(presets), row_size):
            row_controls = []
            for name, payload in presets[start:start + row_size]:
                c, t = self._pill(name, False, expand=True)
                c.on_click = self._with_bounce(
                    c, lambda e, p=payload, n=name: self.send_preset_eq(p, n)
                )
                self.preset_buttons[name] = (c, t)
                row_controls.append(c)
            rows.append(
                ft.Row(
                    row_controls,
                    spacing=10,
                    expand=True,
                    vertical_alignment=ft.CrossAxisAlignment.STRETCH,
                )
            )
        return ft.Column(
            rows,
            spacing=10,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

    def build_manual_eq_view(self):
        self.manual_eq_levels = {"bass": 0, "mid": 0, "treble": 0}
        self.manual_eq_payloads = {
            "bass": [[1, 8], [1, 7], [1, 6], [1, 5], [1, 4], [1, 3], [1, 2], [1, 1], [1, 0]],
            "mid": [[1, 17], [1, 16], [1, 15], [1, 14], [1, 13], [1, 12], [1, 11], [1, 10], [1, 9]],
            "treble": [[1, 26], [1, 25], [1, 24], [1, 23], [1, 22], [1, 21], [1, 20], [1, 19], [1, 18]],
        }

        rows = []
        self.manual_eq_sliders = {}
        self.manual_eq_labels = {}

        for key, title in [("bass", "Bass"), ("mid", "Mid"), ("treble", "Treble")]:
            slider = ft.Slider(
                min=0, max=8, value=4, divisions=8,
                expand=True,
                on_change=lambda e, channel=key: self.on_manual_eq_slider_change(channel, e.control.value),
                active_color=self.ACCENT_BLUE,
                inactive_color=self.CARD_BORDER,
            )
            self.manual_eq_sliders[key] = slider
            value_label = ft.Text("0", size=12, color=self.TEXT_MUTED, font_family="monospace", width=28)
            self.manual_eq_labels[key] = value_label
            row_card = ft.Container(
                content=ft.Row(
                    [
                        ft.Text(title, weight=ft.FontWeight.W_500, color=self.TEXT_PRIMARY, width=70, size=13),
                        slider,
                        value_label,
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.Padding(16, 12, 16, 12) if hasattr(ft, "Padding") else 12,
                bgcolor=self.INPUT_BG,
                border=ft.Border.all(1, self.CARD_BORDER),
                border_radius=12,
                animate=150,
            )
            row_card.on_hover = self._hover_bg(
                row_card, self.INPUT_BG, self.INPUT_BG_HOVER,
                **self._hover_style(strength=0.7),
            )
            rows.append(row_card)

        self.surround_switch = ft.Switch(value=False, on_change=self.on_manual_eq_surround_toggle,
                                          active_color=self.ACCENT_BLUE)
        surround = ft.Container(
            content=ft.Row(
                [
                    ft.Text("Surround", weight=ft.FontWeight.W_500, size=13, color=self.TEXT_PRIMARY),
                    self.surround_switch,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=ft.Padding(16, 12, 16, 12) if hasattr(ft, "Padding") else 12,
            bgcolor=self.INPUT_BG,
            border=ft.Border.all(1, self.CARD_BORDER),
            border_radius=12,
            animate=150,
        )
        surround.on_hover = self._hover_bg(
            surround, self.INPUT_BG, self.INPUT_BG_HOVER,
            **self._hover_style(strength=0.7),
        )

        return ft.Column(
            rows + [surround],
            spacing=14,
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

    def build_dbass_view(self):
        off_c, off_t = self._pill("Off", True, expand=True)
        off_c.on_click = self._with_bounce(off_c, lambda e: self.on_dbass_select([1, 54], "off"))
        self.dbass_buttons["off"] = (off_c, off_t)

        level_controls = [off_c]
        for idx in range(1, 7):
            payload = [1, 54 + idx]
            c, t = self._pill(str(idx), False, expand=True)
            c.on_click = self._with_bounce(c, lambda e, p=payload, k=str(idx): self.on_dbass_select(p, k))
            self.dbass_buttons[str(idx)] = (c, t)
            level_controls.append(c)

        beat_on_c, beat_on_t = self._pill("Beat On", False, expand=True)
        beat_on_c.on_click = self._with_bounce(beat_on_c, lambda e: self.on_dbass_beat_select([1, 66], "on"))
        self.beat_buttons["on"] = (beat_on_c, beat_on_t)

        beat_off_c, beat_off_t = self._pill("Beat Off", True, expand=True)
        beat_off_c.on_click = self._with_bounce(beat_off_c, lambda e: self.on_dbass_beat_select([1, 67], "off"))
        self.beat_buttons["off"] = (beat_off_c, beat_off_t)

        return ft.Column(
            [
                ft.Row(
                    level_controls,
                    spacing=10,
                    expand=True,
                    vertical_alignment=ft.CrossAxisAlignment.STRETCH,
                ),
                ft.Divider(color=self.CARD_BORDER, height=1),
                ft.Row(
                    [beat_on_c, beat_off_c],
                    spacing=10,
                    expand=True,
                    vertical_alignment=ft.CrossAxisAlignment.STRETCH,
                ),
            ],
            spacing=16,
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
        )

    # ------------------------------------------------------------------
    # handlers
    # ------------------------------------------------------------------
    def _select_pill(self, group: dict, key: str):
        for k, (c, t) in group.items():
            selected = (k == key)
            c.bgcolor = self.ACCENT_BLUE if selected else self.INPUT_BG
            c.border = ft.Border.all(1, self.ACCENT_BLUE if selected else self.CARD_BORDER)
            t.color = self.TEXT_PRIMARY if selected else self.TEXT_MUTED
            c.data = selected
            c.update()

    def on_manual_eq_slider_change(self, channel: str, value):
        value_int = int(round(float(value)))
        self.manual_eq_levels[channel] = value_int
        payload = self.manual_eq_payloads[channel][value_int]
        self.manual_eq_labels[channel].value = f"{value_int - 4:+d}" if value_int != 4 else "0"
        self.page.update()
        self.send_remocon(payload)

    def on_manual_eq_surround_toggle(self, e):
        payload = [1, 27] if e.control.value is False else [1, 28]
        self.send_remocon(payload)

    def on_dbass_select(self, payload, key):
        self.selected_dbass = key
        self._select_pill(self.dbass_buttons, key)
        self.send_remocon(payload)

    def on_dbass_beat_select(self, payload, key):
        self.selected_beat = key
        self._select_pill(self.beat_buttons, key)
        self.send_remocon(payload)

    def log_message(self, msg: str):
        self.log_lines.append(msg)
        if len(self.log_lines) > 200:
            self.log_lines = self.log_lines[-200:]
        self.log_text.value = "".join(self.log_lines)
        self.page.update()

    def clear_log(self, e=None):
        self.log_lines.clear()
        self.log_text.value = ""
        self.page.update()

    def on_port_select(self, e):
        self.current_port = self.port_combo.value

    def refresh_ports(self, e=None):
        self.port_combo.options = [ft.DropdownOption(key=p, text=p) for p in self.get_available_ports()]
        if self.current_port not in [o.key for o in self.port_combo.options]:
            self.current_port = self.get_available_ports()[0]
            self.port_combo.value = self.current_port
        self.page.update()

    def toggle_connection(self, e=None):
        port = (self.port_combo.value or "").strip().upper()
        if not port:
            self.log_message("No port selected\n")
            return
        if not self.worker.connected:
            self.worker.connected = False
            self.cmd_queue.put({"action": "connect", "port": port, "callback": self.on_connection_result})
            self.page.update()
        else:
            self.cmd_queue.put({"action": "disconnect", "callback": self.on_connection_result})

    def on_connection_result(self, success: bool, message: str):
        self.page.run_task(self._on_connection_result_ui, success, message)

    async def _on_connection_result_ui(self, success: bool, message: str):
        self.status_badge.value = "ONLINE" if success else "OFFLINE"
        self.status_badge.color = self.GREEN_OK if success else self.TEXT_MUTED
        self.status_dot.bgcolor = self.GREEN_OK if success else self.TEXT_MUTED
        self.connect_btn_text.value = "Disconnect" if success else "Connect"
        self.page.update()
        if success:
            self.save_config()

    def send_remocon(self, payload: list):
        if self.worker.connected:
            self.cmd_queue.put({"action": "send_remocon", "payload": payload})
        else:
            self.log_message("Not connected to device\n")

    def send_play_menu(self, e=None):
        payload = [28, -69]
        self.log_message(f"PLAY MENU  payload={payload}\n")
        self.send_remocon(payload)

    def send_preset_eq(self, payload: list, name: str):
        self.log_message(f"PRESET EQ  {name}  payload={payload}\n")
        self.send_remocon(payload)
        self.selected_preset = name
        self._select_pill(self.preset_buttons, name)

    def on_closing(self):
        self.save_config()
        self.worker.stop()
        if self.worker.connected and self.worker.ser and self.worker.ser.is_open:
            self.worker.ser.close()


def main(page: ft.Page):
    app = PanasonicSCAKX200App(page)
    page.on_close = lambda e=None: app._run_cleanup_once()


if __name__ == "__main__":
    ft.run(main)