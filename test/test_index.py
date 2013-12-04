
import json

import base


class TestIndex(base.TestCase):

    """The Index module is fake at the moment, hence the unit tests only
       test the return codes
    """

    def test_users(self):
        # GET
        resp = self.http_client.get('/v1/users/')
        self.assertEqual(resp.status_code, 200, resp.data)
        # POST
        resp = self.http_client.post('/v1/users/',
                                     data=json.dumps('JSON DATA PLACEHOLDER'))
        self.assertEqual(resp.status_code, 201, resp.data)
        # PUT
        resp = self.http_client.put('/v1/users/{0}/'.format(
                                    self.gen_random_string()))
        self.assertEqual(resp.status_code, 204, resp.data)

    def test_repository_images(self):
        repo = 'test/{0}'.format(self.gen_random_string())
        images = [{'id': self.gen_random_string()},
                  {'id': self.gen_random_string()}]
        # PUT
        resp = self.http_client.put('/v1/repositories/{0}/'.format(repo),
                                    data=json.dumps(images))
        self.assertEqual(resp.status_code, 200, resp.data)
        resp = self.http_client.put('/v1/repositories/{0}/images'.format(repo),
                                    data=json.dumps(images))
        self.assertEqual(resp.status_code, 204, resp.data)

        #Upload and Tag Image
        image_one = images[0]['id']
        image_two = images[1]['id']
        layer_data = self.gen_random_string(1024)
        self.upload_image(image_one, parent_id=None, layer=layer_data)
        self.upload_image(image_two, parent_id=None, layer=layer_data)

        url = '/v1/repositories/{0}/tags/1.1'.format(repo)
        resp = self.http_client.put(url, data=json.dumps(image_one))
        url = '/v1/repositories/{0}/tags/1.2'.format(repo)
        resp = self.http_client.put(url, data=json.dumps(image_two))
        # GET
        resp = self.http_client.get('/v1/repositories/{0}/images'.format(repo))
        self.assertEqual(resp.status_code, 200, resp.data)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)
        self.assertTrue('id' in data[0])
        # DELETE
        resp = self.http_client.delete('/v1/repositories/{0}/images'.format(
            repo))
        self.assertEqual(resp.status_code, 204, resp.data)

    def test_auth(self):
        repo = 'test/{0}'.format(self.gen_random_string())
        resp = self.http_client.put('/v1/repositories/{0}/auth'.format(repo))
        self.assertEqual(resp.status_code, 200, resp.data)

    def test_search(self):
        search_term = self.gen_random_string()
        resp = self.http_client.get('/v1/search?q={0}'.format(search_term))
        self.assertEqual(resp.status_code, 200, resp.data)
