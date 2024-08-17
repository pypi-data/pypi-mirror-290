"""
pymdfu CLI: "pymdfu"
"""
import sys
import logging
import os
import textwrap
import argparse
from logging.config import dictConfig
try:
    # When Python 3.11 becomes the minimum supported version for this tool
    # we can remove the tomli fallback solution here since this version
    # will have tomllib in its standard library.
    import tomllib as toml_reader
except ModuleNotFoundError:
    import tomli as toml_reader #pylint: disable=import-error
from appdirs import user_log_dir
from pymdfu.tools import ToolArgumentParser
from pymdfu.mac.exceptions import MacError
from .status_codes import STATUS_SUCCESS, STATUS_FAILURE
from .tools.tools import ToolFactory, supported_tools
from .mdfu import Mdfu, MdfuUpdateError, MdfuProtocolError, mdfu_protocol_version

try:
    from . import __version__ as VERSION
    from . import BUILD_DATE, COMMIT_ID
except ImportError:
    print("Version info not found!")
    VERSION = "0.0.0"
    COMMIT_ID = "N/A"
    BUILD_DATE = "N/A"

def update(args):
    """Perform firmware update

    :param args: Arguments from command line
    :type args: dict
    """
    logger = logging.getLogger(__name__)
    try:
        with open(args.image, "rb") as file:
            image = file.read()
            try:
                tool = ToolFactory.get_tool(args.tool, tool_args=args.tool_args)
            except ValueError as exc:
                help_txt = CliHelp.tool_usage_help(CliHelp.USAGE_UPDATE_CMD, args.tool, msg=exc)
                print(help_txt)
                return STATUS_FAILURE
            except MacError as exc:
                logger.error(exc)
                return STATUS_FAILURE
            mdfu = Mdfu(tool)
            try:
                mdfu.run_upgrade(image)
                logger.info("Upgrade finished successfully")
            except MdfuUpdateError as exc:
                logger.error(exc)
                logger.error("Upgrade failed")
                return STATUS_FAILURE
    except FileNotFoundError:
        logger.error("Invalid image file: No such file or directory '%s'", args.image)
        return STATUS_FAILURE
    return STATUS_SUCCESS

def client_info(args):
    """Get and print client information

    :param args: Command line arguments
    :type args: dict
    """
    logger = logging.getLogger(__name__)
    try:
        tool = ToolFactory.get_tool(args.tool, tool_args=args.tool_args)
    except ValueError as exc:
        help_txt = CliHelp.tool_usage_help(CliHelp.USAGE_CLIENT_INFO_CMD, args.tool, msg=exc)
        print(help_txt)
        return STATUS_FAILURE
    except MacError as exc:
        logger.error(exc)
        return STATUS_FAILURE
    mdfu = Mdfu(tool)
    try:
        mdfu.open()
        client = mdfu.get_client_info(sync=True)
        logger.info(client)
    except (ValueError, MdfuProtocolError):
        logger.error("Failed to get client info")
        return STATUS_FAILURE
    finally:
        mdfu.close()
    return STATUS_SUCCESS

def tools_help(args):
    """Print tool specific parameters
    
    :param args: Command line arguments.
    :type args: dict
    """
    # We expect no parameters for this action so if there are any we
    # print an error and exit
    if len(args.tool_args):
        txt = CliHelp.USAGE_TOOLS_HELP_CMD
        txt += "pymdfu: error: unrecognized arguments: "
        for arg in args.tool_args:
            txt += f"{arg} "
        txt += "\n"
        print(txt, file=sys.stderr)
        return STATUS_FAILURE
    txt = CliHelp.tools_parameter_help()
    print(txt)
    return STATUS_SUCCESS

def setup_logging(user_requested_level=logging.WARNING, default_path='logging.toml',
                  env_key='MICROCHIP_PYTHONTOOLS_CONFIG'):
    """
    Setup logging configuration for this CLI
    """
    # Logging config TOML file can be specified via environment variable
    value = os.getenv(env_key, None)
    if value:
        path = value
    else:
        # Otherwise use the one shipped with this application
        path = os.path.join(os.path.dirname(__file__), default_path)
    # Load the TOML if possible
    if os.path.exists(path):
        try:
            with open(path, 'rb') as file:
                # Load logging configfile from toml
                configfile = toml_reader.load(file)
                # File logging goes to user log directory under Microchip/modulename
                logdir = user_log_dir(__name__, "Microchip")
                # Look through all handlers, and prepend log directory to redirect all file loggers
                num_file_handlers = 0
                for handler in configfile['handlers'].keys():
                    # A filename key
                    if 'filename' in configfile['handlers'][handler].keys():
                        configfile['handlers'][handler]['filename'] = os.path.join(
                            logdir, configfile['handlers'][handler]['filename'])
                        num_file_handlers += 1
                if num_file_handlers > 0:
                    # Create it if it does not exist
                    os.makedirs(logdir, exist_ok=True)

                if user_requested_level <= logging.DEBUG:
                    # Using a different handler for DEBUG level logging to be able to have a more detailed formatter
                    configfile['root']['handlers'].append('console_detailed')
                    # Remove the original console handlers
                    try:
                        configfile['root']['handlers'].remove('console_only_info')
                    except ValueError:
                        # The TOML file might have been customized and the console_only_info handler might
                        # already have been removed
                        pass
                    try:
                        configfile['root']['handlers'].remove('console_not_info')
                    except ValueError:
                        # The TOML file might have been customized and the console_only_info handler might
                        # already have been removed
                        pass
                else:
                    # Console logging takes granularity argument from CLI user
                    configfile['handlers']['console_only_info']['level'] = user_requested_level
                    configfile['handlers']['console_not_info']['level'] = user_requested_level

                # Root logger must be the most verbose of the ALL TOML configurations and the CLI user argument
                most_verbose_logging = min(user_requested_level, getattr(logging, configfile['root']['level']))
                for handler in configfile['handlers'].keys():
                    # A filename key
                    if 'filename' in configfile['handlers'][handler].keys():
                        level = getattr(logging, configfile['handlers'][handler]['level'])
                        most_verbose_logging = min(most_verbose_logging, level)
                configfile['root']['level'] = most_verbose_logging
            dictConfig(configfile)
            return
        except (toml_reader.TOMLDecodeError, TypeError):
            # Error while parsing TOML config file
            print(f"Error parsing logging config file '{path}'")
        except KeyError as keyerror:
            # Error looking for custom fields in TOML
            print(f"Key {keyerror} not found in logging config file")
    else:
        # Config specified by environment variable not found
        print(f"Unable to open logging config file '{path}'")

    # If all else fails, revert to basic logging at specified level for this application
    print("Reverting to basic logging.")
    logging.basicConfig(level=user_requested_level)

class CliHelp():
    """CLI help"""
    USAGE = textwrap.dedent("""\
    pymdfu [--help | -h] [--verbose <level> | -v <level>] [--version | -V] [--release-info | -R] [<action>]
    
    """)
    USAGE_UPDATE_CMD = \
    "pymdfu [--help | -h] [--verbose <level> | -v <level>] [--config-file <file> | -c <file>] "\
    "update --tool <tool> --image <image> [<tools-args>...]\n"

    USAGE_CLIENT_INFO_CMD = \
    "pymdfu [--help | -h] [--verbose <level> | -v <level>] [--config-file <file> | -c <file>] "\
    "client-info --tool <tool> [<tools-args>...]\n"

    USAGE_TOOLS_HELP_CMD = textwrap.dedent("""\
    pymdfu [--help | -h] [--verbose <level> | -v <level>] tools-help
    
    """)
    COMMON_OPTIONS = textwrap.dedent("""\
            -v <level>, --verbose <level>
                            Logging verbosity/severity level. Valid levels are
                            [debug, info, warning, error, critical].
                            Default is info.
    """)
    USAGE_EXAMPLES = textwrap.dedent("""\
    Usage examples

        Update firmware through serial port and with update_image.img
            pymdfu update --tool serial --image update_image.img --port COM11 --baudrate 115200
    """)

    @classmethod
    def cli_help(cls):
        """Create help text for main CLI entrypoint

        Help text for
            pymdfu
            pymdfu --help
        
        :return: CLI help text
        :rtype: str
        """
        cli_help_txt = textwrap.dedent(f'''\
        {cls.USAGE}
            pymdfu: Command line interface for Microchip Device Firmware Update (MDFU) clients.
    
        Actions
            <action>        Action to perform. Valid actions are:
                            client-info: Get MDFU client information
                            tools-help:  Get help on tool specific parameters
                            update:      Perform a firmware update
            
            -h, --help      Show this help message and exit
        
            -V, --version   Print pymdfu version number and exit
        
            -R, --release-info
                            help=Print pymdfu release details and exit

        Optional arguments
        {textwrap.indent(cls.COMMON_OPTIONS,"    ")}
        Usage examples

            Update firmware through serial port and with update_image.img
            pymdfu update --tool serial --image update_image.img --port COM11 --baudrate 115200
        ''')

        return cli_help_txt

    @classmethod
    def client_info_cmd_help(cls):
        """Create help text for client info action

        Help text for
            pymdfu client-info --help
        
        :return: Help text for CLI client-info action
        :rtype: str
        """
        client_info_help = textwrap.dedent(f"""\
        {cls.USAGE_CLIENT_INFO_CMD}
        Required arguments
            --tool <tool>   Tool to use for connecting to MDFU client.
                            Valid tools are {cls.supported_tools()}.
        
            <tool-args>     Tool specific arguments. Run
                                pymdfu tools-help
                            for help on tool specific parameters.
        
        Optional arguments
        {textwrap.indent(cls.COMMON_OPTIONS,"    ")}
            -c, --config-file
                            Configuration file with tool specific parameters.
                            Parameters specified on command line will override
                            any parameters present in the configuration file.

            -h, --help      Show this help message and exit
            
        """)
        return client_info_help

    @classmethod
    def update_cmd_help(cls):
        """Create help text for update action

        Help text for
            pymdfu update --help
        
        :return: Help text for CLI update action
        :rtype: str
        """
        update_help_text = textwrap.dedent(f"""\
        {cls.USAGE_UPDATE_CMD}
        Required arguments      
            --tool <tool>   Tool to use for connecting to MDFU client.
                            Valid tools are {cls.supported_tools()}.
            
            --image <image> FW image file to transfer to MDFU client.
            
            <tool-args>     Tool specific arguments. Run
                                pymdfu tools-help
                            for help on tool specific parameters.
        
        Optional arguments
        {textwrap.indent(cls.COMMON_OPTIONS,"    ")}
            -c, --config-file
                            Configuration file with tool specific parameters.
                            Parameters specified on command line will override
                            any parameters present in the configuration file.
            
            -h, --help      Show this help message and exit
            
        """)
        return update_help_text

    @classmethod
    def tools_help_cmd_help(cls):
        """Create help text for tools-help action

        Help text for
            pymdfu tools-help --help
        
        :return: tools-help action help text
        :rtype: str
        """
        tools_help_text = textwrap.dedent(f"""\
        {cls.USAGE_TOOLS_HELP_CMD}
        Show tools specific command line arguments.

        Optional arguments
        {textwrap.indent(cls.COMMON_OPTIONS,"    ")}
            -h, --help      Show this help message and exit            
        """)
        return tools_help_text

    @classmethod
    def supported_tools(cls):
        """Create a string with supported tools

        E.g. "[serial, aardvark]"
        :return: List of supported tools
        :rtype: str
        """
        supported_tools_txt = "["
        for tool_name,_ in supported_tools.items():
            supported_tools_txt += f"{tool_name}, "
        supported_tools_txt = supported_tools_txt[:-2] + ']'
        return supported_tools_txt

    @classmethod
    def tools_parameter_help(cls):
        """Create help text for tools specific parameters

        Text for
            pymdfu tools-help
        
        :return: Help text
        :rtype: str
        """
        tools_help_txt = ""
        for tool_name in supported_tools:
            tool = ToolFactory.get_tool_class(tool_name)
            tools_help_txt += f"{tool.tool_help()}\n\n{tool.parameter_help()}\n\n"
        return tools_help_txt

    @classmethod
    def tool_usage_help(cls, cli_usage, tool_name, msg=None):
        """Create tool specific CLI usage help

        :param cli_usage: CLI usage text that contains '<tool>'
        and '[<tools-args>...]'. Both of them will be replaced with
        tool specific parameters based on tool_name input.
        :type cli_usage: str
        :param tool_name: Tool name
        :type tool_name: str
        :param msg: Error message, defaults to None
        :type msg: str, optional
        :return: CLI usage wiht optional error message
        :rtype: str
        """
        tool = ToolFactory.get_tool_class(tool_name)
        usage_tool = tool.usage_help()
        usage = cli_usage.replace("<tool>", tool_name)
        usage = usage.replace("[<tools-args>...]", usage_tool)
        if msg:
            usage = usage + "\n" + "Tool parameter error: " + str(msg)
        return usage

def main():
    """
    Entrypoint for installable CLI

    Configures the CLI and parses the arguments
    """
    if len(sys.argv) < 2:
        print(CliHelp.cli_help())
        return STATUS_SUCCESS

    config_parser = ToolArgumentParser(add_help=False)
    config_parser.add_argument("-c", "--config-file", type=str, default=None)
    args, unparsed_args = config_parser.parse_known_args()

    config = None
    if args.config_file:
        with open(args.config_file, 'rb') as file:
            config = toml_reader.load(file)

    # When a config file is availalbe add any parameters from the common section
    # to the command line arguments unless they are already present.
    if config:
        try:
            for key, value in config['common'].items():
                if not any(item in [f"--{key}", f"-{key[0]}"] for item in unparsed_args):
                    unparsed_args.append(f"--{key}")
                    unparsed_args.append(str(value))
        except KeyError:
            pass

    common_argument_parser = ToolArgumentParser(add_help=False)
    common_argument_parser.add_argument("-v", "--verbose",
                                        default="info",
                                        choices=['debug', 'info', 'warning', 'error', 'critical'])
    common_argument_parser.add_argument("-h", "--help", action="store_true")

    parser = argparse.ArgumentParser(
            add_help=False,
            usage=CliHelp.USAGE,
            prog="pymdfu",
            parents=[common_argument_parser])

    # Action-less switches.  These are all "do X and exit"
    parser.add_argument("-V", "--version", action="store_true")
    parser.add_argument("-R", "--release-info", action="store_true")

    # First 'argument' is the command, which is a sub-parser
    subparsers = parser.add_subparsers(title='actions', dest='action')
    # Make the command required but not for -V or -R arguments
    subparsers.required = \
        not any(arg in ["-V", "--version", "-R", "--release-info", "-h", "--help"] for arg in sys.argv)

    client_info_cmd = subparsers.add_parser(name='client-info',
                                        usage=CliHelp.USAGE_CLIENT_INFO_CMD,
                                        prog="pymdfu",
                                        add_help=False,
                                        parents=[common_argument_parser])
    client_info_cmd.set_defaults(func=client_info)

    client_info_cmd.add_argument("--tool", choices=supported_tools,
                                    required= not any(arg in ["-h", "--help"] for arg in sys.argv))

    update_cmd = subparsers.add_parser(name='update',
                                        usage=CliHelp.USAGE_UPDATE_CMD,
                                        add_help=False,
                                        prog="pymdfu",
                                        parents=[common_argument_parser])

    update_cmd.set_defaults(func=update)
    update_cmd.add_argument("--tool", choices=supported_tools,
                            required=not any(arg in ["-h", "--help"] for arg in sys.argv))
    update_cmd.add_argument("--image", type=str, required=not any(arg in ["-h", "--help"] for arg in sys.argv))

    tool_help = subparsers.add_parser(name='tools-help',
                                        add_help=False,
                                        parents=[common_argument_parser])
    tool_help.set_defaults(func=tools_help)

    # Parse
    args, tool_args = parser.parse_known_args(unparsed_args)

    # When a configuration file is avialble we add the parameters as
    # command line arguments unless they already exist there (CLI parameters take precedence).
    # We only allow long parameter form e.g. --baudrate for simplicity.
    if config:
        try:
            for key, value in config[args.tool].items():
                if f"--{key}" not in tool_args:
                    tool_args.append(f"--{key}")
                    tool_args.append(str(value))
        # If we have a key error the specific tool section does not exist in the
        # toml configuration file and we don't have anything to do here.
        except KeyError:
            pass

    args.tool_args = tool_args
    # Setup logging
    setup_logging(user_requested_level=getattr(logging, args.verbose.upper()))
    logger = logging.getLogger("pymdfu")
    logger.debug(args)

    if args.help:
        txt = ""
        if hasattr(args, "action") and args.action is not None:
            if args.action == "update":
                txt = CliHelp.update_cmd_help()
            elif args.action == "client-info":
                txt = CliHelp.client_info_cmd_help()
            elif args.action == "tools-help":
                txt = CliHelp.tools_help_cmd_help()
        else:
            txt = CliHelp.cli_help()
        print(txt)
        return STATUS_SUCCESS
    # Dispatch
    if args.version or args.release_info:
        print(f"pymdfu version {VERSION}")
        print(f"MDFU protocol version {mdfu_protocol_version}")
        if args.release_info:
            print(f"Build date:  {BUILD_DATE}")
            print(f"Commit ID:   {COMMIT_ID}")
            print(f"Installed in {os.path.abspath(os.path.dirname(__file__))}")
        return STATUS_SUCCESS

    # Call the command handler
    return args.func(args)

if __name__ == "__main__":
    sys.exit(main())
