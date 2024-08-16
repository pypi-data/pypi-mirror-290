from asktable.models.client_base import convert_to_object, BaseResourceList
from asktable.api import APIRequest
from atcommon.models.project import ProjectCore, APIKeyCore


class APIKeyClient(APIKeyCore):
    api: APIRequest
    endpoint: str

    def delete(self):
        return self.api.send(
            endpoint=f"{self.endpoint}/{self.id}",
            method="DELETE",
        )


class APIKeyList(BaseResourceList):

    @convert_to_object(cls=APIKeyClient)
    def _get_all_resources(self):
        return self._get_all_resources_request()

    @convert_to_object(cls=APIKeyClient)
    def create(self, ak_role: str) -> APIKeyClient:
        return self.api.send(
            endpoint=self.endpoint,
            method="POST",
            data={"ak_role": ak_role},
        )


class ProjectClient(ProjectCore):
    api: APIRequest
    endpoint: str

    def delete(self):
        return self.api.send(
            endpoint=f"{self.endpoint}/{self.id}",
            method="DELETE",
        )

    def lock(self):
        return self.api.send(
            endpoint=f"{self.endpoint}/{self.id}",
            method="POST",
            data={"locked": 1},
        )

    def unlock(self):
        return self.api.send(
            endpoint=f"{self.endpoint}/{self.id}",
            method="POST",
            data={"locked": 0},
        )

    def rename(self, name: str):
        return self.api.send(
            endpoint=f"{self.endpoint}/{self.id}",
            method="POST",
            data={"name": name},
        )

    @property
    def api_keys(self):
        return APIKeyList(self.api, self.endpoint + f"/{self.id}/api-keys")


class ProjectList(BaseResourceList):

    @convert_to_object(cls=ProjectClient)
    def _get_all_resources(self):
        return self._get_all_resources_request()

    @convert_to_object(cls=ProjectClient)
    def create(self, name: str) -> ProjectClient:
        return self.api.send(
            endpoint=self.endpoint,
            method="POST",
            data={"name": name},
        )

    @convert_to_object(cls=ProjectClient)
    def get(self, id: str) -> ProjectClient:
        return self.api.send(
            endpoint=f"{self.endpoint}/{id}",
            method="GET",
        )



