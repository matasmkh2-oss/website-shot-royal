[app]
title = Website Shot Royal
package.name = websiteshotroyal
package.domain = org.royal
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 5.3

# تثبيت إصدار بايثون و Kivy المستقرين للأندرويد (بدون python-bidi لأن الكود يدعم العربية تلقائياً)
requirements = python3==3.11.6,hostpython3==3.11.6,kivy==2.3.0,arabic-reshaper,openssl,urllib3,certifi

orientation = portrait
fullscreen = 0
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True
p4a.branch = master

[buildozer]
log_level = 1
warn_on_root = 1
