# -*- coding: utf-8 -*-
"""
NHAC NEN CHO WEBSITE
====================
- Bo 1 bai nhac (mp3 / m4a / wav / flac) vao thu muc  D:\\BT3\\mp3\\
- Chay muc 1 cua CAP NHAT WEB.bat (hoac: python tools/nhac_nen.py)
  -> bai MOI NHAT trong thu muc duoc nen lai 128 kbps (nhe cho dien thoai) thanh
     assets/audio/nhac-nen.mp3 va ghi vao data/nhac-nen.json (ten bai / tac gia lay tu the ID3).
- Chi nen lai khi co bai moi (so ten file + ngay sua voi lan truoc), khong dung toi bai
  da chon tren trang quan tri (file trong assets/uploads).
- Can 2 goi Python: miniaudio (doc) + lameenc (ghi mp3). Thieu thi chep nguyen file.
"""
import io, json, os, shutil, struct

TOOLS = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(TOOLS)
THU_MUC = os.path.join(BASE, "mp3")
DATA = os.path.join(BASE, "data", "nhac-nen.json")
RA = "assets/audio/nhac-nen.mp3"
DUOI = (".mp3", ".m4a", ".wav", ".flac", ".ogg")
KBPS = 128


def the_id3(p):
    """Lay ten bai (TIT2) va tac gia (TPE1) tu the ID3v2 cua file mp3."""
    kq = {}
    try:
        b = open(p, "rb").read(200000)
        if b[:3] != b"ID3":
            return kq
        v, sz, i = b[3], (b[6] << 21) | (b[7] << 14) | (b[8] << 7) | b[9], 10
        while i < 10 + sz and i + 10 <= len(b):
            fid = b[i:i + 4]
            if not fid.strip(b"\0"):
                break
            n = struct.unpack(">I", b[i + 4:i + 8])[0]
            if v == 4:
                n = (b[i + 4] << 21) | (b[i + 5] << 14) | (b[i + 6] << 7) | b[i + 7]
            d = b[i + 10:i + 10 + n]
            if fid in (b"TIT2", b"TPE1") and d:
                enc = {0: "latin-1", 1: "utf-16", 2: "utf-16-be", 3: "utf-8"}.get(d[0], "latin-1")
                kq[fid.decode()] = d[1:].decode(enc, "ignore").strip("\0 ").strip()
            i += 10 + n
    except Exception:
        pass
    return kq


def nen(vao, ra):
    """Nen lai mp3 128 kbps. Tra ve True neu nen duoc, False neu chi chep nguyen."""
    try:
        import miniaudio, lameenc
    except ImportError:
        shutil.copy2(vao, ra)
        return False
    am = miniaudio.decode_file(vao, output_format=miniaudio.SampleFormat.SIGNED16, nchannels=2, sample_rate=44100)
    pcm = am.samples.tobytes()
    try:                                              # cat khoang lang dau/cuoi bai -> phat lap khong bi hut
        import numpy as np
        x = np.frombuffer(pcm, dtype=np.int16).reshape(-1, 2)
        co = np.nonzero(np.abs(x).max(axis=1) > 100)[0]          # ~ -50 dB
        if len(co):
            x = x[co[0]:min(len(x), co[-1] + 44100 // 2)].astype(np.float32)
            n = min(len(x), 44100)                                # 1 giay nho dan o cuoi
            x[-n:] *= np.linspace(1, 0, n)[:, None]
            pcm = x.astype(np.int16).tobytes()
    except ImportError:
        pass
    enc = lameenc.Encoder()
    enc.set_bit_rate(KBPS)
    enc.set_in_sample_rate(44100)
    enc.set_channels(2)
    enc.set_quality(2)                                # 2 = chat luong cao
    dl = enc.encode(pcm) + enc.flush()
    open(ra, "wb").write(dl)
    return True


def doc_data():
    if os.path.exists(DATA):
        return json.load(io.open(DATA, encoding="utf-8"))
    return {"bat": True, "file": "", "ghi_nguon": "", "am_luong": 30}


def chay(log=print):
    if not os.path.isdir(THU_MUC):
        return None
    ds = [os.path.join(THU_MUC, f) for f in os.listdir(THU_MUC) if f.lower().endswith(DUOI)]
    if not ds:
        log(u"   Nhạc nền: thư mục mp3\\ trống — giữ nguyên bài đang dùng.")
        return None
    moi = max(ds, key=os.path.getmtime)
    dau = "%s|%d|%d" % (os.path.basename(moi), os.path.getsize(moi), int(os.path.getmtime(moi)))
    d = doc_data()
    if d.get("goc") == dau and os.path.isfile(os.path.join(BASE, RA)):
        log(u"   Nhạc nền: không có bài mới (đang dùng %s)." % os.path.basename(moi))
        return d
    os.makedirs(os.path.dirname(os.path.join(BASE, RA)), exist_ok=True)
    da_nen = nen(moi, os.path.join(BASE, RA))
    t = the_id3(moi)
    ten = " — ".join(x for x in (t.get("TIT2"), t.get("TPE1")) if x)
    d.update({"file": "/" + RA, "goc": dau})
    d["ghi_nguon"] = ten                              # file khong co the ID3 -> de trong, dien tren trang quan tri
    if not ten:
        log(u"   (File không ghi tên bài/tác giả — điền ô Ghi nguồn trong trang quản trị → 🎵 Nhạc nền.)")
    io.open(DATA, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
    log(u"   Nhạc nền: %s -> %s (%.1f MB%s)." % (os.path.basename(moi), RA,
        os.path.getsize(os.path.join(BASE, RA)) / 1048576.0, ", đã nén %d kbps" % KBPS if da_nen else ", chép nguyên"))
    return d


if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    chay()
