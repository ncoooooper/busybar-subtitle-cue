"""Local transport for the BUSY Bar. Reads and actions are serialized in one process."""
import argparse,json,threading
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
from source import Session
def run():
    p=argparse.ArgumentParser();p.add_argument("path",type=Path);p.add_argument("--bind",default="127.0.0.1");p.add_argument("--port",type=int,default=8770);args=p.parse_args()
    model=Session(args.path.expanduser().resolve());lock=threading.Lock()
    class Handler(BaseHTTPRequestHandler):
        def reply(self,status,obj):
            data=json.dumps(obj,ensure_ascii=False).encode();self.send_response(status);self.send_header("Content-Type","application/json; charset=utf-8");self.send_header("Cache-Control","no-store");self.send_header("Content-Length",str(len(data)));self.end_headers();self.wfile.write(data)
        def process(self,write):
            if urlsplit(self.path).path!="/reading":self.reply(404,{"error":"Unknown path"});return
            try:
                with lock:
                    if write:
                        if self.headers.get("Origin") or self.headers.get_content_type()!="application/json":self.reply(403,{"error":"Local JSON client required"});return
                        length=int(self.headers.get("Content-Length","0"))
                        if not 0<length<512:raise ValueError("Invalid command length")
                        key=json.loads(self.rfile.read(length))["key"]
                        if key not in ("up","down","ok","start","hold-ok","hold-start"):raise ValueError("Unknown key")
                        model.action(key)
                    result=model.snapshot()
                self.reply(200,result)
            except (OSError,ValueError,KeyError,TypeError) as e:self.reply(400,{"error":str(e)})
        def do_GET(self):self.process(False)
        def do_POST(self):self.process(True)
        def log_message(self,*args):pass
    server=ThreadingHTTPServer((args.bind,args.port),Handler)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()
if __name__=="__main__":run()
