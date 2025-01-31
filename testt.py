import unittest
from app import app, init_db, get_db_connection, fetch_and_store_cves
from flask_testing import TestCase
import psycopg2

class TestApp(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        
        init_db()

    def tearDown(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS cves, cvss_metrics, cpe;")
        conn.commit()
        cur.close()
        conn.close()

    def test_database_initialization(self):
        conn = get_db_connection()
        cur = conn.cursor()


        cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'cves');")
        self.assertTrue(cur.fetchone()[0])

        cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'cvss_metrics');")
        self.assertTrue(cur.fetchone()[0])


        cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'cpe');")
        self.assertTrue(cur.fetchone()[0])

        cur.close()
        conn.close()

    

    def test_home_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"CVE List", response.data)


    def test_invalid_cve_detail_route(self):
        response = self.client.get("/cves/INVALID-CVE-ID")
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"CVE not found", response.data)

if __name__ == "__main__":
    unittest.main()