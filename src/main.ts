import {surface,panel,label,rect,type Frame,type Key} from "@shared/surface";
import {loadValues} from "@shared/settings";
type Data={caption:string;value:string;lines:string[];version:string;pixels?:string[];palette?:string[];error?:string};
let addr="",closed=false,busy=false,reading:Data|undefined,failed=false;const commands:Key[]=[];
let timer:ReturnType<typeof setTimeout>|undefined;
function draw():Frame{
 const p=reading,frame:Frame=[];if(p?.pixels&&p.palette){
   for(let y=0;y<p.pixels.length;y++){const row=p.pixels[y];for(let x=0;x<row.length;){let end=x+1;while(end<row.length&&row[end]===row[x])end++;
    const color=p.palette[Number(row[x])];if(color&&color!=="#000000")frame.push(rect("px"+y+"-"+x,2+x*2,1+y,(end-x)*2,1,color+"FF"));x=end;}}
   frame.push(label("side",p.caption,51,0,"#82AFD2"+"FF","front","tiny"),label("n",p.value,52,6,"#FFF2D7FF","front","small"));
 }else frame.push(label("head",p?.caption||"Subtitle Cue",1,0,"#82AFD2"+"FF","front","tiny"),label("n",p?.value||(addr?"Offline":"Set URL"),1,6,"#FFF2D7FF"));
 return frame.concat(panel("Subtitle Cue".toUpperCase(),failed?["Companion unavailable",...(p?p.lines.slice(0,4):["Check host and local URL"])]:p?.lines||["Set companion URL in settings","Start the local reader"]));}
async function next(){
 if(!addr||busy||closed)return;if(timer!==undefined)clearTimeout(timer);timer=undefined;busy=true;
 const key=commands.shift();try{
 const res=await fetch(addr,key?{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({key})}:undefined);
 if(!res.ok)throw Error("HTTP "+res.status);const data=await res.json() as Data;if(data.error||typeof data.value!=="string"||!Array.isArray(data.lines))throw Error("Bad frame");
 const changed=!!reading&&reading.version!==data.version;reading=data;failed=false;if(!closed)refresh(changed?"change":undefined);
 }catch(e){failed=true;if(!closed)refresh();}finally{busy=false;if(!closed)timer=setTimeout(()=>{timer=undefined;void next();},commands.length?5:failed?1800:350);}
}
const refresh=surface(draw,k=>{if(!addr)return;if(commands.length<32)commands.push(k);void next();},()=>{closed=true;if(timer!==undefined)clearTimeout(timer);},{motif:"bookmark",color:"#82AFD2",shine:"#FFEBD8"});
void loadValues().then(v=>{if(closed)return;addr=String(v?.bridge||"").trim();refresh();void next();});
