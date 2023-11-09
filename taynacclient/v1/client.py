#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

from nectarclient_lib import exceptions

from taynacclient import client
from taynacclient.v1 import messages


class Client(object):
    """Client for taynac v1 API
    :param string session: session
    :type session: :py:class:`keystoneauth.adapter.Adapter`
    """

    def __init__(self, session=None, service_type='message',
                 **kwargs):
        """Initialize a new client for the taynac v1 API."""
        if session is None:
            raise exceptions.ClientException(
                message='Session is required argument')
        self.http_client = client.SessionClient(
            session, service_type=service_type, **kwargs)
        self.messages = messages.MessageManager(self.http_client)
