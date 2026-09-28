# -*- coding: utf-8 -*-
"""
DUNG TRANG BO SUU TAP TU THU MUC ANH TRONG BT3
================================================
Moi danh muc lay anh tu 1 thu muc trong BT3 (xem DANHMUC ben duoi). Ho tro 3 cap:
    <THU MUC DANH MUC>/<TEN CONCEPT hoac TEN CAP DAU RE>/          -> 1 album
    <THU MUC DANH MUC>/<TEN CONCEPT>/<01, 02, 03...>/              -> moi thu muc con la 1 album

- Ten album = ten thu muc (tu viet hoa chu dau). Muon ten dep hon -> them vao TEN_DEP.
- Anh trung nhau (ke ca khac ten file) tu dong bi loai.
- Anh khong duoc dang (logo co so khac...) -> them ten file vao LOAI_TRU_TEN.
- Doc duoc JPG va PNG.

Chay qua cong cu:  CAP NHAT WEB.bat  ->  muc 1
"""
from PIL import Image, ImageOps
import glob, hashlib, html as html_mod, io, json, os, re, shutil, unicodedata
import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # thu muc BT3
OUT = os.path.join(BASE, "assets", "img", "bo-suu-tap")
THUMB_W, FULL_W, FULL_W_NGANG, Q = 440, 1000, 1400, 80

# ---------------------------------------------------------------------------
# DANH MUC: (ma, ten hien thi, thu muc anh trong BT3, nhan o trong khi chua co anh)
# Thu muc chua ton tai / chua co anh -> hien o "Album se duoc cap nhat".
# Nhieu ten thu muc cho cung 1 danh muc: viet cach nhau bang dau |
# ---------------------------------------------------------------------------
DANHMUC = [
    ("ngoai-canh",  u"Ngoại cảnh",          u"HÌNH NGOẠI CẢNH",                      []),
    ("phim-truong", u"Phim trường",         u"PHIM TRƯỜNG ĐỘC QUYỀN STUDIO QUỐC AN", []),
    ("studio",      u"Studio",              u"HÌNH STUDIO",                          []),
    ("beauty",      u"Concept Beauty",      u"CONCEPT BEAUTY",                       []),
    ("make-up",     u"Make-up cô dâu",      u"layour makeup",                        []),
    ("phong-su",    u"Phóng sự cưới",       u"Hình PSC",                             []),
    ("dam-hoi",     u"Đám hỏi",             u"HÌNH ĐÁM HỎI",                         []),
    ("mam-qua",     u"Mâm quả cưới hỏi",    u"MÂM QUẢ",          [u"Mâm dạm ngõ", u"Mâm cưới hỏi"]),
    ("gia-dinh",    u"Gia đình &amp; Baby", u"BABY & GIA ĐÌNH|GIA ĐÌNH & BABY",      []),
    ("hau-truong",  u"Hậu trường",          u"hậu trường",                           []),
]

# Ten dep cho album (khoa = ten thu muc viet thuong, bo dau). Dau & phai viet &amp;
TEN_DEP = {
    u"bien": u"Biển",
    u"nha tho song vinh": u"Nhà thờ Song Vĩnh",
    u"concept back reu": u"Back rêu",
    u"concept cau thang": u"Cầu thang",
    u"goc ban tiec": u"Góc bàn tiệc",
    u"cua co dien": u"Cửa cổ điển",
    u"dai phun nuoc": u"Đài phun nước",
    u"concept ban tiec studio": u"Bàn tiệc",
    u"concept couple": u"Couple",
    u"concept trai tim do": u"Trái tim đỏ",
    u"concept phong trang khom hoa": u"Phông trắng khóm hoa",
    u"concept phong den": u"Phông đen",
    u"concept tuong nham": u"Tường nhám",
    u"phong xam": u"Phông xám",
    u"phim truong an garden": u"Phim trường An Garden",
    u"concept studio": u"Rèm trắng &amp; hoa tím",
    u"ngoc quang & kieu phuc": u"Ngọc Quang &amp; Kiều Phúc",
    u"kim cong & uyen vi": u"Kim Công &amp; Uyên Vi",
    u"dam ngo": u"Mâm dạm ngõ",
    u"hien dai": u"Mâm quả hiện đại",
    u"truyen thong": u"Mâm quả truyền thống",
    u"set ban tiec phong vo cuc": u"Bàn tiệc phông vô cực",
    u"set khom hoa nau": u"Khóm hoa nâu",
    u"set vai do khom hoa": u"Vải đỏ &amp; khóm hoa",
    u"layour dau don": u"Dâu đơn",
    # --- them 11/09/2026 ---
    u"phom truong sachi garden": u"Phim trường Sachi Garden",
    u"swanbay": u"Swan Bay",
    u"san gold": u"Sân golf",
    u"ban tiec 01": u"Bàn tiệc 01",
    u"ban tiec cong 01": u"Bàn tiệc cong 01",
    u"ban tiec cong 02": u"Bàn tiệc cong 02",
    u"ban tiec reu xanh": u"Bàn tiệc rêu xanh",
    u"phong do": u"Phông đỏ",
    u"phong do 01": u"Phông đỏ 02",            # thu muc "PHONG ĐỎ 01" rieng (khac "PHONG ĐỎ\01")
    u"phong do tron": u"Phông đỏ trơn",
    u"phong xam 01": u"Phông xám 02",          # thu muc "PHONG XÁM 01" rieng (khac "PHONG XÁM\01")
    u"phong trang co xanh": u"Phông trắng cỏ xanh",
    u"beauty ghe den": u"Beauty ghế đen",
    u"concept sinh nhat 01": u"Sinh nhật 01",
    u"concept sinh nhat 02": u"Sinh nhật 02",
    u"dau gia tien": u"Dâu gia tiên",
    u"dau gia tien 01": u"Dâu gia tiên 01",
    u"noel": u"Noel",
    u"tet chuyen tu 01": u"Tết Chuyên Tu 01",
    u"vien chuyen tu 03": u"Viện Chuyên Tu 03",
    u"vien chuyen tu 04": u"Viện Chuyên Tu 04",
    u"yem vien chuyen tu 01": u"Yếm Viện Chuyên Tu 01",
    u"yem vien chuyen tu 02": u"Yếm Viện Chuyên Tu 02",
    u"ao dai vien chuyen tu 01": u"Áo dài Viện Chuyên Tu 01",
    u"dau xinh": u"Dâu xinh",
    u"sachi garden": u"Sachi Garden",
    u"set hoa ban tiec": u"Set hoa bàn tiệc",
    u"psc kieu diem": u"Kiều Diễm",
    u"bau 01": u"Bầu 01",
    u"gia dinh 01": u"Gia đình 01",
}

# Ten cap: web hien CHU RE truoc, CO DAU sau. Thu muc nao dang ghi co dau truoc -> them vao day
# de dao lai (khoa = ten thu muc viet thuong, bo dau). Thu muc moi nen dat san: CHU RE & CO DAU.
DAO_TEN = {
    u"thuy tien & duc anh", u"thuy kieu & thanh loi", u"thuy duong & tan thien",
    u"huynh mai & dang thanh", u"my hang & ngoc vinh", u"nguyen hoa & sy anh",
    u"ngoc tran & quang nghia", u"thao nguyen & manh linh",
    u"huynh nhu & ngoc tuan", u"minh trang & quang huy",
}

# Danh muc chi loai anh GIONG HET (trang album dan san de bi nham la trung)
DO_TRUNG_CHAT = {"phong-su"}

# Thu tu album trong moi danh muc theo ngay chup: "cu-truoc" (cu -> moi) hoac "moi-truoc"
THU_TU = "cu-truoc"

# Anh KHONG dang len web
LOAI_TRU = {u"HÌNH NGOẠI CẢNH/NHÀ THỜ SONG VĨNH/dp1.jpg"}              # chu FOXY STUSIO
LOAI_TRU_TEN = {
    "1789100777344_5412664383963298655_5412664383963298655_d3351f266eaf62a126548702277973a0.jpg",  # logo TAM PHUONG WEDDING
}

ICON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3">'
        '<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="10" r="1.6"/>'
        '<path d="m4 17 5-5 4 4 3-2 4 3"/></svg>')


def kd(s):
    """Bo dau tieng Viet (so sanh ten thu muc khong phu thuoc NFC/NFD)."""
    s = s.replace(u"đ", "d").replace(u"Đ", "D")
    return u"".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def slugify(s):
    return re.sub(r"^(concept|goc|set)-", "", re.sub(r"[^A-Za-z0-9]+", "-", kd(s)).strip("-").lower())


def dep(name):
    name = unicodedata.normalize("NFC", name)
    khoa = re.sub(r"\s+", " ", kd(name).lower().strip())
    if khoa in TEN_DEP:
        return TEN_DEP[khoa]
    if khoa in DAO_TEN and "&" in name:
        a, b = name.split("&", 1)
        name = b.strip() + " & " + a.strip()
    return name.title().replace("&", "&amp;")


def stt(f):
    # sap theo tung cum so (IMG_2 < IMG_10) de giu dung thu tu trang album
    b = os.path.basename(f)
    return ([int(x) for x in re.findall(r"\d+", b)], b)


def anh(d):
    seen, out = set(), []
    for f in sum((glob.glob(os.path.join(d, e)) for e in ("*.jpg", "*.JPG", "*.jpeg", "*.JPEG", "*.png", "*.PNG")), []):
        k = os.path.normcase(os.path.abspath(f))
        if k in seen:
            continue
        seen.add(k)
        rel = unicodedata.normalize("NFC", os.path.relpath(f, BASE).replace("\\", "/"))
        if rel in {unicodedata.normalize("NFC", x) for x in LOAI_TRU}:
            continue
        if os.path.basename(f) in LOAI_TRU_TEN:
            continue
        out.append(f)
    return sorted(out, key=stt)


def thumuc_con(d):
    return sorted([x for x in glob.glob(os.path.join(d, "*")) if os.path.isdir(x)])


def tim_thumuc(ten):
    """Cac thu muc trong BT3 khop ten (bo dau, khong phan biet NFC/NFD). Nhieu ten: 'A|B'."""
    muon = [kd(t).lower().strip() for t in ten.split("|")]
    return [os.path.join(BASE, x) for x in sorted(os.listdir(BASE))
            if os.path.isdir(os.path.join(BASE, x)) and kd(x).lower().strip() in muon]


def ngay_anh(f):
    """Ngay chup trong anh (EXIF); anh khong co (vd tai tu Facebook) -> ngay cua file."""
    try:
        ex = Image.open(f)._getexif() or {}
        d = ex.get(36867) or ex.get(36868) or ex.get(306)
        if d and re.match(r"\d{4}:\d\d:\d\d \d\d:\d\d", d) and not d.startswith("0000"):
            return d[:4] + "-" + d[5:7] + "-" + d[8:10] + "T" + d[11:16]
    except Exception:
        pass
    import time
    return time.strftime("%Y-%m-%dT%H:%M", time.localtime(os.path.getmtime(f)))


def bam(f):
    im = Image.open(f)
    im.draft("L", (256, 256))
    im = ImageOps.exif_transpose(im).convert("L")
    a = np.asarray(im.resize((9, 8), Image.LANCZOS), dtype=int)
    b = np.asarray(im.resize((8, 8), Image.LANCZOS), dtype=int)
    return (a[:, 1:] > a[:, :-1]).flatten(), (b > b.mean()).flatten()


def crop34(im):
    W, H = im.size
    if W / float(H) > 0.75:
        nw = int(H * 0.75); x = (W - nw) // 2
        return im.crop((x, 0, x + nw, H))
    return im.crop((0, 0, W, min(H, int(W / 0.75))))


def luu(im, path):
    im.save(path, "JPEG", quality=Q, optimize=True, progressive=True)
    return hashlib.md5(open(path, "rb").read()).hexdigest()[:8]


def xuly(src, ten):
    """Tao anh lon (+ anh bia neu la anh dau album). Tra ve ma kiem tra noi dung de chong cache."""
    im = Image.open(src)
    im.draft("RGB", (FULL_W_NGANG * 2, FULL_W_NGANG * 2))
    im = ImageOps.exif_transpose(im)
    if im.mode in ("RGBA", "LA", "P"):                     # PNG trong suot -> lot nen trang
        im = im.convert("RGBA"); nen = Image.new("RGB", im.size, "white")
        nen.paste(im, mask=im.getchannel("A")); im = nen
    im = im.convert("RGB")
    W, H = im.size
    fw = FULL_W_NGANG if W > H else FULL_W                  # anh ngang (trang album doi) xuat to hon
    v_full = luu(im.resize((fw, int(fw * H / W)), Image.LANCZOS), os.path.join(OUT, ten + ".jpg"))
    v_thumb = luu(crop34(im).resize((THUMB_W, int(THUMB_W / 0.75)), Image.LANCZOS),
                  os.path.join(OUT, ten + "-thumb.jpg"))
    return v_full, v_thumb


def ten_album_hien_tai():
    """Danh sach ten album dang co trong data/bo-suu-tap.json (de so sanh truoc/sau)."""
    p = os.path.join(BASE, "data", "bo-suu-tap.json")
    if not os.path.exists(p):
        return []
    d = json.load(io.open(p, encoding="utf-8"))
    ten_dm = {x["ma"]: x["ten"] for x in d.get("danh_muc", [])}
    return [unicodedata.normalize("NFC", a["ten"] + " | " + ten_dm.get(a["danh_muc"], a["danh_muc"])) for a in d.get("album", [])]


def dung(log=print, bao_cao_trung=None):
    """Quet thu muc anh trong BT3 -> tao lai anh trong assets/img/bo-suu-tap -> ghi data/bo-suu-tap.json."""
    # ---------- 1) Gom album ----------
    cau_truc = []
    for cat, ten_cat, thumuc, trong in DANHMUC:
        albums = []
        for goc in (tim_thumuc(thumuc) if thumuc else []):
            for c1 in thumuc_con(goc):
                b1 = os.path.basename(c1)
                fs1 = anh(c1)
                if fs1:                                    # anh nam ngay trong concept
                    ten = u"%s %s" % (ten_cat, b1) if re.fullmatch(r"\d+", b1) else dep(b1)
                    albums.append((slugify(b1), ten, fs1))
                for c2 in thumuc_con(c1):                  # tach theo tung cap
                    b2 = os.path.basename(c2)
                    fs2 = anh(c2)
                    if not fs2:
                        continue
                    ten = u"%s %s" % (dep(b1), b2) if re.fullmatch(r"\d+", b2) else dep(b2)
                    albums.append((slugify(b1) + "-" + slugify(b2), ten, fs2))
            if not albums and anh(goc):
                albums.append((u"", ten_cat, anh(goc)))
        cau_truc.append((cat, ten_cat, albums, trong))

    # ---------- 2) Do anh trung ----------
    tat_ca = [f for _, _, albums, _ in cau_truc for _, _, fs in albums for f in fs]
    # Phong su = trang album ghep nhieu anh tren nen trang, bo cuc giong nhau -> chi loai anh giong het
    trang_album = {f for c, _, albums, _ in cau_truc if c in DO_TRUNG_CHAT for _, _, fs in albums for f in fs}
    log(u"   Dò ảnh trùng trên %d ảnh nguồn..." % len(tat_ca))
    hs = [bam(f) for f in tat_ca]
    bo = set()
    for i in range(len(tat_ca)):
        if tat_ca[i] in bo:
            continue
        for j in range(i + 1, len(tat_ca)):
            if tat_ca[j] in bo:
                continue
            nguong = 0 if (tat_ca[i] in trang_album or tat_ca[j] in trang_album) else 6
            if int((hs[i][0] != hs[j][0]).sum()) <= nguong and int((hs[i][1] != hs[j][1]).sum()) <= nguong:
                bo.add(tat_ca[j])
    if bao_cao_trung:
        io.open(bao_cao_trung, "w", encoding="utf-8").write(
            u"\n".join(sorted(unicodedata.normalize("NFC", os.path.relpath(f, BASE).replace("\\", "/")) for f in bo)))

    # ---------- 3) Tao anh + ghi data/bo-suu-tap.json ----------
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    moi, tong_anh, chi_tiet, da_dung = [], 0, [], set()
    for cat, ten_cat, albums, trong in cau_truc:
        for sl, ten_ab, fs in albums:
            fs = [f for f in fs if f not in bo]
            if not fs:
                continue
            slug = goc_slug = ("%s-%s" % (cat, sl)) if sl else cat
            n = 2
            while slug in da_dung:                     # 2 thu muc ra cung ten file -> them so
                slug = "%s-%d" % (goc_slug, n); n += 1
            da_dung.add(slug)
            ds = []
            for i, f in enumerate(fs, 1):
                t = "%s-%02d" % (slug, i)
                xuly(f, t)
                ds.append("/assets/img/bo-suu-tap/%s.jpg" % t)
                tong_anh += 1
                if i > 1:                                  # chi giu anh bia (-thumb) cua anh dau
                    p = os.path.join(OUT, t + "-thumb.jpg")
                    if os.path.exists(p):
                        os.remove(p)
            ten = html_mod.unescape(ten_ab)
            moi.append({"danh_muc": cat, "ten": ten, "ngay": min(ngay_anh(f) for f in fs),
                        "anh_bia": "/assets/img/bo-suu-tap/%s-01-thumb.jpg" % slug, "anh": ds, "nguon": "thu-muc"})
            chi_tiet.append((ten_cat, ten, len(ds)))

    # Gop voi album them tu trang quan tri -> giu nguyen, dung truoc album tu thu muc.
    # Album "tu thu muc" = moi anh nam trong assets/img/bo-suu-tap (bo dung lai moi lan).
    p = os.path.join(BASE, "data", "bo-suu-tap.json")
    cu = json.load(io.open(p, encoding="utf-8")) if os.path.exists(p) else {}
    tu_thu_muc = lambda a: a.get("anh") and all(str(x).lstrip("/").startswith("assets/img/bo-suu-tap/") for x in a["anh"])
    cms = [a for a in cu.get("album", []) if not tu_thu_muc(a)]
    danh_muc = [{"ma": c, "ten": html_mod.unescape(t), "thu_muc": f, "nhan_trong": tr} for c, t, f, tr in DANHMUC]
    album = []
    for d in danh_muc:
        nhom = [a for a in cms if a.get("danh_muc") == d["ma"]] + [a for a in moi if a["danh_muc"] == d["ma"]]
        nhom.sort(key=lambda a: a.get("ngay") or "9999", reverse=(THU_TU == "moi-truoc"))
        album += nhom
    album += [a for a in cms if a.get("danh_muc") not in {d["ma"] for d in danh_muc}]
    io.open(p, "w", encoding="utf-8").write(json.dumps({"danh_muc": danh_muc, "album": album}, ensure_ascii=False, indent=1) + "\n")
    return {"album": len(moi), "anh": tong_anh, "trung": len(bo), "chi_tiet": chi_tiet, "album_cms": len(cms)}
