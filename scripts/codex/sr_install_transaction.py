"""Content-based SR installation transactions. No source-version branching."""
from __future__ import annotations
import base64
import hashlib
import json
import os
import tempfile
import uuid
from pathlib import Path

STATE = 'docs/codex/SR_MANAGED_STATE.json'
START = '<!-- AURORA_SR_PACK_START -->'
END = '<!-- AURORA_SR_PACK_END -->'

def digest(data):
    return hashlib.sha256(data).hexdigest() if data is not None else None

def safe_path(root, relative):
    rel = Path(relative)
    if rel.is_absolute() or '..' in rel.parts or not rel.parts:
        raise ValueError(f'unsafe path: {relative}')
    current = root
    for part in rel.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError(f'symlink requires manual review: {relative}')
    if not current.resolve().is_relative_to(root.resolve()):
        raise ValueError(f'path escapes target: {relative}')
    return current

def read(path):
    if path.exists() and not path.is_file():
        raise ValueError(f'expected file: {path}')
    return path.read_bytes() if path.exists() else None

def atomic_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = path.stat().st_mode & 0o777 if path.exists() else 0o644
    fd, tmp = tempfile.mkstemp(prefix='.sr-write-', dir=path.parent)
    try:
        with os.fdopen(fd, 'wb') as handle:
            handle.write(data); handle.flush(); os.fsync(handle.fileno())
        os.chmod(tmp, mode)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)

def encode(data):
    return base64.b64encode(data).decode() if data is not None else None

def decode(data):
    return base64.b64decode(data, validate=True) if data is not None else None

def merge_missing(current, defaults):
    # Existing scalars/lists are project policy, never broaden them with defaults.
    if not isinstance(current, dict) or not isinstance(defaults, dict):
        raise ValueError('profile must be a mapping')
    result = dict(current)
    for key, value in defaults.items():
        if key not in result: result[key] = value
        elif isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_missing(result[key], value)
    return result

def managed_block(text):
    if text.count(START) != text.count(END) or text.count(START) > 1:
        raise ValueError('malformed or duplicate managed block')
    if START not in text: return None
    a, b = text.index(START), text.index(END)+len(END)
    if b < a: raise ValueError('reversed managed block')
    return text[a:b]

def build_plan(source, target, mapping, dirs, owned, agents_block, skill_block, profile='default'):
    if Path(profile).name != profile or profile in {"", ".", ".."}:
        raise ValueError("profile must be a local profile name")
    source, target = source.resolve(), target.resolve()
    if source == target or target.is_relative_to(source):
        raise ValueError('target must not be the source pack or a child of the source pack')
    state_path = safe_path(target, STATE)
    state = json.loads(state_path.read_text()) if state_path.exists() else {}
    if not isinstance(state, dict) or (state and (state.get('schema_version') != 1 or not isinstance(state.get('hashes'),dict))):
        raise ValueError('unknown managed-state schema; manual review required')
    known_path = source/'core/SR_MANAGED_HASHES.json'
    known = json.loads(known_path.read_text()) if known_path.exists() else {}
    files = dict(mapping)
    for src_dir, dst_dir in dirs.items():
        for path in sorted((source/src_dir).rglob('*')):
            if path.is_symlink(): raise ValueError(f'source symlink: {path}')
            if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc':
                files[str(path.relative_to(source))] = str(Path(dst_dir)/path.relative_to(source/src_dir))
    operations, conflicts, preserved = [], [], []
    next_hashes = dict(state.get('hashes', {}))
    for src, rel in sorted(files.items()):
        incoming = safe_path(source, src).read_bytes()
        path = safe_path(target, rel); before = read(path); desired = incoming
        try:
            if before is not None and before != incoming:
                if rel in ('AGENTS.md','docs/codex/SKILL_MAP.md'):
                    text = before.decode(); block = agents_block.strip() if rel == 'AGENTS.md' else skill_block.strip()
                    old = managed_block(text)
                    hashes = known.get(rel, [])
                    if old and old != block and digest(old.encode()) not in known.get(rel+'#block',[]) and digest(before) != state.get('hashes',{}).get(rel):
                        raise ValueError('locally modified/unknown managed block')
                    if old: desired = text.replace(old, block, 1).encode()
                    elif digest(before) in hashes:
                        # Recognized full template: replace only known pack contents.
                        desired = incoming
                    else:
                        desired = (text.rstrip()+'\n\n'+block+'\n').encode()
                elif rel == 'docs/codex/SR_PACK_VERSION.json':
                    current = json.loads(before)
                    if not isinstance(current, dict): raise ValueError('version metadata must be an object')
                    desired = (json.dumps({**current, **json.loads(incoming)},indent=2)+'\n').encode()
                elif rel == 'docs/codex/PROJECT_PROFILE.yaml':
                    try:
                        import yaml
                    except ImportError as exc:
                        raise ValueError("PyYAML unavailable: cannot safely merge the existing profile") from exc
                    current = yaml.safe_load(before.decode())
                    defaults_path = source/'profiles'/profile/'PROJECT_PROFILE.yaml'
                    defaults = yaml.safe_load(defaults_path.read_text() if defaults_path.exists() else incoming.decode())
                    merged = merge_missing(current, defaults)
                    desired = before if merged == current else yaml.safe_dump(merged,sort_keys=False,allow_unicode=True).encode()
                elif rel in owned or rel.startswith('docs/codex/project-skills/'):
                    desired = before; preserved.append(rel)
                elif digest(before) != state.get('hashes',{}).get(rel) and digest(before) not in known.get(rel,[]):
                    raise ValueError('unknown or locally customized pack file')
            if before is None and rel == 'docs/codex/PROJECT_PROFILE.yaml':
                prof = source/'profiles'/profile/'PROJECT_PROFILE.yaml'
                if prof.exists(): desired = prof.read_bytes()
            next_hashes[rel] = digest(desired)
            if before != desired:
                operations.append({'path':rel,'before':digest(before),'after':digest(desired),'content':encode(desired), 'mode':(path.stat().st_mode & 0o777) if before is not None else (safe_path(source,src).stat().st_mode & 0o777)})
        except (ValueError, UnicodeError) as exc:
            conflicts.append({'path':rel,'reason':str(exc)})
    ignore = safe_path(target,'.gitignore');before=read(ignore)
    entry=b'.playwright/.auth/'
    if entry not in (before or b''):
        desired=(before or b'').rstrip()+b'\n# SR local authentication state\n'+entry+b'\n'
        operations.append({'path':'.gitignore','before':digest(before),'after':digest(desired),'content':encode(desired)})
    # Even files not changed by the plan are guarded against concurrent edits.
    guards = {rel:digest(read(safe_path(target,rel))) for rel in files.values()}
    guards['.gitignore']=digest(read(ignore));guards[STATE]=digest(read(state_path))
    data=(json.dumps({'schema_version':1,'hashes':next_hashes},sort_keys=True,indent=2)+'\n').encode()
    if read(state_path) != data:
        operations.append({'path':STATE,'before':digest(read(state_path)),'after':digest(data),'content':encode(data)})
    return {'schema_version':1,'target':str(target),'operations':operations,'guards':guards,'conflicts':conflicts,'preserved':preserved}

def restore(target, journal_path):
    target=target.resolve(); journal_path=journal_path.resolve()
    if not journal_path.is_relative_to(target/'docs/codex/upgrade_backups'):
        raise ValueError('journal must belong to target upgrade_backups')
    journal=json.loads(journal_path.read_text())
    if journal['target'] != str(target): raise ValueError('journal target mismatch')
    entries=journal['entries']
    # All checks before any restoration: no overwriting later user edits.
    for e in entries:
        current=read(safe_path(target,e['path']))
        if digest(current) not in (e['before_hash'],e['after']):
            raise ValueError(f"post-install edit preserved; cannot restore {e['path']}")
        current_path=safe_path(target,e['path'])
        if current is not None and 'after_mode' in e:
            allowed_modes={e['after_mode'], e.get('before_mode')}
            if journal.get('status') == 'applying' and e['before_hash'] is None: allowed_modes.add(0o644)
            if current_path.stat().st_mode & 0o777 not in allowed_modes:
                raise ValueError(f"post-install mode edit preserved: {e['path']}")
        if digest(decode(e['before_content'])) != e['before_hash']:
            raise ValueError('corrupted backup')
    for e in reversed(entries):
        p=safe_path(target,e['path']);data=decode(e['before_content'])
        if data is None:
            if p.exists():p.unlink()
        else:
            atomic_write(p,data)
            if e.get('before_mode') is not None: os.chmod(p,e['before_mode'])
    journal['status']='restored';atomic_write(journal_path,(json.dumps(journal,indent=2)+'\n').encode())

def apply_plan(plan, target):
    target=target.resolve()
    if plan.get('schema_version') != 1 or plan['target'] != str(target):raise ValueError('plan target/schema mismatch')
    if plan['conflicts']:raise ValueError('unresolved conflicts; no files written')
    for rel, expected in plan['guards'].items():
        if digest(read(safe_path(target,rel))) != expected:raise ValueError(f'plan stale: {rel}')
    for op in plan['operations']:
        safe_path(target,op['path'])
        if digest(read(safe_path(target,op['path']))) != op['before']:raise ValueError('stale operation')
        if digest(decode(op['content'])) != op['after']:raise ValueError('corrupted plan content')
    if not plan['operations']:return None
    journal_path=safe_path(target,'docs/codex/upgrade_backups/'+uuid.uuid4().hex+'/transaction.json')
    journal={'schema_version':1,'target':str(target),'status':'applying','entries':[]}
    atomic_write(journal_path,(json.dumps(journal,indent=2)+'\n').encode())
    try:
        for op in plan['operations']:
            p=safe_path(target,op['path']);before=read(p)
            if digest(before) != op['before']:raise ValueError(f"concurrent edit: {op['path']}")
            before_mode=(p.stat().st_mode & 0o777) if before is not None else None
            after_mode=before_mode if before_mode is not None else op.get('mode',0o644)
            journal['entries'].append({'path':op['path'],'before_content':encode(before),'before_hash':digest(before),'after':op['after'],'before_mode':before_mode,'after_mode':after_mode})
            atomic_write(journal_path,(json.dumps(journal,indent=2)+'\n').encode())
            atomic_write(p,decode(op['content']))
            os.chmod(p,after_mode)
        journal['status']='applied';atomic_write(journal_path,(json.dumps(journal,indent=2)+'\n').encode())
    except Exception:
        restore(target,journal_path)
        raise
    return journal_path
