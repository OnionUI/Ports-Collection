#!/bin/sh
mydir=`pwd`
miyoodir=/mnt/SDCARD/miyoo
sysdir=/mnt/SDCARD/.tmp_update
export SDL_VIDEODRIVER=mmiyoo
export EGL_VIDEODRIVER=mmiyoo
export SDL_AUDIODRIVER=dsp

if [ -e "$sysdir/bin/infoPanel" ]; then
    if [ ! -e "$mydir/Data.rsdk" ]; then
        infoPanel -t "Missing data files" -m "File: Data.rsdk \n Does not exist in the root of this app \n\n Please acquire the file and try again" --auto 2> /dev/null
        touch /tmp/dismiss_info_panel
        sleep 4
        rm -rf /tmp/dismiss_info_panel
        exit
    fi
fi

CUST_CPUCLOCK=1
if [ "$CUST_CPUCLOCK" = "1" ]; then
    echo "set customized cpuspeed"
    ./cpuclock 1600
fi

cd "$mydir"
export LD_PRELOAD="$mydir/lib/libSDL2-2.0.so.0:$miyoodir/lib/libpadsp.so"
./RSDKv5U
unset LD_PRELOAD
