/* =========================================================================
 * GREN Propertykost — Shared brand helpers
 * Depends on config.js (window.LANDING_CONFIG). Load once per page.
 * ========================================================================= */
(function () {
  'use strict';

  function getCleanPhone() {
    const cfg = window.LANDING_CONFIG || {};
    return (cfg.nomorWhatsApp || '6281234567890').replace(/[^0-9]/g, '');
  }

  function trackLeadEvent(data) {
    const cfg = window.LANDING_CONFIG || {};
    if (typeof fbq === 'function') {
      fbq('track', 'Lead', { content_name: cfg.namaProperti || 'GREN Propertykost', unit: data.unit });
    }
    if (typeof gtag === 'function') {
      gtag('event', 'generate_lead', { event_category: 'Lead', event_label: data.unit });
    }
    if (window.dataLayer && Array.isArray(window.dataLayer)) {
      window.dataLayer.push({ event: 'lead_form_submitted', leadData: data });
    }
  }

  function openDirectWA(pesan) {
    const cfg = window.LANDING_CONFIG || {};
    const msg = pesan || cfg.pesanDefault || 'Halo Tim GREN Property, saya ingin menanyakan informasi unit dan pricelist resmi.';
    trackLeadEvent({ unit: 'Direct WhatsApp Click' });
    window.open('https://wa.me/' + getCleanPhone() + '?text=' + encodeURIComponent(msg), '_blank');
  }

  function formatPhone(raw) {
    const d = (raw || '').replace(/[^0-9]/g, '');
    if (d.startsWith('62') && d.length >= 10) {
      return '+62 ' + d.substring(2, 5) + '-' + d.substring(5, 9) + '-' + d.substring(9);
    }
    return '+' + d;
  }

  const SOCIAL_SVG = {
    instagram:
      '<path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>',
    tiktok:
      '<path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-5.2 1.74 2.89 2.89 0 0 1 2.31-4.64c.298-.002.595.042.88.13V9.4a6.33 6.33 0 0 0-1-.08A6.34 6.34 0 0 0 3 15.66a6.34 6.34 0 0 0 10.86 4.43v-7a8.16 8.16 0 0 0 4.77 1.52v-3.4a4.85 4.85 0 0 1-3.04-1.52z"/>',
    youtube:
      '<path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>',
    facebook:
      '<path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>'
  };

  function buildSocialIcons(s) {
    let html = '';
    if (s.instagram && s.instagram.trim() !== '') {
      html += '<a href="' + s.instagram + '" target="_blank" rel="noopener noreferrer" class="w-8 h-8 rounded-lg bg-slate-800 hover:bg-pink-700 text-slate-300 hover:text-white flex items-center justify-center transition-all" title="Instagram" aria-label="Instagram"><svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">' + SOCIAL_SVG.instagram + '</svg></a>';
    }
    if (s.tiktok && s.tiktok.trim() !== '') {
      html += '<a href="' + s.tiktok + '" target="_blank" rel="noopener noreferrer" class="w-8 h-8 rounded-lg bg-slate-800 hover:bg-slate-600 text-slate-300 hover:text-white flex items-center justify-center transition-all" title="TikTok" aria-label="TikTok"><svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">' + SOCIAL_SVG.tiktok + '</svg></a>';
    }
    if (s.youtube && s.youtube.trim() !== '') {
      html += '<a href="' + s.youtube + '" target="_blank" rel="noopener noreferrer" class="w-8 h-8 rounded-lg bg-slate-800 hover:bg-red-700 text-slate-300 hover:text-white flex items-center justify-center transition-all" title="YouTube" aria-label="YouTube"><svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">' + SOCIAL_SVG.youtube + '</svg></a>';
    }
    if (s.facebook && s.facebook.trim() !== '') {
      html += '<a href="' + s.facebook + '" target="_blank" rel="noopener noreferrer" class="w-8 h-8 rounded-lg bg-slate-800 hover:bg-blue-700 text-slate-300 hover:text-white flex items-center justify-center transition-all" title="Facebook" aria-label="Facebook"><svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">' + SOCIAL_SVG.facebook + '</svg></a>';
    }
    return html;
  }

  function renderFooterContact() {
    const cfg = window.LANDING_CONFIG || {};

    const elAlamat = document.getElementById('footer-alamat');
    if (elAlamat && cfg.alamatKantor) elAlamat.textContent = cfg.alamatKantor;

    const elMaps = document.getElementById('footer-maps-link');
    if (elMaps) {
      if (cfg.googleMapsUrl && cfg.googleMapsUrl.trim() !== '') {
        elMaps.href = cfg.googleMapsUrl;
        elMaps.classList.remove('hidden');
      } else {
        elMaps.classList.add('hidden');
      }
    }

    const elEmail = document.getElementById('footer-email');
    if (elEmail && cfg.emailResmi) {
      elEmail.textContent = cfg.emailResmi;
      elEmail.href = 'mailto:' + cfg.emailResmi;
    }

    const elPhone = document.getElementById('footer-phone');
    if (elPhone && cfg.nomorWhatsApp) {
      elPhone.textContent = formatPhone(cfg.nomorWhatsApp);
    }

    const elDev = document.getElementById('footer-developer');
    if (elDev && cfg.developer) elDev.textContent = cfg.developer;

    const elSocials = document.getElementById('footer-socials');
    if (elSocials && cfg.socialMedia) {
      elSocials.innerHTML = buildSocialIcons(cfg.socialMedia);
    }
  }

  function initMobileNav() {
    const btn = document.getElementById('mobile-toggle');
    const drawer = document.getElementById('mobile-drawer');
    if (btn && drawer) {
      btn.addEventListener('click', function () {
        drawer.classList.toggle('hidden');
      });
      drawer.querySelectorAll('a').forEach(function (a) {
        a.addEventListener('click', function () {
          drawer.classList.add('hidden');
        });
      });
    }
  }

  function initFaq() {
    document.querySelectorAll('.faq-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        const body = this.nextElementSibling;
        const icon = this.querySelector('.faq-icon');
        const isHidden = body.classList.contains('hidden');
        document.querySelectorAll('.faq-body').forEach(function (b) {
          b.classList.add('hidden');
        });
        document.querySelectorAll('.faq-icon').forEach(function (i) {
          i.textContent = '+';
        });
        if (isHidden) {
          body.classList.remove('hidden');
          if (icon) icon.textContent = '\u2212';
        }
      });
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    initMobileNav();
    initFaq();
    renderFooterContact();
  });

  window.getCleanPhone = getCleanPhone;
  window.trackLeadEvent = trackLeadEvent;
  window.openDirectWA = openDirectWA;
  window.renderFooterContact = renderFooterContact;
  window.buildSocialIcons = buildSocialIcons;
})();
