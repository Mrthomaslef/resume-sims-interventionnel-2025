import json, os
P="/Users/thomaslefevre/.t3/projects/resume-de-la-sims-interventionnel-2025"
V="/Users/thomaslefevre/2nd brain/05 - Biblio, Zotero & Enseignement/SIMS RI 2025"
d=json.load(open(P+"/data/fiches.json")); S={s["id"]:s for s in d["sessions"]}
cal={"warning":"WARNING","tip":"TIP","important":"IMPORTANT"}
def fmt(t): t=int(t); return f"{t//60}:{t%60:02d}"
def clean(x): return x.replace("/", "-").replace(":", " -").replace("?","").replace("«","").replace("»","").replace('"',"").strip()[:90]
names={}
for f in d["fiches"]:
    s=S[f["session"]]; name=f"{f['horaire']} — {clean(f['titre'])}"; names[f["id"]]=name
    L=["---",f"tags: [sims, ri, congres, {', '.join(t.lower().replace(' ','-') for t in f.get('tags',[]))}]","domaine: Radiologie interventionnelle",
       "date: 2025-12-13","statut: résumé",f"orateur: \"{f['orateur']}\"","---","",f"# {f['titre']}","",
       f"**{f['orateur']}** · {s['titre']} · {f['horaire']} · ↩︎ [[00 - SIMS RI 2025 — Index]]","",f"> [!abstract] En bref\n> {f['resume']}",""]
    if f.get("chiffres"): L+=["| Chiffre | Signification |","|---|---|"]+[f"| **{c['val']}** | {c['label']} |" for c in f["chiffres"]]+[""]
    L+=["## Points clés"]+[f"- {x}" for x in f["points_cles"]]+[""]
    if f.get("technique"): L+=["## Technique / en pratique"]+[f"{i+1}. {x}" for i,x in enumerate(f["technique"])]+[""]
    for a in f.get("alertes",[]): L+=[f"> [!{cal.get(a['type'],'NOTE')}]\n> {a['texte']}",""]
    if f.get("cochin"): L+=[f"> [!TIP] Pour notre pratique (Radio B Cochin)\n> {f['cochin']}",""]
    L+=["## Illustrations"]+[f"![[{os.path.basename(im['src'])}]]\n*{im['legende']}*\n" for im in f["images"]]
    L+=[f"---\n🎬 Vidéo « {s['titre']} » ({s['duree']}) : {fmt(f['t_start'])} → {fmt(f['t_end'])} · Liens : [[Index RI Ostéo-Articulaire Cochin]]"]
    open(f"{V}/{name}.md","w").write("\n".join(L))
I=["---","tags: [sims, ri, congres, index]","domaine: Radiologie interventionnelle","date: 2025-12-13","statut: résumé","---","",
   "# SIMS — 4ᵉ journée « Actualités en imagerie interventionnelle » (13/12/2025)","",
   f"{len(d['fiches'])} fiches résumés illustrées, une par présentation. Version web : `/Users/thomaslefevre/.t3/projects/resume-de-la-sims-interventionnel-2025/index.html`.",""]
for s in d["sessions"]:
    I+=[f"## {s['titre']} ({s['horaire']})"]+[f"- [[{names[f['id']]}]] — {f['orateur']}" for f in d["fiches"] if f["session"]==s["id"]]+[""]
I+=["Voir aussi : [[Index RI Ostéo-Articulaire Cochin]] · [[Check-list Pré-Procédurale & Anticoagulants]] · [[Passerelle BiblioOstéo, Zotero & Quiz]]"]
open(f"{V}/00 - SIMS RI 2025 — Index.md","w").write("\n".join(I)); print(len(names),"notes")
