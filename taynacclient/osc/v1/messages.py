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

import logging
from nectarclient_lib import exceptions
from osc_lib.command import command


class SendMessage(command.ShowOne):
    """Send message"""

    log = logging.getLogger(__name__ + '.SendMessage')

    def get_parser(self, prog_name):
        parser = super(SendMessage, self).get_parser(prog_name)
        parser.add_argument(
            '--recipient',
            required=True,
            metavar='<recipient>',
            help="Email address of the recipient"
        )
        parser.add_argument(
            '--subject',
            metavar='<subject>',
            required=True,
            help="Email subject"
        )
        parser.add_argument(
            '--body',
            required=True,
            metavar='<body>',
            help='Email body',
        )
        parser.add_argument(
            '--cc',
            action='append',
            metavar='<cc>',
            default=[],
            help='Carbon Copy recipient.\
                 To add multiple CC\'s specify this option multiple times'
        )

        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.taynac
        try:
            data = client.messages.send(parsed_args.subject,
                                        parsed_args.body,
                                        parsed_args.recipient,
                                        parsed_args.cc)
        except Exception as ex:
            raise exceptions.CommandError(str(ex))

        return self.dict2columns(data.to_dict())
