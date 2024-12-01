from django.contrib.auth.models import User


class EmailAuthBackend:
    '''Authenticate using an e-mail address.'''

    def authenticate(self, request, username=None, password=None):
        '''Hey'''
        return self