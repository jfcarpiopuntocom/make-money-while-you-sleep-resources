"""Render owned educational material locally. No provider or publishing calls."""
import argparse, hashlib, hmac, json, os, re, shutil, subprocess, tempfile
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'outputs'
ASSETS = ROOT / 'assets'

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def validate(job):
    if job.get('approved') is not True:
        raise ValueError('Approve the exact script and scenes first')
    if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,63}', job.get('job_id', '')):
        raise ValueError('Invalid job_id')
    text = job.get('script_text')
    if not isinstance(text, str) or not text.strip() or len(text) > 12000:
        raise ValueError('Invalid script_text')
    if hashlib.sha256(text.encode('utf8')).hexdigest() != job.get('script_sha256'):
        raise ValueError('Approved script hash does not match script_text')
    scenes = job.get('scenes')
    if not isinstance(scenes, list) or not 1 <= len(scenes) <= 6:
        raise ValueError('Expected 1–6 scenes')
    for s in scenes:
        if not isinstance(s, dict): raise ValueError('Invalid scene')
        for key, limit in [('title', 60), ('body', 180)]:
            if not isinstance(s.get(key), str) or not s[key].strip() or len(s[key]) > limit:
                raise ValueError('Scene text exceeds the readable card limits')
    seconds = job.get('seconds_per_scene', 4)
    if type(seconds) not in (int, float) or not 2 <= seconds <= 10:
        raise ValueError('Use 2–10 seconds per scene')
    if not isinstance(job.get('title', ''), str) or len(job.get('title', '')) > 70:
        raise ValueError('Invalid title')
    audio = None
    if job.get('narration_file'):
        audio = (ASSETS / job['narration_file']).resolve()
        if not audio.is_relative_to(ASSETS.resolve()) or not audio.is_file():
            raise ValueError('Narration must be a file inside assets')
    return audio

def font(size, bold=False):
    custom = os.environ.get('STUDIO_FONT_BOLD' if bold else 'STUDIO_FONT')
    candidates = [custom] if custom else []
    candidates += [r'C:\Windows\Fonts\arialbd.ttf' if bold else r'C:\Windows\Fonts\arial.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
    for p in candidates:
        if p and Path(p).is_file(): return ImageFont.truetype(p, size)
    raise RuntimeError('Set STUDIO_FONT and STUDIO_FONT_BOLD to readable local TTF fonts')

def wrap(draw, text, face, width):
    lines, line = [], ''
    for word in text.split():
        if draw.textlength(word, font=face) > width: raise ValueError('A word is too wide for the card; rewrite it')
        candidate = f'{line} {word}'.strip()
        if draw.textlength(candidate, font=face) <= width: line = candidate
        else: lines.append(line); line = word
    if line: lines.append(line)
    return lines

def card(scene, index, total, output):
    image = Image.new('RGB', (720, 1280), '#ffffff')
    d = ImageDraw.Draw(image)
    d.rectangle((54, 70, 666, 80), fill='#ed4b16')
    d.text((54, 115), f'{index:02d} / {total:02d}', font=font(26, True), fill='#07172d')
    y = 260
    for line in wrap(d, scene['title'], font(64, True), 610):
        d.text((54, y), line, font=font(64, True), fill='#07172d'); y += 78
    y += 70
    for line in wrap(d, scene['body'], font(42), 610):
        if y > 1080: raise ValueError('Text does not fit; shorten the scene')
        d.text((54, y), line, font=font(42), fill='#07172d'); y += 58
    image.save(output)

def run(command):
    try:
        return subprocess.run(command, check=True, capture_output=True, text=True, timeout=90)
    except subprocess.CalledProcessError as e:
        raise RuntimeError('Media command failed: ' + e.stderr[-1200:]) from e

def render(job):
    audio = validate(job)
    ffmpeg, ffprobe = shutil.which('ffmpeg'), shutil.which('ffprobe')
    if not ffmpeg or not ffprobe: raise RuntimeError('FFmpeg and ffprobe must be available on PATH')
    OUTPUT.mkdir(exist_ok=True)
    target = OUTPUT / job['job_id']
    canonical = json.dumps(job, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode('utf8')
    job_hash = hashlib.sha256(canonical).hexdigest()
    if target.exists():
        old = json.loads((target / 'manifest.json').read_text('utf8'))
        if old['job_sha256'] != job_hash: raise ValueError('Job ID already belongs to different content; choose another ID')
        for filename, expected in old['files'].items():
            if digest(target / filename) != expected: raise ValueError('Saved output changed; do not return it as verified')
        return old
    temporary = Path(tempfile.mkdtemp(prefix=job['job_id']+'-', dir=OUTPUT))
    try:
        inputs = []
        seconds = job.get('seconds_per_scene', 4)
        for i, scene in enumerate(job['scenes']):
            p = temporary / f'card-{i+1:02d}.png'
            card(scene, i+1, len(job['scenes']), p)
            inputs.extend(['-loop', '1', '-t', str(seconds), '-i', str(p)])
        n = len(job['scenes']); duration = seconds*n
        command = [ffmpeg, '-hide_banner', '-loglevel', 'error', '-y', *inputs]
        if audio: command += ['-i', str(audio)]
        chain = ''.join(f'[{i}:v]' for i in range(n)) + f'concat=n={n}:v=1:a=0,format=yuv420p[v]'
        command += ['-filter_complex', chain, '-map', '[v]']
        if audio: command += ['-map', f'{n}:a', '-af', 'apad', '-c:a', 'aac']
        command += ['-t', str(duration), '-r', '25', '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', '22', '-movflags', '+faststart', str(temporary / 'video.mp4')]
        run(command)
        probe = json.loads(run([ffprobe, '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(temporary/'video.mp4')]).stdout)
        video = next(s for s in probe['streams'] if s['codec_type'] == 'video')
        if video['width'] != 720 or video['height'] != 1280 or abs(float(probe['format']['duration'])-duration) > .3:
            raise RuntimeError('Rendered video has unexpected dimensions or duration')
        (temporary/'script.txt').write_text(job['script_text'],encoding='utf8')
        # Scene timing is a draft accessibility aid, not word-aligned narration.
        def stamp(value):
            ms=round(value*1000); return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
        srt='\n\n'.join(f'{i+1}\n{stamp(i*seconds)} --> {stamp((i+1)*seconds)}\n{s["body"]}' for i,s in enumerate(job['scenes']))+'\n'
        (temporary/'captions-draft.srt').write_text(srt,encoding='utf8')
        files={p.name:digest(p) for p in temporary.iterdir() if p.is_file()}
        manifest={'job_id':job['job_id'],'job_sha256':job_hash,'status':'READY_FOR_REVIEW','approved':False,'video_sha256':files['video.mp4'],'output_dir':str(target),'width':720,'height':1280,'duration_seconds':duration,'has_narration':audio is not None,'captions':'scene-timed draft; review before use','files':files}
        (temporary/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
        temporary.rename(target)
        return manifest
    except Exception as e:
        (temporary/'failure.txt').write_text(str(e),encoding='utf8')
        raise

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args): pass
    def do_POST(self):
        token = os.environ.get('READER_STUDIO_TOKEN', '')
        if not token or not hmac.compare_digest(self.headers.get('Authorization',''), 'Bearer '+token):
            self.send_error(401); return
        if self.path != '/render': self.send_error(404); return
        try:
            length = int(self.headers.get('Content-Length','0'))
            if not 0 < length <= 50000: self.send_error(413); return
            result = render(json.loads(self.rfile.read(length)))
            data = json.dumps(result).encode('utf8')
            self.send_response(200); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data)
        except (ValueError,TypeError,KeyError) as e:
            self.send_error(400, str(e))
        except Exception:
            self.send_error(500,'Local render failed; inspect the local outputs folder')

if __name__ == '__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--job', type=Path); parser.add_argument('--serve', action='store_true'); args=parser.parse_args()
    if args.serve:
        if len(os.environ.get('READER_STUDIO_TOKEN','')) < 24: raise SystemExit('Set a random READER_STUDIO_TOKEN of at least 24 characters')
        server=HTTPServer(('127.0.0.1',8765),Handler); server.timeout=30
        print('Local media studio listening on 127.0.0.1:8765; no public tunnel.'); server.serve_forever()
    elif args.job:
        print(json.dumps(render(json.loads(args.job.read_text('utf8'))),indent=2))
    else: parser.error('Choose --job FILE or --serve')
