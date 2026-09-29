# uso: qa.sh <dir_lingua> <Scena>  -> contact sheet dell'ultimo fotogramma di ogni slide
cd $1
S=$2; rm -rf qa_$S; mkdir -p qa_$S
python3 - "$S" <<'P'
import json,sys,subprocess
S=sys.argv[1]; d=json.load(open(f'slides/{S}.json'))
for i,sl in enumerate(d['slides']):
    subprocess.run(['ffmpeg','-loglevel','error','-sseof','-0.1','-i',sl['file'],'-frames:v','1','-update','1',f'qa_{S}/{i:03d}.png','-y'])
from PIL import Image; import glob
fs=sorted(glob.glob(f'qa_{S}/*.png'))
for k in range(0,len(fs),9):
    ims=[Image.open(x) for x in fs[k:k+9]]; w,h=ims[0].size
    Sh=Image.new('RGB',(w*3+20,h*3+20),(200,200,200))
    for j,im in enumerate(ims): Sh.paste(im,((j%3)*(w+10),(j//3)*(h+10)))
    Sh.save(f'qa_{S}/sheet{k//9}.png')
print(len(fs))
P
