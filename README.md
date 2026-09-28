# quocanstudio.vn — Website Quốc An Studio

Website tĩnh (HTML/CSS/JS) + **trang quản trị `/admin`** (Decap CMS) để sửa nội dung trên
điện thoại/máy tính, không cần đụng code. Chuyển sang cách làm này ngày 11/09/2026.

## ⭐ Cách làm việc

```
templates\*.html  (khung 6 trang, giữ nguyên thiết kế)
      +                                  tools\build_site.py
data\*.json       (nội dung sửa được)  ───────────────────────►  _site\   (web hoàn chỉnh)
```

| Muốn làm gì | Làm ở đâu |
|---|---|
| Sửa **giá, gói**, đội ngũ, đánh giá, việc làm, banner, hotline, tài khoản ngân hàng | **Trang quản trị** `https://quocanstudio.vn/admin` (điện thoại hoặc máy tính) |
| Thêm **album** vài ảnh | Trang quản trị → 📷 Bộ sưu tập → *Add album* |
| Thêm **nhiều ảnh một lúc** (cả buổi chụp) | Bỏ vào thư mục trong BT3 → `CAP NHAT WEB.bat` → **1** → **3** |
| Sửa bố cục, màu sắc, chữ cố định (giới thiệu, thế mạnh...) | `templates\*.html`, `assets\css\style.css` (nhờ hỗ trợ) |

**Trên web thật:** bấm **Công bố** trong trang quản trị → nội dung lưu vào GitHub → Netlify tự
dựng lại web, khoảng 1 phút sau là thấy (Ctrl+F5 nếu vẫn thấy bản cũ).

**Trên máy (không cần mạng):** `CAP NHAT WEB.bat` → **2** mở web + trang quản trị ở
`http://localhost:8080/admin/` (bấm *Đăng nhập* là vào, không mật khẩu). Bấm *Công bố* là ghi thẳng
vào `data\` và dựng lại web ngay. Nhớ chọn **3** để đưa các thay đổi đó lên web thật.

### Menu `CAP NHAT WEB.bat`

| Số | Việc |
|---|---|
| **1** | Cập nhật ảnh từ thư mục BT3: lấy bản mới từ GitHub → quét ảnh → Bộ sưu tập (loại ảnh trùng) → nhạc nền mới trong `mp3\` → kiểm tra lỗi → dựng web + zip |
| **2** | Mở trang quản trị + xem thử web trên máy |
| **3** | Đưa lên web (GitHub → Netlify; nếu chưa có GitHub mà có FTP thì gửi qua FTP) |
| 4 | Kiểm tra ảnh / link hỏng |
| 5 | Lấy bản mới nhất từ GitHub (sau khi sửa trên điện thoại) |
| 6 | Mở thư mục `_site` |
| **7** | Kết nối GitHub lần đầu (dán link kho — tự điền cấu hình trang quản trị rồi gửi web lên) |

**Quan trọng:** trước khi sửa trên máy, công cụ tự *lấy bản mới* (mục 1 làm sẵn) để không ghi đè
những gì đã sửa trên điện thoại.

### Trang quản trị có những mục nào

| Mục | Sửa được | Tự cập nhật theo |
|---|---|---|
| 💰 Bảng giá | 6 khối (thêm/xoá/kéo đổi thứ tự), từng gói: tên, giá, nhãn, nổi bật, danh sách, quà tặng; bảng giá tiệc; ảnh bảng giá; ô lưu ý; 3 thẻ giá tóm tắt ở Trang chủ | Ô *Gói quan tâm* trong form Liên hệ |
| 📷 Bộ sưu tập | Thêm/sửa/xoá album, chọn danh mục, ảnh bìa, từng ảnh | — |
| 👥 Đội ngũ | Thành viên: ảnh, tên, chức danh, giới thiệu, Facebook, nhãn | — |
| ⭐ Đánh giá | Điểm Fanpage/Google, từng đánh giá (thẻ lớn + polaroid, thẻ nhỏ) | — |
| 📝 Tuyển dụng | Vị trí, nhãn, mô tả/yêu cầu/quyền lợi | Ô chọn vị trí trong form ứng tuyển |
| 🖼️ Banner | Ảnh chạy trên banner trang chủ | — |
| 🎵 Nhạc nền | Bật/tắt, file nhạc, ghi nguồn, âm lượng | Nút 🎵 góc trái dưới + dòng ghi nguồn ở chân trang |
| 📞 Liên hệ | Địa chỉ, hotline, Zalo, email, giờ mở cửa, Fanpage, Instagram, tài khoản ngân hàng + QR | Đầu trang, chân trang, nút nổi, khối thanh toán, trang Liên hệ, form (email nhận) |

Ảnh tải lên qua trang quản trị nằm ở `assets\uploads\`; trên Netlify được **tự thu nhỏ/cắt**
theo chỗ dùng (Netlify Image CDN) nên cứ tải ảnh gốc từ điện thoại. Trang quản trị chỉ thêm
**từng ảnh một** — buổi chụp nhiều ảnh thì dùng thư mục + mục 1 cho nhanh.

Album từ thư mục (ảnh trong `assets\img\bo-suu-tap\`) được mục 1 dựng lại mỗi lần; album thêm
trên trang quản trị (ảnh trong `assets\uploads\`) **luôn được giữ nguyên**.

### Quy ước Bộ sưu tập (từ 11/09/2026)

- **Thứ tự album: theo ngày, từ cũ đến mới** trong mỗi danh mục. Ngày lấy từ *ngày chụp ghi trong
  ảnh* (EXIF máy ảnh); ảnh không có (vd tải từ Facebook) thì lấy *ngày của file*. Album thêm trên
  trang quản trị dùng ô **Ngày chụp** (mặc định là ngày thêm). Muốn đảo lại mới → cũ: đổi
  `THU_TU = "moi-truoc"` trong `tools\bo_suu_tap.py` và `THU_TU_ALBUM` trong `tools\build_site.py`.
- **Tên cặp đôi: CHÚ RỂ & CÔ DÂU.** Thư mục mới nên đặt sẵn theo thứ tự này. Thư mục đang ghi cô dâu
  trước thì thêm tên (viết thường, bỏ dấu) vào `DAO_TEN` trong `tools\bo_suu_tap.py` để web tự đảo.
- **Tên hiển thị / sửa chính tả tên thư mục:** thêm vào `TEN_DEP` (vd `PHOM TRƯỜNG` → *Phim trường*,
  `VIÊN CHUYÊN TU` → *Viện Chuyên Tu*, `SÂN GOLD` → *Sân golf*, `PSC KIỀU DIỄM` → *Kiều Diễm*).
- **Danh mục Đám hỏi** lấy từ thư mục `HÌNH ĐÁM HỎI\`. **Gia đình & Baby** lấy từ cả
  `BABY & GIA ĐÌNH\` và `GIA ĐÌNH & BABY\`.
- Hai thư mục ra cùng tên file (vd `PHONG XÁM\01` và `PHONG XÁM 01`) được tự đánh số khác nhau để
  không ghi đè ảnh; `PHONG XÁM 01` / `PHONG ĐỎ 01` (thư mục riêng) hiển thị là *Phông xám 02* / *Phông đỏ 02*.

### 🎵 Nhạc nền (từ 11/09/2026)

- **Đổi bài:** bỏ file nhạc (mp3/m4a/wav) vào `D:\BT3\mp3\` → `CAP NHAT WEB.bat` → **1**. Bài **mới nhất**
  trong thư mục được nén còn 128 kbps (~3–4 MB) thành `assets\audio\nhac-nen.mp3`, tên bài/tác giả lấy
  từ file để ghi nguồn ở chân trang (`tools\nhac_nen.py`, cần 2 gói Python `miniaudio` + `lameenc` — đã cài).
  Hoặc đổi trong trang quản trị → 🎵 Nhạc nền (tắt hẳn: bỏ tick *Bật nhạc nền*).
- **Cách phát:** trình duyệt (Chrome, Safari iPhone, Facebook/Zalo) **không cho tự phát nhạc có tiếng** khi
  vừa mở trang → nhạc bắt đầu ở **lần chạm/bấm đầu tiên**. Âm lượng 30%, tăng dần, phát lặp. Sang trang
  khác nghe tiếp đoạn đang nghe; chuyển tab/app thì tạm dừng. Khách bấm 🎵 để tắt → web nhớ, không tự bật
  lại. Bật chế độ tiết kiệm dữ liệu thì không tự phát. File chỉ tải khi phát (không làm chậm trang).
- **Bản quyền — chỉ dùng nhạc có giấy phép.** Nhạc tải từ YouTube, bài hát thương mại (kể cả bản
  cover/piano/slowed) đều vi phạm. Bài đang dùng: **Piano Moment — Good_B_Music**, tải từ
  [Pixabay Music](https://pixabay.com/music/solo-piano-piano-moment-9835/) ngày 11/09/2026, giấy phép Pixabay
  (dùng thương mại miễn phí). Thông tin giấy phép lưu ở `mp3\GIAY-PHEP-NHAC-NEN.txt`. Bài cũ (Happy Memories,
  Uppbeat — giấy phép miễn phí chưa rõ cho web doanh nghiệp) để ở `mp3\cu\`.
- Khi nén, khoảng lặng đầu/cuối bài được cắt để phát lặp không bị hụt. File không ghi sẵn tên bài/tác giả
  (như file Pixabay) thì điền ô *Ghi nguồn* trong trang quản trị.
- Nhạc gốc trong `mp3\` không đưa lên GitHub (chỉ bản đã nén trong `assets\audio\`).

## 🚀 Đưa web lên mạng (làm 1 lần — anh tự làm các bước tài khoản)

1. **GitHub — ĐÃ XONG (28/09/2026):** kho `qt16tc32nghoainam-a11y/website-Wedding`, nhánh `main`.
   Máy đã nhớ kho này (`git remote origin`, dùng HTTPS vì máy chưa cài khoá SSH) và tên kho cũng
   đã ghi trong `admin\config.yml`.
2. **Gửi bản mới lên:** nhấp đúp `CAP NHAT WEB.bat` → **3**. (Kho khác: mục **7** rồi dán link kho.)
   Lần đầu Windows mở trang đăng nhập GitHub → anh đăng nhập để cho phép. ~219 MB, 5–15 phút tuỳ mạng.
3. **Netlify:** vào app.netlify.com → *Sign up with GitHub* → *Add new site → Import an existing
   project → GitHub* → chọn `website-Wedding` → *Deploy*. Netlify tự đọc `netlify.toml`
   (lệnh dựng `python tools/build_site.py`, thư mục `_site`). Có ngay link `xxx.netlify.app`.
4. **Cho phép đăng nhập trang quản trị bằng GitHub:**
   - GitHub → *Settings → Developer settings → OAuth Apps → New OAuth App*:
     Homepage URL = link Netlify (hoặc `https://quocanstudio.vn`),
     Authorization callback URL = `https://api.netlify.com/auth/done` → *Register* →
     chép **Client ID**, bấm *Generate a new client secret* → chép **Client secret**.
   - Netlify → site → *Site configuration → Access & security → OAuth → Install provider →
     GitHub* → dán Client ID + Client secret. **(Anh tự dán — không gửi mã này cho ai.)**
5. **Tên miền:** Netlify → *Domain management → Add a domain* → `quocanstudio.vn` → làm theo
   hướng dẫn DNS, nhập ở trang quản lý tên miền Mắt Bão. Netlify tự cấp HTTPS.
6. Mở `https://quocanstudio.vn/admin` → *Đăng nhập với GitHub* → sửa thử.
7. **Nhân viên muốn sửa** (vd chị Huyền): tạo tài khoản GitHub riêng → anh vào kho →
   *Settings → Collaborators → Add people*.

Sau khi web chạy thật: kích hoạt FormSubmit một lần cho mỗi form (xem mục Form bên dưới).

## Cấu trúc thư mục

```
D:\BT3\
├── CAP NHAT WEB.bat     Menu công cụ (nhấp đúp)
├── netlify.toml         Cấu hình Netlify
├── admin\               Trang quản trị: index.html + config.yml (các ô nhập tiếng Việt)
├── data\                NỘI DUNG: bang-gia, bo-suu-tap, doi-ngu, danh-gia, tuyen-dung, banner, lien-he (.json)
├── templates\           KHUNG 6 trang. <!-- CMS:ten-khoi --> và {{bien}} được điền từ data\
├── assets\              css, js, img (ảnh web), audio (nhạc nền), uploads (ảnh tải lên qua trang quản trị)
├── tools\               build_site.py (dựng web), bo_suu_tap.py (ảnh từ thư mục),
│                        capnhat.py (menu), cms_server.py (trang quản trị trên máy)
├── _site\               Web hoàn chỉnh — TỰ SINH, không sửa tay
├── _backup_truoc_cms\   Bản 6 trang HTML trước khi chuyển sang trang quản trị
└── HÌNH..., MÂM QUẢ\, hậu trường\, ...   Ảnh gốc (không đưa lên GitHub — xem .gitignore)
```

> Các mục hướng dẫn cũ bên dưới có nhắc sửa `index.html`, `bang-gia.html`... — từ 11/09/2026
> nội dung đó sửa trong **trang quản trị**; phần bố cục cố định nằm trong `templates\`.

## Cách xem

`CAP NHAT WEB.bat` → **2**, hoặc chạy:

```bash
cd D:/BT3 && python tools/cms_server.py --port 8080
```

Rồi mở `http://localhost:8080` (web) và `http://localhost:8080/admin/` (trang quản trị).
Chỉ dựng web: `python tools/build_site.py` → kết quả trong `_site\`.

## Cần bạn thay thế

### 1. Ảnh bìa (banner) — ĐÃ XONG

12 ảnh trong thư mục `ẢNH BANNER` đã được cắt sang **khổ ngang** và nén cho web:

| File | Kích thước | Dùng khi |
|---|---|---|
| `banner-01.jpg` … `banner-12.jpg` | 1600×900 | Máy tính |
| `banner-m01.jpg` … `banner-m12.jpg` | 1080×810 | Điện thoại (cắt sát hơn, vẫn khổ ngang) |
| `about.jpg` | 900×1125 | Ảnh khối "Về chúng tôi" |

Slider tự chạy, đổi ảnh mỗi 5,5 giây, có 12 chấm để bấm chuyển tay.
Ảnh **nạp dần khi tới lượt** (chỉ tải ảnh đang xem + ảnh kế tiếp) nên web vẫn nhẹ.

**Thêm / bớt ảnh banner:** mở `index.html`, tìm khối `<div class="hero__slides">`.
Mỗi ảnh là 1 dòng, copy rồi sửa số thứ tự:

```html
<div class="hero__slide" data-bg="assets/img/banner-13.jpg" data-bg-m="assets/img/banner-m13.jpg"></div>
```

Ảnh gốc trong thư mục `ẢNH BANNER`, file `AO7A2636.jpg` và file QR `1788948....jpg`
**không được website dùng** — xoá được trước khi đưa lên hosting cho nhẹ.

### 1b. Slogan trên banner

Slogan **"Phim trường độc quyền · Ngoại cảnh trọn gói"** nằm ở `index.html`, thẻ
`<p class="hero__slogan">` — sửa chữ trực tiếp tại đó.

### 2. Bộ sưu tập — 89 album / 1306 ảnh · 10 danh mục (cập nhật 11/09/2026)

Mỗi thẻ ngoài lưới là **một album**, bấm vào xem toàn bộ ảnh của album đó.

| Danh mục | Album |
|---|---|
| Ngoại cảnh (4) | **Biển 01(10)** *(ảnh tải từ Facebook 1366×2048 — đủ nét ở cỡ web 1000px)* · Biển 02(6) · Nhà thờ Song Vĩnh(13) · Phim trường An Garden(8) |
| **Phim trường** (5) | Back rêu(10) · Cầu thang(25) · Cửa cổ điển(18) · **Đài phun nước(14)** · Góc bàn tiệc(20) |
| Studio (14) | Bàn tiệc(20) · **Bàn tiệc phông vô cực(16)** · Couple(24) · **Khóm hoa nâu(18)** · Phông đen 01/02/03(8/30/26) · Phông trắng khóm hoa 01/02(24/7) · Phông xám(38) · **Rèm trắng & hoa tím(31)** · Trái tim đỏ(29) · Tường nhám(6) · **Vải đỏ & khóm hoa(10)** |
| **Concept Beauty** (1) | **Dâu đơn(9)** — thư mục `CONCEPT BEAUTY/LAYOUR DÂU ĐƠN/` |
| Make-up (7) | Hương Ly(6) · **Minh Anh(11)** · Mỹ Tâm 01(8) · Mỹ Tâm 02(11) · Thu Thảo(7) · Tiên An(12) · Đỗ Quyên(8) |
| **Phóng sự cưới** (1) | **Ngọc Quang & Kiều Phúc(37)** — lễ dạm ngõ, từ thư mục `Hình PSC/` |
| **Mâm quả cưới hỏi** (3) | Mâm dạm ngõ(10) · Mâm quả hiện đại(42) · Mâm quả truyền thống(8) — từ thư mục `MÂM QUẢ/` |
| Hậu trường (6) | Hương Vy(3) · Kim Công & Uyên Vi(4) · Ngọc Anh & Mỹ Tâm(17) · Quốc Anh & Phương Bùi(10) · Tiên An(5) · Đỗ Quyên(5) |

**Concept Beauty** nằm giữa *Studio* và *Make-up cô dâu*. Thư mục `CONCEPT BEAUTY/` đã tạo
sẵn trong BT3 — mỗi thư mục con (ví dụ `CONCEPT BEAUTY/TÊN CÔ DÂU/`) là một album; bỏ ảnh
thẳng vào `CONCEPT BEAUTY/` thì thành một album chung.

**Tên album = tên thư mục** (tự viết hoa chữ đầu, giữ dấu). Đổi tên thư mục thì tên file
ảnh trong `assets/img/bo-suu-tap/` cũng đổi theo.

#### Ảnh trang chủ & trang Đội ngũ — thư mục `assets/img/chon-loc/`

8 ảnh trang chủ (4 hậu trường + 4 ảnh "Bộ sưu tập") và 4 ảnh hậu trường ở trang Đội ngũ
dùng **bản chép riêng** trong `assets/img/chon-loc/`, không trỏ thẳng vào
`assets/img/bo-suu-tap/`. Lý do: ngày 11/09/2026 đổi tên thư mục `hậu trường/01…04` sang
tên cặp dâu rể làm tên file đổi theo, 8 ảnh trên hai trang này bị mất. Giờ dựng lại
Bộ sưu tập bao nhiêu lần cũng không ảnh hưởng hai trang đó. Muốn đổi ảnh: ghi đè file
trong `chon-loc/` (giữ nguyên tên).

Bộ dựng đọc được cả **JPG và PNG** (PNG có nền trong suốt được lót nền trắng). Album
*Kim Công & Uyên Vi* có 1 ảnh PNG (`053A0088.png`).

**Còn để trống:** Gia đình & Baby (thư mục `GIA ĐÌNH & BABY/` đã tạo sẵn)

**Mâm quả** — thư mục con `DẠM NGỎ`, `HIỆN ĐẠI`, `TRUYỀN THỐNG` hiển thị thành *Mâm dạm ngõ*,
*Mâm quả hiện đại*, *Mâm quả truyền thống* (tên đặt trong `TEN_DEP` của bộ dựng; tên thư mục
ghi "NGỎ" nhưng web hiện đúng chính tả "ngõ"). Loại 1 ảnh có logo **TÂM PHƯỢNG WEDDING**
(`MÂM QUẢ/HIỆN ĐẠI/1789100777344_…d3351f266eaf62a126548702277973a0.jpg`) và 6 ảnh trùng.

**Phóng sự cưới** lấy từ thư mục `Hình PSC/`, mỗi thư mục con đặt theo tên cặp dâu rể
(ví dụ `Hình PSC/NGỌC QUANG & KIỀU PHÚC/`) là một album. Ảnh ở đây là **trang album
dàn sẵn** (bìa dọc + trang đôi ngang), nên ảnh ngang được xuất rộng 1400px (ảnh dọc
vẫn 1000px) cho chữ và ảnh nhỏ trong trang không bị nhoè. Thứ tự trang giữ đúng theo
số đầu tên file — trang bìa *"Memorable Day"* là ảnh bìa album.

#### Ảnh đã loại (22 tấm)

- `NHÀ THỜ SONG VĨNH/dp1.jpg` — in chữ *"THE WEDDING PHOTOBOOK by FOXY STUSIO"*
- `MÂM QUẢ/HIỆN ĐẠI/1789100777344_….jpg` — logo *"TÂM PHƯỢNG WEDDING"*
- 20 ảnh trùng, dò bằng perceptual hash trên toàn bộ ảnh nguồn (danh sách trong `_trung.txt`)

#### Cấu trúc thư mục — hỗ trợ 3 cấp

```
HÌNH STUDIO/CONCEPT COUPLE/            -> 1 album "Couple"
HÌNH STUDIO/Concept Phông đen/01/      -> album "Phông đen 01"
                              /02/     -> album "Phông đen 02"
```

- Concept **có ảnh trực tiếp** → 1 album
- Concept **chia 01, 02, 03…** → mỗi thư mục con là 1 album riêng
- Tên album lấy từ tên thư mục, bỏ chữ `CONCEPT` / `GÓC` / `SET` ở đầu

| Danh mục web | Thư mục gốc |
|---|---|
| Ngoại cảnh | `HÌNH NGOẠI CẢNH/` |
| Phim trường | `PHIM TRƯỜNG ĐỘC QUYỀN STUDIO QUỐC AN/` |
| Studio | `HÌNH STUDIO/` |
| Make-up cô dâu | `layour makeup/` |
| Hậu trường | `hậu trường/` |

#### ⚠️ Hai tên album em đặt khác tên thư mục

| Thư mục | Tên trên web | Vì sao |
|---|---|---|
| `PHÒNG XÂM` | **Phông xám** | Ảnh chụp nền phông xám, không liên quan xăm hình |
| `CONCEPT STUDIO` | **Rèm trắng & hoa tím** | Để "Studio" thì thẻ đọc thành *Studio / Studio*, trùng tên danh mục |

Muốn giữ đúng tên thư mục thì đổi tên thư mục rồi báo dựng lại.

### 2b. Trang Đội ngũ — `doi-ngu.html`

Trang riêng, đã thêm vào menu chính (giữa *Bảng giá* và *Tuyển dụng*) và footer cả 6 trang.

Gồm 4 phần:

1. **Thành viên** — lưới thẻ nhân viên: ảnh đại diện tròn, tên, chức danh, mô tả ngắn,
   nút **Facebook** dẫn thẳng tới trang cá nhân
2. **Vai trò** — 6 thẻ: Photographer · Make-up artist · Ê-kíp set dáng · Stylist trang phục ·
   Hậu kỳ · Tư vấn & giữ lịch
3. **Hậu trường** — 4 ảnh ê-kíp đang làm việc, bấm xem lớn được
4. **CTA** — dẫn sang trang Tuyển dụng

Trang chủ giữ lại mục Đội ngũ ngắn gọn (4 ảnh hậu trường) kèm nút **Xem đội ngũ studio**.

#### Đã điền: 7 thành viên (còn 2 ô "Đang cập nhật": Ê-kíp set dáng, Hậu kỳ)

| # | Tên | Chức danh | Ảnh | Facebook |
|---|---|---|---|---|
| 1 | Quốc An | Owner *(nhãn Người sáng lập)* | `nv-01.jpg` | facebook.com/lu.vic.509 |
| 2 | Dương Huyền | **Quản lý & Make-up Artist** — *"Quản lý nhân sự, phụ trách chuyên môn Makeup và Đào tạo học viên chuyên nghiệp – nâng cao."* | `nv-02.jpg` | facebook.com/duong.huyen.869417 |
| 3 | Trọng Linh | Photographer | `nv-03.jpg` | facebook.com/hoang.vann.linh |
| 4 | Hoài Nam | Photographer | `nv-04.jpg` | facebook.com/nguyen.hoai.nam.889657 |
| 5 | Minh Thuận | Stylist &amp; Support | `nv-05.jpg` | facebook.com/ben1x0 |

**Minh Thuận** — ảnh gốc `đội ngũ/photo/053A0035.jpg` (ảnh studio trắng đen), cắt vuông
500×500 phần đầu – vai thành `assets/img/doi-ngu/nv-05.jpg`, khai báo ở `data/doi-ngu.json`.
Facebook hiển thị tên *"Nguyễn Bùi Minh Thuận"* — web để **Minh Thuận**.

**Thành viên 06 — Quỳnh Như**, Make-up & Chăm sóc khách hàng, ảnh `nv-06.jpg`,
facebook.com/le.quynh.nhu.453725. Điền vào ô trống *"Make-up artist"* cũ. Ảnh cắt từ `đội ngũ/makeup và chăm sóc khách hàng/`.
Facebook hiển thị tên *"Lê Quỳnh Như"* — web để **Quỳnh Như**.

**Thành viên 07 — Hải Yến**, Make-up & Chăm sóc khách hàng, ảnh `nv-07.jpg`,
facebook.com/le.thi.hai.yen.751554 (link gốc, đổi từ link rút gọn `facebook.com/share/…`).
Ảnh cắt sát mặt từ `đội ngũ/makeup và chăm sóc khách hàng/1789096783366_…jpg` để tránh
lẫn các gương mặt trên poster phía sau. Facebook hiển thị *"Lê Thị Hải Yến (Hải Yến Makeup
Artist)"* — web để **Hải Yến**.

Ảnh Hoài Nam lấy từ `đội ngũ/photo/560621644_…_n.jpg` (ảnh gốc chỉ 640×960, cắt vuông phần
đầu vai). Facebook hiển thị tên *"Nguyễn Hoài Nam"*, giới thiệu *"HOÀI NAM PHOTO"* — web để
**Hoài Nam** cho đồng bộ với thẻ Trọng Linh.

Ảnh cắt vuông 500×500 từ `đội ngũ/owner/`, `đội ngũ/Makeup Artis/` và `đội ngũ/photo/`.

⚠️ **Tên "Trọng Linh"** — Facebook hiển thị *"Hoàng Trọng Lyng"*, phần giới thiệu ghi
*"TRỌNG LINH PHOTO"*. Em để **Trọng Linh** theo tên thương hiệu. Muốn ghi đủ họ tên thì
sửa thẻ `<h3>` trong `doi-ngu.html`.

Link anh gửi là dạng rút gọn `facebook.com/share/...`. Em đổi sang **link gốc** vì link
rút gọn có thể hết hạn, link gốc thì không.

Thẻ owner được làm nổi hơn: viền vàng, ảnh to hơn, có nhãn *Người sáng lập* phía trên.

**Tên "Dương Huyền"** — đã chốt theo yêu cầu (11/09/2026), bỏ dòng "theo nghề từ năm 2022",
thay bằng *"Đào tạo make-up chuyên nghiệp"*. Tên chủ tài khoản ngân hàng ở khối thanh toán
vẫn giữ đúng *"DƯƠNG THỊ NGỌC HUYỀN"* như trên mã QR.

#### ⚠️ Còn 2 thẻ chờ điền

2 thẻ còn lại (Ê-kíp set dáng, Hậu kỳ) vẫn ghi *"Đang cập nhật"*, dùng ảnh đại diện mặc định. Cách điền:

**Bước 1 — ảnh:** chép ảnh chân dung vào `assets/img/doi-ngu/`, đặt tên `nv-01.jpg`,
`nv-02.jpg`… Ảnh nên **vuông** (ví dụ 500×500), chụp nửa người là đẹp nhất.

**Bước 2 — thông tin:** mở `doi-ngu.html`, ngay trên lưới thành viên có **mẫu một thẻ
đã điền đầy đủ** trong phần ghi chú — copy rồi thay 4 chỗ: đường dẫn ảnh, tên,
chức danh, link Facebook.

Muốn thêm/bớt người thì copy hoặc xoá cả khối `<article class="member">`.
Lưới tự dàn lại, không cần sửa gì thêm.

Hoặc gửi em: **ảnh + tên + chức danh + link Facebook** của từng người, em điền giúp.

### 3. Mã QR Google Map & mục Đánh giá khách hàng

**QR + nút "Chỉ đường"** (trang chủ và Liên hệ) giờ mở thẳng trang **"Studio Quốc An"**
trên Google Maps: `https://www.google.com/maps?cid=17296204885652745400` (5,0 sao,
1701 Đ. Hùng Vương). Khách bấm "Viết bài đánh giá" ở đó.

Trang Google Maps này **chưa được chủ xác nhận** ("Xác nhận doanh nghiệp này"). Nên xác nhận
qua Google Business Profile: được trả lời đánh giá, thêm ảnh, giờ mở cửa, website
quocanstudio.vn — và lấy link ngắn mở thẳng ô viết đánh giá (dạng
`https://g.page/r/xxxxxxxx/review`) để thay vào QR.

**Mục "Feedback khách hàng"** — trang chủ, `<section id="khach-hang">` (làm lại 11/09/2026 theo mẫu
poster Quốc An: ảnh cưới **khung dọc 2:3 đúng tỉ lệ ảnh Bộ sưu tập → hiện trọn ảnh, không cắt, không chữ đè lên ảnh** · logo + slogan · "FEEDBACK / Khách Hàng ♡" ·
thẻ đánh giá kiểu Facebook hoặc Google · "Thank you — vì đã tin tưởng Studio Quốc An" · thanh 4 biểu tượng
*Ảnh đẹp tự nhiên / Váy cưới đa dạng / Makeup chuyên nghiệp / Ekip nhiệt tình* + Nhơn Trạch, Đồng Nai).

- **32 đánh giá thật**: 29 trên Fanpage (chép nguyên văn từ 8 ảnh chụp màn hình trong
  `ĐÁNH GIÁ CỦA KHÁCH HÀNG\PAGE\`, từ 12/2024 đến 9/2026) + 3 Google Maps, mỗi đánh giá có thư mục riêng
  (ảnh cưới + ảnh chụp đánh giá) và được *Ghim*: Kim Công & Uyên Vi (*uyên vi nguyễn thị*, 11/09/2026),
  Hoàng Vũ & Thúy Vân (*time belong*, 12/09/2026), Minh Hiếu & Hồng Liên (*Minh hiếu Nguyễn*, 13/09/2026 —
  ảnh `minh-hieu-hong-lien.jpg`, ảnh chụp gốc `khach-hang-03.jpg`). Trang ghi *98% đề xuất (38 lượt đánh giá)*.
  **Thêm đánh giá có thư mục riêng:** ảnh cưới cắt đúng 2:3 → 720×1080, ảnh đại diện 140×140, ảnh chụp màn hình
  bỏ thanh trạng thái → `khach-hang-NN.jpg` (+ bản `-thumb` rộng 600). **Không đăng** đánh giá của *Quốc Thanh* vì khách chọn *không đề xuất*.
  Đánh giá *Huy Nguyen* bị cắt ở mép ảnh chụp nên chưa có nội dung — chụp lại thì thêm được.
- **Lướt qua lại** (nút ‹ › , vuốt trên điện thoại, tự chuyển 8 giây khi đang xem, dừng khi rê chuột).
  Xếp **mới nhất trước**; đánh giá được *Ghim* lên đầu. Lời dài hiện 8 dòng + nút *Xem thêm*.
  Chỉ tải ảnh của đánh giá đang xem và kế tiếp → web vẫn nhẹ.
- **Ảnh bên trái tự chọn** (`tools\chon_anh_dep.py`, chạy trong mục 1 của `CAP NHAT WEB.bat`): chấm điểm
  mọi ảnh trong Bộ sưu tập (ảnh dọc, nét, đủ sáng, có màu, không phải trang album/ảnh ghép) →
  lấy tối đa 2 ảnh/album. Đánh giá nhắc *makeup / trang điểm* → ảnh cô dâu (mục Make-up); còn lại → ảnh
  cặp đôi (Ngoại cảnh, Phim trường, Studio). 30 đánh giá = 30 ảnh khác nhau. Ghi đè bằng ô **Ảnh bên trái**
  hoặc **Album liên quan** trong trang quản trị. Đang ghi đè: Uyên Vi (ảnh hậu trường Kim Công & Uyên Vi),
  Kiều Diễm (`assets\img\danh-gia\kieu-diem.jpg`, cắt từ trang album phóng sự của chính cô dâu).
- **Ảnh đại diện thật của khách** (theo yêu cầu, để khách thấy đánh giá là thật): cắt từ chính ảnh chụp
  màn hình Fanpage, lưu `assets\img\danh-gia\avatar\<ten-khach>.jpg`. Khách để ảnh mặc định của Facebook
  (Kim Luc, Thu Ngân, Thu Trân) giữ đúng hình người xám mặc định. Đánh giá mới: tải ảnh đại diện vào ô
  *Ảnh đại diện khách* trong trang quản trị (để trống thì hiện chữ cái đầu tên).
- Thêm / sửa đánh giá: trang quản trị → ⭐ Đánh giá khách hàng. **Chỉ đăng đánh giá thật, giữ nguyên lời khách.**

#### Sửa lỗi menu điện thoại (11/09/2026)

Thanh đầu trang dùng `backdrop-filter` (làm mờ nền). Thuộc tính này khiến menu trượt
(`position:fixed`) bị giam trong thanh đầu trang: trên điện thoại bấm ☰ thì menu nằm ngoài
màn hình, chỉ cao 150px, và cả trang bị rộng gấp đôi (707px thay vì 375px). Đã tắt
`backdrop-filter` ở màn hình ≤ 900px — menu giờ trượt vào đủ chiều cao, trang đúng bề ngang.

Hoặc đơn giản hơn: chụp/lưu ảnh QR có sẵn trên tờ rơi thành `assets\img\qr-google-map.png`
rồi đổi thẻ `<img>` thành `<img src="assets/img/qr-google-map.png" alt="...">`.

### 3b. Mã QR ngân hàng — 2 TÀI KHOẢN SONG SONG

Khối **"Chuyển khoản qua VietQR"** ở cuối cả 5 trang, hiện 2 mã QR cạnh nhau:

| Thứ tự | Nhãn | Chủ tài khoản | Số tài khoản | Ảnh |
|---|---|---|---|---|
| 1 | Tài khoản chính | HỘ KINH DOANH QUỐC AN STUDIO | 103887090768 | `assets/img/qr-bank.png` |
| 2 | Tài khoản phụ | HỘ KINH DOANH DƯƠNG THỊ NGỌC HUYỀN | 106887090192 | `assets/img/qr-bank-2.png` |

Cả hai đều VietinBank — CN Nhơn Trạch — Hội Sở, mỗi ô có nút **Sao chép** riêng.

Muốn đổi thứ tự / bỏ bớt: sửa khối `<section class="pay">` trong cả 5 trang
(ô nào mang class `pay__acc--main` thì được làm nổi lên).

### 4. Facebook — ĐÃ XONG

- **Fanpage** (link chính, dùng cho nút Facebook ở đầu trang + footer của cả 5 trang):
  https://www.facebook.com/chupanhdepNhonTrach
- **Facebook cá nhân** (chỉ hiện thêm ở trang Liên hệ):
  https://www.facebook.com/duong.huyen.869417

### 5. Form — ĐÃ GỬI ĐƯỢC VỀ MAIL

Cả **form đặt lịch** (`lien-he.html`) và **form ứng tuyển** (`tuyen-dung.html`) đã gửi thật
về `quocan6339@gmail.com` qua dịch vụ **FormSubmit** — miễn phí, không cần tạo tài khoản.

#### ⚠️ Phải kích hoạt một lần trước khi dùng

FormSubmit chỉ gửi mail sau khi xác nhận chủ hộp thư. Làm đúng 1 lần:

1. Đưa web lên `quocanstudio.vn` xong, vào trang Liên hệ
2. Điền thử một lượt rồi bấm **Gửi yêu cầu**
3. Mở hộp thư `quocan6339@gmail.com` → có mail của FormSubmit → bấm nút xác nhận
4. Từ lần sau mọi thông tin khách điền sẽ về thẳng hộp thư

Làm tương tự một lần nữa cho form ứng tuyển (tiêu đề mail khác nhau nên cần xác nhận riêng).

#### Cách hoạt động

- Khách bấm gửi → FormSubmit nhận → gửi mail → trả khách về `?gui=ok`
- Web thấy `?gui=ok` thì ẩn form đi và hiện lời cảm ơn
- Nút gửi tự khoá lại sau khi bấm, tránh khách bấm hai lần
- Có ô bẫy spam ẩn (`_honey`), không cần khách nhập captcha

#### Muốn đổi mail nhận

Sửa `action="https://formsubmit.co/mail-moi@..."` trong cả 2 file, rồi kích hoạt lại.

**Ẩn địa chỉ mail:** sau khi kích hoạt, FormSubmit cấp một mã ngẫu nhiên dạng
`https://formsubmit.co/xxxxxxxxxxxx`. Thay mã đó vào `action` thì địa chỉ mail không
còn lộ trong mã nguồn trang — nên làm để tránh spam.

### 6. Bảng giá — CẬP NHẬT 10/09/2026

Gõ lại từ 11 tấm bảng giá trong thư mục `bảng giá`, chia 5 nhóm + gallery ảnh gốc:

| Nhóm | Neo | Giá |
|---|---|---|
| Gói cưới trọn gói (4 gói) | `#goi-cuoi` | 6.000.000đ – 13.900.000đ |
| **Gói đám hỏi** *(mới)* | `#dam-hoi` | 4.900.000đ |
| Gói chụp album cưới (5 gói) | `#album` | 6.900.000đ – 9.900.000đ |
| Gói ảnh cổng (2 gói × 2 chất liệu) | `#anh-cong` | 1.800.000đ – 4.200.000đ |
| **Chụp tiệc cưới** *(mới)* | `#tiec-cuoi` | 2.000.000đ – 5.500.000đ |
| Bảng giá dạng ảnh (11 poster) | `#bang-gia-anh` | — |

**Thay đổi so với bảng giá cũ:**

| Gói | Cũ | Mới |
|---|---|---|
| 1 ngày cưới Cơ Bản | 6.500.000đ | **6.000.000đ** |
| 1 ngày cưới VIP | 7.500.000đ | **7.000.000đ** |
| 2 ngày cưới Cơ Bản | 13.500.000đ | **11.500.000đ** |
| 2 ngày cưới VIP | 15.500.000đ | **13.900.000đ** |
| Gói ảnh cổng 1 tấm | 7 ảnh chỉnh sửa | **6 ảnh chỉnh sửa** |

Giá 5 gói album và gói ảnh cổng giữ nguyên. Quà tặng gói 2 ngày bỏ dòng *"kèm nơ cho nam"*.

Trang chủ và ô "Gói quan tâm" trong form đặt lịch đã đồng bộ theo giá mới.

Địa chỉ trên web giữ nguyên **1701 Đ. Hùng Vương** (đã xác nhận) — xem mục 10.

### 7. Bộ nhớ đệm trình duyệt

Link CSS/JS có gắn số phiên bản: `style.css?v=20260910`. **Mỗi lần sửa file CSS hoặc JS,
đổi số này** (ví dụ `?v=20260911`) trong cả 5 trang, để khách không bị xem bản cũ.

### 8. Logo — ĐÃ XONG

Dùng đúng file PNG nền trong suốt anh gửi trong thư mục `logo`. Logo vàng nổi thẳng
trên nền tối, không cần tấm lót:

| File | Kích thước | Dùng ở đâu |
|---|---|---|
| `assets/img/logo-mark.png` | 300×191 | Đầu trang — chữ lồng QA, cao 52px |
| `assets/img/logo-full.png` | 620×448 | Cuối trang — logo đầy đủ, rộng 210px |
| `assets/img/favicon.png` | 180×180 | Biểu tượng trên tab trình duyệt (nền tối bo góc) |

Muốn đổi logo khác: ghi đè 3 file trên, giữ nguyên **nền trong suốt (PNG)** vì đầu trang
và cuối trang đều nền tối.

Ảnh gốc trong thư mục `logo` **website không dùng** — xoá được trước khi lên hosting.

### 9. Thế mạnh: phim trường độc quyền

Trang chủ có khối riêng nền tối **"Phim trường ngoại cảnh độc quyền ngay tại studio"**
(`index.html`, `<section class="usp" id="phim-truong">`) với 5 luận điểm:
không phát sinh phí thuê cảnh · không phải đi xa · lịch chụp chủ động · nhiều góc cảnh
trong một buổi · chủ động dựng đạo cụ và concept hot trend.

Bên dưới 5 ô đó là khối nhấn mạnh **"Chỉ chụp ảnh cổng thôi cũng đã có view ngoại cảnh"**
(`.usp__hl`) — so sánh với việc nơi khác phải đặt gói album ngoại cảnh mới có được.

Ở trang Bảng giá, gói **Phim trường tại Studio (6.900.000đ)** được gắn nhãn
*"Phim trường độc quyền"* và làm nổi lên.

Muốn sửa lời văn: mở `index.html`, tìm `id="phim-truong"`.

## Thông tin đang dùng trên website

- **Tên**: Quốc An Studio — Wedding Photography
- **Địa chỉ**: 1701 Đ. Hùng Vương, Phước An, Đồng Nai
- **Hotline**: 0354 501 333 (Mr An) — 0334 923 634 (Mrs Huyền) — tên người nghe sửa ở trang quản trị → Liên hệ
- **Zalo**: 0334 923 634
- **Fanpage**: https://www.facebook.com/chupanhdepNhonTrach
- **Facebook cá nhân**: https://www.facebook.com/duong.huyen.869417
- **Instagram**: @lu.vic.509 — https://www.instagram.com/lu.vic.509/
- **Email**: quocan6339@gmail.com
- **Giờ mở cửa**: 8:00 – 20:00, Thứ 2 – Chủ nhật
- **Khuyến mãi**: đánh giá 5 sao Google Map → tặng 01 ảnh bàn 15x21 chất liệu Titan
- **Tài khoản nhận tiền / đặt cọc**: HỘ KINH DOANH QUỐC AN STUDIO — 103887090768 —
  VietinBank CN Nhơn Trạch — Hội Sở

Bảng giá đã là **giá thật** theo ảnh anh gửi. Riêng nội dung trang **Tuyển dụng**
(mức lương, số lượng cần tuyển, quyền lợi) vẫn là **số liệu mẫu** — sửa lại trong
`tuyen-dung.html` cho đúng thực tế.

## Đưa lên tên miền quocanstudio.vn

Website tĩnh nên chỉ cần upload toàn bộ thư mục lên hosting:

- **Hosting thường (cPanel)**: upload hết vào thư mục `public_html`.
- **Netlify / Vercel / Cloudflare Pages**: kéo thả cả thư mục, rồi trỏ tên miền về.
- **GitHub Pages**: đẩy code lên repo, bật Pages, thêm file `CNAME` chứa `quocanstudio.vn`.

### 10. Địa chỉ — ĐÃ XÁC NHẬN (11/09/2026)

Địa chỉ đúng là **1701 Đ. Hùng Vương, Phước An, Đồng Nai** — giữ nguyên trên web,
bản đồ nhúng và mã QR Google Map ở trang Liên hệ.

Dòng *"Ấp Vũng Gấm"* chỉ nằm trong ảnh bảng giá gốc (phần *Bảng giá dạng ảnh*), không
phải chữ trên web.
