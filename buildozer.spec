[app]
title = Website Shot Royal
package.name = websiteshotroyal
package.domain = org.royal
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 5.3

requirements = python3,kivy==2.3.0,arabic-reshaper,urllib3,certifi

orientation = portrait
fullscreen = 0
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
