import unittest
import os

os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
    
    def test_home(self):
        response = self.client.get("/aboutSebas")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert '''<h3>A passionate fullstack developer from Mexico</h3>''' in html

        response = self.client.get("/aboutSebas-work")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<h2>Work Experience and Projects</h2>" in html

        response = self.client.get("/aboutSebas-hobbies")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<h2>Hobbies</h2>" in html

        response = self.client.get("/aboutSebas-education")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<h2>Education</h2>" in html

        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert '''<h1 class="timeline-title">My Timeline</h1>''' in html
        
    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        
    
    def test_timeline_post_endpoint(self):
        response=self.client.post("/api/timeline_post", data= {"name":"alice","email":"alicia@example.com","content":"Hello world,I'm Alicia!"})
        assert response.is_json
        json = response.get_json()
        assert "alice" in json["name"]

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post", data={"email": "john@example.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Name is required." in html

        # POST request with empty content
        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Content is required." in html

        # POST request with malformed email
        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "not-an-email", "content": "Hello  world, I'm John"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
