# 견적서 만들기 스킬 (Claude Code)

고객 요구사항 메모만 주면 **우리 회사 양식의 견적서 PDF**를 만들어 주는 [Claude Code](https://claude.com/claude-code) 스킬입니다.

```
> ○○사 홈페이지 리뉴얼 견적서 만들어줘. 메인 1장, 서브 8장, 게시판 필요. 재계약이라 80만 원 할인.
```

![예시 견적서](examples/sample-quote.png)

## 이 스킬의 원칙

- **단가를 지어내지 않습니다.** 모든 단가는 `prices.csv`(단가표)에서만 가져오고, 단가표에 없는 품목은 금액을 비운 채 **"확인 필요"** 로 표시합니다.
- **회사 정보는 한 곳에서만.** 상호·주소·사업자번호는 `company.md` 에만 적습니다. 여기저기 적어두면 한쪽만 고쳐져서 틀린 견적서가 나갑니다.
- **할인은 단가를 깎지 않고 별도 행으로.** 할인율과 사유를 함께 적습니다.
- **도장은 기본으로 넣지 않습니다.** 그림으로 그린 도장은 가짜 티가 납니다. 필요하면 실제 도장을 스캔한 이미지를 넣으세요.
- 만들어진 견적서는 **초안**입니다. 보내기 전에 사람이 확인해 주세요.

## 설치

필요한 것: Claude Code, Python 3, 크롬 또는 엣지(PDF 변환용)

```bash
git clone https://github.com/jungpasa-dev-team/claude-quote-skill.git
mkdir -p ~/.claude/skills
cp -r claude-quote-skill/quote ~/.claude/skills/quote
```

Windows는 `quote` 폴더를 `%USERPROFILE%\.claude\skills\quote` 로 복사하면 됩니다.

## 우리 회사에 맞게 고치기 (처음 한 번)

1. **`company.md`** — 회사명·대표자·사업자번호·주소·연락처를 적습니다. 예전 회사명이나 예전 주소가 있으면 "옛 표기"에 적어두세요. 견적서를 뽑은 뒤 그 말이 남아 있는지 검사합니다.
2. **`prices.csv`** — 우리 회사 품목과 단가로 바꿉니다. 엑셀에서 열어 고치고 CSV(UTF-8)로 저장하면 됩니다.
3. (선택) **`assets/quote-template.html`** — 색·글꼴·표 모양을 바꾸고 싶으면 이 파일을 고칩니다. 기존에 쓰던 견적서 PDF를 Claude Code에 보여주고 "이 모양대로 양식을 바꿔줘"라고 해도 됩니다.

## 쓰는 법

Claude Code에서 평소처럼 말하면 됩니다.

```
> ○○사 견적서 만들어줘. (통화 메모나 고객 메일을 그대로 붙여도 됩니다)
> 부가세 포함 550만 원에 맞춰서 견적서 다시 만들어줘
> /quote ○○사 유지보수 월 견적
```

PDF만 따로 만들 때:

```bash
python3 ~/.claude/skills/quote/scripts/render.py 채운견적서.html 견적서.pdf
```

## 폴더 구성

```
quote/
├── SKILL.md                     # Claude Code가 읽는 작업 규칙
├── company.md                   # 회사 고정 정보 (직접 수정)
├── prices.csv                   # 단가표 (직접 수정)
├── assets/quote-template.html   # A4 견적서 양식
└── scripts/render.py            # HTML → PDF (표준 라이브러리만 사용)
examples/                        # 예시 견적서(가상의 회사·금액)
```

## 라이선스

MIT. 자유롭게 고쳐서 쓰세요. 예시의 회사·금액은 모두 가상입니다.
