#!/usr/bin/env bash
set -e
BASEDIR="$(cd "$(dirname "$0")" && pwd)"
cd "$BASEDIR"

# Install buildozer jika belum ada
if ! command -v buildozer &> /dev/null; then
    pip install --upgrade pip
    pip install buildozer cython
    pkg install -y python3 clang libffi libffi-dev git zlib zlib-dev
fi

# Inisialisasi buildozer jika belum
if [ ! -f buildozer.spec ]; then
    buildozer init
    sed -i 's/package.name = .*/package.name = gpt_text2video/' buildozer.spec
    sed -i 's/package.domain = .*/package.domain = org.bot/' buildozer.spec

    # Tambahkan requirements python dan sumber untuk KivyMD
    sed -i '/requirements = /c\
requirements = python3,kivy,kivymd,requests' buildozer.spec
fi

# Build APK
buildozer -v android debug
APK_PATH=$(ls bin/*.apk | head -n 1)
cp "$APK_PATH" "$BASEDIR/../../gpt_text2video.apk"
echo "✅ APK berhasil dibuat: $BASEDIR/../../gpt_text2video.apk"
