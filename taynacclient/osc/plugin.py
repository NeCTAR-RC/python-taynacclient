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

from osc_lib import utils


DEFAULT_API_VERSION = '1'

# Required by the OSC plugin interface
API_NAME = 'taynac'
API_VERSION_OPTION = 'os_taynac_api_version'
API_VERSIONS = {
    '1': 'taynacclient.v1.client.Client',
}


# Required by the OSC plugin interface
def make_client(instance):
    """Returns a client to the ClientManager

    Called to instantiate the requested client version.  instance has
    any available auth info that may be required to prepare the client.

    :param ClientManager instance: The ClientManager that owns the new client
    """
    plugin_client = utils.get_client_class(
        API_NAME, instance._api_version[API_NAME], API_VERSIONS
    )

    endpoint = instance._cli_options.taynac_endpoint
    client = plugin_client(
        session=instance.session, endpoint_override=endpoint
    )
    return client


# Required by the OSC plugin interface
def build_option_parser(parser):
    """Hook to add global options

    Called from openstackclient.shell.OpenStackShell.__init__()
    after the builtin parser has been initialized.  This is
    where a plugin can add global options such as an API version setting.

    :param argparse.ArgumentParser parser: The parser object that has been
        initialized by OpenStackShell.
    """
    parser.add_argument(
        '--os-taynac-api-version',
        metavar='<taynac-api-version>',
        help='taynac API version, default='
        + DEFAULT_API_VERSION
        + ' (Env: OS_taynac_API_VERSION)',
    )
    parser.add_argument(
        '--os-taynac-endpoint',
        metavar='<taynac-endpoint>',
        help='taynac API endpoint',
    )
    return parser
