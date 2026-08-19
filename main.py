import argparse, os, collections, subprocess
import requests
import config, scraper, excel_handler

OUTPUT_DIR = config.OUTPUT_DIR

def download_pdfs(items, download_dir):
    os.makedirs(download_dir, exist_ok=True)
    pdf_items = [i for i in items if i["link"].lower().endswith('.pdf')]
    if not pdf_items: return
    new = 0
    for item in pdf_items:
        url = item["link"]
        filename = url.split("/")[-1].split("?")[0]
        if not filename.endswith('.pdf'): filename = f"{item['title'][:50].replace(' ','_')}.pdf"
        filepath = os.path.join(download_dir, filename)
        if os.path.exists(filepath): continue
        try:
            head = requests.head(url, timeout=10, allow_redirects=True, headers={"User-Agent":"Mozilla/5.0"})
            if "application/pdf" not in head.headers.get("Content-Type",""): continue
            r = requests.get(url, stream=True, timeout=30, headers={"User-Agent":"Mozilla/5.0"})
            r.raise_for_status()
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(8192): f.write(chunk)
            if os.path.getsize(filepath)>0:
                print(f"  Downloaded: {filename}")
                new += 1
        except Exception as e:
            print(f"  Failed {url}: {e}")
    if new: print(f"Downloaded {new} new PDF(s) to {download_dir}")
    else: print("No new PDFs downloaded.")
    subprocess.run(["open", download_dir])

def main():
    parser = argparse.ArgumentParser(description="AI Outreach Tool")
    parser.add_argument("--mode", choices=["jobs","courses","pdfs","all"], default="all")
    parser.add_argument("--filter", "-f", help="Extra job keywords")
    parser.add_argument("--download", action="store_true", help="Download PDFs")
    args = parser.parse_args()
    extra = [k.strip() for k in args.filter.split(",")] if args.filter else []
    job_items, course_items, pdf_items = [], [], []

    if args.mode in ("jobs","all"):
        print("\n--- JOB SEARCH ---")
        job_items = scraper.run_jobs(extra)
        if not job_items:
            job_items = config.FALLBACK_JOBS
        print(f"Jobs saved: {len(job_items)}")
        cnt = collections.Counter(i["category"] for i in job_items)
        for cat, n in cnt.most_common(): print(f"  {cat:30s}: {n}")

    if args.mode in ("courses","all"):
        print("\n--- COURSE SEARCH ---")
        course_items = scraper.run_courses()
        if not course_items:
            course_items = config.FALLBACK_COURSES
        print(f"Courses saved: {len(course_items)}")
        cnt = collections.Counter(i["category"] for i in course_items)
        for cat, n in cnt.most_common(): print(f"  {cat:30s}: {n}")
        if args.download:
            print("\nDownloading course PDFs...")
            download_pdfs(course_items, os.path.join(OUTPUT_DIR, "downloads"))

    if args.mode in ("pdfs","all"):
        print("\n--- PDF SEARCH ---")
        pdf_items = scraper.run_pdfs()
        print(f"PDFs saved: {len(pdf_items)}")

    if job_items or course_items or pdf_items:
        excel_path = os.path.join(OUTPUT_DIR, "AI_Jobs_Courses.xlsx")
        excel_handler.update_excel_safe(job_items, course_items, pdf_items, excel_path)

    if args.download and args.mode in ("pdfs","all") and pdf_items:
        print("\nDownloading dedicated PDFs...")
        download_pdfs(pdf_items, os.path.join(OUTPUT_DIR, "downloads"))

if __name__ == "__main__":
    main()
