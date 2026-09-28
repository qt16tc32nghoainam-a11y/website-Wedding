# -*- coding: utf-8 -*-
"""
MAY CHU XEM THU + TRANG QUAN TRI CHAY TREN MAY (khong can Node, khong can mang)
==============================================================================
    python tools/cms_server.py [--port 8080]

- http://localhost:8080/          -> xem web (ban dung trong _site, tu dung lai khi sua)
- http://localhost:8080/admin/    -> trang quan tri; bam "Luu" la ghi thang vao data/ tren o dia
- /api/v1 (cung cong): "local backend" cua Decap CMS (thay cho decap-server cua Node)
"""
import base64, hashlib, http.server, io, json, mimetypes, os, re, socketserver, sys, threading, time, urllib.parse

TOOLS = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)
import build_site

SITE = os.path.join(BASE, "_site")
mimetypes.add_type("text/yaml", ".yml")
mimetypes.add_type("image/webp", ".webp")
mimetypes.add_type("audio/mpeg", ".mp3")
_lock = threading.Lock()
_hen = [None]


def dung_lai(tre=0.8):
    """Dung lai HTML sau khi luu (gom nhieu lan luu lien tiep thanh 1 lan)."""
    def chay():
        with _lock:
            try:
                build_site.dung(ra=SITE, chep_assets=False, log=lambda s: None)
                print(time.strftime("%H:%M:%S"), "  da dung lai web sau khi luu")
            except Exception as e:
                print("LOI khi dung lai web:", e)
    if _hen[0]:
        _hen[0].cancel()
    _hen[0] = threading.Timer(tre, chay)
    _hen[0].start()


def an_toan(rel):
    p = os.path.normpath(os.path.join(BASE, rel))
    if not p.startswith(BASE):
        raise ValueError("duong dan ngoai BT3: %s" % rel)
    return p


def sha(b):
    return hashlib.sha256(b).hexdigest()


def doc_entry(rel, label=None):
    try:
        b = open(an_toan(rel), "rb").read()
        return {"data": b.decode("utf-8"), "file": {"path": rel.replace("\\", "/"), "label": label, "id": sha(b)}}
    except OSError:
        return {"data": None, "file": {"path": rel.replace("\\", "/"), "label": label, "id": None}}


def doc_media(rel):
    b = open(an_toan(rel), "rb").read()
    return {"id": sha(b), "content": base64.b64encode(b).decode(), "encoding": "base64",
            "path": rel.replace("\\", "/"), "name": os.path.basename(rel)}


def liet_ke(thu_muc, duoi="", sau=1):
    goc = an_toan(thu_muc)
    out = []
    if not os.path.isdir(goc):
        return out
    for dp, dn, fn in os.walk(goc):
        muc = 0 if dp == goc else os.path.relpath(dp, goc).count(os.sep) + 1
        if muc >= sau - 1:                       # sau=1: chi lay file nam ngay trong thu muc
            dn[:] = []
        for f in fn:
            if f.startswith(".") or (duoi and not f.endswith("." + duoi.lstrip("."))):
                continue
            out.append(os.path.relpath(os.path.join(dp, f), BASE).replace("\\", "/"))
    return out


def ghi(rel, noi_dung):
    p = an_toan(rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "wb") as f:
        f.write(noi_dung)


def xu_ly(action, pr):
    if action == "info":
        return {"repo": os.path.basename(BASE), "publish_modes": ["simple"], "type": "local_fs"}
    if action == "entriesByFolder":
        return [doc_entry(f) for f in liet_ke(pr["folder"], pr.get("extension", ""), pr.get("depth", 1))]
    if action == "entriesByFiles":
        return [doc_entry(f["path"], f.get("label")) for f in pr["files"]]
    if action == "getEntry":
        return doc_entry(pr["path"])
    if action == "persistEntry":
        ds = pr.get("dataFiles") or [pr["entry"]]
        for d in ds:
            ghi(d["path"], d["raw"].encode("utf-8"))
        for a in pr.get("assets", []):
            ghi(a["path"], base64.b64decode(a["content"]) if a.get("encoding") == "base64" else a["content"].encode("utf-8"))
        for d in ds:
            if d.get("newPath"):
                os.replace(an_toan(d["path"]), an_toan(d["newPath"]))
        dung_lai()
        return {"message": "entry persisted"}
    if action == "getMedia":
        return [doc_media(f) for f in liet_ke(pr["mediaFolder"], "", 1)]
    if action == "getMediaFile":
        return doc_media(pr["path"])
    if action == "persistMedia":
        a = pr["asset"]
        ghi(a["path"], base64.b64decode(a["content"]) if a.get("encoding") == "base64" else a["content"].encode("utf-8"))
        return doc_media(a["path"])
    if action == "deleteFile":
        os.remove(an_toan(pr["path"]))
        dung_lai()
        return {"message": "deleted file %s" % pr["path"]}
    if action == "deleteFiles":
        for x in pr["paths"]:
            os.remove(an_toan(x))
        dung_lai()
        return {"message": "deleted files"}
    if action == "getDeployPreview":
        return None
    raise ValueError("Unknown action %s" % action)


class ApiMixin(object):
    """API "local backend" cua Decap CMS, chay chung cong voi web tai /api/v1."""
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")

    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()

    def do_POST(self):
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
            res, code = xu_ly(body.get("action"), body.get("params") or {}), 200
        except Exception as e:
            res, code = {"error": str(e)}, 422
        b = json.dumps(res, ensure_ascii=False).encode("utf-8")
        self.send_response(code); self._cors()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)


class Web(ApiMixin, http.server.SimpleHTTPRequestHandler):
    """/admin va /assets lay truc tiep tu BT3 (thay anh moi tai len ngay); con lai lay tu _site."""
    def translate_path(self, path):
        p = urllib.parse.unquote(urllib.parse.urlsplit(path).path)
        goc = BASE if p.startswith(("/admin", "/assets")) else SITE
        full = os.path.normpath(os.path.join(goc, p.lstrip("/")))
        return full if full.startswith(goc) else SITE

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def send_head(self):
        """Ho tro 'Range' (nhac nen tua / nghe tiep giua cac trang giong web that)."""
        path = self.translate_path(self.path)
        if os.path.normcase(path) == os.path.normcase(os.path.join(BASE, "admin", "config.yml")):
            return self._config(path)
        rng = self.headers.get("Range", "")
        m = re.match(r"bytes=(\d*)-(\d*)$", rng.strip())
        if not m or not os.path.isfile(path) or not (m.group(1) or m.group(2)):
            return super().send_head()
        size = os.path.getsize(path)
        if m.group(1):
            dau, cuoi = int(m.group(1)), min(int(m.group(2) or size - 1), size - 1)
        else:
            dau, cuoi = max(0, size - int(m.group(2))), size - 1
        if dau >= size or dau > cuoi:
            self.send_response(416)
            self.send_header("Content-Range", "bytes */%d" % size)
            self.end_headers()
            return None
        f = open(path, "rb")
        f.seek(dau)
        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Range", "bytes %d-%d/%d" % (dau, cuoi, size))
        self.send_header("Content-Length", str(cuoi - dau + 1))
        self.end_headers()
        return _Doan(f, cuoi - dau + 1)

    def _config(self, path):
        """admin/config.yml: 'local_backend: true' -> API tren chinh cong nay (chay nhieu ban cung luc khong dung nhau)."""
        s = io.open(path, encoding="utf-8").read()
        url = "http://%s/api/v1" % (self.headers.get("Host") or "localhost:%d" % self.server.server_address[1])
        s = re.sub(r"(?m)^local_backend:\s*true\s*$", lambda m: "local_backend:\n  url: " + url, s)
        b = s.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/yaml; charset=utf-8")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        return io.BytesIO(b)

    def log_message(self, *a):
        pass


class _Doan(object):
    """Doc toi da n byte tu file (cho phan hoi 206)."""
    def __init__(self, f, n):
        self.f, self.con = f, n

    def read(self, k=65536):
        if self.con <= 0:
            return b""
        b = self.f.read(min(k, self.con))
        self.con -= len(b)
        return b

    def close(self):
        self.f.close()


class May(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def chay(port=8080, mo_trinh_duyet=False):
    print("Dang dung web..."); build_site.dung(ra=SITE, chep_assets=False, log=lambda s: None)
    web = May(("127.0.0.1", port), Web)
    print("Xem web:        http://localhost:%d/" % port)
    print("Trang quan tri: http://localhost:%d/admin/   (bam Luu la ghi thang vao data/)" % port)
    if mo_trinh_duyet:
        import webbrowser
        webbrowser.open("http://localhost:%d/admin/" % port)
    try:
        web.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    port = int(sys.argv[sys.argv.index("--port") + 1]) if "--port" in sys.argv else int(os.environ.get("PORT") or 8080)
    chay(port, "--mo" in sys.argv)
