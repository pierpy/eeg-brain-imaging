#!/bin/bash
COURSE_ROOT="${COURSE_ROOT:-$(d="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; while [ ! -e "$d/.course_root" ] && [ "$d" != "/" ]; do d="$(dirname "$d")"; done; echo "$d")}"
# uso: build_pptx.sh <k>  -> out/EEG_L<k>_{en,it}.pptx + QA (qa_<lang>_*.png)
set -e
k=$1; LD=$COURSE_ROOT/L$k; cd $LD; mkdir -p out
for L in en it; do
  node build_pptx$k.js $L >/dev/null
  F="out/EEG_L${k}_$L.pptx"
  /usr/bin/python3 $COURSE_ROOT/common/fix_ppr.py "$F"
  { [ -f "$PPTX_VALIDATE" ] && python3 "$PPTX_VALIDATE" "$F" | tail -1 || true; }
  cd out; rm -rf q_$L; mkdir q_$L; cp "EEG_L${k}_$L.pptx" q_$L/x.pptx; cd q_$L
  soffice --headless --convert-to pdf x.pptx >/dev/null 2>&1
  pdftoppm -jpeg -r 55 x.pdf s
  python3 -c "
from PIL import Image; import glob
fs=sorted(glob.glob('s-*.jpg'))
for j in range(0,len(fs),9):
  ims=[Image.open(f) for f in fs[j:j+9]];w,h=ims[0].size
  S=Image.new('RGB',(w*3+20,h*3+20),(120,120,120))
  for i,im in enumerate(ims): S.paste(im,((i%3)*(w+10),(i//3)*(h+10)))
  S.save(f'../qa_${L}_{j//9}.png')
print(len(fs))"
  cd $LD
done
