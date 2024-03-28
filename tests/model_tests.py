import pytest
from blogProject import create_app, db
from blogProject.models import Admin, BlogPost

@pytest.fixture(scope='module')
def test_app():
    """Create and configure a new app instance for each test."""
    app = create_app()  # Assuming you have a testing config
    with app.app_context():
        db.create_all()
        yield app  # this is where the testing happens!
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def new_admin():
    """Fixture to create a new admin."""
    admin = Admin(user_name='admin', email='admin@example.com')
    admin.set_password('test')
    return admin

@pytest.fixture(scope='function')
def new_blog_post(new_admin):
    """Fixture to create a new blog post."""
    post = BlogPost(title='Test Post', content='Test content', admin_id=new_admin.id)
    return post

def test_admin_password_setter(new_admin):
    """Test password is being hashed."""
    assert new_admin.password is not None

def test_admin_password_verification(new_admin):
    """Test password hashing and verification."""
    assert new_admin.check_password('test')
    assert not new_admin.check_password('wrong')

def test_admin_password_salts_are_random():
    """Ensure different salts are used for hashing."""
    admin1 = Admin(user_name='admin1', email='admin1@example.com')
    admin2 = Admin(user_name='admin2', email='admin2@example.com')
    admin1.set_password('test')
    admin2.set_password('test')
    assert admin1.password != admin2.password

def test_blog_post_creation(test_app, new_admin):
    """Test blog post creation."""
    with test_app.app_context():
        db.session.add(new_admin)
        db.session.commit()
        post = BlogPost(title='Test Post', content='Test content', admin_id=new_admin.id)
        db.session.add(post)
        db.session.commit()
        assert post.id is not None
        assert post.title == 'Test Post'
        assert post.content == 'Test content'
        assert post.admin_id == new_admin.id
