import json, os, subprocess, re, unicodedata
slug=lambda x: re.sub(r"[^a-z0-9]+","-",unicodedata.normalize("NFD",x).encode("ascii","ignore").decode().lower()).strip("-")
B="/Volumes/GamingSSD/sims-interventionnel-2025"; P="/Users/thomaslefevre/.t3/projects/resume-de-la-sims-interventionnel-2025"
SESS={88:("Interventionnel MSK : transmettre l'information et les consignes","8h30–9h00"),89:("Échographie démo « Re-live 1 »","9h00–10h45"),
90:("Mini-battle : Lisfranc & LCA mucoïde","10h45–11h10"),91:("Battles géniculés","11h10–11h50"),92:("Échographie : muscles","11h50–12h30"),
93:("Interventionnel « Re-live 2 »","14h00–14h50"),94:("Mini-battle rayons X","14h50–16h10"),95:("Embolisations, RF, moelle osseuse : indications & résultats","17h00–17h45")}
os.makedirs(f"{P}/img",exist_ok=True); os.makedirs(f"{P}/data",exist_ok=True)
sessions=[]; fiches=[]; ids=set(); n=0
for c,(t,h) in SESS.items():
    dur=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"{B}/videos/{c}.mp4"]))
    sessions.append({"id":f"s{c}","titre":t,"horaire":h,"duree":f"{int(dur//60)} min"})
    d=json.load(open(f"{B}/out/{c}.json"))
    for f in sorted(d["fiches"],key=lambda f:f.get("t_start",0)):
        f["session"]=f"s{c}"; f["id"]=slug(f["id"])
        while f["id"] in ids: f["id"]+="-b"
        ids.add(f["id"]); imgs=[]
        for k,im in enumerate(f.get("images",[])):
            out=f"img/{f['id']}-{k+1}.jpg"
            vf="crop=1490:834:420:128,scale=1280:-2" if im.get("crop","slide")=="slide" else "scale=1280:-2"
            if not os.path.exists(f"{P}/{out}"):
                subprocess.run(["ffmpeg","-nostdin","-loglevel","error","-y","-ss",str(im["t"]),"-i",f"{B}/videos/{c}.mp4","-frames:v","1","-vf",vf,"-q:v","5",f"{P}/{out}"],check=True)
            imgs.append({"src":out,"legende":im.get("legende",""),"t":im["t"]}); n+=1
        f["images"]=imgs; fiches.append(f)
data={"sessions":sessions,"fiches":fiches}
json.dump(data,open(f"{P}/data/fiches.json","w"),ensure_ascii=False,indent=1)
open(f"{P}/data/embedded_data.js","w").write("window.SIMS_DATA = "+json.dumps(data,ensure_ascii=False)+";\n")
print(len(fiches),"fiches,",n,"images")
