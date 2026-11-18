"""SRT rehearsal transport with indexed seeking and an elapsed-time playback clock."""
import bisect,re,textwrap,time,html
from pathlib import Path
stamp=r"(\d{1,3}):(\d{2}):(\d{2})[,.](\d{3})"
line=re.compile(stamp+r"\s*-->\s*"+stamp)
def seconds(bits):
    h,m,s,ms=map(int,bits);return h*3600+m*60+s+ms/1000
def format_time(n):
    sec=int(max(0,n));return f"{sec//3600:02}:{sec//60%60:02}:{sec%60:02}"
class Session:
    def __init__(self,file):
        raw=file.read_text(encoding="utf-8-sig").replace("\r\n","\n").replace("\r","\n");cues=[]
        for block in re.split(r"\n\s*\n",raw.strip()):
            lines=block.splitlines()
            for i,text in enumerate(lines):
                m=line.match(text.strip())
                if m:
                    a,b=seconds(m.groups()[:4]),seconds(m.groups()[4:]);words=html.unescape(re.sub(r"<[^>]*>",""," ".join(lines[i+1:]))).strip()
                    if b>a and words:cues.append((a,b,words))
                    break
        if not cues:raise ValueError("No timed SRT cues found")
        self.cues=sorted(cues,key=lambda x:x[0]);self.starts=[c[0] for c in self.cues];self.index=0;self.offset=self.starts[0];self.origin=None;self.line=0
    def current(self):return self.offset+(time.monotonic()-self.origin if self.origin is not None else 0)
    def sync(self):
        t=self.current();index=max(0,bisect.bisect_right(self.starts,t)-1)
        if index!=self.index:self.index=index;self.line=0
        if self.origin is not None and t>=self.cues[-1][1]:self.origin=None;self.offset=self.cues[-1][1]
    def action(self,key):
        self.sync()
        if key in ("up","down"):
            i=min(len(self.cues)-1,max(0,self.index+(1 if key=="up" else -1)))
            self.index=i;self.offset=self.starts[i];self.line=0
            if self.origin is not None:self.origin=time.monotonic()
        elif key in ("ok","start"):
            if self.origin is None:
                if self.offset>=self.cues[-1][1]:self.index=0;self.line=0;self.offset=self.starts[0]
                self.origin=time.monotonic()
            else:self.offset=self.current();self.origin=None
        elif key=="hold-ok":self.line+=1
        elif key=="hold-start":
            self.index=0;self.line=0;self.offset=self.starts[0];self.origin=None
    def snapshot(self):
        self.sync();a,b,words=self.cues[self.index];pos=self.current();lines=textwrap.wrap(words,width=23) or [""]
        pages=(len(lines)+2)//3;part=self.line%pages;shown=lines[part*3:part*3+3]
        state="PLAY" if self.origin is not None else "PAUSE"
        if pos>=b and self.index+1<len(self.cues):state="GAP"
        return dict(caption=f"{state}   {self.index+1}/{len(self.cues)}",value=format_time(pos)[3:] if pos<3600 else format_time(pos),lines=[format_time(a)+" - "+format_time(b),*shown,f"Page {part+1}/{pages}  /  hold OK", "Wheel: cue / Click: play"],version=str(self.index)+"-"+state)
