from ast import literal_eval

from django.test import TestCase, Client

# Create your tests here.
class URLShortenerAPITest(TestCase):
    """ URL Shortener API test """

    def test_index(self):
        """ index() test """
        # should be 200 for GET method and 403 for the others
        client = Client()
        response = client.get("/")
        self.assertEqual(response.status_code, 200)

        response = client.post("/", {})
        self.assertEqual(response.status_code, 403)

        response = client.put("/", {})
        self.assertEqual(response.status_code, 403)
        
        response = client.delete("/", {})
        self.assertEqual(response.status_code, 403)
    
    def test_post_encode(self):
        """ post_encode_url() test """
        # should be 200 for correct URL
        client = Client()
        response = client.post("/url-enc", {"url": "https://www.github.com/"})
        self.assertEqual(response.status_code, 200)
        content_previous = response.content

        # should return the same shorten url if an URL that already exists in DB
        response = client.post("/url-enc", {"url": "https://www.github.com/"})
        self.assertEqual(response.content, content_previous)

        # should also be 200 for correct url (http protocol omitted)
        response = client.post("/url-enc", {"url": "www.github.com"})
        self.assertEqual(response.status_code, 200)

        # if given URL is not valid, response status code should not be 200
        response = client.post("/url-enc", {"url": "github"})
        self.assertNotEqual(response.status_code, 200)
    
        # should be 403 for the other methods
        client = Client()
        response = client.get("/url-enc", {"url": "https://www.github.com/"})
        self.assertEqual(response.status_code, 403)

        response = client.put("/url-enc", {"url": "https://www.github.com/"})
        self.assertEqual(response.status_code, 403)
        
        response = client.delete("/url-enc", {"url": "https://www.github.com/"})
        self.assertEqual(response.status_code, 403)
    
    def test_get_decode(self):
        """ get_decode_url() test """
        # setup        
        client = Client()
        response = client.post("/url-enc", {"url": "https://www.github.com/"})
        shorten_url = literal_eval(response.content.decode("utf-8"))["shorten_url"]
        code = shorten_url[shorten_url.rfind("/")+1:]

        # should be 302 (redirected) for GET method
        response = client.get("/"+code)
        self.assertEqual(response.status_code, 302)

        # should be 404 for URL that does not exist in DB
        response = client.get("/"+code[::-1])
        self.assertEqual(response.status_code, 404)

        # should be 403 for the other methods
        response = client.post("/"+code, {})
        self.assertEqual(response.status_code, 403)

        response = client.put("/"+code, {})
        self.assertEqual(response.status_code, 403)
        
        response = client.delete("/"+code, {})
        self.assertEqual(response.status_code, 403)
