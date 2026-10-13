"""Real DeepSeek/Chromium visual and video probes, with independent fixtures."""
import hashlib,json,re,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/'src'))
from evaluation.live import PaidLedger,LiveEmployee
from workflow_runtime import WorkflowToolLoop
out=Path('docs/dataset-evaluation/reports/full-tool-coverage/round-17-browser-capabilities')
root=Path('/tmp/chimera-browser-probe17');root.mkdir(exist_ok=False)
key=Path('/tmp/chimera-full-tools-private.key').read_text().strip()
ledger=PaidLedger(out/'costs.jsonl',5)
business=root/'business';business.mkdir()
(business/'canvas.html').write_text('<canvas id="shape" width="160" height="120"></canvas><script>let c=document.querySelector("canvas").getContext("2d");c.fillStyle="red";c.fillRect(0,0,160,120)</script>')
subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-f','lavfi','-i','color=c=red:s=160x120:d=1','-f','lavfi','-i','color=c=blue:s=160x120:d=1','-filter_complex','[0:v][1:v]concat=n=2:v=1:a=0[out]','-map','[out]','-y',str(business/'clip.mp4')],check=True)
(business/'video.html').write_text('<video src="clip.mp4" controls width="160" height="120"></video>')
results=[]
for case,page,question in [('canvas','canvas.html','What color is the rectangle in the canvas? Inspect the rendered screenshot; answer its color.'),('video','video.html','Use ask_question_about_video on selector video to identify the two dominant full-screen colors in temporal order. The question is: Which color appears first and which color appears second?')]:
 context={'run_id':'visual-probe17','task_id':case}
 employee=LiveEmployee({'variant':0},context,key,ledger)
 loop=WorkflowToolLoop(root/case,member_id='employee',trace_id=case,context=context,base_tools=True,business_workspace=business)
 failure=None
 try:loop.run('Use browse_url to visit '+(business/page).as_uri()+'. Browser task: '+question+' Set round_limit=8. Read the browser answer, finish_task, then answer briefly.',workflow_id='general',chat_fn=employee,max_steps=16)
 except Exception as e:failure=type(e).__name__
 events=[json.loads(s.split(' ',1)[1]) for s in loop.log_path.read_text().splitlines()]
 answers=[e['result']['payload']['answer'] for e in events if e.get('tool_name')=='browse_url' and e.get('status')=='success']
 if case=='canvas':good=any(re.search(r'\bred\b',s,re.I) for s in answers)
 else:
  videos=[e['result']['payload'] for e in events if e.get('tool_name')=='browser_action' and e.get('status')=='success' and e['arguments'].get('action')=='ask_question_about_video']
  good=bool(videos) and any(re.search(r'red.*blue',v['video_answer'],re.I|re.S) for v in videos)
  if videos:
   from PIL import Image
   frames=videos[-1]['video_frames'];a=Image.open(frames[0]['path']).getpixel((100,100));b=Image.open(frames[-1]['path']).getpixel((100,100))
   good=good and a[0]>200 and a[2]<30 and b[2]>200 and b[0]<30
 results.append({'case':case,'status':'PASS' if good and failure is None else 'FAIL','exception':failure,'answers':answers})
print(results,flush=True)
(out/'report.json').write_text(json.dumps({'status':'PASS' if all(r['status']=='PASS' for r in results) else 'FAIL','results':results,'cost_usd_peak_upper':ledger.spent,'requests':ledger.calls,'scope':'real Chromium/DeepSeek screenshot and temporal visual frames; no audio claim'},indent=2)+'\n')
import tarfile
with tarfile.open(out/'evidence.tar.gz','w:gz') as archive:archive.add(root,arcname='study')
