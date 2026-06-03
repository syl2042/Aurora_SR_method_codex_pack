#!/usr/bin/env python3
import argparse,subprocess,datetime,hashlib
from pathlib import Path
def compact(text,max_lines=120):
    lines=text.splitlines(); keys=('error','failed','failure','warning','traceback','exception','fatal')
    hits=[l for l in lines if any(k in l.lower() for k in keys)]
    out=['## Compact command output','',f'- Raw lines: {len(lines)}',f'- Highlighted lines: {len(hits)}','']
    out+=lines[:30]
    if len(lines)>60: out+=['','... output truncated ...']+lines[-30:]
    else: out+=lines[30:]
    if hits: out+=['','## Highlighted errors/warnings']+hits[:max_lines]
    return '\n'.join(out[:max_lines])+'\n'
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--max-lines',type=int,default=120); ap.add_argument('cmd',nargs=argparse.REMAINDER); a=ap.parse_args()
    cmd=a.cmd[1:] if a.cmd and a.cmd[0]=='--' else a.cmd
    if not cmd: raise SystemExit('missing command after --')
    stamp=datetime.datetime.now().strftime('%Y%m%d_%H%M%S'); slug=hashlib.sha1(' '.join(cmd).encode()).hexdigest()[:8]
    raw=Path('output/codex/raw'); comp=Path('output/codex/compact'); raw.mkdir(parents=True,exist_ok=True); comp.mkdir(parents=True,exist_ok=True)
    rp=raw/f'{stamp}_{slug}.log'; cp=comp/f'{stamp}_{slug}.summary.md'
    proc=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    rp.write_text(proc.stdout,encoding='utf-8'); summary=compact(proc.stdout,a.max_lines); cp.write_text(summary,encoding='utf-8')
    print(summary); print(f'\nRaw output: {rp}\nCompact output: {cp}')
    raise SystemExit(proc.returncode)
if __name__=='__main__': main()
