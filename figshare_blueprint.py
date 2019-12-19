from flask_dance.consumer import OAuth2ConsumerBlueprint
from functools import partial
from flask.globals import LocalProxy, _lookup_app_object

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


__maintainer__ = "David Nicholson <nicholdav@gmail.com>"


def make_figshare_blueprint(
    client_id=None,
    client_secret=None,
    scope=None,
    redirect_url=None,
    redirect_to=None,
    login_url=None,
    authorized_url=None,
    rerequest_declined_permissions=False,
    session_class=None,
    storage=None,
):
    """
    Make a blueprint for authenticating with Facebook using OAuth 2. This requires
    a client ID and client secret from Facebook. You should either pass them to
    this constructor, or make sure that your Flask application config defines
    them, using the variables :envvar:`FIGSHARE_OAUTH_CLIENT_ID` and
    :envvar:`FIGSHARE_OAUTH_CLIENT_SECRET`.

    Args:
        client_id (str): The client ID for your application on Figshare.
        client_secret (str): The client secret for your application on Figshare
        scope (str, optional): comma-separated list of scopes for the OAuth token
        redirect_url (str): the URL to redirect to after the authentication
            dance is complete
        redirect_to (str): if ``redirect_url`` is not defined, the name of the
            view to redirect to after the authentication dance is complete.
            The actual URL will be determined by :func:`flask.url_for`
        login_url (str, optional): the URL path for the ``login`` view.
            Defaults to ``/figshare``
        authorized_url (str, optional): the URL path for the ``authorized`` view.
            Defaults to ``/figshare/authorized``.
        rerequest_declined_permissions (bool, optional): should the blueprint ask again for declined permissions.
            Defaults to ``False``
        session_class (class, optional): The class to use for creating a
            Requests session. Defaults to
            :class:`~flask_dance.consumer.requests.OAuth2Session`.
        storage: A token storage class, or an instance of a token storage
                class, to use for this blueprint. Defaults to
                :class:`~flask_dance.consumer.storage.session.SessionStorage`.

    :rtype: :class:`~flask_dance.consumer.OAuth2ConsumerBlueprint`
    :returns: A :ref:`blueprint <flask:blueprints>` to attach to your Flask app.
    """
    authorization_url_params = {}
    if rerequest_declined_permissions:
        authorization_url_params["auth_type"] = "rerequest"
    figshare_bp = OAuth2ConsumerBlueprint(
        "figshare",
        __name__,
        client_id=client_id,
        client_secret=client_secret,
        scope=scope,
        base_url="https://api.figshare.com/v2",
        authorization_url='https://figshare.com/account/applications/authorize',
        authorization_url_params=authorization_url_params,
        token_url='https://api.figshare.com/v2/token',
        redirect_url=redirect_url,
        redirect_to=redirect_to,
        login_url=login_url,
        authorized_url=authorized_url,
        session_class=session_class,
        storage=storage,
    )
    figshare_bp.from_config["client_id"] = "FIGSHARE_OAUTH_CLIENT_ID"
    figshare_bp.from_config["client_secret"] = "FIGSHARE_OAUTH_CLIENT_SECRET"

    @figshare_bp.before_app_request
    def set_applocal_session():
        ctx = stack.top
        ctx.figshare_oauth = figshare_bp.session

    return figshare_bp


figshare = LocalProxy(partial(_lookup_app_object, "figshare_oauth"))
