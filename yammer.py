import json
import time
import urllib
import urlparse
import oauth2 as oauth

class Endpoint(object):
    def __init__(self, yammer):
        self.yammer = yammer

    def _get(self, endpoint, **params):
        return self.yammer._apicall(endpoint, 'GET', **params)

    def _post(self, endpoint, **params):
        return self.yammer._apicall(endpoint, 'POST', **params)

    def _delete(self, endpoint, **params):
        return self.yammer._apicall(endpoint, 'DELETE', **params)


class MessageEndpoint(Endpoint):

    def all(self, older_than=None, newer_than=None, threaded=None):
        return self._get('messages', older_than=older_than,
                         newer_than=newer_than, threaded=threaded)

    def sent(self, older_than=None, newer_than=None, threaded=None):
        return self._get('messages/sent', older_than=older_than,
                         newer_than=newer_than, threaded=threaded)

    def received(self, older_than=None, newer_than=None, threaded=None):
        return self._get('messages/received', older_than=older_than,
                         newer_than=newer_than, threaded=threaded)

    def following(self, older_than=None, newer_than=None, threaded=None):
        return self._get('messages/following', older_than=older_than,
                         newer_than=newer_than, threaded=threaded)

    def from_user(self, id, older_than=None, newer_than=None, threaded=None):
        return self._get('messages/from_user/%s' % id, older_than=older_than,
                         newer_than=newer_than, threaded=threaded)

    def from_bot(self, id, older_than=None, newer_than=None, threaded=None):
        return self._get('messages/from_bot/%s' % id, older_than=older_than,
                         newer_than=newer_than, threaded=threaded)

    def tagged_with(self, id, older_than=None, newer_than=None, threaded=None):
        return self._get('messages/tagged_with/%s' % id, older_than=older_than,
                         newer_than=newer_than, threaded=threaded)

    def in_group(self, id, older_than=None, newer_than=None, threaded=None):
        return self._get('messages/in_group/%s' % id, older_than=older_than,
                         newer_than=newer_than, threaded=threaded)

    def favorites_of(self, id, older_than=None, newer_than=None, threaded=None):
        return self._get('messages/favorites_of/%s' % id, older_than=older_than,
                         newer_than=newer_than, threaded=threaded)

    def in_thread(self, id, older_than=None, newer_than=None, threaded=None):
        return self._get('messages/in_thread/%s' % id, older_than=older_than,
                         newer_than=newer_than, threaded=threaded)

    def post(self, body, group_id=None, replied_to_id=None, direct_to_id=None):
        # doesn't support attachments
        return self._post('messages/', group_id=group_id,
                          replied_to_id=replied_to_id, body=body,
                          direct_to_id=direct_to_id)

    def delete(self, message_id):
        return self._delete('messages/%s' % message_id)

class Yammer(object):
    request_token_url = 'https://www.yammer.com/oauth/request_token'
    access_token_url = 'https://www.yammer.com/oauth/access_token'
    authorize_url = 'https://www.yammer.com/oauth/authorize'
    base_url = 'https://www.yammer.com/api/v1/'

    def __init__(self, consumer_key, consumer_secret, oauth_token=None, oauth_token_secret=None):
        self.consumer = oauth.Consumer(consumer_key, consumer_secret)
        if oauth_token and oauth_token_secret:
            self.token = oauth.Token(oauth_token, oauth_token_secret)
        else:
            self.token = None
        self.client = oauth.Client(self.consumer, self.token)

        # connect endpoints
        self.messages = MessageEndpoint(self)

    # authorization
    @property
    def request_token(self):
        if not hasattr(self, '_request_token'):
            resp, content = self.client.request(self.request_token_url, "GET")
            if resp['status'] != '200':
                raise Exception("Invalid response %s." % resp['status'])

            self._request_token = dict(urlparse.parse_qsl(content))
        return self._request_token

    def get_authorize_url(self):
        return "%s?oauth_token=%s" % (self.authorize_url, self.request_token['oauth_token'])

    def get_access_token(self, oauth_verifier):
        # set verifier
        token = oauth.Token(self.request_token['oauth_token'],
                            self.request_token['oauth_token_secret'])
        token.set_verifier(oauth_verifier)
        self.client = oauth.Client(self.consumer, token)

        # parse response
        resp, content = yammer.client.request(self.access_token_url, "POST")
        access_token = dict(urlparse.parse_qsl(content))
        return access_token

    # requests
    def _apicall(self, endpoint, method, **params):
        if method == 'GET':
            suffix = '.json'
        else:
            suffix = ''
        url = '%s%s%s' % (self.base_url, endpoint, suffix)
        print url
        body = None
        cleaned_params = dict([(k,v) for k,v in params.iteritems() if v])

        if cleaned_params:
            body = urllib.urlencode(cleaned_params)
            if method == 'GET':
                url = '%s?%s' % (url, body)
                body = None

        resp, content = self.client.request(url, method=method, body=body)
        return json.loads(content)


