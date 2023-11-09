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

from nectarclient_lib.tests.unit import utils

from taynacclient.tests.unit.v1 import fakes


class MessageTest(utils.TestCase):

    def setUp(self):
        super(MessageTest, self).setUp()
        self.cs = fakes.FakeClient()

    def test_send(self):
        response = self.cs.messages.send(
            subject="Test", body="Hi",
            recipient="bob@example.com",
            cc=["jack@example.com"])
        self.cs.assert_called('POST', '/v1/message/')
        self.assertEqual(fakes.generic_message['backend_id'],
                         response.backend_id)
