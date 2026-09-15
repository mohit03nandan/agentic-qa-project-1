import sys
import markdown
from xhtml2pdf import pisa

src, dst = sys.argv[1], sys.argv[2]

with open(src, "r", encoding="utf-8") as f:
    md_text = f.read()

body_html = markdown.markdown(
    md_text, extensions=["extra", "sane_lists", "toc"]
)

html = f"""<html>
<head>
<meta charset="utf-8">
<style>
  @page {{ size: A4; margin: 2cm; }}
  body {{ font-family: Helvetica, Arial, sans-serif; font-size: 10.5pt; line-height: 1.45; color: #1a1a1a; }}
  h1 {{ font-size: 20pt; margin-top: 0; border-bottom: 2px solid #333; padding-bottom: 6px; }}
  h2 {{ font-size: 15pt; margin-top: 22px; border-bottom: 1px solid #999; padding-bottom: 4px; }}
  h3 {{ font-size: 12.5pt; margin-top: 14px; color: #222; }}
  code {{ background: #f2f2f2; padding: 1px 4px; border-radius: 3px; font-family: Courier, monospace; font-size: 9.5pt; }}
  pre {{ background: #f2f2f2; padding: 8px; border-radius: 4px; font-family: Courier, monospace; font-size: 9pt; }}
  hr {{ border: none; border-top: 1px solid #ccc; margin: 16px 0; }}
  table {{ border-collapse: collapse; width: 100%; margin: 8px 0; }}
  th, td {{ border: 1px solid #ccc; padding: 5px 8px; font-size: 9.5pt; }}
  th {{ background: #eee; }}
  a {{ color: #0645ad; }}
  strong {{ color: #000; }}
  blockquote {{ margin: 8px 0; padding-left: 10px; border-left: 3px solid #ccc; color: #444; }}
</style>
</head>
<body>
{body_html}
</body>
</html>"""

with open(dst, "w+b") as f:
    pisa.CreatePDF(html, dest=f)

print("done")
