#!/usr/bin/env python3
"""
librus_nu_full.py

Usage:
  python -u librus_nu_full.py --user USER --password PASS [--out nu_days.txt] [--headful]

What it does:
- Uses Playwright to open portal, dismiss consent, open Synergia -> Zaloguj, log in with provided credentials.
- Navigates to https://synergia.librus.pl/przegladaj_nb/uczen and extracts NU (non‑justified) numbers per date.
- Writes lines with YYYY-MM-DD<TAB>NU for NU>0 to output file.
"""
from __future__ import annotations
import argparse, os, sys, time, traceback, re
from datetime import datetime
from typing import List, Tuple

from bs4 import BeautifulSoup

# Playwright import
try:
    from playwright.sync_api import sync_playwright
    _sync_playwright = sync_playwright  # type: ignore
    HAS_PLAYWRIGHT = True
except Exception:
    _sync_playwright = None
    HAS_PLAYWRIGHT = False

PORTAL_START = "https://portal.librus.pl/rodzina/synergia/loguj"
ATTENDANCE_PAGE = "https://synergia.librus.pl/przegladaj_nb/uczen"
USER_AGENT = "absence-extractor/1.0"

def dismiss_consent_modal(page) -> None:
    try:
        modal = page.query_selector("#consent-categories-modal, .consent-categories-modal-wrapper, .cookie-consent, .cookie-modal, #consentModal")
        if modal:
            btn = page.query_selector("#consent-categories-modal button[type=submit], #consent-categories-modal button:has-text('Akceptuj'), .cookie-modal button, .cookie-consent button, button:has-text('Akceptuję'), button:has-text('Zgadzam się')")
            if btn:
                try:
                    btn.click(timeout=2000)
                    page.wait_for_timeout(300)
                    return
                except Exception:
                    pass
            page.evaluate("""() => {
                const sel = document.querySelector('#consent-categories-modal, .consent-categories-modal-wrapper, .cookie-consent, .cookie-modal, #consentModal');
                if (sel) sel.remove();
            }""")
            page.wait_for_timeout(200)
    except Exception:
        pass

def open_portal_and_click_zaloguj(page):
    page.goto(PORTAL_START, wait_until="networkidle", timeout=20000)
    dismiss_consent_modal(page)
    # click Synergia opener
    synergia_selectors = [
        "a[href='https://portal.librus.pl/rodzina#']",
        "a[href$='/rodzina#']",
        "a:has-text('Synergia')",
        "a:has-text('LIBRUS Synergia')",
        "button:has-text('Synergia')"
    ]
    for sel in synergia_selectors:
        try:
            el = page.query_selector(sel)
            if not el:
                continue
            try:
                el.click(timeout=3000)
            except Exception:
                page.evaluate("(el)=>el.click()", el)
            page.wait_for_timeout(350)
            break
        except Exception:
            continue
    # click Zaloguj
    try:
        login_link = page.query_selector("a[href*='/rodzina/zaloguj'], a:has-text('Zaloguj')")
        if login_link:
            try:
                login_link.click(timeout=3000)
            except Exception:
                page.evaluate("(el)=>el.click()", login_link)
            page.wait_for_timeout(500)
    except Exception:
        pass
    # popup fallback
    pages = page.context.pages
    if len(pages) > 1:
        new_page = pages[-1]
        if new_page is not page:
            page = new_page
            page.wait_for_timeout(400)
    return page

def find_login_context(page, wait_seconds: int = 8):
    deadline = time.time() + wait_seconds
    while time.time() < deadline:
        try:
            if page.query_selector("#Login") and page.query_selector("#Pass"):
                return page
        except Exception:
            pass
        for f in page.frames:
            try:
                if f.query_selector("#Login") and f.query_selector("#Pass"):
                    return f
            except Exception:
                pass
        page.wait_for_timeout(400)
    # final direct attempt
    try:
        page.goto("https://portal.librus.pl/rodzina/zaloguj", wait_until="networkidle", timeout=10000)
        page.wait_for_timeout(400)
    except Exception:
        pass
    for f in page.frames:
        try:
            if f.query_selector("#Login") and f.query_selector("#Pass"):
                return f
        except Exception:
            pass
    if page.query_selector("#Login") and page.query_selector("#Pass"):
        return page
    return None

def parse_nu_from_html(html: str) -> List[Tuple[str,int]]:
    soup = BeautifulSoup(html, "html.parser")
    results: List[Tuple[str,int]] = []
    # iterate rows in the main table
    for tr in soup.select("table.center.big.decorated tbody tr"):
        tds = tr.find_all("td")
        if not tds:
            continue
        first = tds[0].get_text(" ", strip=True)
        # skip section header rows
        mdate = re.search(r"(\d{4}-\d{2}-\d{2})|(\d{2}\.\d{2}\.\d{4})", first)
        if not mdate:
            continue
        s = mdate.group(1) or mdate.group(2)
        try:
            if "." in s:
                date_iso = datetime.strptime(s, "%d.%m.%Y").date().isoformat()
            else:
                date_iso = datetime.strptime(s, "%Y-%m-%d").date().isoformat()
        except Exception:
            continue
        # find numeric-right TDs (U, NU, U+NU, SP, ZW)
        right_tds = [td.get_text(" ", strip=True).replace("\xa0","") for td in tds if "right" in " ".join(td.get("class") or [])]
        nu = None
        if len(right_tds) >= 2:
            cand = right_tds[1]
            nu = int(cand) if cand.isdigit() else None
        else:
            # fallback: try tds[2]
            if len(tds) >= 4:
                cand = tds[2].get_text(" ", strip=True).replace("\xa0","")
                nu = int(cand) if cand.isdigit() else None
        if nu is None:
            nu = 0
        results.append((date_iso, nu))
    return results

def run_full_flow(username: str, password: str, headful: bool = False) -> List[Tuple[str,int]]:
    if not HAS_PLAYWRIGHT or _sync_playwright is None:
        raise RuntimeError("Playwright not installed. Run: pip install playwright ; python -m playwright install")
    with _sync_playwright() as pw:
        browser = pw.chromium.launch(headless=not headful)
        context = browser.new_context(user_agent=USER_AGENT)
        page = context.new_page()
        page = open_portal_and_click_zaloguj(page)
        ctx = find_login_context(page, wait_seconds=10)
        if ctx is None:
            browser.close()
            raise RuntimeError("Login form not found. Inspect page manually.")
        # fill and submit using ids present in page
        ctx.fill("#Login", username)
        ctx.fill("#Pass", password)
        # submit
        try:
            if ctx.query_selector("#LoginBtn"):
                try:
                    ctx.click("#LoginBtn")
                except Exception:
                    ctx.evaluate("(el)=>el.click()", ctx.query_selector("#LoginBtn"))
            else:
                ctx.press("#Pass", "Enter")
        except Exception:
            ctx.press("#Pass", "Enter")
        try:
            page.wait_for_load_state("networkidle", timeout=15000)
        except Exception:
            pass
        # check for incorrect login/password message
        # --- detect incorrect login/password and stop early ---
        def _login_failed_in_context(ctx_page) -> bool:
            try:
                txt = ctx_page.content()
                if "Nieprawidłowy login i/lub hasło." in txt:
                    return True
            except Exception:
                pass
            return False

        # check top-level page
        if _login_failed_in_context(page):
            print("Nieprawidłowy login i/lub hasło.", file=sys.stderr, flush=True)
            browser.close()
            sys.exit(2)

        # check frames (some sites render the message inside a frame)
        for f in page.frames:
            try:
                if _login_failed_in_context(f):
                    print("Nieprawidłowy login i/lub hasło.", file=sys.stderr, flush=True)
                    browser.close()
                    sys.exit(2)
            except Exception:
                continue
        # --- end incorrect-login check ---
        # navigate to attendance
        try:
            page.goto(ATTENDANCE_PAGE, wait_until="networkidle", timeout=15000)
        except Exception:
            # fallback
            try:
                page.goto("https://synergia.librus.pl/przegladaj_nb/uczen", wait_until="networkidle", timeout=15000)
            except Exception:
                pass
        page.wait_for_timeout(800)
        html = page.content()
        browser.close()
        return parse_nu_from_html(html)

def save_results(items: List[Tuple[str,int]], filename: str) -> str:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(script_dir, filename)
    with open(path, "w", encoding="utf-8") as fh:
        for date_iso, nu in items:
            if nu > 0:
                fh.write(f"{date_iso}\t{nu}\n")
    return path
def make_compact_mail(items: List[Tuple[str,int]], signer: str) -> str:
    dates = sorted({d for d, nu in items if nu > 0})
    if not dates:
        return "Dzień dobry,\nBrak nieusprawiedliwionych nieobecności.\n\nZ wyrazami szacunku\n" + signer + "\n"
    parsed = []
    years = set()
    for iso in dates:
        try:
            dt = datetime.strptime(iso, "%Y-%m-%d").date()
        except Exception:
            continue
        parsed.append(dt)
        years.add(dt.year)
    if not parsed:
        return "Dzień dobry,\nBrak nieusprawiedliwionych nieobecności.\n\nZ wyrazami szacunku\n" + signer + "\n"
    day_months = ",".join(dt.strftime("%d.%m") for dt in parsed)
    if len(years) == 1:
        year_part = f"roku pańskiego {next(iter(years))}."
    else:
        year_part = "."
    msg = (
        "Dzień dobry,\n"
        "Proszę o usprawiedliwienie moich nieobecności z dnia:\n"
        f"{day_months} {year_part}\n\n"
        "Z wyrazami szacunku\n"
        f"{signer}\n"
    )
    return msg

def save_mail_body_compact(items: List[Tuple[str,int]], filename: str, signer: str) -> str:
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(make_compact_mail(items, signer=signer))
    return path


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--user", required=True)
    p.add_argument("--password", required=True)
    p.add_argument("--out", default="nu_days.txt")
    p.add_argument("--mail-out", default="usprawiedliwienie.txt")
    p.add_argument("--signer", help="name to use in mail signature")
    p.add_argument("--headful", action="store_true", help="show browser")
    p.add_argument("--skip-mail", action="store_true", help="skip mail body creation")
    args = p.parse_args()
    if not args.skip_mail and not args.signer:
        p.error("--signer is required unless --skip-mail is specified")
    try:
        # 1) run Playwright flow and extract NU rows
        rows = run_full_flow(args.user, args.password, headful=args.headful)
        absences = [(date_iso, nu) for date_iso, nu in rows if nu > 0]
        if not absences:
            print("There is no absences.")
            sys.exit(0)
        # 2) save raw NU rows (only NU>0)
        out = save_results(rows, args.out)
        print(f"[result] extracted {len(absences)} NU rows; saved to: {out}", flush=True)
        # 3) build and save mail body (unless skipped)
        if not args.skip_mail:
            mail_path = save_mail_body_compact(rows, args.mail_out, signer=args.signer)
            print(f"[result] mail body saved to: {mail_path}", flush=True)
    except Exception as e:
        tb = "".join(traceback.format_exception(type(e), e, e.__traceback__))
        print("[error] Exception:", file=sys.stderr, flush=True)
        print(tb, file=sys.stderr, flush=True)
        sys.exit(1)

if __name__ == "__main__":
    main()