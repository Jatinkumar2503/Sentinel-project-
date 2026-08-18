import urllib.request
import json
import sys

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run_verification():
    print("=== 1. CHECKING SENTINEL AI DASHBOARD SUMMARY ===")
    res = urllib.request.urlopen('http://127.0.0.1:8000/api/dashboard/summary').read()
    summary = json.loads(res.decode('utf-8'))
    print(f"Total Scrapers: {summary['total_scrapers']}")
    print(f"Total Products Monitored: {summary['total_products_monitored']}")
    print(f"Average Fleet Health: {summary['average_health_score']}%")
    print(f"Self-Healing Success Rate: {summary['healing_success_rate']}%")

    print("\n=== 2. RUNNING SCRAPER ON MUTATED TARGET & TRIGGERING SELF-HEALING ===")
    req = urllib.request.Request(
        'http://127.0.0.1:8000/api/self-healing/trigger',
        data=json.dumps({'scraper_id': 1, 'force_repair': True}).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    heal_res = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    print(f"Status: {heal_res['status']}")
    print(f"Records Recovered: {heal_res['records_after']} / 6")
    print(f"Repaired Selectors: {heal_res['repaired_selectors']['price']}")

    print("\n=== 3. LATEST COMPETITIVE INTELLIGENCE DELTA ALERTS ===")
    intel = json.loads(urllib.request.urlopen('http://127.0.0.1:8000/api/intelligence/events?limit=4').read().decode('utf-8'))
    for ev in intel:
        print(f"[{ev['severity']}] {ev['event_type']} - {ev['title']}")

if __name__ == '__main__':
    run_verification()
