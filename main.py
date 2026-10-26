# -*- coding: utf-8 -*-
"""
Website Shot Royal v5.2 Masterpiece — Precision-Crafted Single-Screen UI
Fixed DP Heights | Dark Preview Placeholder | Centered Inputs | Desktop Viewport
"""
import os
import re
import threading
from datetime import datetime
from urllib.parse import urlparse

import requests
from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.core.clipboard import Clipboard
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.image import Image

try:
    import arabic_reshaper
    ARABIC_SUPPORT = True
except Exception:
    ARABIC_SUPPORT = False

try:
    from bidi.algorithm import get_display
    BIDI_SUPPORT = True
except Exception:
    BIDI_SUPPORT = False

# ==================== لوحة الألوان الملكية المتناسقة ====================
BG          = (0.027, 0.035, 0.059, 1)  # كحلي ليلي عميق
CARD_BG     = (0.063, 0.078, 0.122, 1)  # خلفية البطاقات
CARD_INNER  = (0.094, 0.114, 0.173, 1)  # خلفية الحقول والأزرار
PREVIEW_BG  = (0.043, 0.055, 0.090, 1)  # خلفية شاشة المعاينة الداكنة
GOLD        = (0.920, 0.740, 0.370, 1)  # ذهبي ملكي
GOLD_DARK   = (0.680, 0.500, 0.200, 1)  # ذهبي عند الضغط
GOLD_SOFT   = (0.920, 0.740, 0.370, 0.28)
BORDER_SUB  = (0.155, 0.190, 0.270, 1)
WHITE       = (0.965, 0.975, 0.995, 1)
MUTED       = (0.560, 0.620, 0.720, 1)
GREEN       = (0.220, 0.840, 0.580, 1)
RED         = (0.960, 0.360, 0.380, 1)


def find_arabic_font():
    candidates = [
        "/system/fonts/NotoSansArabic-Regular.ttf",
        "/system/fonts/NotoNaskhArabic-Regular.ttf",
        "/system/fonts/NotoSansArabicUI-Regular.ttf",
        "/system/fonts/NotoNaskhArabicUI-Regular.ttf",
        "/system/fonts/DroidSansArabic.ttf",
        "/system/fonts/DroidSans.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return path
    return None


FONT = find_arabic_font()
if FONT:
    try:
        LabelBase.register(name="ArabicUI", fn_regular=FONT)
    except Exception:
        FONT = None


def font_name():
    return "ArabicUI" if FONT else "Roboto"


def rtl_fallback(text):
    tokens = re.findall(r'[\u0600-\u06FF\uFE70-\uFEFF]+|[^\u0600-\u06FF\uFE70-\uFEFF]+', text)
    out = []
    for tok in tokens:
        if re.search(r'[\u0600-\u06FF\uFE70-\uFEFF]', tok):
            out.append(tok[::-1])
        else:
            out.append(tok)
    return "".join(reversed(out))


def ar(text):
    text = str(text)
    if ARABIC_SUPPORT:
        try:
            reshaped = arabic_reshaper.reshape(text)
            text = get_display(reshaped) if BIDI_SUPPORT else rtl_fallback(reshaped)
        except Exception:
            pass
    if FONT:
        text = re.sub(
            r'([^\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF\s\[\]]+)',
            r'[font=Roboto]\1[/font]',
            text
        )
    return text


class LuxuryCard(BoxLayout):
    def __init__(self, bg=CARD_BG, border_color=BORDER_SUB, radius=14, border_width=1.0, **kwargs):
        super().__init__(**kwargs)
        self._radius = dp(radius)
        with self.canvas.before:
            self.bg_col = Color(*bg)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[self._radius])
            self.border_col = Color(*border_color)
            self.border_line = Line(
                rounded_rectangle=(self.x, self.y, self.width, self.height, self._radius),
                width=dp(border_width)
            )
        self.bind(pos=self._update, size=self._update)

    def _update(self, *_):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.border_line.rounded_rectangle = (self.x, self.y, self.width, self.height, self._radius)

    def set_border(self, rgba):
        self.border_col.rgba = rgba


class RoyalButton(Button):
    def __init__(self, gold=False, radius=10, font_sz="12.5sp", **kwargs):
        self.gold = gold
        self._radius = dp(radius)
        kwargs.setdefault("background_normal", "")
        kwargs.setdefault("background_down", "")
        kwargs.setdefault("background_color", (0, 0, 0, 0))
        kwargs.setdefault("color", BG if gold else WHITE)
        kwargs.setdefault("font_name", font_name())
        kwargs.setdefault("font_size", font_sz)
        kwargs.setdefault("markup", True)
        kwargs.setdefault("bold", gold)
        super().__init__(**kwargs)
        with self.canvas.before:
            self.col = Color(*(GOLD if self.gold else CARD_INNER))
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[self._radius])
            self.b_col = Color(*(GOLD if self.gold else BORDER_SUB))
            self.b_line = Line(
                rounded_rectangle=(self.x, self.y, self.width, self.height, self._radius),
                width=dp(1.0)
            )
        self.bind(pos=self._update, size=self._update, state=self._update_state)

    def _update(self, *_):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.b_line.rounded_rectangle = (self.x, self.y, self.width, self.height, self._radius)

    def _update_state(self, *_):
        if self.state == "down":
            self.col.rgba = GOLD_DARK if self.gold else (0.15, 0.18, 0.26, 1)
        else:
            self.col.rgba = GOLD if self.gold else CARD_INNER
        self.b_col.rgba = GOLD if self.gold else BORDER_SUB
        self.color = BG if self.gold else WHITE

    def set_active(self, active):
        self.gold = active
        self.bold = active
        self._update_state()


class RoyalSpinnerOption(SpinnerOption):
    def __init__(self, **kwargs):
        kwargs.setdefault("background_normal", "")
        kwargs.setdefault("background_color", (0.07, 0.09, 0.14, 1))
        kwargs.setdefault("color", WHITE)
        kwargs.setdefault("font_name", font_name())
        kwargs.setdefault("font_size", "12sp")
        kwargs.setdefault("markup", True)
        kwargs.setdefault("height", dp(38))
        super().__init__(**kwargs)


class RoyalSpinner(Spinner):
    def __init__(self, **kwargs):
        self._radius = dp(10)
        kwargs.setdefault("background_normal", "")
        kwargs.setdefault("background_down", "")
        kwargs.setdefault("background_color", (0, 0, 0, 0))
        kwargs.setdefault("color", WHITE)
        kwargs.setdefault("font_name", font_name())
        kwargs.setdefault("font_size", "12sp")
        kwargs.setdefault("markup", True)
        kwargs.setdefault("option_cls", RoyalSpinnerOption)
        super().__init__(**kwargs)
        with self.canvas.before:
            self.col = Color(*CARD_INNER)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[self._radius])
            self.b_col = Color(*BORDER_SUB)
            self.b_line = Line(
                rounded_rectangle=(self.x, self.y, self.width, self.height, self._radius),
                width=dp(1.0)
            )
        self.bind(pos=self._update, size=self._update)

    def _update(self, *_):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.b_line.rounded_rectangle = (self.x, self.y, self.width, self.height, self._radius)


class CenteredInput(TextInput):
    """حقل نصي يتوسط النص عمودياً بشكل تلقائي ودقيق"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self._align_vertical, text=self._align_vertical)

    def _align_vertical(self, *_):
        pad_y = max(dp(4), (self.height - self.line_height) / 2.0)
        self.padding = [dp(10), pad_y, dp(10), pad_y]


class WebsiteShotRoyal(App):
    title = "Website Shot Royal Studio v5.2"

    def build(self):
        Window.clearcolor = BG
        self.busy = False
        self.selected_w = 1366
        self.selected_h = 768
        self.mode = "visible"

        self.output_dir = "/storage/emulated/0/Pictures/WebsiteShots"
        try:
            os.makedirs(self.output_dir, exist_ok=True)
        except Exception:
            self.output_dir = os.path.join(os.path.expanduser("~"), "Pictures", "WebsiteShots")
            os.makedirs(self.output_dir, exist_ok=True)

        # الحاوية الرئيسية (أبعاد ثابتة للبطاقات العلوية والسفلية، ومساحة مرنة للمعاينة)
        root = BoxLayout(orientation="vertical", padding=[dp(12), dp(10), dp(12), dp(10)], spacing=dp(8))

        # ==================== 1. الهيدر العلوي (ارتفاع ثابت 56dp) ====================
        header = LuxuryCard(
            size_hint_y=None, height=dp(56), padding=[dp(12), dp(8)], spacing=dp(10),
            bg=(0.05, 0.065, 0.10, 1), border_color=GOLD_SOFT, radius=14
        )
        self.dim_badge = LuxuryCard(
            size_hint=(None, None), size=(dp(92), dp(32)), pos_hint={"center_y": 0.5},
            bg=(0.08, 0.16, 0.13, 1), border_color=(0.22, 0.84, 0.58, 0.45), radius=9
        )
        self.dim_badge_lbl = Label(
            text="[b]1366 x 768[/b]", markup=True, font_name="Roboto", font_size="11sp", color=GREEN
        )
        self.dim_badge.add_widget(self.dim_badge_lbl)
        header.add_widget(self.dim_badge)

        brand_box = BoxLayout(orientation="vertical", spacing=dp(1))
        brand_box.add_widget(self.rtl_label("استوديو تصوير المواقع الملكي", 14, WHITE, bold=True))
        brand_box.add_widget(self.rtl_label("ROYAL STUDIO  -  PRO EDITION v5.2", 9.5, GOLD))
        header.add_widget(brand_box)

        logo = LuxuryCard(
            size_hint=(None, None), size=(dp(38), dp(38)), pos_hint={"center_y": 0.5},
            bg=GOLD, border_color=GOLD, radius=10
        )
        logo.add_widget(Label(text="[b]WS[/b]", markup=True, font_name="Roboto", font_size="13.5sp", color=BG))
        header.add_widget(logo)
        root.add_widget(header)

        # ==================== 2. بطاقة الرابط (ارتفاع ثابت 84dp) ====================
        url_card = LuxuryCard(
            orientation="vertical", size_hint_y=None, height=dp(84),
            padding=[dp(11), dp(8)], spacing=dp(6)
        )
        url_card.add_widget(self.card_title("01", "رابط الموقع المستهدف"))

        url_row = BoxLayout(spacing=dp(6), size_hint_y=None, height=dp(40))
        clear_btn = RoyalButton(text=ar("مسح"), size_hint_x=None, width=dp(52), font_sz="12sp", radius=9)
        paste_btn = RoyalButton(text=ar("لصق"), gold=True, size_hint_x=None, width=dp(56), font_sz="12sp", radius=9)
        clear_btn.bind(on_press=lambda *_: setattr(self.url_input, "text", ""))
        paste_btn.bind(on_press=self.paste_url)

        input_wrap = LuxuryCard(bg=CARD_INNER, border_color=BORDER_SUB, radius=9, padding=[dp(4), 0])
        self.url_input = CenteredInput(
            hint_text="https://example.com", multiline=False,
            font_size="13.5sp", font_name="Roboto", foreground_color=WHITE, hint_text_color=MUTED,
            cursor_color=GOLD, background_normal="", background_active="", background_color=(0, 0, 0, 0)
        )
        input_wrap.add_widget(self.url_input)

        url_row.add_widget(clear_btn)
        url_row.add_widget(paste_btn)
        url_row.add_widget(input_wrap)
        url_card.add_widget(url_row)
        root.add_widget(url_card)

        # ==================== 3. بطاقة النطاق والمقاسات (ارتفاع ثابت 166dp) ====================
        size_card = LuxuryCard(
            orientation="vertical", size_hint_y=None, height=dp(166),
            padding=[dp(11), dp(8)], spacing=dp(7)
        )
        size_card.add_widget(self.card_title("02", "نطاق الالتقاط وأبعاد الشاشة"))

        # صف النطاق (ارتفاع 38dp)
        mode_row = GridLayout(cols=2, spacing=dp(8), size_hint_y=None, height=dp(38))
        self.full_btn = RoyalButton(text=ar("الصفحة بالكامل"), gold=False, font_sz="12sp", radius=9)
        self.visible_btn = RoyalButton(text=ar("الشاشة المرئية فقط"), gold=True, font_sz="12sp", radius=9)
        self.visible_btn.bind(on_press=lambda *_: self.set_mode("visible"))
        self.full_btn.bind(on_press=lambda *_: self.set_mode("full"))
        mode_row.add_widget(self.full_btn)
        mode_row.add_widget(self.visible_btn)
        size_card.add_widget(mode_row)

        # صف الأجهزة القياسية (4 أزرار متناسقة بارتفاع 36dp)
        preset_row = GridLayout(cols=4, spacing=dp(6), size_hint_y=None, height=dp(36))
        self.btn_fhd     = RoyalButton(text=ar("شاشة FHD"), font_sz="11.5sp", radius=9)
        self.btn_desktop = RoyalButton(text=ar("كمبيوتر"), gold=True, font_sz="11.5sp", radius=9)
        self.btn_tablet  = RoyalButton(text=ar("تابلت"), font_sz="11.5sp", radius=9)
        self.btn_phone   = RoyalButton(text=ar("موبايل"), font_sz="11.5sp", radius=9)

        self.preset_btns = [self.btn_phone, self.btn_tablet, self.btn_desktop, self.btn_fhd]

        self.btn_phone.bind(on_press=lambda *_: self.set_resolution(390, 844, self.btn_phone))
        self.btn_tablet.bind(on_press=lambda *_: self.set_resolution(768, 1024, self.btn_tablet))
        self.btn_desktop.bind(on_press=lambda *_: self.set_resolution(1366, 768, self.btn_desktop))
        self.btn_fhd.bind(on_press=lambda *_: self.set_resolution(1920, 1080, self.btn_fhd))

        preset_row.add_widget(self.btn_fhd)
        preset_row.add_widget(self.btn_desktop)
        preset_row.add_widget(self.btn_tablet)
        preset_row.add_widget(self.btn_phone)
        size_card.add_widget(preset_row)

        # صف كبسولات الأبعاد المدمجة (ارتفاع 38dp)
        dim_row = GridLayout(cols=2, spacing=dp(8), size_hint_y=None, height=dp(38))

        # كبسولة الارتفاع (على اليسار)
        h_pill = LuxuryCard(bg=CARD_INNER, border_color=BORDER_SUB, radius=9, padding=[dp(8), dp(2)], spacing=dp(4))
        self.height_input = CenteredInput(
            text="768", multiline=False, input_filter="int",
            font_name="Roboto", font_size="13.5sp", halign="center",
            foreground_color=GOLD, cursor_color=GOLD,
            background_normal="", background_active="", background_color=(0, 0, 0, 0)
        )
        h_pill.add_widget(Label(text="px", font_name="Roboto", font_size="11sp", color=MUTED, size_hint_x=None, width=dp(20)))
        h_pill.add_widget(self.height_input)
        h_pill.add_widget(self.rtl_label("الارتفاع:", 11.5, WHITE, size_hint_x=None, width=dp(52)))

        # كبسولة العرض (على اليمين)
        w_pill = LuxuryCard(bg=CARD_INNER, border_color=BORDER_SUB, radius=9, padding=[dp(8), dp(2)], spacing=dp(4))
        self.width_input = CenteredInput(
            text="1366", multiline=False, input_filter="int",
            font_name="Roboto", font_size="13.5sp", halign="center",
            foreground_color=GOLD, cursor_color=GOLD,
            background_normal="", background_active="", background_color=(0, 0, 0, 0)
        )
        w_pill.add_widget(Label(text="px", font_name="Roboto", font_size="11sp", color=MUTED, size_hint_x=None, width=dp(20)))
        w_pill.add_widget(self.width_input)
        w_pill.add_widget(self.rtl_label("العرض:", 11.5, WHITE, size_hint_x=None, width=dp(45)))

        self.width_input.bind(text=self.on_manual_dim_edit)
        self.height_input.bind(text=self.on_manual_dim_edit)

        dim_row.add_widget(h_pill)
        dim_row.add_widget(w_pill)
        size_card.add_widget(dim_row)
        root.add_widget(size_card)

        # ==================== 4. بطاقة الخيارات الثلاثية (ارتفاع ثابت 82dp) ====================
        opt_card = LuxuryCard(
            orientation="vertical", size_hint_y=None, height=dp(82),
            padding=[dp(11), dp(8)], spacing=dp(6)
        )
        opt_card.add_widget(self.card_title("03", "المحرك، وقت الانتظار، وصيغة الحفظ"))

        opt_grid = GridLayout(cols=3, spacing=dp(6), size_hint_y=None, height=dp(38))
        self.format_spinner = RoyalSpinner(
            text=ar("صيغة PNG"),
            values=(ar("صيغة PNG"), ar("صيغة JPG"))
        )
        self.wait_spinner = RoyalSpinner(
            text=ar("انتظار 5s"),
            values=(ar("انتظار 2s"), ar("انتظار 5s"), ar("انتظار 8s"), ar("انتظار 12s"))
        )
        self.engine_spinner = RoyalSpinner(
            text=ar("محرك ذكي"),
            values=(ar("محرك ذكي"), ar("Microlink HD"), ar("Thum.io Pro"))
        )
        opt_grid.add_widget(self.format_spinner)
        opt_grid.add_widget(self.wait_spinner)
        opt_grid.add_widget(self.engine_spinner)
        opt_card.add_widget(opt_grid)
        root.add_widget(opt_card)

        # ==================== 5. بطاقة المعاينة الحية (تأخذ المساحة المتبقية بذكاء) ====================
        self.status_card = LuxuryCard(
            orientation="vertical", size_hint_y=1, padding=[dp(11), dp(8)], spacing=dp(6),
            border_color=BORDER_SUB
        )
        status_top = BoxLayout(size_hint_y=None, height=dp(24), spacing=dp(6))
        self.status_text = self.rtl_label("اختر الرابط والمقاس ثم اضغط زر الالتقاط بالأسفل", 10.5, MUTED)
        self.status_title = self.rtl_label("الاستوديو جاهز", 12, GREEN, bold=True, width=dp(95))
        status_top.add_widget(self.status_text)
        status_top.add_widget(self.status_title)
        self.status_card.add_widget(status_top)

        # شاشة المعاينة الداكنة (بدون أي مربع أبيض عند عدم وجود صورة)
        self.preview_container = LuxuryCard(
            orientation="vertical", padding=dp(6),
            bg=PREVIEW_BG, border_color=(0.14, 0.17, 0.25, 1), radius=11
        )
        self.empty_placeholder = AnchorLayout()
        ph_box = BoxLayout(orientation="vertical", size_hint=(None, None), size=(dp(240), dp(54)), spacing=dp(2))
        ph_title = Label(
            text=ar("منطقة المعاينة الحية"), font_name=font_name(),
            font_size="13sp", color=GOLD, bold=True, markup=True
        )
        ph_sub = Label(
            text=ar("ستظهر لقطة الموقع هنا فور انتهاء التصوير"),
            font_name=font_name(), font_size="10.5sp", color=MUTED, markup=True
        )
        ph_box.add_widget(ph_title)
        ph_box.add_widget(ph_sub)
        self.empty_placeholder.add_widget(ph_box)

        self.preview_img = Image(allow_stretch=True, keep_ratio=True)
        # نعرض الـ Placeholder الداكن أولاً بدلاً من عنصر Image الأبيض
        self.preview_container.add_widget(self.empty_placeholder)
        self.status_card.add_widget(self.preview_container)
        root.add_widget(self.status_card)

        # ==================== 6. زر الالتقاط الملكي (ارتفاع ثابت ومثالي 50dp) ====================
        self.capture_btn = RoyalButton(
            text=ar("التقاط وحفظ صورة الموقع الآن"),
            gold=True, size_hint_y=None, height=dp(50), font_sz="14.5sp", radius=13
        )
        self.capture_btn.bind(on_press=self.start_capture)
        root.add_widget(self.capture_btn)

        return root

    def rtl_label(self, text, size, color, bold=False, size_hint_x=1.0, width=None):
        kwargs = dict(
            text=ar(text), font_name=font_name(), font_size=f"{size}sp",
            color=color, bold=bold, markup=True, halign="right", valign="middle"
        )
        if width is not None:
            kwargs["size_hint_x"] = None
            kwargs["width"] = width
        else:
            kwargs["size_hint_x"] = size_hint_x
        lab = Label(**kwargs)
        lab.bind(size=lambda obj, val: setattr(obj, "text_size", (max(0, val[0] - dp(4)), val[1])))
        return lab

    def card_title(self, num, title):
        row = BoxLayout(size_hint_y=None, height=dp(20), spacing=dp(7))
        row.add_widget(self.rtl_label(title, 11.5, WHITE, bold=True))
        badge = LuxuryCard(
            size_hint=(None, None), size=(dp(24), dp(20)), pos_hint={"center_y": 0.5},
            bg=(0.14, 0.13, 0.10, 1), border_color=GOLD_SOFT, radius=6
        )
        badge.add_widget(Label(text=num, font_name="Roboto", font_size="10sp", bold=True, color=GOLD))
        row.add_widget(badge)
        return row

    def paste_url(self, *_):
        try:
            clip = Clipboard.paste().strip()
            if clip:
                self.url_input.text = clip
                self.set_status("تم اللصق", clip, GOLD, GOLD_SOFT)
        except Exception:
            pass

    def set_mode(self, mode):
        self.mode = mode
        self.visible_btn.set_active(mode == "visible")
        self.full_btn.set_active(mode == "full")

    def set_resolution(self, w, h, active_btn):
        self._updating_preset = True
        for btn in self.preset_btns:
            btn.set_active(btn is active_btn)
        self.selected_w = w
        self.selected_h = h
        self.width_input.text = str(w)
        self.height_input.text = str(h)
        self.dim_badge_lbl.text = f"[b]{w} x {h}[/b]"
        self._updating_preset = False

    def on_manual_dim_edit(self, *_):
        if getattr(self, "_updating_preset", False):
            return
        try:
            w = int(self.width_input.text or 0)
            h = int(self.height_input.text or 0)
            if w > 0 and h > 0:
                self.selected_w = w
                self.selected_h = h
                self.dim_badge_lbl.text = f"[b]{w} x {h}[/b]"
                # إلغاء تفعيل الأزرار الجاهزة إذا كتب المستخدم رقماً مخصصاً
                presets = {(390, 844): self.btn_phone, (768, 1024): self.btn_tablet,
                           (1366, 768): self.btn_desktop, (1920, 1080): self.btn_fhd}
                active = presets.get((w, h))
                for btn in self.preset_btns:
                    btn.set_active(btn is active)
        except Exception:
            pass

    def set_status(self, title, text, color=GREEN, border=BORDER_SUB):
        self.status_title.text = ar(title)
        self.status_title.color = color
        self.status_text.text = ar(text)
        self.status_card.set_border(border)

    def start_capture(self, *_):
        if self.busy:
            return
        url = self.url_input.text.strip()
        if not url:
            self.set_status("الرابط مطلوب", "يرجى إدخال رابط الموقع أو لصقه أولاً.", RED, RED)
            return
        if not re.match(r"^https?://", url, re.I):
            url = "https://" + url
            self.url_input.text = url

        parsed = urlparse(url)
        if parsed.scheme not in ("http", "https") or not parsed.hostname or "." not in parsed.hostname:
            self.set_status("رابط خاطئ", "اكتب رابطاً صحيحاً مثل https://example.com", RED, RED)
            return

        try:
            w = int(self.width_input.text.strip())
            h = int(self.height_input.text.strip())
            if not (200 <= w <= 2560 and 200 <= h <= 10000):
                raise ValueError
        except Exception:
            self.set_status("أبعاد خاطئة", "العرض 200-2560 والارتفاع 200-10000 بكسل.", RED, RED)
            return

        wait_nums = re.findall(r"\d+", self.wait_spinner.text)
        wait = int(wait_nums[0]) if wait_nums else 5
        fmt = "jpg" if "JPG" in self.format_spinner.text else "png"

        eng_text = self.engine_spinner.text
        if "Microlink" in eng_text:
            engine = "microlink"
        elif "Thum" in eng_text:
            engine = "thum"
        else:
            engine = "auto"

        self.busy = True
        self.capture_btn.disabled = True
        self.capture_btn.text = ar(f"جار التصوير بأبعاد {w}x{h}...")
        device_type = "كمبيوتر" if w >= 1000 else ("تابلت" if w >= 700 else "موبايل")
        self.set_status("جار الالتقاط...", f"وضع {device_type} ({w}x{h}) - يرجى الانتظار...", GOLD, GOLD)
        threading.Thread(target=self.capture_worker, args=(url, w, h, self.mode, wait, fmt, engine), daemon=True).start()

    def fetch_via_microlink(self, url, w, h, mode, wait, fmt):
        is_mobile = "true" if w < 700 else "false"
        params = {
            "url": url,
            "screenshot": "true",
            "meta": "false",
            "viewport.width": str(w),
            "viewport.height": str(h),
            "viewport.isMobile": is_mobile,
            "viewport.hasTouch": is_mobile,
            "viewport.deviceScaleFactor": "1",
            "screenshot.type": "jpeg" if fmt == "jpg" else "png",
            "waitForTimeout": str(min(wait * 1000, 8000)),
        }
        if mode == "full":
            params["screenshot.fullPage"] = "true"

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            )
        }
        r = requests.get("https://api.microlink.io", params=params, timeout=90, headers=headers)
        r.raise_for_status()
        data = r.json()
        shot_url = data.get("data", {}).get("screenshot", {}).get("url")
        if not shot_url:
            raise RuntimeError("لم يرجع المحرك الأول رابط صورة.")

        img_res = requests.get(shot_url, timeout=90, headers=headers)
        img_res.raise_for_status()
        return img_res.content

    def fetch_via_thum(self, url, w, h, mode, wait, fmt):
        parts = [
            "noanimate",
            "viewportWidth", str(w),
            "width", str(w),
        ]
        if fmt == "png":
            parts.insert(0, "png")
        if mode == "full":
            parts.append("fullpage")
        else:
            parts.extend(["crop", str(h)])
        if wait:
            parts.extend(["wait", str(wait)])

        api_url = f"https://image.thum.io/get/{'/'.join(parts)}/{url}"
        r = requests.get(api_url, timeout=120, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        content_type = r.headers.get("Content-Type", "").lower()
        if "image/gif" in content_type or len(r.content) < 8500:
            raise RuntimeError("أرجعت الخدمة صورة انتظار مؤقتة.")
        return r.content

    def capture_worker(self, url, w, h, mode, wait, fmt, engine):
        try:
            img_bytes = None
            used_engine = ""

            if engine == "microlink":
                img_bytes = self.fetch_via_microlink(url, w, h, mode, wait, fmt)
                used_engine = "Microlink HD"
            elif engine == "thum":
                img_bytes = self.fetch_via_thum(url, w, h, mode, wait, fmt)
                used_engine = "Thum.io"
            else:
                try:
                    img_bytes = self.fetch_via_microlink(url, w, h, mode, wait, fmt)
                    used_engine = "Microlink HD"
                except Exception:
                    img_bytes = self.fetch_via_thum(url, w, h, mode, wait, fmt)
                    used_engine = "Thum.io"

            if not img_bytes or len(img_bytes) < 2000:
                raise RuntimeError("حجم الصورة المستلمة صغير جداً.")

            os.makedirs(self.output_dir, exist_ok=True)
            host = re.sub(r"[^A-Za-z0-9.-]", "_", urlparse(url).hostname or "site")[:35]
            name = f"{host}_{w}x{h}_{mode}_{datetime.now().strftime('%H%M%S')}.{fmt}"
            path = os.path.join(self.output_dir, name)
            with open(path, "wb") as f:
                f.write(img_bytes)
            Clock.schedule_once(lambda dt: self.capture_done(path, len(img_bytes), w, h, used_engine), 0)
        except Exception as exc:
            msg = str(exc) or exc.__class__.__name__
            Clock.schedule_once(lambda dt, m=msg: self.capture_failed(m), 0)

    def capture_done(self, path, size, w, h, used_engine):
        self.busy = False
        self.capture_btn.disabled = False
        self.capture_btn.text = ar("التقاط وحفظ صورة الموقع الآن")
        info = f"{used_engine}  |  {w}x{h}  |  {size/1024:.0f} KB"
        self.set_status("تم الحفظ بنجاح", info, GREEN, GREEN)

        # استبدال الـ Placeholder الداكن بصورة الموقع الحقيقية
        self.preview_container.clear_widgets()
        self.preview_img.source = path
        self.preview_img.reload()
        self.preview_container.add_widget(self.preview_img)

    def capture_failed(self, message):
        self.busy = False
        self.capture_btn.disabled = False
        self.capture_btn.text = ar("التقاط وحفظ صورة الموقع الآن")
        self.set_status("فشل التصوير", message[:110], RED, RED)


if __name__ == "__main__":
    WebsiteShotRoyal().run()
