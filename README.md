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
![image](https://github.com/user-attachments/assets/f8999ea0-67f7-4999-8c0e-6c780ac02a12)


2. **User Interface**:
   - Displays a table of CVEs with a "Total Records" count.
   - Allows users to filter results by year, CVSS score, and last modified date.
   - Provides a "Results Per Page" dropdown to control the number of records displayed.
   - Redirects to a detailed view when a CVE row is clicked.
  
     ![image](https://github.com/user-attachments/assets/5eb5ced0-fd49-470a-af68-b6f56bd78fd0)

     ![image](https://github.com/user-attachments/assets/a08cf207-243b-4379-9655-ccfffebf341e)

3. **Periodic Synchronization**:
   - Synchronizes CVE data periodically (every 6 hours) using a background scheduler.
  
   ![image](https://github.com/user-attachments/assets/9702546a-1677-4a67-b350-30602b93087c)

4.**API Endpoints**:
   - `/cves/list`: Returns a paginated list of CVEs with filtering options.
   - `/cves/<cve_id>`: Returns detailed information about a specific CVE.

5. **Unit Tests**:
   - Includes well-defined unit tests for database initialization, data fetching, and route handling.
      ![image](https://github.com/user-attachments/assets/dba3b665-6adb-4bcf-a8a8-881cc05b169b)






