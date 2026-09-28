# -*- coding: utf-8 -*-
"""
BO DUNG WEBSITE: templates/*.html + data/*.json  ->  _site/  (ban hoan chinh de dua len web)

- Trang quan tri (/admin) sua cac file trong data/.
- Moi lan luu, Netlify tu chay file nay de dung lai web (xem netlify.toml).
- Tren may: CAP NHAT WEB.bat hoac  python tools/build_site.py

Trong templates/ co 2 loai cho trong:
    <!-- CMS:ten-khoi -->    -> ca mot khoi HTML duoc dung tu data (bang gia, doi ngu...)
    {{ten_bien}}             -> 1 gia tri (hotline, email, dia chi...)
"""
import datetime, hashlib, html, io, json, os, re, shutil, sys, urllib.parse

TOOLS = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(TOOLS)
TPL = os.path.join(BASE, "templates")
DATA = os.path.join(BASE, "data")
OUT = os.path.join(BASE, "_site")
TEN_MIEN = "https://quocanstudio.vn"
NETLIFY = os.environ.get("NETLIFY") == "true"       # Netlify tu dat bien nay khi build
THU_TU_ALBUM = "cu-truoc"      # album trong Bo suu tap: "cu-truoc" (cu -> moi) hoac "moi-truoc"

TRANG = [("index.html", u"Trang chủ"), ("bo-suu-tap.html", u"Bộ sưu tập"), ("bang-gia.html", u"Bảng giá"),
         ("doi-ngu.html", u"Đội ngũ"), ("tuyen-dung.html", u"Tuyển dụng"), ("lien-he.html", u"Liên hệ")]

SVG_FB = ('<svg viewBox="0 0 24 24" fill="currentColor"><path d="M14 9h3V6h-3a4 4 0 0 0-4 4v2H8v3h2v7h3v-7h2.5l.5-3H13v-2a1 1 0 0 1 1-1z"/></svg>')
SVG_ZALO = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M21 11.5a8.4 8.4 0 0 1-9 8.4 9.5 9.5 0 0 1-4.3-1L3 20l1.2-3.5A8.2 8.2 0 0 1 3 11.5 8.4 8.4 0 0 1 12 3a8.4 8.4 0 0 1 9 8.5z"/></svg>')
P_TEL = ('M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 '
         '2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z')
ICON_TRONG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.3">'
              '<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="10" r="1.6"/>'
              '<path d="m4 17 5-5 4 4 3-2 4 3"/></svg>')


# ============================================================ tien ich
def doc(ten):
    return json.load(io.open(os.path.join(DATA, ten), encoding="utf-8"))


def e(s):
    """Chu thuong -> HTML an toan."""
    return html.escape(str(s or ""), quote=False)


def ea(s):
    """Gia tri thuoc tinh HTML."""
    return html.escape(str(s or ""), quote=True)


def rich(s):
    """Chu co **dam** va xuong dong."""
    s = e(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    return s.replace("\n", "<br>")


def so(s):
    """'0354 501 333' -> '0354501333' (cho link tel:, zalo.me)."""
    return re.sub(r"[^\d+]", "", str(s or ""))


_ver = {}


def phien_ban(p):
    if p not in _ver:
        f = os.path.join(BASE, p)
        _ver[p] = hashlib.md5(open(f, "rb").read()).hexdigest()[:8] if os.path.isfile(f) else ""
    return _ver[p]


def anh(p, w=None, h=None):
    """Duong dan anh. Anh tai len qua trang quan tri (assets/uploads) duoc Netlify tu thu nho."""
    p = str(p or "").strip()
    if not p or re.match(r"^(https?:)?//", p):
        return p
    p = p.lstrip("/")
    if NETLIFY and p.startswith("assets/uploads/") and (w or h):
        q = {"url": "/" + p, "q": "80"}
        if w: q["w"] = str(w)
        if h: q["h"] = str(h); q["fit"] = "cover"
        return "/.netlify/images?" + urllib.parse.urlencode(q, quote_via=urllib.parse.quote)
    if w and w <= 600:                               # co ban -thumb san (anh cu) thi dung cho nhe
        nho = re.sub(r"(\.\w+)$", r"-thumb\1", p)
        if os.path.isfile(os.path.join(BASE, nho)):
            p = nho
    v = phien_ban(p)
    return p + ("?v=" + v if v else "")


def gia_html(g):
    g = str(g or "").strip()
    return e(g[:-1]) + "<sup>đ</sup>" if g.endswith("đ") else e(g) + ("<sup>đ</sup>" if re.search(r"\d", g) else "")


def gia_chu(g):
    g = str(g or "").strip()
    return g if (not g or g.endswith("đ") or not re.search(r"\d", g)) else g + "đ"


# ============================================================ khoi dung chung
def k_header(trang):
    menu = "\n".join(u'        <li><a href="%s"%s>%s</a></li>' % (f, ' class="active"' if f == trang else "", t) for f, t in TRANG)
    return u'''<header class="site-header">
  <div class="wrap">
    <nav class="nav">
      <a href="index.html" class="brand">
        <img class="brand__logo" src="assets/img/logo-mark.png" alt="Logo Quốc An Studio"
             onerror="this.remove()">
        <span class="brand__text">
          <span class="brand__name">QUỐC AN STUDIO</span>
          <span class="brand__sub">Wedding Photography</span>
        </span>
      </a>

      <ul class="menu" id="menu">
%s
      </ul>

      <div class="nav__cta">
        <a href="tel:{{hotline_1_so}}" class="nav__phone">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="%s"/></svg>
          {{hotline_1}}
        </a>
        <a href="lien-he.html" class="btn btn--sm">Đặt lịch</a>
        <button class="burger" aria-label="Mở menu" aria-expanded="false" aria-controls="menu">
          <span></span><span></span><span></span>
        </button>
      </div>
    </nav>
  </div>
</header>''' % (menu, P_TEL)


def k_thanh_toan(lh):
    the = []
    for tk in lh.get("tai_khoan", []):
        chinh = tk.get("chinh")
        the.append(u'''      <article class="pay__acc%s">
        <span class="pay__badge%s">%s</span>
        <div class="pay__brands"><b>VietinBank</b><b>VIETQR</b><b>napas 247</b></div>
        <div class="pay__qr-box">
          <img src="%s"
               alt="%s" loading="lazy">
        </div>
        <h3>%s</h3>
        <p class="pay__num">
          <span>%s</span>
          <button type="button" class="pay__copy" data-copy="%s">Sao chép</button>
        </p>
        <p class="pay__bank">%s</p>
      </article>''' % (" pay__acc--main" if chinh else "", "" if chinh else " pay__badge--alt", e(tk.get("nhan")),
                       ea(anh(tk.get("qr"))), ea(tk.get("mo_ta_qr") or ("Mã QR chuyển khoản — " + tk.get("chu_tk", ""))),
                       e(tk.get("chu_tk")), e(tk.get("so_tk")), ea(so(tk.get("so_tk"))), e(tk.get("ngan_hang"))))
    return u'''<section class="pay" id="thanh-toan">
  <div class="wrap">
    <div class="pay__head">
      <p class="eyebrow">Thanh toán &amp; đặt cọc</p>
      <h2>Chuyển khoản qua VietQR</h2>
      <p>Quét mã bằng app ngân hàng là tự điền sẵn số tài khoản, không lo gõ nhầm.</p>
    </div>

    <div class="pay__accounts">

%s

    </div>

    <p class="pay__note">
      Nội dung chuyển khoản: <em>Họ tên &ndash; Số điện thoại &ndash; Ngày chụp</em>.
      Sau khi chuyển, vui lòng nhắn ảnh biên lai qua Zalo <em>{{zalo}}</em> để studio xác nhận giữ lịch.
    </p>
  </div>
</section>''' % "\n\n".join(the)


def k_footer(trang, lh, nn=None):
    nn = nn or {}
    nguon = (u'\n      <span class="footer-nhac">♪ Nhạc nền: %s</span>' % e(nn["ghi_nguon"])) if nhac_bat(nn) and nn.get("ghi_nguon") else ""
    dg = "#danh-gia" if trang in ("index.html", "lien-he.html") else "index.html#danh-gia"
    dc = e(lh.get("dia_chi", "")).split(",", 1)
    dc = dc[0] + ",<br>" + dc[1].strip() if len(dc) == 2 else dc[0]
    return u'''<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <img class="footer-logo" src="assets/img/logo-full.png" alt="Quốc An Studio — More than a wedding, a lasting story"
             onerror="this.remove(); this.parentNode.querySelectorAll('[hidden]').forEach(function(e){e.hidden=false});">
        <span class="brand__name" hidden>QUỐC AN STUDIO</span>
        <span class="footer-tagline" hidden>More than a wedding — A lasting story</span>
        <p>Studio chụp ảnh cưới tại Phước An – Đồng Nai. Chụp ảnh cưới ngoại cảnh, phim trường,
           studio và phóng sự cưới trọn gói.</p>
        <div class="social">
          <a href="{{fanpage}}" target="_blank" rel="noopener" aria-label="Facebook">
            %s
          </a>
          <a href="https://zalo.me/{{zalo_so}}" target="_blank" rel="noopener" aria-label="Zalo">
            %s
          </a>
          <a href="{{instagram}}" target="_blank" rel="noopener" aria-label="Instagram">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.2" cy="6.8" r="1" fill="currentColor" stroke="none"/></svg>
          </a>
          <a href="tel:{{hotline_1_so}}" aria-label="Điện thoại">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="%s"/></svg>
          </a>
        </div>
      </div>

      <div>
        <h4>Liên kết</h4>
        <ul>
          <li><a href="index.html">Trang chủ</a></li>
          <li><a href="bo-suu-tap.html">Bộ sưu tập</a></li>
          <li><a href="doi-ngu.html">Đội ngũ</a></li>
          <li><a href="bang-gia.html">Bảng giá</a></li>
          <li><a href="tuyen-dung.html">Tuyển dụng</a></li>
          <li><a href="lien-he.html">Liên hệ</a></li>
        </ul>
      </div>

      <div>
        <h4>Dịch vụ</h4>
        <ul>
          <li><a href="bang-gia.html#goi-cuoi">Gói cưới trọn gói</a></li>
          <li><a href="bang-gia.html#album">Gói chụp album cưới</a></li>
          <li><a href="bang-gia.html#anh-cong">Gói ảnh cổng</a></li>
          <li><a href="bo-suu-tap.html">Mâm quả cưới hỏi</a></li>
          <li><a href="lien-he.html">Đào tạo nhiếp ảnh &amp; make-up</a></li>
          <li><a href="bo-suu-tap.html">Bộ sưu tập ảnh cưới</a></li>
        </ul>
      </div>

      <div>
        <h4>Thông tin liên hệ</h4>
        <ul>
          <li>%s</li>
          <li><a href="tel:{{hotline_1_so}}">Hotline: {{hotline_1_day}}</a></li>
          <li><a href="tel:{{hotline_2_so}}">Hotline: {{hotline_2_day}}</a></li>
          <li><a href="mailto:{{email}}">{{email}}</a></li>
          <li>Giờ mở cửa: {{gio_mo_cua}}</li>
          <li><a href="#thanh-toan">Thông tin chuyển khoản</a></li>
          <li><a href="%s">Đánh giá Google Maps</a></li>
        </ul>
      </div>
    </div>

    <div class="footer-bottom">
      <span>© 2020 Quốc An Studio — quocanstudio.vn. All rights reserved.</span>
      <span>Wedding Photography · Đồng Nai</span>%s
    </div>
  </div>
</footer>''' % (SVG_FB, SVG_ZALO, P_TEL, dc, dg, nguon)


def nhac_bat(nn):
    return bool(nn.get("bat") and nn.get("file"))


def k_nut_noi(nn):
    nut = u'''<div class="floating">
  <a href="https://zalo.me/{{zalo_so}}" class="zalo" target="_blank" rel="noopener" aria-label="Chat Zalo">
    %s
  </a>
  <a href="tel:{{hotline_1_so}}" aria-label="Gọi hotline">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9"><path d="%s"/></svg>
  </a>
</div>''' % (SVG_ZALO, P_TEL)
    if not nhac_bat(nn):
        return nut
    am = min(100, max(5, int(nn.get("am_luong") or 30))) / 100.0
    ten = (u"Nhạc nền: " + nn["ghi_nguon"]) if nn.get("ghi_nguon") else u"Nhạc nền"
    return nut + u'''
<button type="button" class="nhac" id="nhac" data-src="%s" data-vol="%.2f"
        aria-label="Bật nhạc nền" aria-pressed="false" title="%s">
  <svg class="nhac__not" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M9 18V5l11-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="17" cy="16" r="3"/></svg>
  <span class="nhac__song" aria-hidden="true"><i></i><i></i><i></i><i></i></span>
</button>''' % (ea(anh(nn["file"])), am, ea(ten))


# ============================================================ trang chu
def k_banner(bn):
    dong = []
    for i, x in enumerate(bn.get("anh", [])):
        a = x.get("anh")
        dt = x.get("anh_dien_thoai") or a
        pc, mb = anh(a, 1600, 900), anh(dt, 1080, 810)
        dong.append(u'    <div class="hero__slide%s" data-bg="%s" data-bg-m="%s"%s></div>'
                    % (" active" if i == 0 else "", ea(pc), ea(mb),
                       (" style=\"background-image:url('%s')\"" % ea(pc)) if i == 0 else ""))
    return u'  <div class="hero__slides">\n%s\n  </div>' % "\n".join(dong)


def the_gia_tom_tat(g):
    return u'''      <article class="price%s">%s
        <h3 class="price__name">%s</h3>
        <p class="price__desc">%s</p>
        <div class="price__amount">%s</div>
        <div class="price__unit">%s</div>
        <ul>
%s
        </ul>
        <a href="%s" class="btn%s">Xem chi tiết</a>
      </article>''' % (" price--featured" if g.get("noi_bat") else "",
                       ('\n        <span class="price__tag">%s</span>' % e(g["nhan"])) if g.get("nhan") else "",
                       e(g.get("ten")), e(g.get("mo_ta")), gia_html(g.get("gia")), e(g.get("don_vi")),
                       "\n".join("          <li>%s</li>" % rich(m) for m in g.get("muc", [])),
                       ea(g.get("link") or "bang-gia.html"), "" if g.get("noi_bat") else " btn--ghost")


def k_gia_tom_tat(bg):
    return u'    <div class="price-grid reveal">\n%s\n    </div>' % "\n\n".join(the_gia_tom_tat(g) for g in bg.get("tom_tat_trang_chu", []))


def k_khach_hang(dg, bst=None):
    """Muc Feedback khach hang: moi danh gia la 1 'trang' (anh lon trai + the danh gia phai), luot qua lai."""
    ds = [x for x in dg.get("danh_gia", []) if x.get("noi_dung") and x.get("de_xuat", True) is not False]
    ds.sort(key=lambda x: (not x.get("ghim"), [-int(n) for n in re.findall(r"\d+", x.get("ngay") or "0")]))
    dep = (bst or {}).get("anh_dep", {})
    theo_album = dep.get("theo_album", {})
    da_dung, gan_day = set(), []

    def chon_anh(r):
        if r.get("anh"):
            return r["anh"]
        if r.get("album") and theo_album.get(r["album"]):
            return theo_album[r["album"]][0]
        makeup = re.search(r"make|trang điểm|méc cúp", r.get("noi_dung", ""), re.I)
        chinh = (dep.get("co_dau") if makeup else dep.get("cap_doi")) or []
        phu = (dep.get("cap_doi") if makeup else dep.get("co_dau")) or []
        tat = chinh + [x for x in phu if x not in chinh]
        if not tat:
            return "/assets/img/about.jpg"
        # nhom theo co dau / concept: "make-up-my-tam-03-04.jpg" -> "make-up-my-tam" (gop Mỹ Tâm 01/02/03)
        album_cua = lambda x: re.sub(r"(-\d+)+(-thumb)?\.\w+$", "", x.rsplit("/", 1)[-1])
        album_da = {album_cua(x) for x in da_dung}
        # 1) album chua dung (uu tien dung nhom) -> moi danh gia 1 co dau / 1 buoi chup khac nhau
        x = next((x for k in (chinh, phu) for x in k if x not in da_dung and album_cua(x) not in album_da), None)
        # 2) het album moi: anh chua dung, tranh album cua 3 danh gia lien truoc
        if not x:
            x = next((x for x in tat if x not in da_dung and album_cua(x) not in {album_cua(y) for y in gan_day[-3:]}), None)
        x = x or tat[len(da_dung) % len(tat)]
        da_dung.add(x)
        gan_day.append(x)
        return x

    def ngay_vn(s):
        m = re.match(r"(\d{4})-(\d\d)-(\d\d)", s or "")
        return "%d thg %d, %s" % (int(m.group(3)), int(m.group(2)), m.group(1)) if m else e(s)

    SAO = u"★★★★★"
    anh_html, the_html = [], []
    for i, r in enumerate(ds):
        a = chon_anh(r)
        lop = " is-active" if i == 0 else ""
        nap = 'src="%s"' % ea(anh(a, 1000)) if i == 0 else 'data-src="%s"' % ea(anh(a, 1000))
        anh_html.append(u'      <img class="fbk__img%s" %s alt="Ảnh cưới Quốc An Studio — đánh giá của %s" loading="lazy">'
                        % (lop, nap, ea(r.get("ten"))))
        chu = (r.get("ten") or "?").strip()[:1].upper()
        av = (u'<img class="fbk-card__av" src="%s" alt="">' % ea(anh(r["anh_dai_dien"], 120, 120))) if r.get("anh_dai_dien") \
            else u'<span class="fbk-card__av fbk-card__av--chu">%s</span>' % e(chu)
        if (r.get("nguon") or "").lower().startswith("google"):
            dau = u'''<b class="fbk-card__ten">%s</b>
              <span class="fbk-card__sao" aria-label="%s sao">%s</span> <small>%s · Google Maps</small>''' % (
                e(r.get("ten")), e(r.get("so_sao") or 5), SAO[:int(r.get("so_sao") or 5)], ngay_vn(r.get("ngay")))
            chan = (u'''
            <a class="card fbk-card__goc" data-full="%s" data-title="Ảnh chụp đánh giá gốc — %s">
              <img src="%s" alt="">Xem ảnh chụp đánh giá gốc
            </a>''' % (ea(anh(r["anh_chup_goc"], 1000)), ea(r.get("ten")), ea(anh(r["anh_chup_goc"], 80, 80)))) if r.get("anh_chup_goc") else ""
            chan = u'<div class="fbk-card__chan fbk-card__chan--gg"><span class="fbk-card__g">G</span> Đánh giá trên Google Maps%s</div>' % chan
        else:
            dau = u'''<b class="fbk-card__ten">%s <svg class="fbk-card__huy" viewBox="0 0 16 16" aria-hidden="true"><rect width="16" height="16" rx="3" fill="#f02849"/><path d="M8 3.2l1.4 2.9 3.2.4-2.3 2.2.6 3.1L8 10.3l-2.9 1.5.6-3.1-2.3-2.2 3.2-.4z" fill="#fff"/></svg></b>
              <span>đề xuất <b>Chụp Ảnh Cưới Nhơn Trạch - Studio Quốc An.</b></span>
              <small>%s · <svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="6.3" fill="none" stroke="currentColor" stroke-width="1.3"/><path d="M1.8 8h12.4M8 1.7c2 2 2 10.6 0 12.6M8 1.7c-2 2-2 10.6 0 12.6" fill="none" stroke="currentColor" stroke-width="1.1"/></svg></small>''' % (
                e(r.get("ten")), ngay_vn(r.get("ngay")))
            chan = u'''<div class="fbk-card__chan">
              <span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 11v9H4v-9h3zm3 9h7.5a2 2 0 0 0 2-1.6l1.2-6A2 2 0 0 0 18.7 10H14l.8-3.8a1.8 1.8 0 0 0-3.3-1.3L8.6 10.4V20z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>Thích</span>
              <span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 11.5a8 8 0 0 1-11.6 7.1L4 20l1.3-4A8 8 0 1 1 20 11.5z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>Bình luận</span>
              <span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 5l7 7-7 7v-4c-5 0-8 1.5-10 5 .7-5.5 3.5-10 10-11V5z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>Chia sẻ</span>
            </div>'''
        the_html.append(u'''        <article class="fbk-card%s" data-i="%d">
          <div class="fbk-card__dau">
            %s
            <div class="fbk-card__who">
              %s
            </div>
            <span class="fbk-card__more" aria-hidden="true">&bull;&bull;&bull;</span>
          </div>
          <p class="fbk-card__text">%s</p>
          <button type="button" class="fbk-card__them" hidden>Xem thêm</button>
          %s
        </article>''' % (lop, i, av, dau, rich(r.get("noi_dung")), chan))

    DAC_DIEM = [
        (u"Ảnh đẹp<br>tự nhiên", '<path d="M4 8h3l1.5-2h7L17 8h3v11H4z"/><circle cx="12" cy="13.5" r="3.6"/>'),
        (u"Váy cưới<br>đa dạng", '<path d="M9 3h6l-1 4 5 13H5l5-13z"/><path d="M10 7h4"/>'),
        (u"Makeup<br>chuyên nghiệp", '<rect x="5" y="3" width="5" height="9" rx="2"/><path d="M7.5 12v9"/><path d="M15 5c2 0 3 1.5 3 3.5V21h-5V8.5C13 6.5 13.5 5 15 5z"/>'),
        (u"Ekip<br>nhiệt tình", '<circle cx="12" cy="7" r="3"/><circle cx="5.5" cy="9" r="2.2"/><circle cx="18.5" cy="9" r="2.2"/><path d="M6.5 20v-2.5a5.5 5.5 0 0 1 11 0V20M1.5 19v-1.2A3.8 3.8 0 0 1 5 14M22.5 19v-1.2A3.8 3.8 0 0 0 19 14"/>'),
    ]
    thanh = u"\n".join(u'''      <div class="fbk__dd"><span class="fbk__dd-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round" stroke-linecap="round">%s</svg></span><span>%s</span></div>''' % (s, t) for t, s in DAC_DIEM)

    return u'''<section class="fbk" id="khach-hang" aria-label="Feedback khách hàng">
 <div class="fbk__san">
  <div class="fbk__khung">
    <!-- Khung doc 2:3 dung ti le anh Bo suu tap -> hien tron anh, khong cat -->
    <div class="fbk__anh">
%s
    </div>

    <div class="fbk__phai">
      <div class="fbk__dau">
        <div class="fbk__brand">
          <b>QUỐC AN</b><span class="fbk__script">Studio</span>
          <small>Lưu giữ những khoảnh khắc<br>hạnh phúc trọn đời</small>
        </div>
        <p class="fbk__quote">&ldquo;Mỗi câu chuyện tình yêu<br>đều xứng đáng được lưu giữ<br>theo cách đẹp nhất&rdquo;</p>
      </div>
      <h2 class="fbk__tieude">Feedback <span class="fbk__script">Khách Hàng <i>♡</i></span></h2>

      <div class="fbk__the" aria-live="polite">
%s
      </div>

      <div class="fbk__dieu-khien">
        <button type="button" class="fbk__nut" data-fbk="-1" aria-label="Đánh giá trước">&#8249;</button>
        <span class="fbk__dem"><b>1</b> / %d đánh giá</span>
        <button type="button" class="fbk__nut" data-fbk="1" aria-label="Đánh giá sau">&#8250;</button>
      </div>
      <p class="fbk__tong">
        <a href="{{fanpage}}/reviews" target="_blank" rel="noopener"><b>%s</b> đề xuất · %s lượt đánh giá Fanpage</a>
        <a href="{{google_maps}}" target="_blank" rel="noopener"><b>%s★</b> Google Maps</a>
      </p>

      <p class="fbk__cam-on"><span class="fbk__script">Thank you <i>♡</i></span>
        <small>Vì đã tin tưởng<br>Studio Quốc An</small></p>
    </div>
  </div>

  <div class="fbk__thanh">
%s
    <div class="fbk__noi">
      <span><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.4"/></svg> Nhơn Trạch, Đồng Nai</span>
      <small>More than a photo<br>It&rsquo;s a memory of love</small>
    </div>
  </div>
 </div>

  <div class="fbk__nut-duoi">
    <a href="{{fanpage}}/reviews" target="_blank" rel="noopener" class="btn btn--ghost">Xem tất cả đánh giá trên Fanpage</a>
    <a href="#danh-gia" class="btn">Viết đánh giá &mdash; nhận quà</a>
  </div>
</section>''' % ("\n".join(anh_html), "\n".join(the_html), len(ds), e(dg.get("facebook_phan_tram")),
                 e(dg.get("facebook_so_danh_gia")), e(dg.get("google_diem")), thanh)


# ============================================================ bang gia
def the_gia(g):
    nhom = []
    for n in g.get("nhom", []):
        li = "\n".join("%s<li>%s</li>" % ("            " if n.get("kieu") == "qua" else "          ", rich(m)) for m in n.get("muc", []))
        if n.get("kieu") == "qua":
            nhom.append(u'''        <div class="price__gift-box">
          <h4>%s</h4>
          <ul>
%s
          </ul>
        </div>''' % (e(n.get("tieu_de") or u"Gói quà tặng"), li))
        elif n.get("kieu") == "2cot":
            nhom.append(u'''        <p class="price__sub">%s</p>
        <ul class="price__list2">
%s
        </ul>''' % (e(n.get("tieu_de")), li))
        else:
            nhom.append((u'        <p class="price__sub">%s</p>\n' % e(n["tieu_de"]) if n.get("tieu_de") else "") +
                        u"        <ul>\n%s\n        </ul>" % li)
    return u'''      <article class="price%s">%s
        <h3 class="price__name">%s</h3>
        <p class="price__desc">%s</p>
        <div class="price__amount">%s</div>
        <div class="price__unit">%s</div>
%s
        <a href="lien-he.html" class="btn%s">Đặt gói này</a>
      </article>''' % (" price--featured" if g.get("noi_bat") else "",
                       ('\n        <span class="price__tag">%s</span>' % e(g["nhan"])) if g.get("nhan") else "",
                       e(g.get("ten")), e(g.get("mo_ta")), gia_html(g.get("gia")), e(g.get("don_vi")),
                       "\n".join(nhom), "" if g.get("noi_bat") else " btn--ghost")


def the_cong(g):
    lc = g.get("lua_chon", [])
    opts = "\n".join(u'''          <div class="gate__opt%s"%s>
            <b>%s</b>
            <span>%s</span>
          </div>''' % (" is-best" if o.get("noi_bat") else "", ' style="grid-column:1/-1"' if len(lc) == 1 else "",
                       e(o.get("ten")), gia_html(o.get("gia"))) for o in lc)
    nhom = "\n\n".join(u'''        <h4>%s</h4>
        <ul>
%s
        </ul>''' % (e(n.get("tieu_de")), "\n".join("          <li>%s</li>" % rich(m) for m in n.get("muc", []))) for n in g.get("nhom", []))
    nut = (u'''
        <div class="btn-row" style="margin-top:6px">
          <a href="%s" class="btn btn--ghost btn--sm">%s</a>
        </div>''' % (ea(g.get("nut_link") or "lien-he.html"), e(g["nut_chu"]))) if g.get("nut_chu") else ""
    return u'''      <article class="gate">
        <h3>%s</h3>
        <p class="gate__lead">%s</p>
        <div class="gate__options">
%s
        </div>

%s%s
      </article>''' % (e(g.get("ten")), e(g.get("mo_ta")), opts, nhom, nut)


def k_bang_gia(bg):
    ds = bg.get("muc", [])
    nav = "\n".join(u'      <a href="#%s">%s</a>' % (ea(m["ma"]), e(m.get("nhan_menu") or m.get("tieu_de"))) for m in ds)
    out = [u'''<!-- ===== ĐIỀU HƯỚNG NHANH ===== -->
<section class="section" style="padding-bottom:0">
  <div class="wrap">
    <nav class="jump-nav reveal">
%s
    </nav>
  </div>
</section>''' % nav]
    for i, m in enumerate(ds):
        k = m.get("kieu")
        if k == "the":
            ls = m.get("goi", [])
            than = u'    <div class="price-grid %s reveal">\n%s\n    </div>' % (
                "price-grid--4" if len(ls) == 4 else "price-grid--auto", "\n\n".join(the_gia(g) for g in ls))
        elif k == "cong":
            than = u'    <div class="gate-grid reveal">\n\n%s\n\n    </div>' % "\n\n".join(the_cong(g) for g in m.get("goi", []))
        elif k == "bang":
            cot = (m.get("cot") or [u"Gói", u"Giá"]) + [u"Giá"]
            than = u'''    <div class="table-wrap reveal">
      <table>
        <thead>
          <tr><th>%s</th><th>%s</th></tr>
        </thead>
        <tbody>
%s
        </tbody>
      </table>
    </div>''' % (e(cot[0]), e(cot[1]), "\n".join(u'          <tr><td>%s</td><td class="price-cell">%s</td></tr>'
                                                      % (e(d.get("ten")), e(gia_chu(d.get("gia")))) for d in m.get("dong", [])))
        else:
            than = u'    <div class="grid grid--4 reveal">\n%s\n    </div>' % "\n".join(u'''      <a class="card card--poster" data-title="%s"
         data-full="%s">
        <img src="%s" alt="%s" loading="lazy">
        <div class="card__overlay"><h3>%s</h3><span>%s</span></div>
      </a>''' % (ea(a.get("chu_thich") or a.get("tieu_de")), ea(anh(a.get("anh"), 1400)),
                 ea(anh(a.get("anh_nho") or a.get("anh"), 600)), ea(a.get("chu_thich") or a.get("tieu_de")),
                 e(a.get("tieu_de")), e(a.get("nhom"))) for a in m.get("anh", []))
        ly = m.get("luu_y") or {}
        note = (u'''

    <div class="note reveal" style="margin-top:32px">
      <h3>%s</h3>
      <ul>
%s
      </ul>
    </div>''' % (e(ly.get("tieu_de") or u"Lưu ý"), "\n".join("        <li>%s</li>" % rich(x) for x in ly["muc"]))) if ly.get("muc") else ""
        out.append(u'''<!-- ===== %s ===== -->
<section class="section%s" id="%s">
  <div class="wrap">
    <div class="head reveal">
      <p class="eyebrow">%s</p>
      <h2>%s</h2>
      <div class="divider"><span></span></div>
      <p>%s</p>
    </div>

%s%s
  </div>
</section>''' % (e(m.get("tieu_de", "")).upper(), " section--tint" if i % 2 else "", ea(m["ma"]), e(m.get("nhan_nho")),
                 e(m.get("tieu_de")), rich(m.get("mo_ta")), than, note))
    return "\n\n".join(out)


def k_goi_options(bg):
    nhom = []
    for m in bg.get("muc", []):
        op = []
        if m.get("kieu") == "the":
            op = ["%s — %s" % (g.get("ten"), gia_chu(g.get("gia"))) for g in m.get("goi", [])]
        elif m.get("kieu") == "cong":
            for g in m.get("goi", []):
                gs = [o.get("gia") for o in g.get("lua_chon", []) if o.get("gia")]
                if not gs:
                    continue
                ts = sorted(gs, key=lambda x: int(so(x) or 0))
                op.append("%s — %s%s" % (g.get("ten"), "từ " if len(gs) > 1 else "", gia_chu(ts[0])))
        elif m.get("kieu") == "bang":
            op = ["%s — %s" % (d.get("ten"), gia_chu(d.get("gia"))) for d in m.get("dong", [])]
        if op:
            nhom.append(u'              <optgroup label="%s">\n%s\n              </optgroup>'
                        % (ea(m.get("tieu_de")), "\n".join(u"                <option>%s</option>" % e(o) for o in op)))
    return "\n".join(nhom) + u"\n              <option>Khác — cần tư vấn thêm</option>"


# ============================================================ doi ngu / tuyen dung / lien he
def k_thanh_vien(dn):
    the = []
    for i, t in enumerate(dn.get("thanh_vien", []), 1):
        fb = (u'''        <a class="member__fb" href="%s"
           target="_blank" rel="noopener">
          %s
          Facebook
        </a>''' % (ea(t["facebook"]), SVG_FB)) if t.get("facebook") else u'        <span class="member__fb member__fb--off">Chưa có Facebook</span>'
        the.append(u'''      <!-- Thành viên %02d -->
      <article class="member%s">%s
        <div class="member__avatar">
          <img src="%s" alt="%s" loading="lazy">
        </div>
        <h3>%s</h3>
        <p class="member__role">%s</p>
        <p class="member__bio">%s</p>
%s
      </article>''' % (i, " member--owner" if t.get("noi_bat") else "",
                       ('\n        <span class="member__badge">%s</span>' % e(t["nhan"])) if t.get("nhan") else "",
                       ea(anh(t.get("anh") or "assets/img/doi-ngu/avatar-mac-dinh.svg", 500, 500)),
                       ea("%s — %s" % (t.get("ten"), t.get("chuc_danh"))), e(t.get("ten")), e(t.get("chuc_danh")),
                       rich(t.get("gioi_thieu")), fb))
    return u'    <div class="members reveal">\n%s\n    </div>' % "\n".join(the)


def k_viec_lam(td):
    the = []
    for i, v in enumerate(td.get("viec_lam", [])):
        tag = "\n".join(u'            <span class="tag%s">%s</span>' % (" tag--hot" if n.get("noi_bat") else "", e(n.get("chu")))
                        for n in v.get("nhan", []))
        than = "\n".join(u"          <h4>%s</h4>\n          <ul>\n%s\n          </ul>"
                         % (e(n.get("tieu_de")), "\n".join("            <li>%s</li>" % rich(m) for m in n.get("muc", [])))
                         for n in v.get("nhom", []))
        the.append(u'''      <article class="job%s">
        <div class="job__head">
          <h3>%s</h3>
          <div class="job__meta">
%s
          </div>
          <div class="job__toggle">+</div>
        </div>
        <div class="job__body">
%s
        </div>
      </article>''' % (" is-open" if i == 0 else "", e(v.get("ten")), tag, than))
    return u'    <div class="jobs reveal">\n\n%s\n\n    </div>' % "\n\n".join(the)


def k_vi_tri_options(td):
    return "\n".join(u"              <option>%s</option>" % e(v.get("ten")) for v in td.get("viec_lam", []))


def k_thong_tin(lh):
    dc = e(lh.get("dia_chi", "")).split(",", 1)
    dc = dc[0] + ",<br>" + dc[1].strip() if len(dc) == 2 else dc[0]
    mxh = []
    if lh.get("zalo"):
        mxh.append(u'<a href="https://zalo.me/{{zalo_so}}" target="_blank" rel="noopener">Chat Zalo {{zalo}}</a>')
    for k, t in (("fanpage", "fanpage_ten"), ("facebook_ca_nhan", "facebook_ca_nhan_ten"), ("instagram", "instagram_ten")):
        if lh.get(k):
            ten = lh.get(t) or lh[k]
            if k == "instagram" and not ten.lower().startswith("instagram"):
                ten = "Instagram: " + ten
            mxh.append(u'<a href="%s" target="_blank" rel="noopener">%s</a>' % (ea(lh[k]), e(ten)))
    hl = u'<a href="tel:{{hotline_1_so}}">{{hotline_1_day}}</a>' + (u'<br>\n            <a href="tel:{{hotline_2_so}}">{{hotline_2_day}}</a>' if lh.get("hotline_2") else "")
    muc = [("M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z", '<circle cx="12" cy="10" r="3"/>', u"Địa chỉ studio", "<span>%s</span>" % dc),
           (P_TEL, "", u"Hotline", hl),
           (None, '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/>', u"Email", u'<a href="mailto:{{email}}">{{email}}</a>'),
           (None, '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>', u"Giờ mở cửa", u"<span>%s: {{gio_mo_cua}}</span>" % e(lh.get("ngay_mo_cua") or u"Hằng ngày")),
           ("M21 11.5a8.4 8.4 0 0 1-9 8.4 9.5 9.5 0 0 1-4.3-1L3 20l1.2-3.5A8.2 8.2 0 0 1 3 11.5 8.4 8.4 0 0 1 12 3a8.4 8.4 0 0 1 9 8.5z", "", u"Mạng xã hội", "<br>\n            ".join(mxh))]
    out = []
    for p, extra, b, noidung in muc:
        out.append(u'''        <div class="info">
          <div class="info__icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7">%s%s</svg>
          </div>
          <div>
            <b>%s</b>
            %s
          </div>
        </div>''' % (('<path d="%s"/>' % p) if p else "", extra, b, noidung))
    return u'      <div class="info-list">\n%s\n      </div>' % "\n\n".join(out)


# ============================================================ bo suu tap
def k_bo_suu_tap(bst):
    dm = bst.get("danh_muc", [])
    albums = bst.get("album", [])
    nut = "\n".join(u'      <button data-filter="%s"%s>%s</button>' % (ea(d["ma"]), ' class="active"' if i == 0 else "", e(d["ten"]))
                    for i, d in enumerate(dm))
    the = []
    for d in dm:
        co = [a for a in albums if a.get("danh_muc") == d["ma"] and a.get("anh")]
        # xep theo ngay chup (album chua co ngay coi nhu moi nhat)
        co.sort(key=lambda a: a.get("ngay") or "9999", reverse=(THU_TU_ALBUM == "moi-truoc"))
        if not co:
            for nhan in (d.get("nhan_trong") or [d["ten"], d["ten"]]):
                the.append(u'      <div class="card card--empty" data-cat="%s">\n        %s\n        <b>%s</b>\n'
                           u'        <span>Album sẽ được cập nhật</span>\n      </div>' % (ea(d["ma"]), ICON_TRONG, e(nhan)))
            continue
        for a in co:
            ds = a["anh"]
            bia = a.get("anh_bia") or ds[0]
            links = "\n".join(u'          <a data-full="%s" data-title="%s · %02d"></a>' % (ea(anh(p, 1400)), ea(a.get("ten")), n)
                              for n, p in enumerate(ds, 1))
            the.append(u'''      <article class="album" data-cat="%s">
        <a class="card album__cover">
          <img src="%s" alt="Album %s" loading="lazy">
          <span class="album__count">%d ảnh</span>
        </a>
        <div class="album__info"><h3>%s</h3><span>%s</span></div>
        <div class="album__photos" hidden>
%s
        </div>
      </article>''' % (ea(d["ma"]), ea(anh(bia, 440, 587)), ea(a.get("ten")), len(ds), e(a.get("ten")), e(d["ten"]), links))
    return (u'    <div class="filters filters--main reveal">\n%s\n    </div>\n\n'
            u'    <div class="grid grid--4 gallery reveal">\n%s\n    </div>' % (nut, "\n".join(the)))


# ============================================================ dung trang
def bien(lh):
    dc = lh.get("dia_chi", "")
    ten1 = (" (%s)" % lh["hotline_1_ten"]) if lh.get("hotline_1_ten") else ""
    ten2 = (" (%s)" % lh["hotline_2_ten"]) if lh.get("hotline_2_ten") else ""
    return {"hotline_1": lh.get("hotline_1", ""), "hotline_1_so": so(lh.get("hotline_1")),
            "hotline_2": lh.get("hotline_2", ""), "hotline_2_so": so(lh.get("hotline_2")),
            "hotline_1_ten": lh.get("hotline_1_ten", ""), "hotline_2_ten": lh.get("hotline_2_ten", ""),
            "hotline_1_day": lh.get("hotline_1", "") + ten1, "hotline_2_day": lh.get("hotline_2", "") + ten2,
            "zalo": lh.get("zalo", ""), "zalo_so": so(lh.get("zalo")), "email": lh.get("email", ""),
            "dia_chi": dc, "dia_chi_url": urllib.parse.quote(dc), "gio_mo_cua": lh.get("gio_mo_cua", ""),
            "google_maps": lh.get("google_maps", ""), "google_maps_url": urllib.parse.quote(lh.get("google_maps", ""), safe=""),
            "fanpage": (lh.get("fanpage") or "").rstrip("/"), "instagram": lh.get("instagram", "")}


def dung_trang(ten, d):
    s = io.open(os.path.join(TPL, ten), encoding="utf-8").read()
    khoi = {
        "header": lambda: k_header(ten),
        "thanh-toan": lambda: k_thanh_toan(d["lh"]),
        "footer": lambda: k_footer(ten, d["lh"], d["nn"]),
        "nut-noi": lambda: k_nut_noi(d["nn"]),
        "banner": lambda: k_banner(d["bn"]),
        "gia-tom-tat": lambda: k_gia_tom_tat(d["bg"]),
        "khach-hang": lambda: k_khach_hang(d["dg"], d["bst"]),
        "bang-gia": lambda: k_bang_gia(d["bg"]),
        "goi-options": lambda: k_goi_options(d["bg"]),
        "thanh-vien": lambda: k_thanh_vien(d["dn"]),
        "viec-lam": lambda: k_viec_lam(d["td"]),
        "vi-tri-options": lambda: k_vi_tri_options(d["td"]),
        "thong-tin": lambda: k_thong_tin(d["lh"]),
        "bo-suu-tap": lambda: k_bo_suu_tap(d["bst"]),
    }

    def thay_khoi(m):
        k = m.group(1)
        if k not in khoi:
            raise KeyError(u"Khối lạ trong %s: %s" % (ten, k))
        return khoi[k]()
    s = re.sub(r"<!-- CMS:([\w-]+) -->", thay_khoi, s)
    b = bien(d["lh"])

    def thay_bien(m):
        k = m.group(1)
        v = b.get(k, "")
        return v if k.endswith(("_so", "_url")) else ea(v)
    s = re.sub(r"\{\{(\w+)\}\}", thay_bien, s)
    # ban CSS/JS moi -> khach khong bi xem ban cu
    s = re.sub(r"(assets/(?:css/style\.css|js/main\.js))(\?v=[\w-]+)?", lambda m: anh(m.group(1)), s)
    return s


def dung(ra=OUT, chep_assets=True, log=print):
    d = {"lh": doc("lien-he.json"), "bg": doc("bang-gia.json"), "dn": doc("doi-ngu.json"), "dg": doc("danh-gia.json"),
         "td": doc("tuyen-dung.json"), "bn": doc("banner.json"), "bst": doc("bo-suu-tap.json"),
         "nn": doc("nhac-nen.json") if os.path.exists(os.path.join(DATA, "nhac-nen.json")) else {}}
    _ver.clear()
    if chep_assets and os.path.isdir(ra):
        for x in os.listdir(ra):                      # giu nguyen thu muc, xoa noi dung cu
            p = os.path.join(ra, x)
            shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    os.makedirs(ra, exist_ok=True)
    for ten, _ in TRANG:
        io.open(os.path.join(ra, ten), "w", encoding="utf-8", newline="\n").write(dung_trang(ten, d))
    if chep_assets:
        shutil.copytree(os.path.join(BASE, "assets"), os.path.join(ra, "assets"))
        shutil.copytree(os.path.join(BASE, "admin"), os.path.join(ra, "admin"))
    for f in ("_headers", "_redirects"):
        if os.path.exists(os.path.join(BASE, f)):
            shutil.copy2(os.path.join(BASE, f), ra)
    io.open(os.path.join(ra, "robots.txt"), "w", encoding="utf-8", newline="\n").write(
        u"User-agent: *\nAllow: /\nDisallow: /admin/\n\nSitemap: %s/sitemap.xml\n" % TEN_MIEN)
    hom_nay = datetime.date.today().isoformat()
    io.open(os.path.join(ra, "sitemap.xml"), "w", encoding="utf-8", newline="\n").write(
        u'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        u"".join(u"  <url><loc>%s/%s</loc><lastmod>%s</lastmod></url>\n" % (TEN_MIEN, "" if t == "index.html" else t, hom_nay)
                 for t, _ in TRANG) + u"</urlset>\n")
    log(u"   Dựng xong %d trang vào %s" % (len(TRANG), os.path.basename(os.path.normpath(ra))))
    return d


if __name__ == "__main__":
    dung()
