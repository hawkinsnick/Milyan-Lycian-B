"""Private-source glyph audit; requires the exact lawfully held PDF and optional PyMuPDF.
No source text is emitted by the public alignment command. Font remaps are edition-specific.
"""
import hashlib,json,unicodedata
from pathlib import Path
PDF_SHA256='1ef1d894e82f6ab5ea651d75f51ee69ab3517613c1a4463fe1b028d629a9e64f'
def decode(font,raw):
 if font=='SabonLinguistic-Italic':return {'r':'m̃','\\':'ẽ'}[raw],[]
 if font=='TimesTenGreekP-Inclined':
  if raw!='\x02':raise ValueError('unknown custom Greek glyph')
  return 'χ',[]
 if font=='KronosPunkt':
  if raw!='x':raise ValueError('unknown custom dotted glyph')
  return 'χ',['underdot']
 if font.startswith('SabonPunkt-'):return raw,['underdot']
 if font not in ['Sabon-Italic','Sabon-Roman','Sabon-Bold']:raise ValueError('unreviewed font')
 return raw,[]
def extract(pdf):
 if hashlib.sha256(Path(pdf).read_bytes()).hexdigest()!=PDF_SHA256:raise ValueError("wrong source PDF; no automatic replacement edition")
 import fitz
 doc=fitz.open(pdf);result=[];label=0
 for pi,lo,hi,xmin in [(26,537,645,148),(27,175,352,168)]:
  page=doc[pi];underlines=[fitz.Rect(item[1],item[2]) for d in page.get_drawings() for item in d['items'] if item[0]=='l' and abs(item[1].y-item[2].y)<.01 and lo<item[1].y<hi]
  for block in page.get_text('rawdict')['blocks']:
   if block['type']:continue
   for line in block['lines']:
    if not lo<line['bbox'][1]<hi:continue
    text=''.join(c['c'] for s in line['spans'] for c in s['chars'])
    if text.strip() in [str(n) for n in range(1,10)]:label=int(text.strip());continue
    glyphs=[]
    for span in line['spans']:
     for char in span['chars']:
      if char['bbox'][0]<xmin:continue
      raw=char['c'];font=span['font'];marks=[]
      value,marks=decode(font,raw)
      box=[round(v,4) for v in char['bbox']]
      if value==':' and any(abs(r.x0-box[0])<.3 and abs(r.x1-box[2])<.3 and box[1]<r.y0<box[3] for r in underlines):marks.append('underline')
      glyphs.append({'text':value,'marks':marks,'raw_glyph':raw,'font':font,'bbox':box})
    # Roman vacat/vac. are editorial descriptions, not inscription signs.
    rawtext=''.join(g['text'] for g in glyphs)
    vacpos=next((k for k in range(len(glyphs)) if ''.join(g['text'] for g in glyphs[k:]).strip() in ['vacat','vac.']),None)
    for k,g in enumerate(glyphs):
     g.update(source_label=label,pdf_ordinal=pi+1,printed_page=pi+95,physical_print_row=len(result)+1)
     g['role']='EDITORIAL_VACAT' if vacpos is not None and k>=vacpos else ('PRINT_WRAP_HYPHEN' if g['text']=='-' and k==len(glyphs)-1 else 'CONTENT')
    result.append(glyphs)
 # Merge the explicitly printed p/l alternative into one comparative position, preserving all three rendered glyphs.
 units=[]
 for lineglyphs in result:
  i=0
  while i<len(lineglyphs):
   g=lineglyphs[i];seq=''.join(x['text'] for x in lineglyphs[i:i+3])
   if seq=='p/l':
    children=lineglyphs[i:i+3];g=dict(g,text='p/l',alternatives=['p','l'],rendered_glyphs=children,marks=['explicit_alternative']);g['bbox']=[min(x['bbox'][0] for x in children),min(x['bbox'][1] for x in children),max(x['bbox'][2] for x in children),max(x['bbox'][3] for x in children)];i+=3
   else:i+=1
   units.append(g)
 for n,u in enumerate(units,1):u['id']=f'S2005-G{n:04}'
 return {'format':'tl55-private-checked-source-glyphs-v1','pdf_sha256':hashlib.sha256(Path(pdf).read_bytes()).hexdigest(),'source_layer':'Revised transcription121–122 only; not reconstruction132–133','method':'Font-specific decoding checked against rendered page crops; rendered glyph uncertainty and underline drawings retained. No global transliteration normalization.','glyph_units':units}
