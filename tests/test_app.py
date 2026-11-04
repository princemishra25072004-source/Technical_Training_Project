import os
import tempfile
import unittest
from pathlib import Path

import app


class StockwiseTestCase(unittest.TestCase):
    def setUp(self):
        # Create a temporary database for each test to ensure test isolation
        self.db_fd, self.db_path = tempfile.mkstemp(suffix='.db')
        app.DB = Path(self.db_path)
        app.app.config['TESTING'] = True
        app.app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.app.test_client()

        with app.app.app_context():
            app.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def login(self, username='admin', password='admin123'):
        return self.client.post('/login', data={
            'username': username,
            'password': password
        }, follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_login_page_renders(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome back', response.data)

    def test_login_valid_credentials(self):
        response = self.login('admin', 'admin123')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Inventory dashboard', response.data)

    def test_login_invalid_credentials(self):
        response = self.login('admin', 'wrongpassword')
        self.assertIn(b'Username or password is incorrect', response.data)

    def test_unauthenticated_access_redirects(self):
        response = self.client.get('/', follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.headers['Location'])

    def test_dashboard_metrics(self):
        self.login()
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Inventory value', response.data)
        self.assertIn(b'Low stock', response.data)

    def test_add_product_success(self):
        self.login()
        response = self.client.post('/products/new', data={
            'name': 'Ergonomic Desk Chair',
            'sku': 'CHR-5001',
            'category': 'Furniture',
            'price': '8499.00',
            'quantity': '15',
            'reorder_level': '3',
            'supplier': 'ComfortWorks'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Product saved successfully', response.data)
        self.assertIn(b'Ergonomic Desk Chair', response.data)

    def test_add_product_duplicate_sku(self):
        self.login()
        # ACC-1001 is seeded by init_db
        response = self.client.post('/products/new', data={
            'name': 'Duplicate Mouse',
            'sku': 'ACC-1001',
            'category': 'Accessories',
            'price': '500',
            'quantity': '10',
            'reorder_level': '2',
            'supplier': 'Tech'
        }, follow_redirects=True)
        self.assertIn(b'SKU already exists', response.data)

    def test_stock_adjustment_increase_and_decrease(self):
        self.login()
        # Find a seeded product id
        with app.connect() as db:
            row = db.execute("SELECT id, quantity FROM products WHERE sku='ACC-1001'").fetchone()
            pid = row['id']
            initial_qty = row['quantity']

        # Increase stock by 5
        res = self.client.post(f'/products/{pid}/stock', data={'change': '5'}, follow_redirects=True)
        self.assertIn(b'Stock updated', res.data)

        with app.connect() as db:
            updated = db.execute('SELECT quantity FROM products WHERE id=?', (pid,)).fetchone()
            self.assertEqual(updated['quantity'], initial_qty + 5)

        # Decrease stock by 3
        res = self.client.post(f'/products/{pid}/stock', data={'change': '-3'}, follow_redirects=True)
        self.assertIn(b'Stock updated', res.data)

        with app.connect() as db:
            updated = db.execute('SELECT quantity FROM products WHERE id=?', (pid,)).fetchone()
            self.assertEqual(updated['quantity'], initial_qty + 2)

    def test_stock_cannot_go_negative(self):
        self.login()
        with app.connect() as db:
            row = db.execute("SELECT id, quantity FROM products WHERE sku='ACC-1001'").fetchone()
            pid = row['id']
            current_qty = row['quantity']

        # Attempt to subtract more than current quantity
        res = self.client.post(f'/products/{pid}/stock', data={'change': str(-(current_qty + 10))}, follow_redirects=True)
        self.assertIn(b'Stock cannot go below zero', res.data)

    def test_edit_product(self):
        self.login()
        with app.connect() as db:
            row = db.execute("SELECT id FROM products WHERE sku='ACC-1002'").fetchone()
            pid = row['id']

        response = self.client.post(f'/products/{pid}/edit', data={
            'name': 'Pro Mechanical Keyboard v2',
            'sku': 'ACC-1002',
            'category': 'Keyboards',
            'price': '2999',
            'quantity': '10',
            'reorder_level': '5',
            'supplier': 'KeyWorks Global'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Product saved successfully', response.data)
        self.assertIn(b'Pro Mechanical Keyboard v2', response.data)

    def test_delete_product(self):
        self.login()
        with app.connect() as db:
            row = db.execute("SELECT id FROM products WHERE sku='DIS-2001'").fetchone()
            pid = row['id']

        response = self.client.post(f'/products/{pid}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Product deleted', response.data)

    def test_search_and_filter(self):
        self.login()
        # Search by keyword
        res = self.client.get('/?q=Webcam')
        self.assertIn(b'Webcam HD', res.data)

        # Low stock filter
        res_low = self.client.get('/?low=1')
        self.assertEqual(res_low.status_code, 200)


if __name__ == '__main__':
    unittest.main()
