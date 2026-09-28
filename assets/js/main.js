/* ============================================================
   QUOC AN STUDIO — main.js
   ============================================================ */
(function () {
  'use strict';

  var $  = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---------- 1. Menu mobile ---------- */
  var burger = $('.burger');
  var menu = $('.menu');
  if (burger && menu) {
    burger.addEventListener('click', function () {
      var open = menu.classList.toggle('is-open');
      burger.classList.toggle('is-open', open);
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      document.body.classList.toggle('no-scroll', open);
    });
    $$('.menu a').forEach(function (a) {
      a.addEventListener('click', function () {
        menu.classList.remove('is-open');
        burger.classList.remove('is-open');
        document.body.classList.remove('no-scroll');
      });
    });
  }

  /* ---------- 2. Header dinh khi cuon ---------- */
  var header = $('.site-header');
  if (header) {
    var onScroll = function () {
      header.classList.toggle('is-stuck', window.scrollY > 10);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---------- 3. Slider trang chu ---------- */
  var slides = $$('.hero__slide');
  var dotsBox = $('.hero__dots');
  if (slides.length > 1 && dotsBox) {
    var idx = 0, timer = null;
    var isNarrow = window.matchMedia('(max-width:760px)').matches;

    // Nap anh nen khi toi luot (tranh tai het 12 anh cung luc)
    function loadSlide(n) {
      var el = slides[(n + slides.length) % slides.length];
      if (!el || el.dataset.loaded) return;
      var url = (isNarrow && el.dataset.bgM) ? el.dataset.bgM : el.dataset.bg;
      if (!url) return;
      var pre = new Image();
      pre.onload = function () { el.style.backgroundImage = "url('" + url + "')"; };
      pre.src = url;
      el.dataset.loaded = '1';
    }

    slides.forEach(function (_, i) {
      var b = document.createElement('button');
      b.type = 'button';
      b.setAttribute('aria-label', 'Anh ' + (i + 1));
      if (i === 0) b.classList.add('active');
      b.addEventListener('click', function () { go(i); restart(); });
      dotsBox.appendChild(b);
    });
    var dots = $$('button', dotsBox);

    function go(n) {
      slides[idx].classList.remove('active');
      dots[idx].classList.remove('active');
      idx = (n + slides.length) % slides.length;
      loadSlide(idx);
      loadSlide(idx + 1); // chuan bi truoc anh ke tiep
      slides[idx].classList.add('active');
      dots[idx].classList.add('active');
    }
    function restart() {
      clearInterval(timer);
      timer = setInterval(function () { go(idx + 1); }, 5500);
    }

    // Anh dau tien: nap ngay (ban mobile hoac desktop tuy man hinh)
    slides[0].dataset.loaded = '';
    loadSlide(0);
    loadSlide(1);
    restart();
  }

  /* ---------- 4. Loc bo suu tap (2 cap: danh muc + danh muc con) ---------- */
  var mainBtns = $$('.filters--main button');
  var subWraps = $$('.filters--sub');       // co the co nhieu hang loc con
  var curCat = 'all';
  var curSub = 'all';

  function subCuaCat() {                    // hang loc con cua danh muc dang chon
    return subWraps.filter(function (w) { return w.dataset.parent === curCat; })[0] || null;
  }

  function applyFilter() {
    // Moi phan tu con truc tiep cua luoi (album hoac o trong) deu mang data-cat
    $$('.gallery [data-cat]').forEach(function (el) {
      var okCat = curCat === 'all' || el.dataset.cat === curCat;
      var okSub = curSub === 'all' || el.dataset.sub === curSub;
      el.classList.toggle('is-hidden', !(okCat && okSub));
    });
    subWraps.forEach(function (w) { w.hidden = w.dataset.parent !== curCat; });
  }

  function selectCat(btn) {
    mainBtns.forEach(function (b) { b.classList.remove('active'); });
    btn.classList.add('active');
    curCat = btn.dataset.filter;

    // Vao danh muc co muc con -> chon san muc con dau tien
    var w = subCuaCat();
    var bs = w ? $$('button', w) : [];
    if (bs.length) {
      curSub = bs[0].dataset.sub;
      bs.forEach(function (b, i) { b.classList.toggle('active', i === 0); });
    } else {
      curSub = 'all';
    }
    applyFilter();
  }

  mainBtns.forEach(function (btn) {
    btn.addEventListener('click', function () { selectCat(btn); });
  });

  subWraps.forEach(function (w) {
    $$('button', w).forEach(function (btn) {
      btn.addEventListener('click', function () {
        $$('button', w).forEach(function (b) { b.classList.remove('active'); });
        btn.classList.add('active');
        curSub = btn.dataset.sub;
        applyFilter();
      });
    });
  });

  // Trang thai ban dau: chon danh muc dang duoc danh dau active trong HTML
  if (mainBtns.length) {
    var first = mainBtns.filter(function (b) { return b.classList.contains('active'); })[0] || mainBtns[0];
    selectCat(first);
  }

  /* ---------- 5. Lightbox ---------- */
  var lb = $('.lightbox');
  if (lb) {
    var lbImg = $('.lightbox img', lb);
    var lbCap = $('.lightbox__caption', lb);
    var items = [], cur = 0;

    function collect() {
      items = $$('.card:not(.is-hidden)').filter(function (c) {
        return $('img', c) && !c.classList.contains('album__cover');
      });
    }
    function open(i) {
      cur = (i + items.length) % items.length;
      var el = items[cur];
      var img = $('img', el);
      // Uu tien ban anh lon neu co data-full
      lbImg.src = el.dataset.full || (img ? img.src : '');
      lbImg.alt = el.dataset.title || (img ? img.alt : '');
      if (lbCap) lbCap.textContent = el.dataset.title || (img ? img.alt : '') || '';
      lb.classList.add('is-open');
      document.body.classList.add('no-scroll');
    }
    function close() {
      lb.classList.remove('is-open');
      document.body.classList.remove('no-scroll');
    }

    document.addEventListener('click', function (e) {
      if (!e.target.closest) return;

      // Bam vao bia album -> xem toan bo anh cua cap do
      var alb = e.target.closest('.album');
      if (alb) {
        var ds = $$('.album__photos a', alb);
        if (ds.length) {
          e.preventDefault();
          items = ds;
          open(0);
        }
        return;
      }

      // Cac the anh don le (poster bang gia, anh ngoai trang chu...)
      var card = e.target.closest('.card');
      if (card && $('img', card)) {
        collect();
        var i = items.indexOf(card);
        if (i > -1) { e.preventDefault(); open(i); }
      }
    });

    var closeBtn = $('.lightbox__close', lb);
    var prevBtn = $('.lightbox__nav.prev', lb);
    var nextBtn = $('.lightbox__nav.next', lb);
    if (closeBtn) closeBtn.addEventListener('click', close);
    if (prevBtn) prevBtn.addEventListener('click', function () { open(cur - 1); });
    if (nextBtn) nextBtn.addEventListener('click', function () { open(cur + 1); });
    lb.addEventListener('click', function (e) { if (e.target === lb) close(); });

    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('is-open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowLeft') open(cur - 1);
      if (e.key === 'ArrowRight') open(cur + 1);
    });
  }

  /* ---------- 6. Accordion (FAQ + Tuyen dung) ---------- */
  $$('.faq__q').forEach(function (q) {
    q.addEventListener('click', function () {
      q.parentElement.classList.toggle('is-open');
    });
  });
  $$('.job__head').forEach(function (h) {
    h.addEventListener('click', function () {
      h.parentElement.classList.toggle('is-open');
    });
  });

  /* ---------- 7. Hieu ung reveal khi cuon ---------- */
  var reveals = $$('.reveal');
  if (reveals.length && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add('is-in');
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -60px' });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('is-in'); });
  }

  /* ---------- 8. Form ---------- */
  // Form gui that qua FormSubmit. Gui xong FormSubmit tra ve trang nay kem ?gui=ok
  // -> hien thong bao cam on va an form di.
  if (/[?&]gui=ok/.test(window.location.search)) {
    $$('.form-msg[data-ok]').forEach(function (msg) {
      msg.classList.add('is-visible');
      var form = $('form', msg.parentNode);
      if (form) form.hidden = true;
      setTimeout(function () {
        msg.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }, 300);
    });
  }

  // Chan bam gui hai lan
  $$('form[action*="formsubmit"]').forEach(function (form) {
    form.addEventListener('submit', function () {
      var btn = $('button[type="submit"]', form);
      if (btn) {
        btn.disabled = true;
        btn.textContent = 'Đang gửi…';
      }
    });
  });

  /* ---------- 9. Sao chep so tai khoan ---------- */
  $$('.pay__copy').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var stk = btn.dataset.copy || '';
      var done = function () {
        var old = btn.textContent;
        btn.textContent = 'Đã chép';
        btn.classList.add('is-done');
        setTimeout(function () {
          btn.textContent = old;
          btn.classList.remove('is-done');
        }, 1800);
      };

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(stk).then(done, fallback);
      } else {
        fallback();
      }

      function fallback() {
        var ta = document.createElement('textarea');
        ta.value = stk;
        ta.style.position = 'fixed';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand('copy'); done(); } catch (e) { /* bo qua */ }
        document.body.removeChild(ta);
      }
    });
  });

  /* ---------- Feedback khach hang: luot qua lai tung danh gia ---------- */
  var fbk = $('.fbk');
  if (fbk) {
    var fImgs = $$('.fbk__img', fbk);
    var fCards = $$('.fbk-card', fbk);
    var fDem = $('.fbk__dem b', fbk);
    var fCur = 0, fTimer = null, fDung = false, fThay = false;

    var fNap = function (i) {                  // chi tai anh khi can -> web nhe
      var im = fImgs[(i + fImgs.length) % fImgs.length];
      if (im && im.getAttribute('data-src')) {
        im.src = im.getAttribute('data-src');
        im.removeAttribute('data-src');
      }
    };
    var fHien = function (i) {
      if (!fCards.length) return;
      fCur = (i + fCards.length) % fCards.length;
      fImgs.forEach(function (im, k) { im.classList.toggle('is-active', k === fCur); });
      fCards.forEach(function (c, k) { c.classList.toggle('is-active', k === fCur); });
      if (fDem) fDem.textContent = fCur + 1;
      fNap(fCur); fNap(fCur + 1);
      var c = fCards[fCur], p = $('.fbk-card__text', c), nut = $('.fbk-card__them', c);
      if (p && nut && !c.classList.contains('mo')) nut.hidden = p.scrollHeight <= p.clientHeight + 2;
    };
    $$('.fbk-card__them', fbk).forEach(function (nut) {
      nut.addEventListener('click', function () { nut.closest('.fbk-card').classList.add('mo'); nut.hidden = true; fDung = true; });
    });
    var fChay = function () {
      clearInterval(fTimer);
      fTimer = setInterval(function () { if (!fDung && fThay) fHien(fCur + 1); }, 8000);
    };

    $$('[data-fbk]', fbk).forEach(function (b) {
      b.addEventListener('click', function () { fHien(fCur + parseInt(b.getAttribute('data-fbk'), 10)); fChay(); });
    });
    fbk.addEventListener('mouseenter', function () { fDung = true; });
    fbk.addEventListener('mouseleave', function () { fDung = false; });

    var fX = null;                               // vuot tren dien thoai
    fbk.addEventListener('touchstart', function (e) { fX = e.touches[0].clientX; }, { passive: true });
    fbk.addEventListener('touchend', function (e) {
      if (fX === null) return;
      var dx = e.changedTouches[0].clientX - fX;
      if (Math.abs(dx) > 50) { fHien(fCur + (dx < 0 ? 1 : -1)); fChay(); }
      fX = null;
    }, { passive: true });

    if ('IntersectionObserver' in window) {      // chi tu chuyen khi dang nhin thay muc nay
      new IntersectionObserver(function (es) { fThay = es[0].isIntersecting; }, { threshold: 0.35 }).observe(fbk);
    } else {
      fThay = true;
    }
    fHien(0);
    fChay();
  }

  /* ---------- Nhac nen ----------
     Trinh duyet chan tu phat nhac co tieng -> thu phat ngay (Chrome cho phep khi khach da bam
     o trang truoc), khong duoc thi cho lan cham/bam dau tien. Khach tat -> nho, khong tu bat lai. */
  var nhac = $('#nhac');
  if (nhac && window.Audio) {
    var au = new Audio();
    var nVol = parseFloat(nhac.getAttribute('data-vol')) || 0.3;
    var nDoc = function (s, k) { try { return window[s].getItem(k); } catch (e) { return null; } };
    var nGhi = function (s, k, v) { try { window[s].setItem(k, v); } catch (e) {} };
    var nDang = false, nCtx = null, nGain = null, nFade = null, nMoi = 0;
    var nVolDuoc = (function () { var a = new Audio(); a.volume = 0.5; return a.volume === 0.5; })();  // iPhone: khong chinh duoc volume
    au.loop = true;
    au.preload = 'none';

    var nHien = function () {
      nhac.classList.toggle('is-playing', nDang);
      nhac.setAttribute('aria-pressed', nDang ? 'true' : 'false');
      nhac.setAttribute('aria-label', nDang ? 'Tắt nhạc nền' : 'Bật nhạc nền');
    };
    var nNguon = function () {
      if (au.src) return;
      var t = parseFloat(nDoc('sessionStorage', 'qa-nhac-t')) || 0;   // nghe tiep doan dang nghe o trang truoc
      au.src = nhac.getAttribute('data-src') + (t > 1 ? '#t=' + t.toFixed(1) : '');
    };
    var nTang = function () {                    // tang dan am luong cho em tai
      clearInterval(nFade);
      if (nGain) { nGain.gain.value = nVol; return; }
      if (!nVolDuoc) return;
      au.volume = 0;
      nFade = setInterval(function () {
        au.volume = Math.min(nVol, au.volume + nVol / 15);
        if (au.volume >= nVol) clearInterval(nFade);
      }, 80);
    };
    var nPhat = function (tuCham) {
      nNguon();
      if (tuCham && !nVolDuoc && !nCtx && (window.AudioContext || window.webkitAudioContext)) {
        try {                                    // iPhone: giam am luong qua Web Audio
          nCtx = new (window.AudioContext || window.webkitAudioContext)();
          nGain = nCtx.createGain();
          nGain.gain.value = nVol;
          nCtx.createMediaElementSource(au).connect(nGain);
          nGain.connect(nCtx.destination);
        } catch (e) { nCtx = null; nGain = null; }
      }
      if (nCtx && nCtx.state === 'suspended') nCtx.resume();
      var p = au.play();
      var ok = function () { nDang = true; nHien(); nTang(); boCho(); };
      if (p && p.then) {
        p.then(ok, function () { nDang = false; nHien(); });
      } else {
        ok();
      }
    };
    var nDung = function () {
      clearInterval(nFade);
      au.pause();
      nDang = false;
      nHien();
    };

    var suKien = ['pointerup', 'touchend', 'mousedown', 'keydown', 'click'];
    var choCham = function (e) {
      if (nhac.contains(e.target) || nDang) return;   // bam nut nhac: de nut tu xu ly
      if (e.type === 'keydown' && e.key === 'Escape') return;
      nPhat(true);
    };
    var boCho = function () { suKien.forEach(function (s) { document.removeEventListener(s, choCham, true); }); };

    nhac.addEventListener('click', function () {
      if (nDang) {
        nDung();
        nGhi('localStorage', 'qa-nhac', 'tat');
      } else {
        nGhi('localStorage', 'qa-nhac', 'bat');
        nPhat(true);
      }
    });

    au.addEventListener('timeupdate', function () {
      var now = Date.now();
      if (now - nMoi > 2000) { nMoi = now; nGhi('sessionStorage', 'qa-nhac-t', au.currentTime.toFixed(1)); }
    });
    window.addEventListener('pagehide', function () {
      if (au.src) nGhi('sessionStorage', 'qa-nhac-t', au.currentTime.toFixed(1));
    });
    var nAn = false;                             // chuyen tab / sang app khac -> tam dung
    document.addEventListener('visibilitychange', function () {
      if (document.hidden && nDang) { nAn = true; nDung(); }
      else if (!document.hidden && nAn) { nAn = false; nPhat(false); }
    });

    var tietKiem = navigator.connection && navigator.connection.saveData;
    if (nDoc('localStorage', 'qa-nhac') !== 'tat' && !tietKiem) {
      suKien.forEach(function (s) { document.addEventListener(s, choCham, true); });
      if (nDoc('sessionStorage', 'qa-nhac-t')) nPhat(false);   // da nghe o trang truoc -> thu phat tiep ngay
    }
  }

})();
