#!/bin/bash
COURSE_ROOT="${COURSE_ROOT:-$(d="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"; while [ ! -e "$d/.course_root" ] && [ "$d" != "/" ]; do d="$(dirname "$d")"; done; echo "$d")}"
# uso: hq_lecture.sh <k> "<nome EN>" "<nome IT>" SceneA SceneB ...   (file scena: s<k>a.py, s<k>b.py ... in ordine)
k=$1; NEN=$2; NIT=$3; shift 3; SC="$@"
[ -f ~/mvenv/bin/activate ] && source ~/mvenv/bin/activate
for L in en it; do
  cd $COURSE_ROOT/L$k/manim/$L
  i=0; for S in $SC; do l=$(echo abcdefgh | cut -c$((i+1))); f=s$k$l.py
    echo "L$k $L $S"; EEG_LANG=$L manim-slides render --resolution 1920,1080 --frame_rate 30 --media_dir mediaHQ_$l $f $S > hq_$S.log 2>&1 || echo "FAIL $L $S"; i=$((i+1)); done
  N=$([ $L = en ] && echo "$NEN" || echo "$NIT")
  bash $COURSE_ROOT/common/export_eeg.sh $COURSE_ROOT/L$k/manim/$L $COURSE_ROOT/L$k/final_$L "$N" "$N" $SC > /tmp/eegexp_${k}_$L.log 2>&1 && echo "EXPORT OK $L" || echo "EXPORT FAIL $L"
done
echo EEGDONE
