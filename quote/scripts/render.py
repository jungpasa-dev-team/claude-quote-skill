#!/usr/bin/env python3
"""채운 견적서 HTML → A4 PDF. 크롬(또는 엣지·크로미움)의 headless 인쇄를 쓴다. 표준 라이브러리만 사용.

  python3 render.py quote.html quote.pdf
"""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

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


def main(src: str, out: str) -> None:
    src, out = os.path.abspath(src), os.path.abspath(out)
    body = re.sub(r'<!--.*?-->', '', open(src, encoding='utf-8').read(), flags=re.S)  # 주석 속 설명은 제외
    left = sorted(set(re.findall(r'\{\{[^}]+\}\}', body)))
    if left:
        sys.exit('아직 채우지 않은 토큰: ' + ', '.join(left))
    subprocess.run([find_browser(), '--headless=new', '--disable-gpu', '--no-pdf-header-footer',
                    f'--print-to-pdf={out}', Path(src).as_uri()],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if not os.path.exists(out) or os.path.getsize(out) == 0:
        sys.exit('PDF가 만들어지지 않았습니다.')
    print(out)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
