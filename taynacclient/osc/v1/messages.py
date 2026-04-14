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
import os

from nectarclient_lib import exceptions
from osc_lib.command import command


class SendMessage(command.ShowOne):
    """Send message"""

    log = logging.getLogger(__name__ + '.SendMessage')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        parser.add_argument(
            '--recipient',
            required=True,
            metavar='<recipient>',
            help="Email address of the recipient",
        )
        parser.add_argument(
            '--subject',
            metavar='<subject>',
            required=True,
            help="Email subject.",
        )
        body_group = parser.add_mutually_exclusive_group(required=True)
        body_group.add_argument(
            '--body',
            metavar='<body>',
            help='Email body as a string.',
        )
        body_group.add_argument(
            '--body-file',
            metavar='<body-file>',
            dest='body_file',
            help='Path to a file containing the email body.',
        )
        parser.add_argument(
            '--cc',
            action='append',
            metavar='<cc>',
            default=[],
            help='Carbon Copy recipient. \
                 To add multiple CCs specify this option multiple times.',
        )
        parser.add_argument(
            '--tag',
            action='append',
            metavar='<tag>',
            dest='tags',
            default=[],
            help='Freshdesk tag. \
                 To add multiple tags specify this option multiple times',
        )
        parser.add_argument(
            '--backend-id',
            default=None,
            metavar='<backend-id>',
            dest='backend_id',
            help='A backend-id for a previous user notification. '
            'If this is provided, this message is a reply. '
            'Some other options may be ignored by the '
            'the user notification service backend.',
        )
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        client = self.app.client_manager.taynac
        if parsed_args.body_file:
            body_file = os.path.expanduser(parsed_args.body_file)
            with open(body_file) as f:
                body = f.read()
        else:
            body = parsed_args.body
        try:
            data = client.messages.send(
                parsed_args.subject,
                body,
                parsed_args.recipient,
                parsed_args.cc,
                parsed_args.tags,
                parsed_args.backend_id,
            )
        except Exception as ex:
            raise exceptions.CommandError(str(ex))

        return self.dict2columns(data.to_dict())
