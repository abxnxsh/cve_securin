import time
from flask import Flask, render_template, request, jsonify
import requests
import psycopg2
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)


def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="infodb",
        user="postgres",
        password="1234",
    )
    return conn


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS cves (
            id TEXT PRIMARY KEY,
            description TEXT,
            published_date TEXT,
            last_modified_date TEXT,
            status TEXT
        );
    """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS cvss_metrics (
            id SERIAL PRIMARY KEY,
            cve_id TEXT REFERENCES cves(id),
            severity TEXT,
            base_score FLOAT,
            vector_string TEXT,
            access_vector TEXT,
            access_complexity TEXT,
            authentication TEXT,
            confidentiality_impact TEXT,
            integrity_impact TEXT,
            exploitability_score FLOAT,
            impact_score FLOAT
        );
    """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS cpe (
            id SERIAL PRIMARY KEY,
            cve_id TEXT REFERENCES cves(id),
            criteria TEXT,
            match_criteria_id TEXT,
            vulnerable BOOLEAN
        );
    """
    )

    conn.commit()
    cur.close()
    conn.close()


init_db()


NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
# API_KEY = "c3ec834e-d046-4348-9687-d0dc11ddf155"


def fetch_and_store_cves():
    start_index = 0
    results_per_page = 100
    max_cves_to_fetch = 500
    total_fetched = 0
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        # "apiKey": API_KEY,
    }

    while total_fetched < max_cves_to_fetch:
        try:
            print(f"Fetching CVEs from index {start_index}...")
            response = requests.get(
                NVD_API_URL,
                params={"startIndex": start_index, "resultsPerPage": results_per_page},
                headers=headers,
                timeout=60,
            )

            print(f"API Response Status Code: {response.status_code}")
            if response.status_code == 403:
                print("❌ Error 403: Forbidden - Check your API key!")
                return

            if response.status_code == 429:
                print("⚠️ Rate limit exceeded. Waiting for 60 seconds...")
                time.sleep(60)
                continue
            if response.status_code != 200:
                print(f"❌ Failed to fetch CVE data: {response.status_code}")
                return

            data = response.json()
            vulnerabilities = data.get("vulnerabilities", [])

            if not vulnerabilities:
                print("✅ No more CVEs to fetch.")
                break

            conn = get_db_connection()
            cur = conn.cursor()

            for cve in vulnerabilities:
                if total_fetched >= max_cves_to_fetch:
                    break

                cve_id = cve["cve"]["id"]
                description = cve["cve"]["sourceIdentifier"]
                published_date = cve["cve"]["published"]
                last_modified_date = cve["cve"]["lastModified"]
                status = cve["cve"]["vulnStatus"]

                cur.execute(
                    """
                    INSERT INTO cves (id, description, published_date, last_modified_date, status)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                    description = EXCLUDED.description,
                    published_date = EXCLUDED.published_date,
                    last_modified_date = EXCLUDED.last_modified_date,
                    status = EXCLUDED.status;
                """,
                    (cve_id, description, published_date, last_modified_date, status),
                )

                if "metrics" in cve["cve"] and "cvssMetricV2" in cve["cve"]["metrics"]:
                    cvss_metric = cve["cve"]["metrics"]["cvssMetricV2"][0]["cvssData"]
                    print(f"CVSS Metrics for {cve_id}: {cvss_metric}")  # Debug

                    cur.execute(
                        """
                        INSERT INTO cvss_metrics (cve_id, severity, base_score, vector_string, access_vector, access_complexity, authentication, confidentiality_impact, integrity_impact, exploitability_score, impact_score)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (cve_id) DO UPDATE SET
                        severity = EXCLUDED.severity,
                        base_score = EXCLUDED.base_score,
                        vector_string = EXCLUDED.vector_string,
                        access_vector = EXCLUDED.access_vector,
                        access_complexity = EXCLUDED.access_complexity,
                        authentication = EXCLUDED.authentication,
                        confidentiality_impact = EXCLUDED.confidentiality_impact,
                        integrity_impact = EXCLUDED.integrity_impact,
                        exploitability_score = EXCLUDED.exploitability_score,
                        impact_score = EXCLUDED.impact_score;
                    """,
                        (
                            cve_id,
                            cve["cve"]["metrics"]["cvssMetricV2"][0]["baseSeverity"],
                            cvss_metric["baseScore"],
                            cvss_metric["vectorString"],
                            cvss_metric["accessVector"],
                            cvss_metric["accessComplexity"],
                            cvss_metric["authentication"],
                            cvss_metric["confidentialityImpact"],
                            cvss_metric["integrityImpact"],
                            cve["cve"]["metrics"]["cvssMetricV2"][0][
                                "exploitabilityScore"
                            ],
                            cve["cve"]["metrics"]["cvssMetricV2"][0]["impactScore"],
                        ),
                    )

                if "configurations" in cve["cve"]:
                    for config in cve["cve"]["configurations"]:
                        for node in config["nodes"]:
                            for cpe_match in node["cpeMatch"]:
                                cur.execute(
                                    """
                                    INSERT INTO cpe (cve_id, criteria, match_criteria_id, vulnerable)
                                    VALUES (%s, %s, %s, %s)
                                    ON CONFLICT (cve_id, criteria) DO UPDATE SET
                                    match_criteria_id = EXCLUDED.match_criteria_id,
                                    vulnerable = EXCLUDED.vulnerable;
                                """,
                                    (
                                        cve_id,
                                        cpe_match["criteria"],
                                        cpe_match.get("matchCriteriaId", "N/A"),
                                        cpe_match["vulnerable"],
                                    ),
                                )

                total_fetched += 1

            conn.commit()
            cur.close()
            conn.close()

            start_index += results_per_page

            if total_fetched >= max_cves_to_fetch:
                print(f"✅ Fetched {total_fetched} CVEs. Stopping.")
                break

            time.sleep(6)

        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            time.sleep(30)
            continue

        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return


@app.route("/")
def home():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM cves;")
    total_records = cur.fetchone()[0]

    cur.close()
    conn.close()

    return render_template("index.html", total_records=total_records)


@app.route("/cves/list", methods=["GET"])
def cve_list():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    sort_by = request.args.get("sort_by", "published_date")
    sort_order = request.args.get("sort_order", "desc")
    filter_type = request.args.get("filter_type", "published_date") 
    year = request.args.get("year")
    cvss_score = request.args.get("cvss_score")
    cve_id = request.args.get("cve_id")

    conn = get_db_connection()
    cur = conn.cursor()

    query = """
        SELECT cves.* 
        FROM cves
        LEFT JOIN cvss_metrics ON cves.id = cvss_metrics.cve_id
        WHERE 1=1
    """
    filters = []

    if year:
        if filter_type == "published_date":
            filters.append(f"cves.published_date LIKE '{year}%'")
        elif filter_type == "last_modified_date":
            filters.append(f"cves.last_modified_date LIKE '{year}%'")

    if cvss_score:
        filters.append(f"cvss_metrics.base_score = {float(cvss_score)}")

    if cve_id:
        filters.append(f"cves.id = '{cve_id}'")

    if filters:
        query += " AND " + " AND ".join(filters)

    query += f" ORDER BY {sort_by} {sort_order} LIMIT {per_page} OFFSET {(page-1) * per_page};"
    cur.execute(query)
    cves = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM cves")
    total_count = cur.fetchone()[0]

    cur.close()
    conn.close()

    return jsonify({"total": total_count, "cves": cves})


@app.route("/cves/<cve_id>", methods=["GET"])
def cve_detail(cve_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM cves WHERE id = %s;", (cve_id,))
    cve = cur.fetchone()

    if not cve:
        return jsonify({"message": "CVE not found"}), 404

    cur.execute("SELECT * FROM cvss_metrics WHERE cve_id = %s;", (cve_id,))
    cvss_metrics = cur.fetchone()

    cur.execute("SELECT * FROM cpe WHERE cve_id = %s;", (cve_id,))
    cpe_details = cur.fetchall()

    cur.close()
    conn.close()

    cve_data = {
        "cve_id": cve[0],
        "description": cve[1],
        "published_date": cve[2],
        "last_modified_date": cve[3],
        "status": cve[4],
        "cvss_metrics": {
            "severity": cvss_metrics[2] if cvss_metrics else "N/A",
            "base_score": cvss_metrics[3] if cvss_metrics else "N/A",
            "vector_string": cvss_metrics[4] if cvss_metrics else "N/A",
            "access_vector": cvss_metrics[5] if cvss_metrics else "N/A",
            "access_complexity": cvss_metrics[6] if cvss_metrics else "N/A",
            "authentication": cvss_metrics[7] if cvss_metrics else "N/A",
            "confidentiality_impact": cvss_metrics[8] if cvss_metrics else "N/A",
            "integrity_impact": cvss_metrics[9] if cvss_metrics else "N/A",
            "exploitability_score": cvss_metrics[10] if cvss_metrics else "N/A",
            "impact_score": cvss_metrics[11] if cvss_metrics else "N/A",
        },
        "cpe_details": [
            {
                "criteria": cpe[2],
                "match_criteria_id": cpe[3],
                "vulnerable": cpe[4],
            }
            for cpe in cpe_details
        ],
    }

    return render_template("row.html", **cve_data)


scheduler = BackgroundScheduler()
scheduler.add_job(fetch_and_store_cves, "interval", hours=6)
scheduler.start()

if __name__ == "__main__":
    fetch_and_store_cves()
    app.run(debug=False)
