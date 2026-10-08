import sys, json, shutil, subprocess, os
sys.path.insert(0, os.path.dirname(__file__))
import pandas as pd
from engine import NM, C
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from docx import Document
from docx.shared import Pt
from pptx import Presentation
from pptx.util import Inches, Pt as PPt
T = '/tmp/claude-0/-home-user-iconic/118b864e-7445-5af4-819d-cfe4bc0666d5/scratchpad/task15'
RAW, OUT = f'{T}/raw', f'{T}/inputs'
CH = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'
fig = json.load(open(f'{T}/build/figures.json'))
draw = {int(k): v for k, v in fig['draw'].items()}; tp = {int(k): v for k, v in fig['tp'].items()}
proj25, h1 = fig['proj25'], fig['h1_26']
FIPS = {v: k for k, v in NM.items()}
fmt = lambda x: f'${x:,.0f}'
os.makedirs(OUT, exist_ok=True)

# 1-2. real QCEW files, stacked as published
pd.concat([pd.read_csv(f'{RAW}/a{c}_{y}.csv', dtype=str) for y in range(2018, 2026) for c in NM]).to_csv(f'{OUT}/qcew_aacog_counties_annual_2018_2025.csv', index=False)
pd.concat([pd.read_csv(f'{RAW}/q{c}_2026_1.csv', dtype=str) for c in NM]).to_csv(f'{OUT}/qcew_aacog_counties_2026_q1.csv', index=False)
# 3-6. real reference files
shutil.copy(f'{RAW}/industry_titles.csv' if os.path.exists(f'{RAW}/industry_titles.csv') else f'{T}/../task14/raw/industry_titles.csv', f'{OUT}/qcew_industry_titles.csv')
shutil.copy(f'{RAW}/layout_annual.pdf', f'{OUT}/QCEW_annual_file_layout.pdf')
shutil.copy(f'{RAW}/BLS_Handbook_of_Methods_QCEW.pdf', f'{OUT}/BLS_Handbook_of_Methods_QCEW.pdf')
shutil.copy(f'{T}/../task14/raw/conc_2017_2022.xlsx', f'{OUT}/2017_to_2022_NAICS.xlsx')
# 7. charter
subprocess.run([CH, '--headless=new', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={OUT}/compact_charter.pdf', f'file://{T}/src/compact_charter.html'], capture_output=True)

# 8. round ledger
DECIDED = {2020: '2020-11-19', 2021: '2021-11-18', 2022: '2022-11-17', 2023: '2023-11-16', 2024: '2024-11-21', 2025: '2025-11-20'}
wb = Workbook(); ws = wb.active; ws.title = 'Draws'
ws.append(['Alamo Region Manufacturing Compact: Breadth Fund round ledger']); ws['A1'].font = Font(bold=True, size=12)
ws.append(['Prepared by the Compact secretariat. Confirmed draws by round. Scenario document authored for this exercise; figures derived from published BLS QCEW county counts.'])
ws.append([])
hdr = ['Round', 'Confirmed by board', 'County', 'County FIPS', 'BLS counts year', 'Draw ($)', 'Change on previous round (%)', 'Notice given', 'Transition payment ($)']
ws.append(hdr)
for c in ws[4]: c.font = Font(bold=True); c.fill = PatternFill('solid', fgColor='DDE4EE')
for R in range(2020, 2026):
    for c in C:
        prev = draw.get(R - 1, {}).get(c) if R > 2020 else None
        chg = round((draw[R][c] - prev) / prev * 100, 1) if prev else None
        t = tp[R][c] if R > 2020 else 0
        ws.append([R, DECIDED[R], c, FIPS[c], R - 1, draw[R][c], chg, 'Yes' if t else 'No', t])
for col, w in zip('ABCDEFGHI', [8, 18, 12, 11, 15, 12, 26, 13, 22]): ws.column_dimensions[col].width = w
for row in ws.iter_rows(min_row=5):
    row[5].number_format = '#,##0'; row[8].number_format = '#,##0'
ws.freeze_panes = 'A5'
rs = wb.create_sheet('Rounds')
rs.append(['Round', 'Confirmed by board', 'Breadth Fund ($)', 'Total draws confirmed ($)', 'BLS counts year', 'Notices given', 'Transition payments ($)'])
for c in rs[1]: c.font = Font(bold=True)
for R in range(2020, 2026):
    rs.append([R, DECIDED[R], 5_000_000, sum(draw[R].values()), R - 1, sum(1 for v in tp.get(R, {}).values() if v) if R > 2020 else 0, sum(tp[R].values()) if R > 2020 else 0])
res = wb.create_sheet('Reserve')
res.append(['Round', 'Opening balance ($)', 'Top-up from contributions ($)', 'Transition payments ($)', 'Closing balance ($)'])
for c in res[1]: c.font = Font(bold=True)
bal = 300_000
for R in range(2020, 2026):
    pay = sum(tp[R].values()) if R > 2020 else 0
    top = 250_000 - bal if bal < 250_000 else 0
    res.append([R, bal, top, pay, bal + top - pay]); bal = bal + top - pay
for s in (rs, res):
    for col in 'ABCDEFG': s.column_dimensions[col].width = 24
wb.save(f'{OUT}/breadth_fund_ledger_2020_2025.xlsx')
open(f'{T}/build/reserve_close_2025.txt', 'w').write(str(bal))

# 9. June 2025 projection memo (the projection that missed)
rows = ''.join(f'<tr><td>{c}</td><td style="text-align:right">{fmt(draw[2024][c])}</td><td style="text-align:right">{fmt(proj25[c])}</td></tr>' for c in C)
html = f'''<!doctype html><html><head><meta charset="utf-8"><title>2025 round projection</title><style>
@page{{size:Letter;margin:0.9in}}body{{font-family:Arial,Helvetica,sans-serif;font-size:10.5pt;line-height:1.45;color:#1a1a1a}}
h1{{font-size:15pt;margin:0 0 4px}}.meta{{color:#555;font-size:9pt}}table{{border-collapse:collapse;margin-top:10px}}td,th{{border:1px solid #aaa;padding:3px 10px}}th{{background:#e8edf3}}
</style></head><body><h1>Breadth Fund: projected draws for the 2025 round</h1>
<p class="meta">Finance office memo to member counties &middot; 30 June 2025 &middot; planning only (charter Article 7)<br>Scenario document authored for this exercise.</p>
<p>BLS released the 2024 county establishment counts this month, so we can give members an early view of the 2025 round for their grant planning. Each county's projected draw is its 2024 draw moved in line with the change in its count of private manufacturing establishments between 2023 and 2024. The board confirms the actual draws in November.</p>
<table><tr><th>County</th><th>2024 draw (confirmed)</th><th>2025 draw (projected)</th></tr>{rows}</table>
<p style="margin-top:12px">Questions to the finance office. We will issue the 2026 round projection after BLS releases the 2025 county counts.</p></body></html>'''
open(f'{T}/src/projection_2025.html', 'w').write(html)
subprocess.run([CH, '--headless=new', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={OUT}/finance_projection_2025_round.pdf', f'file://{T}/src/projection_2025.html'], capture_output=True)

# 10. October 2026 revised projection deck (model v2)
prs = Presentation(); prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
def slide(title, bullets=None):
    s = prs.slides.add_slide(prs.slide_layouts[5]); s.shapes.title.text = title
    s.shapes.title.text_frame.paragraphs[0].font.size = PPt(30)
    if bullets:
        tb = s.shapes.add_textbox(Inches(0.7), Inches(1.6), Inches(12), Inches(5)).text_frame; tb.word_wrap = True
        for k, b in enumerate(bullets):
            p = tb.paragraphs[0] if k == 0 else tb.add_paragraph(); p.text = b; p.font.size = PPt(18); p.space_after = PPt(10)
    return s
def table(s, data, top=1.5, widths=None, size=12):
    t = s.shapes.add_table(len(data), len(data[0]), Inches(0.6), Inches(top), Inches(12.1), Inches(0.3 * len(data))).table
    for r, row in enumerate(data):
        for k, v in enumerate(row):
            cell = t.cell(r, k); cell.text = str(v)
            for p in cell.text_frame.paragraphs: p.font.size = PPt(size); p.font.bold = (r == 0)
s = slide('Breadth Fund: 2026 round projection (model v2)', ['Finance office briefing for the board, 2 October 2026', 'Planning only (charter Article 7). The board confirms the 2026 round on 19 November.', 'Scenario document authored for this exercise.'])
slide('What changed after the 2025 round', [
    'The June 2025 projection moved each county\'s last draw with its own establishment count. It missed Medina by 46.5% and McMullen by 28.0%.',
    'As the board asked in November 2025, we rebuilt the projection model and tested it against past rounds before using it.',
    'Model v2 rebuilds every county\'s draw from the BLS county establishment counts for the four-digit manufacturing industries, rather than moving last year\'s draw.',
    'Tested against the 2023, 2024 and 2025 rounds, model v2 reproduces every county\'s confirmed draw to the dollar.',
    'BLS released the 2025 county counts on 28 August 2026; the projection below uses them.'])
s = slide('Model v2 against confirmed draws')
bt = [['County', '2023 ledger', '2023 model v2', '2024 ledger', '2024 model v2', '2025 ledger', '2025 model v2', 'Difference']]
for c in C: bt.append([c] + sum([[fmt(draw[R][c]), fmt(draw[R][c])] for R in (2023, 2024, 2025)], []) + ['$0'])
table(s, bt, top=1.35, size=11)
s = slide('2026 round: projected draws')
pr = [['County', '2025 draw (confirmed)', '2026 draw (projected)', 'Change']]
for c in C: pr.append([c, fmt(draw[2025][c]), fmt(h1[c]), f'{(h1[c] - draw[2025][c]) / draw[2025][c] * 100:+.1f}%'])
pr.append(['Total', fmt(sum(draw[2025].values())), fmt(sum(h1.values())), ''])
table(s, pr, top=1.35, size=11)
dn = [c for c in C if fig['d_tp'][c]]
gz = dn[0]
slide('Notices and the transition reserve', [
    f'{gz} County\'s projected draw falls {abs((h1[gz] - draw[2025][gz]) / draw[2025][gz] * 100):.1f}% on the 2025 round, so a notice is due by 1 December (charter Article 4.1).',
    f'Transition payment to {gz} County from the reserve: {fmt(fig["d_tp"][gz])} (half of the fall, Article 4.2).',
    'No other county\'s projected draw falls by more than ten per cent.',
    'Largest projected rises: ' + ', '.join(f'{c} {(h1[c] - draw[2025][c]) / draw[2025][c] * 100:+.1f}%' for c in sorted(C, key=lambda c: -(h1[c] - draw[2025][c]) / draw[2025][c])[:3]) + '.'])
slide('Next steps', ['Board to note the projection on 19 November and confirm the 2026 round.', f'Secretariat to prepare the notice to {gz} County.', 'Finance office to hold the transition payment in the reserve for January.'])
prs.save(f'{OUT}/finance_projection_2026_round.pptx')

# 11. November 2025 board minutes
d = Document(); st = d.styles['Normal']; st.font.name = 'Calibri'; st.font.size = Pt(11)
d.add_heading('Alamo Region Manufacturing Compact: minutes of the board', level=1)
d.add_paragraph('Meeting of 20 November 2025, Bexar County Commissioners Court, San Antonio. Scenario document authored for this exercise.')
d.add_paragraph('Present: directors for all thirteen member counties; R. Villarreal (chair). In attendance: the secretariat; the finance officer.')
items = [
 ('1. Minutes', 'The minutes of the meeting of 18 September 2025 were approved.'),
 ('2. The 2025 round', 'The secretariat presented the 2025 round, worked from the BLS county establishment counts for 2024 published in September 2025. The secretariat confirmed that the round had been worked in the same way as every round since the first in 2020. The board confirmed the draws as set out in the round ledger. Total draws: ' + fmt(sum(draw[2025].values())) + '.'),
 ('3. Notices and transition payments', f'The draws of Medina County and Bandera County are more than ten per cent below their 2024 draws. Notices will be sent by 1 December. The board approved transition payments of {fmt(tp[2025]["Medina"])} to Medina County and {fmt(tp[2025]["Bandera"])} to Bandera County, to be paid with the draws in January.'),
 ('4. The June projection', f'The director for Medina County said the finance office\'s June projection had shown {fmt(proj25["Medina"])} for Medina and that the county court had approved retention grants against it; the confirmed draw is {fmt(draw[2025]["Medina"])}. The director asked the board for an explanation. The finance officer said the June projection had moved each county\'s 2024 draw in line with the change in its own count of manufacturing establishments and had not been compared with past rounds. The chair reminded members that projections are for planning only (Article 7). Action: the finance office to rebuild its projection model, test it against past rounds, and bring the 2026 round projection to the board before the November 2026 meeting.'),
 ('5. Reserve', 'The finance officer reported the transition reserve balance after this round\'s payments and confirmed that it will be topped up to the Article 4.4 level before the 2026 round if needed.'),
 ('6. Other business', 'The board noted the Kendall County site visit in October and the state grant confirmation for 2026. Next meeting: 19 February 2026.')]
for h, t in items:
    d.add_paragraph().add_run(h).bold = True; d.add_paragraph(t)
d.save(f'{OUT}/board_minutes_2025_11_20.docx')

# 12. member roster
pd.DataFrame({'county': C, 'county_fips': [FIPS[c] for c in C], 'state': 'TX', 'member_since': '2019-06-06',
              'director_appointed_by': [f'{c} County Commissioners Court' for c in C]}).to_csv(f'{OUT}/member_counties.csv', index=False)
print(sorted(os.listdir(OUT)))

# strip the template's en dash bullet from the slide master (no dashes anywhere in authored files)
import zipfile
p = f'{OUT}/finance_projection_2026_round.pptx'; tmp = p + '.tmp'
with zipfile.ZipFile(p) as zi, zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zo:
    for it in zi.infolist():
        data = zi.read(it.filename)
        if it.filename.endswith('.xml'): data = data.decode('utf8').replace('–', '•').replace('—', '•').encode('utf8')
        zo.writestr(it, data)
os.replace(tmp, p)
