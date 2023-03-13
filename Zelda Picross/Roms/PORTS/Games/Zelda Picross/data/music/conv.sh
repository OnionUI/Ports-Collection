for i in *.wav ; do 
    ffmpeg -i "$i" -acodec libvorbis "$(basename "${i/.wav}").ogg"
done
