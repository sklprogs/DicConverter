#!/bin/bash

product="DicConverter"
python="$HOME/.wine/drive_c/Python34"
pyinstaller="$python/Scripts/pyinstaller.exe"
binariesdir="$HOME/binaries"
srcdir="$HOME/bin/$product/src"
resdir="$HOME/bin/$product/resources"
cmd="$HOME/bin/$product/build/Wine/$product.cmd"
tmpdir="$HOME/.wine/drive_c/users/pete/$product" # Will be deleted!
builddir="$tmpdir/$product"                      # Will be deleted!

if [ ! -e "$pyinstaller" ]; then
    echo "pyinstaller is not installed!"; exit
fi

if [ ! -e "$cmd" ]; then
    echo "File $cmd does not exist!"; exit
fi

if [ ! -d "$binariesdir/$product" ]; then
    echo "Folder $binariesdir/$product does not exist!"; exit
fi

if [ ! -d "$srcdir" ]; then
    echo "Folder $srcdir does not exist!"; exit
fi

if [ ! -d "$resdir" ]; then
    echo "Folder $resdir does not exist!"; exit
fi

# Build with pyinstaller
rm -rf "$tmpdir"
mkdir -p "$builddir/app"
cp -r "$srcdir"/* "$tmpdir"
cp -r "$resdir" "$builddir"
cp "$cmd" "$builddir"
cd "$tmpdir"
# Icon path should be windows-compliant
wine "$pyinstaller" -w -i ./$product/resources/icon_64x64_$product.ico "$product.py"
mv "$tmpdir/dist/$product"/* "$builddir/app"
# Tesh launch
cd "$builddir/app"
wine ./$product.exe&
# Update the archive
read -p "Update the AppImage? (Y/n) " choice
if [ "$choice" = "N" ] || [ "$choice" = "n" ]; then
    exit;
fi
mv -f "$binariesdir/$product/windows.7z" "$binariesdir/$product/windows (OLD).7z"
7z a "$binariesdir/$product/windows.7z" "$builddir"
rm -rf "$tmpdir"
