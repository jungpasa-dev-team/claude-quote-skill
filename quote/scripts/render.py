#!/usr/bin/env python3
"""채운 견적서 HTML → A4 PDF. 크롬(또는 엣지·크로미움)의 headless 인쇄를 쓴다. 표준 라이브러리만 사용.

  python3 render.py quote.html quote.pdf

{{도장}} 을 비워두지 않고 그대로 두면 assets/seal.png(.jpg) 가 있을 때 대표자 옆에 직인을 찍는다.
도장 파일이 없으면 빈칸으로 둔다. 도장을 빼고 싶으면 HTML 에서 {{도장}} 을 빈 문자열로 채운다.
"""
import base64
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / 'assets'
SEAL_FILES = {'seal.png': 'image/png', 'seal.jpg': 'image/jpeg', 'seal.jpeg': 'image/jpeg'}

CANDIDATES = [
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
]


def find_browser() -> str:
    env = os.environ.get('CHROME')
    if env and os.path.exists(env):
        return env
    for p in CANDIDATES:
        if os.path.exists(p):
            return p
    for name in ('google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser', 'microsoft-edge'):
        p = shutil.which(name)
        if p:
            return p
    sys.exit('크롬/엣지를 찾지 못했습니다. 환경변수 CHROME 에 실행 파일 경로를 넣어 주세요.')


def seal_html() -> str:
    for name, mime in SEAL_FILES.items():
        f = ASSETS / name
        if f.is_file():
            data = base64.b64encode(f.read_bytes()).decode()
            return f'<span class="in">(인)<img class="seal" src="data:{mime};base64,{data}" alt=""></span>'
    return ''


def main(src: str, out: str) -> None:
    src, out = os.path.abspath(src), os.path.abspath(out)
    body = re.sub(r'<!--.*?-->', '', open(src, encoding='utf-8').read(), flags=re.S)  # 주석 속 설명은 제외
    body = body.replace('{{도장}}', seal_html())
    left = sorted(set(re.findall(r'\{\{[^}]+\}\}', body)))
    if left:
        sys.exit('아직 채우지 않은 토큰: ' + ', '.join(left))
    # 원본 HTML 은 그대로 두고, 같은 폴더에 임시 파일을 만들어 인쇄한다(상대경로 이미지가 깨지지 않게).
    fd, tmp = tempfile.mkstemp(suffix='.html', dir=os.path.dirname(src))
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(body)
        subprocess.run([find_browser(), '--headless=new', '--disable-gpu', '--no-pdf-header-footer',
                        f'--print-to-pdf={out}', Path(tmp).as_uri()],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    finally:
        os.remove(tmp)
    if not os.path.exists(out) or os.path.getsize(out) == 0:
        sys.exit('PDF가 만들어지지 않았습니다.')
    print(out)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
