"""Lecture d'un classeur .xlsx sans dépendance (zipfile + xml)."""
import re
import zipfile
import xml.etree.ElementTree as ET

NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}


def lire_xlsx(path):
    """{nom de feuille: [ {colonne: valeur} par ligne ]} (lignes vides ignorées)."""
    z = zipfile.ZipFile(path)
    ss = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            ss.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))}
    out = {}
    for sh in wb.find("m:sheets", NS):
        tgt = rels[sh.get("{%s}id" % NS["r"])].lstrip("/")
        tgt = tgt if tgt.startswith("xl/") else "xl/" + tgt
        rows = []
        for row in ET.fromstring(z.read(tgt)).findall(".//m:row", NS):
            vals = {}
            for c in row.findall("m:c", NS):
                col = re.match(r"[A-Z]+", c.get("r")).group(0)
                v, t = c.find("m:v", NS), c.get("t")
                if t == "s" and v is not None:
                    val = ss[int(v.text)]
                elif t == "inlineStr":
                    val = "".join(x.text or "" for x in c.iter("{%s}t" % NS["m"]))
                else:
                    val = v.text if v is not None else ""
                if val != "":
                    vals[col] = val
            if vals:
                rows.append(vals)
        out[sh.get("name")] = rows
    return out


def reperes(path):
    """{repère cible sans '-': {désignation, fab, carac, emplacement, folio}} depuis l'onglet Repères."""
    rows = lire_xlsx(path)["Repères"]
    out = {}
    for r in rows:
        rep = r.get("A", "")
        if not rep.startswith("-"):
            continue
        out[rep.lstrip("-")] = {"des": r.get("C", ""), "fab": r.get("D", ""), "carac": r.get("E", ""),
                                "loc": r.get("F", ""), "folio": r.get("G", ""), "actuel": r.get("B", "")}
    return out


def folios(path):
    rows = lire_xlsx(path)["Folios"]
    out = []
    for r in rows:
        n = r.get("A", "")
        if re.fullmatch(r"\d\d", n):
            out.append({"num": n, "titre": r.get("B", ""), "desc": r.get("E") or r.get("C", ""),
                        "loc": r.get("D", ""), "maitres": r.get("G", "")})
    return out
