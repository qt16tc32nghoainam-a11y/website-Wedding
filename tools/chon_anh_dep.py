# -*- coding: utf-8 -*-
"""
TU CHON ANH DEP TRONG BO SUU TAP (dung cho muc Danh gia khach hang)
=================================================================
Cham diem tung anh da xuat trong assets/img/bo-suu-tap:
  - anh doc (khung ben trai cua the danh gia la khung doc)
  - net (do sac canh o vung giua anh)
  - sang vua phai, du tuong phan
  - loai trang album / anh ghep nen trang (vien trang nhieu)
Ghi ket qua vao data/bo-suu-tap.json  ->  "anh_dep": {"cap_doi": [...], "co_dau": [...], "theo_album": {...}}
Chay: python tools/chon_anh_dep.py   (muc 1 cua CAP NHAT WEB.bat tu chay sau khi dung Bo suu tap)
"""
import io, json, math, os
import numpy as np
from PIL import Image, ImageFilter

TOOLS = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(TOOLS)
DATA = os.path.join(BASE, "data", "bo-suu-tap.json")

NHOM = {
    "cap_doi": {"ngoai-canh", "phim-truong", "studio"},     # anh cap doi cho the danh gia chung
    "co_dau": {"make-up"},                                  # danh gia nhac toi makeup / trang diem (anh co dau)
}


def diem(p, im=None, khat_khe=True):
    """Diem dep cua 1 anh (None = khong dung duoc)."""
    im = im or Image.open(p)
    w, h = im.size
    if h < w * 1.2:                                          # can anh doc
        return None
    nho = im.convert("RGB").resize((120, int(120 * h / w)))
    if np.asarray(nho.convert("HSV"), dtype=float)[:, :, 1].mean() < 14:
        return None                                          # anh den trang
    g = im.convert("L").resize((300, int(300 * h / w)))
    a = np.asarray(g, dtype=float)
    H, W = a.shape
    vien = np.concatenate([a[:, :12].ravel(), a[:, -12:].ravel(), a[:12, :].ravel(), a[-12:, :].ravel()])
    if khat_khe and (vien > 235).mean() > 0.55:              # vien trang -> trang album / anh ghep
        return None
    giua = g.crop((W // 6, H // 6, W * 5 // 6, H * 5 // 6))
    net = np.asarray(giua.filter(ImageFilter.FIND_EDGES), dtype=float).var()
    sang = a.mean()
    tuong_phan = a.std()
    phat_sang = max(0.0, abs(sang - 135) - 40) / 20.0      # qua toi / qua choi bi tru diem
    return math.log(net + 1) + tuong_phan / 40.0 - phat_sang


def nua_trang_dep(a):
    """Tach tung trang album doi (ngang) thanh 2 nua doc, lay nua dep nhat, luu vao assets/img/danh-gia/tu-dong."""
    tot = None
    for x in a.get("anh", []):
        p = os.path.join(BASE, x.lstrip("/"))
        if not os.path.isfile(p):
            continue
        im = Image.open(p).convert("RGB")
        w, h = im.size
        if w < h * 1.2:
            continue
        for trai in (True, False):
            n = im.crop((0, 0, w // 2, h) if trai else (w - w // 2, 0, w, h))
            n = n.crop((0, 0, n.width, min(n.height, int(n.width * 1.45))))
            s = diem(None, n, khat_khe=False)
            if s is not None and (tot is None or s > tot[0]):
                tot = (s, n)
    if not tot:
        return None
    import re, unicodedata
    ten = "".join(c for c in unicodedata.normalize("NFD", a["ten"].replace("Đ", "D").replace("đ", "d")) if unicodedata.category(c) != "Mn")
    ten = re.sub(r"[^a-z0-9]+", "-", ten.lower()).strip("-")
    thu_muc = os.path.join(BASE, "assets", "img", "danh-gia", "tu-dong")
    os.makedirs(thu_muc, exist_ok=True)
    tot[1].save(os.path.join(thu_muc, ten + ".jpg"), "JPEG", quality=85, optimize=True, progressive=True)
    return "/assets/img/danh-gia/tu-dong/%s.jpg" % ten


def chay(log=print):
    d = json.load(io.open(DATA, encoding="utf-8"))
    p_dg = os.path.join(BASE, "data", "danh-gia.json")
    can_anh_rieng = {x.get("album") for x in json.load(io.open(p_dg, encoding="utf-8")).get("danh_gia", [])} if os.path.exists(p_dg) else set()
    ket_qua = {"cap_doi": [], "co_dau": [], "theo_album": {}}
    ung_vien = {"cap_doi": [], "co_dau": []}
    for a in d.get("album", []):
        cham = []
        for x in a.get("anh", []):
            p = os.path.join(BASE, x.lstrip("/"))
            if os.path.isfile(p):
                s = diem(p)
                if s is not None:
                    cham.append((s, x))
        cham.sort(reverse=True)
        if cham:
            ket_qua["theo_album"][a["ten"]] = [x for _, x in cham[:3]]
        elif a.get("ten") in can_anh_rieng:
            nua = nua_trang_dep(a)                           # album toan trang doi ngang -> cat nua trang
            if nua:
                ket_qua["theo_album"][a["ten"]] = [nua]
        for k, dm in NHOM.items():
            if a.get("danh_muc") in dm:
                ung_vien[k] += cham[:2]                      # toi da 2 anh / album cho da dang
    for k in ung_vien:
        ket_qua[k] = [x for _, x in sorted(ung_vien[k], reverse=True)[:40]]
    d["anh_dep"] = ket_qua
    io.open(DATA, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
    log(u"   Chọn ảnh đẹp: %d ảnh cặp đôi, %d ảnh cô dâu, %d album có ảnh riêng."
        % (len(ket_qua["cap_doi"]), len(ket_qua["co_dau"]), len(ket_qua["theo_album"])))
    return ket_qua


if __name__ == "__main__":
    chay()
