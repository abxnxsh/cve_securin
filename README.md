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
  

   ![image](https://github.com/user-attachments/assets/40954ef7-f69b-4a08-83fc-4b41f1238839)







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

# 7. **API Documentation**:
Postman Link:https://documenter.getpostman.com/view/39877724/2sAYdeKWnE
  
## **Endpoints**

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Home route - Displays total CVE records in the database |
| `GET` | `/cves/list` | Fetches a paginated list of CVEs with filtering and sorting options |
| `GET` | `/cves/<cve_id>` | Fetches details of a specific CVE |


---

## **Home Route**
### **`GET /`**
#### **Description**  
Displays the total number of CVE records stored in the database.

#### **Response Example**
```json
{
    "total_records": 350
}

```

## **CVE List**
### **`GET /cves/list`**
#### **Description**  
Fetches a list of CVEs with optional pagination, sorting, and filtering.

#### **Query Parameters**
| Parameter      | Type    | Description                                      | Example                 |
|---------------|--------|--------------------------------------------------|-------------------------|
| `page`        | `int`   | Page number (default: 1)                         | `1`                     |
| `per_page`    | `int`   | Number of records per page (default: 10)         | `20`                    |
| `sort_by`     | `string` | Column to sort by (default: `published_date`)    | `last_modified_date`     |
| `sort_order`  | `string` | Sort order: `asc` or `desc` (default: `desc`)   | `asc`                    |
| `filter_type` | `string` | Filter type (`published_date` or `last_modified_date`) | `published_date`   |
| `year`        | `string` | Filter CVEs by year                              | `2023`                   |
| `cvss_score`  | `float`  | Filter CVEs by CVSS base score                   | `7.5`                    |
| `cve_id`      | `string` | Fetch a specific CVE                             | `CVE-2023-12345`         |

#### **Request Example**


#### **Response Example**
```json
{
    "total": 500,
    "cves": [
        {
            "id": "CVE-2023-12345",
            "description": "cve@mitre.org",
            "published_date": "1996-10-15",
            "last_modified_date": "2024-02-01",
            "status": "Published"
        },
        {
            "id": "CVE-2023-67890",
            "description": "cve@mitre.org",
            "published_date": "1998-11-20",
            "last_modified_date": "2024-01-10",
            "status": "Modified"
        }
    ]
}
```
## **CVE Details**
### **`GET /cves/<cve_id>`**
#### **Description**  
Fetches detailed information about a specific CVE.

#### **Path Parameter**
| Parameter  | Type   | Description                        | Example           |
|------------|--------|------------------------------------|-------------------|
| `cve_id`   | `string` | The unique CVE identifier       | `CVE-2023-12345` |

#### **Request Example**

#### **Response Example**
```json
{
    "id": "CVE-2023-12345",
    "description": "cve@mitre.org",
    "published_date": "2023-10-15",
    "last_modified_date": "2024-02-01",
    "status": "Published",
    "cvss_metrics": {
        "severity": "HIGH",
        "base_score": 8.2,
        "vector_string": "AV:N/AC:L/Au:N/C:P/I:P/A:P",
        "exploitability_score": 3.9,
        "impact_score": 4.5
    },
    "cpe": [
        {
            "criteria": "cpe:/o:linux:linux_kernel:5.4",
            "match_criteria_id": "1234-abcd",
            "vulnerable": true
        }
    ]
}
```

## **Error Responses**
| Status Code | Message | Description |
|------------|---------|-------------|
| `400` | `"Bad Request"` | Invalid query parameters |
| `404` | `"CVE not found"` | The requested CVE ID does not exist |
| `500` | `"Internal Server Error"` | Database connection issues or API failures |



