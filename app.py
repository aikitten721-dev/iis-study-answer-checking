"""Local A2 demonstration. Python standard library only; no model service."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import json
import argparse
import retrieve

ROOT=Path(__file__).resolve().parent

def load_cases():
    cases=json.loads((ROOT/'fixtures.json').read_text(encoding='utf-8'))
    notes={p['file']:p for p in retrieve.load() if p['file'].startswith('sample_notes_')}
    for case in cases:
        note=notes[case['source_file']]
        case['source']=note['text']
        case['location']=note['source']+' · '+note['section']
    return cases

def search(question):
    hits=retrieve.retrieve(question,k=3)
    if not hits or hits[0]['score']<0.25:
        return {'status':'Not verified','message':'No sufficiently matching passage was found in the sample collection. Try another question or inspect the notes manually.','hits':[]}
    return {'status':'Passages to inspect','message':'Ranked by word overlap with your query. Inspect the passages below to check whether they support a claim.','hits':hits,
            'source_status_note':'Superseded passages receive a ×0.3 ranking adjustment and remain available for inspection.' if any(h['superseded'] for h in hits) else ''}

class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,directory=str(ROOT),**kwargs)
    def do_GET(self):
        parsed=urlparse(self.path)
        if parsed.path=='/fixtures.json':
            self.send_json(load_cases())
        elif parsed.path=='/api/search':
            query=parse_qs(parsed.query).get('q',[''])[0][:1000]
            self.send_json(search(query))
        elif parsed.path in ('/','/index.html'):
            super().do_GET()
        else:
            self.send_error(404)

    def send_json(self,data):
        body=json.dumps(data,ensure_ascii=False).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Content-Length',str(len(body)))
        self.end_headers()
        self.wfile.write(body)

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--port',type=int,default=8000)
    args=parser.parse_args()
    server=ThreadingHTTPServer(('127.0.0.1',args.port),Handler)
    print('Open http://127.0.0.1:%d'%server.server_port,flush=True)
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()
