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
from openstackclient.identity import common as identity_common
from osc_lib.command import command


class SendMessage(command.ShowOne):
    """Send message"""

    log = logging.getLogger(__name__ + '.SendMessage')

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        recipient_group = parser.add_mutually_exclusive_group(required=True)
        recipient_group.add_argument(
            '--recipient',
            metavar='<recipient>',
            help="Email address of the recipient",
        )
        recipient_group.add_argument(
            '--project',
            '--project-id',
            metavar='<project>',
            dest='project',
            help='Keystone project (name or ID) to notify. The service '
            'resolves the recipients itself: the first tenant manager '
            'becomes the recipient and other tenant managers and '
            'members are cc\'d.',
        )
        parser.add_argument(
            '--project-domain',
            metavar='<project_domain>',
            default='default',
            help='Domain of the project (name or ID)',
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
        project_id = None
        if parsed_args.project:
            identity_client = self.app.client_manager.identity
            project_id = identity_common.find_project(
                identity_client,
                identity_common._get_token_resource(
                    identity_client, 'project', parsed_args.project
                ),
                parsed_args.project_domain,
            ).id
        try:
            data = client.messages.send(
                subject=parsed_args.subject,
                body=body,
                recipient=parsed_args.recipient,
                cc=parsed_args.cc,
                tags=parsed_args.tags,
                backend_id=parsed_args.backend_id,
                project_id=project_id,
            )
        except Exception as ex:
            raise exceptions.CommandError(str(ex))

        return self.dict2columns(data.to_dict())
