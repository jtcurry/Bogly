from app import app
from unittest import TestCase
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class Usertests(TestCase):

    def setUp(self):
        User.query.delete()
        user = User(first_name="TestFirst", last_name="TestLast")
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id

    def teardown(self):
        db.session.rollback()

    def test_show_users(self):
        """Test if user list shows current users"""
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestFirst', html)

    def test_user_info(self):
        """Test if correct user info is displayed"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h2>TestFirst TestLast</h2>", html)

    def test_add_user(self):
        """Test if new user can be added"""
        with app.test_client() as client:
            d = {"first_name": "Allen", "last_name": "Apple",
                 "image_url": "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<li><a href="/users/2">Allen Apple</a></li>', html)

    def test_remove_user(self):
        """Test if user can be deleted"""
        with app.test_client() as client:
            d = {"first_name": "Billy", "last_name": "Banana",
                 "image_url": "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"}
            client.post("/users/new", data=d, follow_redirects=True)
            resp = client.post("/users/4/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertNotIn(
                '<li><a href="/users/4">Billy Banana</a></li>', html)
