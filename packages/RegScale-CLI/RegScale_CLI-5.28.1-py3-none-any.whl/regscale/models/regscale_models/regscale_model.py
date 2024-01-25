#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Base Regscale Model """

import json
import logging
from typing import List, TypeVar, Optional, Union

from pydantic import BaseModel, Field, ConfigDict

from regscale.core.app.utils.api_handler import (
    APIHandler,
    APIInsertionError,
    APIUpdateError,
)

T = TypeVar("T", bound="RegScaleModel")

logger = logging.getLogger("rich")


class RegScaleModel(BaseModel):
    """Mixin class for RegScale Models to add functionality to interact with RegScale API"""

    _model_slug = "model_slug"
    _model_slug_id_url = "/api/{model_slug}/{id}"
    _model_id = 0
    _model_api_handler = APIHandler()

    extra_data: dict = Field(default={}, hidden=True)
    createdById: Optional[str] = None
    lastUpdatedById: Optional[str] = None

    def __init__(self, *args, **kwargs):
        try:
            super().__init__(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error creating {self.__class__.__name__}: {e} {args}")

    def dict(self, **kwargs) -> Optional[dict]:
        """
        Override the default dict method to exclude hidden fields

        :param kwargs: kwargs
        :return: dict
        """
        try:
            hidden_fields = set(
                attribute_name
                for attribute_name, model_field in self.__fields__.items()
                if model_field.field_info.extra.get("hidden") is True
            )
            kwargs.setdefault("exclude", hidden_fields)
        except AttributeError:
            pass
        return super().dict(**kwargs)

    @classmethod
    def get_module_id(cls) -> int:
        """
        Get the module ID for the model.

        :return: Module ID #
        :rtype: int
        """
        return cls._model_id

    @classmethod
    def get_module_slug(cls) -> str:
        """
        Get the module slug for the model.

        :return: Module slug
        :rtype: str
        """
        return cls._model_slug

    @classmethod
    def _get_endpoints(cls) -> ConfigDict:
        """
        Get the endpoints for the API.

        :return: A dictionary of endpoints
        :rtype: ConfigDict
        """
        endpoints = ConfigDict(
            get=cls._model_slug_id_url,
            insert="/api/{model_slug}/",
            update=cls._model_slug_id_url,
            delete=cls._model_slug_id_url,
            list="/api/{model_slug}/getList",
            get_by_parent="/api/{model_slug}/getAllByParent/{intParentID}/{strModule}",
        )
        endpoints.update(cls._get_additional_endpoints())
        return endpoints

    def __repr__(self) -> str:
        """
        Override the default repr method to return a string representation of the object.

        :return: String representation of the object
        :rtype: str
        """
        return f"<{self.__str__()}>"

    def __str__(self) -> str:
        """
        Override the default str method to return a string representation of the object.

        :return: String representation of the object
        :rtype: str
        """
        fields = (
            "\n  "
            + "\n  ".join(
                f"{name}={value!r},"
                for name, value in self.dict().items()
                # if value is not None
            )
            + "\n"
        )
        return f"{self.__class__.__name__}({fields})"

    def find_by_unique(self):
        """
        Find a functional role by unique fields.

        :raises NotImplementedError: If the method is not implemented
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} does not have a find_by_unique method"
        )

    def get_or_create(self) -> T:
        """
        Get or create an instance.

        :return: The instance
        :rtype: T
        """
        functional_role = self.find_by_unique()
        if functional_role:
            return functional_role
        else:
            return self.create()

    def create_or_update(self):
        """
        Create or update a functional role.

        :return: The functional role
        :rtype: FunctionalRole
        """
        functional_role = self.find_by_unique()
        if functional_role:
            # Update the functional role
            self.id = functional_role.id  # noqa
            return self.save()
        else:
            return self.create()

    @classmethod
    def get_by_parent(cls, parent_id: int, parent_module: str) -> List[T]:
        """
        Get a list of objects by parent.

        :param int parent_id: The ID of the parent
        :param str parent_module: The module of the parent
        :return: A list of objects
        :rtype: List[T]
        """
        response = cls._model_api_handler.get(
            endpoint=cls.get_endpoint("get_by_parent").format(
                intParentID=parent_id,
                strModule=parent_module,
            )
        )
        if not response or response.status_code in [204, 404]:
            return []
        if response.ok:
            json_response = response.json()
            if isinstance(json_response, dict):
                json_response = json_response.get("items", [])
            return [cls(**o) for o in json_response]
        else:
            logger.error(
                f"Failed to get {cls.__name__} for {parent_module}:  {parent_id}"
            )
            return []

    @classmethod
    def get_all_by_parent(cls, parent_id: int, parent_module: str) -> List[T]:
        """
        Get a list of objects by parent.

        :param int parent_id: The ID of the parent
        :param str parent_module: The module of the parent
        :return: A list of objects
        :rtype: List[T]
        """
        response = cls._model_api_handler.get(
            endpoint=cls.get_endpoint("get_all_by_parent").format(
                intId=parent_id,
                strModule=parent_module,
            )
        )
        if not response or response.status_code in [204, 404]:
            return []
        if response.ok:
            json_response = response.json()
            if isinstance(json_response, dict):
                json_response = json_response.get("items", [])
            return [cls(**o) for o in json_response]
        else:
            logger.error(
                f"Failed to get {cls.__name__} for {parent_module}:  {parent_id}"
            )
            return []

    @staticmethod
    def _get_additional_endpoints() -> ConfigDict:
        """
        Get additional endpoints for the API.

        :return: A dictionary of additional endpoints
        :rtype: ConfigDict
        """
        return ConfigDict()

    @classmethod
    def get_endpoint(cls, endpoint_type: str) -> str:
        """
        Get the endpoint for a specific type.

        :param str endpoint_type: The type of endpoint
        :raises ValueError: If the endpoint type is not found
        :return: The endpoint
        :rtype: str
        """
        endpoint = (
            cls._get_endpoints()
            .get(endpoint_type, "na")
            .replace("{model_slug}", cls._model_slug)
        )
        if endpoint == "na":
            logger.error(f"{cls.__name__} does not have endpoint {endpoint_type}")
            raise ValueError(f"Endpoint {endpoint_type} not found")
        return endpoint

    def create(self) -> T:
        """
        Insert a RegScale object.

        :raises APIInsertionError: If the insert fails
        :return: The created object
        :rtype: T
        """
        response = self._model_api_handler.post(
            endpoint=self.get_endpoint("insert"), data=self.dict()
        )
        if response and response.ok:
            return self.__class__(**response.json())
        else:
            logger.error(f"Failed to insert {self.__class__.__name__} {self.dict()}")
            if response is None:
                raise APIInsertionError(logger.error("Response was None"))
            raise APIInsertionError(
                logger.error(f"Response Code: {response.status_code} - {response.text}")
            )

    def save(self) -> T:
        """
        Save changes of the model instance.

        :raises APIUpdateError: If the update fails
        :return: The updated object
        :rtype: T
        """
        response = self._model_api_handler.put(
            endpoint=self.get_endpoint("update").format(id=self.id), data=self.dict()
        )
        if hasattr(response, "ok") and response.ok:
            return self.__class__(**response.json())
        else:
            logger.error(f"Failed to update {self.__class__.__name__} {self.dict()}")
            if response is not None:
                raise APIUpdateError(
                    f"Response Code: {response.status_code} - {response.text}"
                )
            else:
                raise APIUpdateError("Response was None")

    @classmethod
    def get_object(cls, object_id: Union[str, int]) -> Optional[T]:
        """
        Get a RegScale object by ID.

        :param Union[str, int] object_id: The ID of the object
        :return: The object or None if not found
        :rtype: Optional[T]
        """
        response = cls._model_api_handler.get(
            endpoint=cls.get_endpoint("get").format(id=object_id)
        )
        if response and response.ok:
            logger.debug(json.dumps(response.json(), indent=4))
            if response.json() and isinstance(response.json(), list):
                return cls(**response.json()[0])
            else:
                return cls(**response.json())
        else:
            logger.debug(
                f"Failing response: {response.status_code}: {response.reason} {response.text}"
            )
            logger.error(f"Failed to get record {cls.__name__} {object_id}")
            return None

    @classmethod
    def get_list(cls) -> List[T]:
        """
        Get a list of objects.

        :return: A list of objects
        :rtype: List[T]
        """
        response = cls._model_api_handler.get(endpoint=cls.get_endpoint("list"))
        if response.ok:
            return [cls.get_object(object_id=sp["id"]) for sp in response.json()]
        else:
            logger.error(f"Failed to get list of {cls.__name__} {response}")
            return []

    def delete(self) -> bool:
        """
        Delete an object in RegScale.

        :return: True if successful, False otherwise
        :rtype: bool
        """
        response = self._model_api_handler.delete(
            endpoint=self.get_endpoint("delete").format(id=self.id)
        )
        if response.ok:
            return True
        else:
            logger.error(f"Failed to delete {self.__class__.__name__} {self.dict()}")
            return False
