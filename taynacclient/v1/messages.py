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

from nectarclient_lib import base


class Message(base.Resource):

    def __repr__(self):
        return "<Message %s>" % self._info


class MessageManager(base.Manager):

    base_url = 'v1/message'
    resource_class = Message

    def send(self, subject, body, recipient, cc=[]):
        data = {'subject': subject, 'body': body,
                'recipient': recipient, 'cc': cc}
        url = '/%s/' % (self.base_url)
        return self._post(url, data=data)
