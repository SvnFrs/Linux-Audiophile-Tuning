#!/bin/sh

#bash <(curl -s  https://raw.githubusercontent.com/parkmino/audiophile/master/artik710/patch210207.sh)
#bash <(curl -sL https://bit.ly/3oZE4EC)

### 1. Tune ALSA Library

wget -P /etc/ https://github.com/parkmino/audiophile/raw/master/artik710/libasound.so.2.0.0.{min,mix,plug}_1.2.3.1.dev.shm
mv /etc/libasound.so.2.0.0.min_1.2.3.1.dev.shm  /etc/libasound.so.2.0.0.min.dev.shm
mv /etc/libasound.so.2.0.0.mix_1.2.3.1.dev.shm  /etc/libasound.so.2.0.0.mix.dev.shm
mv /etc/libasound.so.2.0.0.plug_1.2.3.1.dev.shm /etc/libasound.so.2.0.0.plug.dev.shm
sed -i 's/libasound.so.2.0.0.min/libasound.so.2.0.0.min.dev.shm/; s/libasound.so.2.0.0.mix/libasound.so.2.0.0.mix.dev.shm/; s/libasound.so.2.0.0.plug/libasound.so.2.0.0.plug.dev.shm/; /^ln.*alsa.conf/s/^/#/' /etc/rc.local

### 2. Tune ALSA Configuration

rm /usr/share/alsa/alsa.conf
sed -i 's/pcm.hw {/pcm.hw{/' /usr/share/alsa/alsa.conf.{min,mix,plug}

### 3. Tune Shell Redirection

sed -i 's/ 1<\/dev\/null 2<\/dev\/null 0<\/dev\/null/  \&>   \/dev\/null  <  \/dev\/null/g' /etc/rc.local
sed -i 's/>\/dev\/null<\/dev\/null 2>\/dev\/null/  \&>   \/dev\/null  <  \/dev\/null/g' /opt/RoonBridge/Bridge/RoonBridge

### 4. Tune MPD buffer_before_play

sed -i 's/0.*%/03975%/' /etc/mpd.conf.sav

### 5. Update Release

sed -i 's/[0-9]*$/210207/' /etc/release

### 5. Clear History & Sync

rm -f /root/.bash_history ~/.bash_history ; history -c
sync

printf "\n* Finished and reboot to take effect. \n* 완료되어 시스템을 다시 시작하면 적용됩니다. (^_^)\n"
