"""
    SnapCTL entrypoint
"""
import configparser
import os
from sys import platform
from typing import Union, Callable
import typer

from snapctl.commands.byosnap import ByoSnap
from snapctl.commands.byogs import ByoGs
from snapctl.commands.snapend import Snapend
from snapctl.config.constants import API_KEY, CONFIG_FILE_MAC, CONFIG_FILE_WIN, DEFAULT_PROFILE, \
    VERSION, SNAPCTL_SUCCESS, SNAPCTL_ERROR
from snapctl.config.endpoints import END_POINTS
from snapctl.config.hashes import CLIENT_SDK_TYPES, SERVER_SDK_TYPES, PROTOS_TYPES, SERVICE_IDS
from snapctl.types.definitions import ResponseType
from snapctl.utils.echo import error, success, info

app = typer.Typer()

######### HELPER METHODS #########


def extract_api_key(profile: str | None = None) -> object:
    """
      Extracts the API Key from the environment variable and if not present from the config file
    """
    result = {
        'location': '',
        'value': None
    }
    # Option 1
    env_api_key = os.getenv(API_KEY)
    if env_api_key is not None:
        result['location'] = 'environment-variable'
        result['value'] = env_api_key
        return result
    # Option 2
    config_file_path: str = ''
    encoding: str | None = None
    if platform == 'win32':
        config_file_path = os.path.expandvars(CONFIG_FILE_WIN)
        encoding = "utf-8-sig"
    else:
        config_file_path = os.path.expanduser(CONFIG_FILE_MAC)
    if os.path.isfile(config_file_path):
        result['location'] = 'config-file'
        config = configparser.ConfigParser()
        config.read(config_file_path, encoding=encoding)
        config_profile: str = DEFAULT_PROFILE
        if profile is not None and profile != '' and profile != DEFAULT_PROFILE:
            result['location'] = f'config-file:profile:{profile}'
            config_profile = f'profile {profile}'
            info(f"Trying to extract API KEY from from profile {profile}")
        result['value'] = config.get(
            config_profile, API_KEY, fallback=None, raw=True
        )
    else:
        error(
            f'Config file on platform {platform} not found at {config_file_path}')
    return result


def get_base_url(api_key: str | None) -> str:
    """
        Returns the base url based on the api_key
    """
    if api_key is None:
        return ''
    if api_key.startswith('dev_'):
        return END_POINTS['DEV']
    if api_key.startswith('playtest_'):
        return END_POINTS['PLAYTEST']
    return END_POINTS['PROD']


def validate_command_context(
        ctx: typer.Context,
):
    """
      Validator to confirm if the context has been set properly
    """
    if ctx.obj['api_key'] is None or ctx.obj['base_url'] == '':
        error(
            "Unable to set command context. "
            f"API Key:{ctx.obj['api_key']}  "
            f"API Key Category:{ctx.obj['api_key_location']} "
            f"Base URL:{ctx.obj['base_url']}"
        )
        raise typer.Exit(SNAPCTL_ERROR)
    info(f"Using API Key from {ctx.obj['api_key_location']}")

######### CALLBACKS #########


def default_context_callback(ctx: typer.Context):
    """
      Common Callback to set the main app context
      This gets called on every command right at the start
    """
    # info("In default callback")
    # Ensure ctx object is instantiated
    ctx.ensure_object(dict)
    # Extract the api_key
    api_key_obj = extract_api_key()
    ctx.obj['version'] = VERSION
    ctx.obj['api_key'] = api_key_obj['value']
    ctx.obj['api_key_location'] = api_key_obj['location']
    ctx.obj['profile'] = DEFAULT_PROFILE
    ctx.obj['base_url'] = get_base_url(api_key_obj['value'])


def api_key_context_callback(
        ctx: typer.Context,
        api_key: str | None = None
):
    """
      Callback to set the context for the api_key
      This gets called only if the user has added a --api-key override
    """
    if api_key is None:
        return None
    # info("In API Key callback")
    # Ensure ctx object is instantiated
    ctx.ensure_object(dict)
    ctx.obj['version'] = VERSION
    ctx.obj['api_key'] = api_key
    ctx.obj['api_key_location'] = 'command-line-argument'
    ctx.obj['base_url'] = get_base_url(api_key)


def profile_context_callback(
        ctx: typer.Context,
        profile: str | None = None
):
    """
      Callback to set the context for the profile
      This gets called only if the user has added a --profile override
    """
    # Its important to early return if user has already entered API Key via command line
    if profile is None or ctx.obj['api_key_location'] == 'command-line-argument':
        return None
    # info("In Profile Callback")
    # Ensure ctx object is instantiated
    ctx.ensure_object(dict)
    api_key_obj = extract_api_key(profile)
    if api_key_obj['value'] is None and profile is not None and profile != '':
        conf_file = ''
        if platform == 'win32':
            conf_file = os.path.expandvars(CONFIG_FILE_WIN)
        else:
            conf_file = os.path.expanduser(CONFIG_FILE_MAC)
        error(
            f'Invalid profile input {profile}. '
            f'Please check your snap config file at {conf_file}'
        )
    ctx.obj['version'] = VERSION
    ctx.obj['api_key'] = api_key_obj['value']
    ctx.obj['api_key_location'] = api_key_obj['location']
    ctx.obj['profile'] = profile if profile else DEFAULT_PROFILE
    ctx.obj['base_url'] = get_base_url(api_key_obj['value'])


# Presently in typer this is the only way we can expose the `--version`
def version_callback(value: bool = True):
    """
        Prints the version and exits
    """
    if value:
        success(f"Snapctl version: {VERSION}")
        raise typer.Exit(SNAPCTL_SUCCESS)


@app.callback()
def common(
    ctx: typer.Context,
    version: bool = typer.Option(
        None, "--version",
        help="Get the Snapctl version.",
        callback=version_callback
    ),
):
    """
    Snapser CLI Tool
    """
    default_context_callback(ctx)

######### TYPER COMMANDS #########


@app.command()
def validate(
    ctx: typer.Context,
    api_key: Union[str, None] = typer.Option(
        None, "--api-key", help="API Key override.", callback=api_key_context_callback
    ),
    profile: Union[str, None] = typer.Option(
        None, "--profile", help="Profile to use.", callback=profile_context_callback
    ),
):
    """
    Validate your Snapctl setup
    """
    validate_command_context(ctx)
    success("Setup is valid")


@app.command()
def byosnap(
    ctx: typer.Context,
    # Required fields
    subcommand: str = typer.Argument(
        ..., help="BYOSnap Subcommands: " + ", ".join(ByoSnap.SUBCOMMANDS) + "."
    ),
    sid: str = typer.Argument(..., help="Snap Id. Should start with byosnap-"),
    # create
    name: str = typer.Option(
        None, "--name", help="(req: create) Name for your snap."
    ),
    desc: str = typer.Option(
        None, "--desc", help="(req: create) Description for your snap"
    ),
    platform_type: str = typer.Option(
        None, "--platform",
        help="(req: create) Platform for your snap - " + \
        ", ".join(ByoSnap.PLATFORMS) + "."
    ),
    language: str = typer.Option(
        None, "--language",
        help="(req: create) Language of your snap - " + \
        ", ".join(ByoSnap.LANGUAGES) + "."
    ),
    # publish-image and publish-version
    tag: str = typer.Option(
        None, "--tag", help="(req: build, push  publish-image and publish-version) Tag for your snap"
    ),
    # publish-image
    path: Union[str, None] = typer.Option(
        None, "--path", help="(req: build, publish-image) Path to your snap code"
    ),
    docker_file: str = typer.Option(
        "Dockerfile", help="Dockerfile name to use"
    ),
    # publish-version
    prefix: str = typer.Option(
        '/v1', "--prefix", help="(req: publish-version) URL Prefix for your snap"
    ),
    version: Union[str, None] = typer.Option(
        None, "--version",
        help="(req: publish-version) Snap version. Should start with v. Example vX.X.X"
    ),
    http_port: Union[str, None] = typer.Option(
        None, "--http-port", help="(req: publish-version) Ingress HTTP port version"
    ),
    # overrides
    api_key: Union[str, None] = typer.Option(
        None, "--api-key", help="API Key override.", callback=api_key_context_callback
    ),
    profile: Union[str, None] = typer.Option(
        None, "--profile", help="Profile to use.", callback=profile_context_callback
    ),
) -> None:
    """
      Bring your own snap commands
    """
    validate_command_context(ctx)
    byosnap_obj: ByoSnap = ByoSnap(
        subcommand, ctx.obj['base_url'], ctx.obj['api_key'], sid,
        name, desc, platform_type, language, tag, path, docker_file,
        prefix, version, http_port
    )
    validate_input_response: ResponseType = byosnap_obj.validate_input()
    if validate_input_response['error']:
        error(validate_input_response['msg'])
        raise typer.Exit(SNAPCTL_ERROR)
    command_method = subcommand.replace('-', '_')
    method: Callable[..., bool] = getattr(byosnap_obj, command_method)
    if not method():
        error(f"BYOSnap {subcommand} failed")
        raise typer.Exit(SNAPCTL_ERROR)
    success(f"BYOSnap {subcommand} complete")


@app.command()
def byogs(
    ctx: typer.Context,
    # Required fields
    subcommand: str = typer.Argument(
        ..., help="BYOGs Subcommands: " + ", ".join(ByoGs.SUBCOMMANDS) + "."
    ),
    sid: str = typer.Argument(
        ...,  help="Game Server Id. Should start with byogs-"
    ),
    # create
    name: str = typer.Option(
        None, "--name", help="(req: create) Name for your snap"
    ),
    desc: str = typer.Option(
        None, "--desc", help="(req: create) Description for your snap"
    ),
    platform_type: str = typer.Option(
        None, "--platform",
        help="(req: create) Platform for your snap - " + \
        ", ".join(ByoGs.PLATFORMS) + "."
    ),
    language: str = typer.Option(
        None, "--language",
        help="(req: create) Language of your snap - " + \
        ", ".join(ByoGs.LANGUAGES) + "."
    ),
    # publish-image and publish-version
    tag: str = typer.Option(
        None, "--tag",
        help="(req: build, push, publish-image and publish-version) Tag for your snap"
    ),
    # publish-image
    path: Union[str, None] = typer.Option(
        None, "--path", help="(req: build, publish-image, upload-docs) Path to your snap code"
    ),
    docker_file: str = typer.Option(
        "Dockerfile", help="Dockerfile name to use"
    ),
    # publish-version
    version: Union[str, None] = typer.Option(
        None, "--version", help="(req: publish-version) Snap version"
    ),
    http_port: Union[str, None] = typer.Option(
        None, "--http-port", help="(req: publish-version) Ingress HTTP port version"
    ),
    debug_port: Union[str, None] = typer.Option(
        None, "--debug-port", help="(optional: publish-version) Debug HTTP port version"
    ),
    # overrides
    api_key: Union[str, None] = typer.Option(
        None, "--api-key", help="API Key override.", callback=api_key_context_callback
    ),
    profile: Union[str, None] = typer.Option(
        None, "--profile", help="Profile to use.", callback=profile_context_callback
    ),
) -> None:
    """
      Bring your own game server commands
    """
    validate_command_context(ctx)
    byogs_obj: ByoGs = ByoGs(
        subcommand, ctx.obj['base_url'], ctx.obj['api_key'], sid,
        name, desc, platform_type, language, tag, path, docker_file,
        version, http_port, debug_port
    )
    validate_input_response: ResponseType = byogs_obj.validate_input()
    if validate_input_response['error']:
        error(validate_input_response['msg'])
        raise typer.Exit(SNAPCTL_ERROR)
    command_method = subcommand.replace('-', '_')
    method: Callable[..., bool] = getattr(byogs_obj, command_method)
    if not method():
        error(f"BYOGs {subcommand} failed")
        raise typer.Exit(SNAPCTL_ERROR)
    success(f"BYOGs {subcommand} complete")


@app.command()
def snapend(
    ctx: typer.Context,
    # Required fields
    subcommand: str = typer.Argument(
        ..., help="Snapend Subcommands: " + ", ".join(Snapend.SUBCOMMANDS) + "."
    ),
    snapend_id: str = typer.Argument(..., help="Snapend Id"),
    # download
    category: str = typer.Option(
        None, "--category",
        help=(
            "(req: download) Category of the Download: " +
            ", ".join(Snapend.DOWNLOAD_CATEGORY) + "."
        )
    ),
    path: Union[str, None] = typer.Option(
        None, "--path", help="(req: download) Path to save the SDK"),
    platform_type: str = typer.Option(
        None, "--type",
        help=(
            "(req: --category client-sdk|server-sdk|protos --type ) "
            "SDK Types: client-sdk(" + ", ".join(CLIENT_SDK_TYPES.keys()) +
            ") server-sdk(" + ", ".join(SERVER_SDK_TYPES.keys()) +
            ") protos(" + ", ".join(PROTOS_TYPES.keys()) + ")"
        )
    ),
    auth_type: str = typer.Option(
        'user', "--auth-type",
        help=(
            "(optional: download) Only applicable for --category server-sdk --auth-type"
            "Auth-Types: ()" + ", ".join(Snapend.AUTH_TYPES) + ")"
        )
    ),
    snaps: Union[str, None] = typer.Option(
        None, "--snaps",
        help=(
            "(optional: download) Comma separated list of snap ids to customize the "
              "SDKs, protos or admin settings. "
              "snaps(" + ", ".join(SERVICE_IDS)
        )
    ),
    # update
    byosnaps: str = typer.Option(
        None, "--byosnaps",
        help=(
            "(optional: update) Comma separated list of BYOSnap ids and versions. "
            "Eg: service-1:v1.0.0,service-2:v1.0.0"
        )
    ),
    byogs: str = typer.Option(
        None, "--byogs",
        help=(
            "(optional: update) Comma separated list of BYOGs fleet name, ids and versions. "
            "Eg: fleet-1:service-1:v1.0.0,fleet-2:service-2:v1.0.0"
        )
    ),
    blocking: bool = typer.Option(
        False, "--blocking",
        help=(
            "(optional: update) Set to true if you want to wait for the update to complete "
            "before returning."
        )
    ),
    # overrides
    api_key: Union[str, None] = typer.Option(
        None, "--api-key", help="API Key override.", callback=api_key_context_callback
    ),
    profile: Union[str, None] = typer.Option(
        None, "--profile", help="Profile to use.", callback=profile_context_callback
    ),
) -> None:
    """
      Snapend commands
    """
    validate_command_context(ctx)
    snapend_obj: Snapend = Snapend(
        subcommand, ctx.obj['base_url'], ctx.obj['api_key'],
        snapend_id, category, platform_type, auth_type,
        path, snaps, byosnaps, byogs, blocking
    )
    validate_input_response: ResponseType = snapend_obj.validate_input()
    if validate_input_response['error']:
        error(validate_input_response['msg'])
        raise typer.Exit(SNAPCTL_ERROR)
    command_method = subcommand.replace('-', '_')
    method: Callable[..., bool] = getattr(snapend_obj, command_method)
    if not method():
        error(f"Snapend {subcommand} failed")
        raise typer.Exit(SNAPCTL_ERROR)
    success(f"Snapend {subcommand} complete")
