from asktable import models
from asktable.api import APIRequest
from atcommon.version import VERSION
from asktable import exceptions as errors


class AskTable:
    __version__ = VERSION
    version = VERSION

    DataSource = models.DataSourceClient
    Policy = models.AuthPolicyClient
    Role = models.AuthRoleClient
    SecureTunnel = models.SecureTunnelClient

    errors = errors

    def __init__(
        self,
        api_url="https://api.asktable.com",
        api_key="key001",
        debug=False,
        user_id=None,
    ):
        self.api_url = api_url
        self.api_key = api_key
        self.debug = debug
        self.user_id = user_id

    @property
    def api(self):
        return APIRequest(
            api_url=self.api_url,
            api_key=self.api_key,
            debug=self.debug,
            user_id=self.user_id,
        )

    @property
    def projects(self):
        return models.ProjectList(self.api, endpoint="/sys/projects")

    @property
    def datasources(self):
        return models.DataSourceList(api=self.api, endpoint="/datasources")

    @property
    def chats(self):
        return models.ChatList(api=self.api, endpoint="/chats")

    @property
    def securetunnels(self):
        return models.SecureTunnelList(api=self.api, endpoint="/securetunnels")

    @property
    def roles(self):
        return models.AuthRoleList(self.api, endpoint="/auth/roles")

    @property
    def policies(self):
        return models.AuthPolicyList(self.api, endpoint="/auth/policies")

    @property
    def bots(self):
        return models.BotList(self.api, endpoint="/bots")

    @property
    def extapis(self):
        return models.ExtAPIList(self.api, endpoint="/extapis")

    @property
    def api_key_id(self):
        data = self.api.send(endpoint="/at-auth/me", method="GET")
        return data

    @property
    def q2s(self):
        return models.Q2SList(self.api, endpoint="/single-turn/q2s")

    @property
    def q2a(self):
        return models.Q2AList(self.api, endpoint="/single-turn/q2a")

