#!/bin/bash
COURSE_ROOT="${COURSE_ROOT:-$(d="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; while [ ! -e "$d/.course_root" ] && [ "$d" != "/" ]; do d="$(dirname "$d")"; done; echo "$d")}"
# uso: export.sh <Ldir> "<Nome file>" "<titolo>" Scene1 Scene2 ...
set -e
MD=$1; FD=$2; N=$3; TI=$4; shift 4; S="$@"
[ -f ~/mvenv/bin/activate ] && source ~/mvenv/bin/activate
cd $MD && mkdir -p $FD
manim-slides convert $S "$FD/$N.html" -cslide_number=true -cprogress=true "-ctitle=$TI" > conv.log 2>&1
cd $FD && A="${N}_assets" && mkdir -p "$A/reveal/plugin/highlight" "$A/reveal/theme"
cp /tmp/rv/package/dist/reveal.css /tmp/rv/package/dist/reveal.js "$A/reveal/"; cp /tmp/rv/package/dist/theme/black.css "$A/reveal/theme/"
cp /tmp/rv/package/dist/plugin/notes.js "$A/reveal/notes.js"; cp /tmp/rv/package/dist/plugin/highlight/zenburn.css "$A/reveal/plugin/highlight/"
python3 - "$N" <<'E'
import sys
N=sys.argv[1]; f=N+'.html'; s=open(f).read()
base='https://cdn.jsdelivr.net/npm/reveal.js@6.0.1/dist/'
s=s.replace(base+'plugin/notes.js',N+'_assets/reveal/notes.js').replace(base,N+'_assets/reveal/')
s=s.replace('</head>','  <style>.reveal-viewport,body{background:#16213A!important}</style>\n</head>',1)
open(f,'w').write(s); print('cdn', s.count('cdn.jsdelivr'), 'mp4', s.count('.mp4'))
E
cd $MD && rm -rf slides_small && cp -r slides slides_small && sed -i 's#"slides/files/#"slides_small/files/#' slides_small/*.json
for f in slides_small/files/*/*.mp4; do ffmpeg -loglevel error -y -i "$f" -c:v libx264 -crf 32 -preset veryfast -pix_fmt yuv420p -an "$f.tmp.mp4" && mv "$f.tmp.mp4" "$f"; done
manim-slides convert --folder slides_small $S "$FD/$N.pptx" > convp.log 2>&1
cd $FD && python3 - "$N" <<'E'
import zipfile,io,sys
from PIL import Image
src=sys.argv[1]+".pptx"; tmp="/tmp/px.pptx"
zi=zipfile.ZipFile(src); zo=zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED)
for it in zi.infolist():
    b=zi.read(it.filename)
    if it.filename.lower().endswith('.png') and 'media' in it.filename:
        im=Image.open(io.BytesIO(b)).convert('RGB').resize((1280,720)).quantize(128)
        o=io.BytesIO(); im.save(o,'PNG',optimize=True); b=o.getvalue()
    zo.writestr(it,b)
zo.close()
E
mv /tmp/px.pptx "$N.pptx"; ls -la; du -sh "${N}_assets"
/usr/bin/python3 $COURSE_ROOT/common/pptx_autonext.py "$FD/$N.pptx" "$MD" $S
cd /mnt/skills/public/pptx/scripts/office && /usr/bin/python3 validate.py "$FD/$N.pptx" 2>&1 | tail -1
