# -*- coding: utf-8 -*-
"""
CONG CU CAP NHAT WEBSITE QUOC AN STUDIO
=======================================
Nhap dup  "CAP NHAT WEB.bat"  o thu muc BT3 de mo menu.

Cach lam viec (tu 11/09/2026):
    templates/*.html  +  data/*.json   --(tools/build_site.py)-->   _site/   (web hoan chinh)
    - Sua noi dung (gia, doi ngu, danh gia, album...): trang quan tri /admin
    - Them nhieu anh 1 luc tu may tinh: bo anh vao thu muc trong BT3 -> muc 1
    - Dua len web: muc 3 (GitHub -> Netlify tu dung lai trong ~1 phut)

Chay truc tiep:
    python tools/capnhat.py tatca | kiemtra | donggoi | xem | tailen | laymoi
"""
import datetime, ftplib, getpass, hashlib, io, json, os, re, shutil, socket, subprocess
import sys, time, webbrowser, zipfile

TOOLS = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)
import build_site

OUT = os.path.join(BASE, "_site")                      # web hoan chinh
ZIP = os.path.join(BASE, "quocanstudio-web.zip")
TEN_MIEN = "https://quocanstudio.vn"
CAU_HINH = os.path.join(TOOLS, "cau-hinh-hosting.txt")
DA_TAI = os.path.join(TOOLS, ".da-tai-len.json")
BAO_CAO_TRUNG = os.path.join(TOOLS, "bao-cao-anh-trung.txt")

HTACCESS = u"""# Quoc An Studio - cau hinh may chu (chi dung khi dua len hosting cPanel / FTP)
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript image/svg+xml
</IfModule>
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/jpeg "access plus 7 days"
  ExpiresByType image/png  "access plus 7 days"
  ExpiresByType image/svg+xml "access plus 7 days"
  ExpiresByType audio/mpeg "access plus 30 days"
  ExpiresByType text/css   "access plus 30 days"
  ExpiresByType application/javascript "access plus 30 days"
  ExpiresByType text/html  "access plus 0 seconds"
</IfModule>
"""

MAU_CAU_HINH = u"""# ================================================================
#  CHI DUNG KHI DUA WEB LEN HOSTING FTP (Mat Bao / cPanel) THAY VI NETLIFY
#  Dien theo email nha cung cap hosting gui. KHONG ghi mat khau vao day.
# ================================================================
may_chu   =
cong      = 21
tai_khoan =
thu_muc   = /public_html
# co = FTPS ma hoa (an toan hon) | khong = FTP thuong
ma_hoa    = co
"""


def in_(s=u""):
    print(s)
    sys.stdout.flush()


def tieu_de(s):
    in_(u"\n" + u"=" * 64)
    in_(u"  " + s)
    in_(u"=" * 64)


# ---------------------------------------------------------------- git
def git(*args):
    return subprocess.run(["git"] + list(args), cwd=BASE, capture_output=True, text=True, encoding="utf-8", errors="replace")


def co_github():
    if not os.path.isdir(os.path.join(BASE, ".git")):
        return False
    try:
        return bool(git("remote", "get-url", "origin").stdout.strip())
    except OSError:
        return False


def lay_ban_moi():
    """Lay cac thay doi da sua tren trang quan tri (GitHub) ve may truoc khi sua tren may."""
    if not co_github():
        return True
    tieu_de(u"LẤY BẢN MỚI NHẤT TỪ GITHUB (các thay đổi đã sửa trên trang quản trị)")
    git("add", "-A")
    if git("diff", "--cached", "--quiet").returncode:
        git("commit", "-m", u"Lưu thay đổi trên máy trước khi lấy bản mới (%s)" % datetime.datetime.now().strftime("%d/%m/%Y %H:%M"))
    r = git("pull", "--rebase", "origin", "main")
    if r.returncode:
        in_(u"   KHÔNG LẤY ĐƯỢC BẢN MỚI:\n   " + (r.stderr or r.stdout).strip().replace("\n", "\n   "))
        git("rebase", "--abort")
        return False
    in_(u"   Đã cập nhật về máy.")
    return True


# ---------------------------------------------------------------- 1. bo suu tap tu thu muc anh
def dung_bo_suu_tap():
    tieu_de(u"QUÉT ẢNH TRONG CÁC THƯ MỤC BT3 -> BỘ SƯU TẬP")
    import bo_suu_tap
    truoc = bo_suu_tap.ten_album_hien_tai()
    t0 = time.time()
    kq = bo_suu_tap.dung(log=in_, bao_cao_trung=BAO_CAO_TRUNG)
    sau = bo_suu_tap.ten_album_hien_tai()
    moi = [x for x in sau if x not in truoc]
    mat = [x for x in truoc if x not in sau]
    in_(u"   Xong sau %d giây: %d album từ thư mục / %d ảnh (bỏ %d ảnh trùng) + %d album thêm trên trang quản trị."
        % (time.time() - t0, kq["album"], kq["anh"], kq["trung"], kq.get("album_cms", 0)))
    for x in moi:
        in_(u"   + Album MỚI:        " + x)
    for x in mat:
        in_(u"   - Album KHÔNG CÒN:  " + x)
    if not moi and not mat:
        in_(u"   (Không có album mới hay album bị bỏ.)")
    import chon_anh_dep                              # chon lai anh dep cho muc Feedback khach hang
    chon_anh_dep.chay(log=in_)
    import nhac_nen                                  # bai moi trong thu muc mp3\ -> nen lai lam nhac nen
    nhac_nen.chay(log=in_)
    return kq


# ---------------------------------------------------------------- 2. kiem tra anh / link hong
def _noi_bo(u):
    u = u.strip()
    if not u or u.startswith(("http:", "https:", "//", "mailto:", "tel:", "#", "javascript:", "data:", "/.netlify/")):
        return None
    return u.split("#")[0].split("?")[0].lstrip("/")


def kiem_tra():
    tieu_de(u"KIỂM TRA ẢNH / LINK HỎNG")
    build_site.dung(ra=OUT, chep_assets=False, log=lambda s: None)
    loi = []
    for f, _ in build_site.TRANG:
        s = io.open(os.path.join(OUT, f), encoding="utf-8").read()
        s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
        refs = re.findall(r'(?:src|href|data-full|data-bg|data-bg-m)="([^"]*)"', s)
        refs += re.findall(r"url\(['\"]?([^'\")]+)['\"]?\)", s)
        for r in refs:
            d = _noi_bo(r)
            if d and not (os.path.exists(os.path.join(BASE, d)) or os.path.exists(os.path.join(OUT, d))):
                loi.append((f, d))
    if loi:
        in_(u"   CÓ %d LỖI — các file sau đang bị trỏ tới nhưng không tồn tại:" % len(loi))
        for f, d in loi[:40]:
            in_(u"     %-16s -> %s" % (f, d))
    else:
        in_(u"   Không có lỗi: %d trang, mọi ảnh và link nội bộ đều tồn tại." % len(build_site.TRANG))
    return loi


# ---------------------------------------------------------------- 3. dong goi
def dong_goi():
    tieu_de(u"DỰNG WEB HOÀN CHỈNH (_site) + FILE ZIP")
    build_site.dung(ra=OUT, chep_assets=True, log=in_)
    io.open(os.path.join(OUT, ".htaccess"), "w", encoding="utf-8", newline="\n").write(HTACCESS)
    so_file, dung_luong = 0, 0
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for goc, _, files in os.walk(OUT):
            for f in files:
                p = os.path.join(goc, f)
                z.write(p, os.path.relpath(p, OUT).replace("\\", "/"))
                so_file += 1
                dung_luong += os.path.getsize(p)
    in_(u"   Thư mục _site: %d file, %.1f MB  |  quocanstudio-web.zip: %.1f MB"
        % (so_file, dung_luong / 1048576.0, os.path.getsize(ZIP) / 1048576.0))


# ---------------------------------------------------------------- 4. xem thu + trang quan tri tren may
def xem_thu():
    tieu_de(u"XEM THỬ WEB + TRANG QUẢN TRỊ TRÊN MÁY")
    port = 8080
    while True:
        with socket.socket() as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                break
        port += 1
    p = subprocess.Popen([sys.executable, os.path.join(TOOLS, "cms_server.py"), "--port", str(port)],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)
    webbrowser.open("http://localhost:%d/index.html" % port)
    webbrowser.open("http://localhost:%d/admin/" % port)
    in_(u"   Web:            http://localhost:%d/" % port)
    in_(u"   Trang quản trị: http://localhost:%d/admin/   (bấm 'Đăng nhập' là vào, không cần mật khẩu)" % port)
    in_(u"   Sửa rồi bấm 'Công bố' -> lưu ngay vào máy, tải lại trang web là thấy.")
    in_(u"   Nhớ chọn mục 3 để đưa các thay đổi này lên web thật.")
    input(u"\n   Xong nhấn Enter để tắt... ")
    p.terminate()


# ---------------------------------------------------------------- 5. dua len web
def tai_len_github():
    tieu_de(u"ĐƯA LÊN WEB: GITHUB -> NETLIFY")
    git("add", "-A")
    co_moi = git("diff", "--cached", "--quiet").returncode != 0
    if co_moi:
        so = len(git("diff", "--cached", "--name-only").stdout.split())
        git("commit", "-m", u"Cập nhật website từ máy tính (%s)" % datetime.datetime.now().strftime("%d/%m/%Y %H:%M"))
        in_(u"   Đã ghi %d file thay đổi." % so)
    r = git("pull", "--rebase", "origin", "main")
    if r.returncode and "couldn't find remote ref" not in (r.stderr or ""):
        in_(u"   LỖI khi lấy bản mới trước khi gửi:\n   " + (r.stderr or r.stdout).strip().replace("\n", "\n   "))
        git("rebase", "--abort")
        return
    r = git("push", "-u", "origin", "main")
    if r.returncode:
        in_(u"   LỖI khi gửi lên GitHub:\n   " + (r.stderr or r.stdout).strip().replace("\n", "\n   "))
        return
    in_(u"   Đã gửi lên GitHub. Netlify tự dựng lại web trong khoảng 1 phút.")
    in_(u"   Xem: %s   (nhấn Ctrl+F5 nếu vẫn thấy bản cũ)" % TEN_MIEN)


def doc_cau_hinh():
    if not os.path.exists(CAU_HINH):
        io.open(CAU_HINH, "w", encoding="utf-8").write(MAU_CAU_HINH)
    ch = {}
    for dong in io.open(CAU_HINH, encoding="utf-8"):
        dong = dong.split("#")[0].strip()
        if "=" in dong:
            k, v = dong.split("=", 1)
            ch[k.strip()] = v.strip()
    return ch


def md5(p):
    h = hashlib.md5()
    with open(p, "rb") as f:
        for khoi in iter(lambda: f.read(1 << 20), b""):
            h.update(khoi)
    return h.hexdigest()


def tai_len_ftp(thu=False):
    tieu_de(u"ĐƯA LÊN HOSTING FTP" + (u" — XEM TRƯỚC (không kết nối)" if thu else u""))
    if not os.path.isfile(os.path.join(OUT, "assets", "css", "style.css")):
        dong_goi()
    ch = doc_cau_hinh()
    khoa = "%s|%s" % (ch.get("may_chu", ""), ch.get("thu_muc", ""))
    da = json.load(io.open(DA_TAI, encoding="utf-8")).get(khoa, {}) if os.path.exists(DA_TAI) else {}
    hien = {}
    for goc, _, files in os.walk(OUT):
        for f in files:
            p = os.path.join(goc, f)
            hien[os.path.relpath(p, OUT).replace("\\", "/")] = md5(p)
    gui = sorted((r for r in hien if da.get(r) != hien[r]), key=lambda r: (r.endswith(".html"), r))
    xoa = [r for r in da if r not in hien]
    in_(u"   Cần gửi: %d file  |  Cần xoá trên host: %d file cũ  |  Giữ nguyên: %d file"
        % (len(gui), len(xoa), len(hien) - len(gui)))
    if thu:
        for r in gui[:25]:
            in_(u"     + " + r)
        return
    if not gui and not xoa:
        in_(u"   Web trên mạng đã là bản mới nhất.")
        return
    if not ch.get("may_chu") or not ch.get("tai_khoan"):
        in_(u"   Chưa kết nối GitHub và chưa có thông tin FTP (tools\\cau-hinh-hosting.txt).")
        in_(u"   Xem hướng dẫn trong README.md, mục 'Đưa web lên mạng'.")
        return
    mk = getpass.getpass(u"   Mật khẩu FTP của %s (gõ không hiện chữ, xong nhấn Enter): " % ch["tai_khoan"])
    cong = int(ch.get("cong") or 21)
    try:
        if ch.get("ma_hoa", "co").lower().startswith("c"):
            ftp = ftplib.FTP_TLS(); ftp.connect(ch["may_chu"], cong, timeout=30); ftp.login(ch["tai_khoan"], mk); ftp.prot_p()
        else:
            ftp = ftplib.FTP(); ftp.connect(ch["may_chu"], cong, timeout=30); ftp.login(ch["tai_khoan"], mk)
    except Exception as e:
        in_(u"   KHÔNG KẾT NỐI ĐƯỢC: %s" % e)
        return
    goc_host = ch.get("thu_muc", "/public_html").rstrip("/") or "/"
    ftp.cwd(goc_host)
    da_tao = set()

    def tao_thu_muc(rel_dir):
        phan = [x for x in rel_dir.split("/") if x]
        for i in range(1, len(phan) + 1):
            d = "/".join(phan[:i])
            if d not in da_tao:
                try:
                    ftp.mkd(goc_host + "/" + d)
                except ftplib.error_perm:
                    pass
                da_tao.add(d)

    def luu_so():
        tat = json.load(io.open(DA_TAI, encoding="utf-8")) if os.path.exists(DA_TAI) else {}
        tat[khoa] = da
        io.open(DA_TAI, "w", encoding="utf-8").write(json.dumps(tat, ensure_ascii=False, indent=0))

    loi = 0
    for i, r in enumerate(gui, 1):
        try:
            tao_thu_muc(os.path.dirname(r))
            with open(os.path.join(OUT, r), "rb") as f:
                ftp.storbinary("STOR " + goc_host + "/" + r, f)
            da[r] = hien[r]
            in_(u"   [%d/%d] %s" % (i, len(gui), r))
        except Exception as e:
            loi += 1
            in_(u"   [%d/%d] LỖI %s: %s" % (i, len(gui), r, e))
        if i % 40 == 0:
            luu_so()
    for r in xoa:
        try:
            ftp.delete(goc_host + "/" + r)
        except Exception:
            pass
        da.pop(r, None)
    luu_so()
    ftp.quit()
    in_(u"   XONG: gửi %d file, xoá %d file cũ%s." % (len(gui) - loi, len(xoa), (u", %d lỗi (chạy lại để gửi tiếp)" % loi) if loi else u""))


def ket_noi_github():
    """Lan dau: gan kho GitHub, dien ten kho vao admin/config.yml roi gui toan bo web len."""
    tieu_de(u"KẾT NỐI GITHUB LẦN ĐẦU")
    in_(u"   Tạo kho trống trên GitHub trước (xem README, mục 'Đưa web lên mạng'), rồi dán link kho vào đây.")
    in_(u"   Ví dụ:  https://github.com/quocanstudio/quocanstudio-web")
    url = input(u"\n   Link kho GitHub: ").strip().rstrip("/")
    m = re.match(r"^(?:https://github\.com/|git@github\.com:)([\w.-]+)/([\w.-]+?)(?:\.git)?$", url)
    if not m:
        in_(u"   Link không đúng dạng https://github.com/<tài khoản>/<tên kho>.")
        return
    kho = "%s/%s" % (m.group(1), m.group(2))
    if not os.path.isdir(os.path.join(BASE, ".git")):
        git("init", "-b", "main")
    git("remote", "remove", "origin")
    git("remote", "add", "origin", "https://github.com/%s.git" % kho)
    p = os.path.join(BASE, "admin", "config.yml")
    s = io.open(p, encoding="utf-8").read()
    s = re.sub(r"(?m)^(  repo: ).*$", r"\g<1>" + kho, s, count=1)
    io.open(p, "w", encoding="utf-8").write(s)
    in_(u"   Đã gắn kho %s và điền vào trang quản trị (admin/config.yml)." % kho)
    in_(u"   Lần gửi đầu ~210 MB, có thể mất 5–15 phút. Nếu trình duyệt mở trang đăng nhập GitHub, anh đăng nhập để cho phép.")
    tai_len_github()


def tai_len(thu=False):
    if co_github() and not thu:
        tai_len_github()
    else:
        tai_len_ftp(thu)


# ---------------------------------------------------------------- menu
def cap_nhat_tat_ca():
    if not lay_ban_moi():
        in_(u"   Dừng lại để tránh ghi đè thay đổi trên trang quản trị. Báo hỗ trợ để xử lý.")
        return
    dung_bo_suu_tap()
    loi = kiem_tra()
    dong_goi()
    tieu_de(u"HOÀN TẤT" + (u" — CÒN %d LỖI, XEM Ở TRÊN" % len(loi) if loi else u""))
    in_(u"   Tiếp theo: chọn 2 để xem thử, rồi 3 để đưa lên web.")


def menu():
    while True:
        tieu_de(u"CÔNG CỤ CẬP NHẬT WEBSITE — QUỐC AN STUDIO")
        in_(u"   1. Cập nhật ảnh từ thư mục BT3  (quét ảnh -> Bộ sưu tập -> kiểm tra -> dựng web)")
        in_(u"   2. Mở trang quản trị + xem thử web trên máy")
        in_(u"   3. Đưa lên web" + (u"  (GitHub -> Netlify)" if co_github() else u"  (chưa kết nối GitHub — xem README)"))
        in_(u"   4. Kiểm tra ảnh / link hỏng")
        in_(u"   5. Lấy bản mới nhất từ GitHub (sau khi sửa trên điện thoại)")
        in_(u"   6. Mở thư mục web hoàn chỉnh (_site)")
        in_(u"   7. Kết nối GitHub lần đầu" + (u"  (đã kết nối)" if co_github() else u""))
        in_(u"   0. Thoát")
        c = input(u"\n   Chọn số rồi nhấn Enter: ").strip()
        if c == "1":
            cap_nhat_tat_ca()
        elif c == "2":
            xem_thu()
        elif c == "3":
            tai_len()
        elif c == "4":
            kiem_tra()
        elif c == "5":
            lay_ban_moi() if co_github() else in_(u"   Chưa kết nối GitHub.")
        elif c == "6":
            if not os.path.isfile(os.path.join(OUT, "index.html")):
                dong_goi()
            os.startfile(OUT)
        elif c == "7":
            ket_noi_github()
        elif c == "0":
            return
        input(u"\n   Nhấn Enter để quay lại menu...")


if __name__ == "__main__":
    lenh = sys.argv[1] if len(sys.argv) > 1 else "menu"
    {"menu": menu, "tatca": cap_nhat_tat_ca, "kiemtra": kiem_tra, "donggoi": dong_goi, "xem": xem_thu,
     "dung": dung_bo_suu_tap, "laymoi": lay_ban_moi,
     "tailen": lambda: tai_len(thu="--thu" in sys.argv)}.get(lenh, menu)()
