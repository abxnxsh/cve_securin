# Assessment

## **About**

This project involves consuming CVE data from the National Vulnerability Database API, storing it in a database, and providing an API and a user interface for accessing, filtering, and visualizing CVE details. The goal is to implement an efficient, scalable system for consuming, storing, and presenting vulnerability data.

## **Technologies Used**

- **Flask**: Python web framework for building the backend API.
- **PostgreSQL**: Relational database to store CVE data.
- **HTML, CSS, JavaScript**: For building the user interface.
- **APScheduler**: Library used for running periodic tasks, like refreshing CVE data in the background.

## **Tasks and Implementation**

1. **Fetch and Store CVE Data**:
   - Fetches CVE data from the NVD API in chunks using pagination.
   - Stores the data in a PostgreSQL database with tables for CVEs, CVSS metrics, and CPE detail
  

   ![image](https://github.com/user-attachments/assets/de0caecf-2da1-4a17-94f5-e5e941299aa7)






2. **User Interface**:
   - Displays a table of CVEs with a "Total Records" count.
   - Allows users to filter results by year, CVSS score, and last modified date.
   - Provides a "Results Per Page" dropdown to control the number of records displayed.
   - Redirects to a detailed view when a CVE row is clicked.
  
     

      ![image](https://github.com/user-attachments/assets/5eb5ced0-fd49-470a-af68-b6f56bd78fd0)


   **Vulnerability-Free**

   SQL Injection :
   - Uses parameterized queries (eg. cur.execute) which prevents SQL injection.

4. **Sorting**:
   - Sort CVE records by:
     - Published Date (ascending/descending)
     - Last Modified Date (ascending/descending)

   ![image](https://github.com/user-attachments/assets/c9f32c9a-d843-4c57-a392-e554b8cecd99)



5. **Filtering**:
   - Filter CVE records by:
     - Date (e.g., show only CVEs published in 2023).
   
   - Filtering options for PUBLISHED date and LAST MODIDIFIED date.

   - ![image](https://github.com/user-attachments/assets/450e8747-1efb-4504-8789-b10839fb2f7c)


    - CVSS Score (e.g., 7.5).

    - CVE ID (e.g., CVE-2023-1234).
  

    - ![image](https://github.com/user-attachments/assets/38346bb1-d4bc-4da4-a4db-6d7e6405325e)





     

7. **Periodic Synchronization**:
   - Synchronizes CVE data periodically (every 6 hours) using a background scheduler.
  
   ![image](https://github.com/user-attachments/assets/9702546a-1677-4a67-b350-30602b93087c)

4.**API Endpoints**:
   - `/cves/list`: Returns a paginated list of CVEs with filtering options.
   - `/cves/<cve_id>`: Returns detailed information about a specific CVE.

6. **Unit Tests**:
   - Includes well-defined unit tests for database initialization, data fetching, and route handling.
     
      ![image](https://github.com/user-attachments/assets/dba3b665-6adb-4bcf-a8a8-881cc05b169b)

7. **API Documentation**:
   -Get CVE List

   - Endpoint: /cves/list

    - Method: GET

   {
  "total": 1000,
  "cves": [
    {
      "id": "CVE-1999-0095",
      "description": "Test CVE",
      "published_date": "1999-01-01",
      "last_modified_date": "2023-01-01",
      "status": "Analyzed"
    },
    ...
  ]
}

Get CVE Details

    - Endpoint: /cves/<cve_id>

    - Method: GET

{
  "cve_id": "CVE-1999-0095",
  "description": "Test CVE",
  "published_date": "1999-01-01",
  "last_modified_date": "2023-01-01",
  "status": "Analyzed",
  "cvss_metrics": {
    "severity": "HIGH",
    "base_score": 9.8,
    "vector_string": "AV:N/AC:L/Au:N/C:C/I:C/A:C",
    "access_vector": "NETWORK",
    "access_complexity": "LOW",
    "authentication": "NONE",
    "confidentiality_impact": "COMPLETE",
    "integrity_impact": "COMPLETE",
    "exploitability_score": 3.9,
    "impact_score": 10.0
  },
  "cpe_details": [
    {
      "criteria": "cpe:2.3:a:eric_allman:sendmail:5.58:*:*:*:*:*:*:*",
      "match_criteria_id": "1D07F493-9C8D-44A4-8652-F28B46CBA27C",
      "vulnerable": true
    },
    ...
  ]
}


    Fetch All CVEs:

        To fetch the first 10 CVEs sorted by published date in descending order:
        Copy

        GET /cves/list

        To fetch CVEs published in 2023:
        Copy

        GET /cves/list?year=2023

        To fetch 50 CVEs per page on page 2:
        Copy

        GET /cves/list?page=2&per_page=50

    Fetch CVE Details:

        To fetch details for a specific CVE:
        Copy

        GET /cves/CVE-2023-1234

    Synchronize CVE Data:

        To manually synchronize CVE data:
        Copy

        POST /cves/sync






