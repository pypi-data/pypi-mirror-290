from fastapi import Depends, HTTPException, Request, status
from pydantic import BaseModel

from .api import BaseApi, ModelRestApi, SQLAInterface
from .api.interface import PARAM_BODY_QUERY
from .db import QueryManager, UserDatabase, get_user_db
from .decorators import expose, login_required
from .globals import g
from .models import Api, Permission, PermissionApi, Role, User
from .routers import get_auth_router, get_oauth_router
from .schemas import (
    GeneralResponse,
    UserCreate,
    UserRead,
    UserReadWithStringRoles,
    UserUpdate,
)
from .utils import SelfDepends, SelfType, smart_run

__all__ = [
    "AuthApi",
    "InfoApi",
    "PermissionsApi",
    "PermissionViewApi",
    "RolesApi",
    "UsersApi",
    "ViewsMenusApi",
]


class PermissionViewApi(ModelRestApi):
    resource_name = "permissionview"
    datamodel = SQLAInterface(PermissionApi)
    max_page_size = 200
    base_permissions = ["can_get", "can_info"]


class ViewsMenusApi(ModelRestApi):
    resource_name = "viewsmenus"
    datamodel = SQLAInterface(Api)
    max_page_size = 200
    base_permissions = ["can_get", "can_info"]


class PermissionsApi(ModelRestApi):
    resource_name = "permissions"
    datamodel = SQLAInterface(Permission)
    max_page_size = 200
    base_permissions = ["can_get", "can_info"]


class RolesApi(ModelRestApi):
    resource_name = "roles"
    datamodel = SQLAInterface(Role)
    max_page_size = 200


class InfoApi(BaseApi):
    resource_name = "info"

    security_level_apis = [
        "PermissionsApi",
        "RolesApi",
        "UsersApi",
        "ViewsMenusApi",
        "PermissionViewApi",
    ]
    excluded_apis = ["InfoApi", "AuthApi"]

    def __init__(self):
        expose("/")(self.get_info)
        login_required(self.get_info)
        super().__init__()

    def get_info(self):
        if not self.toolkit:
            return []

        apis = self.cache.get("get_info", [])
        if apis:
            return apis

        for api in self.toolkit.apis:
            if api.__class__.__name__ in self.excluded_apis:
                continue

            api_info = {}
            api_info["name"] = api.resource_name.capitalize()
            api_info["icon"] = "Table" if hasattr(api, "datamodel") else ""
            api_info["permission_name"] = api.__class__.__name__
            api_info["path"] = api.resource_name
            api_info["type"] = "table" if hasattr(api, "datamodel") else "default"
            api_info["level"] = (
                "security"
                if api.__class__.__name__ in self.security_level_apis
                else "default"
            )
            apis.append(api_info)

        self.cache["get_info"] = apis
        return apis


class UsersApi(ModelRestApi):
    resource_name = "users"
    datamodel = SQLAInterface(User)
    list_exclude_columns = ["password", "hashed_password"]
    show_exclude_columns = ["password", "hashed_password"]
    add_exclude_columns = [
        "active",
        "last_login",
        "login_count",
        "fail_login_count",
        "created_on",
        "changed_on",
        "oauth_accounts",
    ]
    edit_exclude_columns = [
        "username",
        "last_login",
        "login_count",
        "fail_login_count",
        "created_on",
        "changed_on",
        "oauth_accounts",
    ]
    label_columns = {"password": "Password"}

    async def post_headless(
        self,
        body: BaseModel = SelfType().add_schema,
        query: QueryManager = SelfDepends().get_query_manager,
    ):
        """
        Creates a new item in a headless mode.

        Args:
            body (BaseModel): The request body.
            query (QueryManager): The query manager object.

        Returns:
            add_return_schema: The add return schema.

        ### Note:
            If you are overriding this method, make sure to copy all the decorators too.
        """
        body_json = await smart_run(
            self._process_body, query.db, body, self.add_query_rel_fields
        )
        item: User = self.datamodel.obj(**body_json)
        await smart_run(self.pre_add, item, PARAM_BODY_QUERY(body=body, query=query))
        item = await g.current_app.security.create_user(
            username=item.username,
            email=item.email,
            password=item.password,
            first_name=item.first_name,
            last_name=item.last_name,
            roles=[role.name for role in item.roles],
            session=query.db,
        )
        await smart_run(
            query.add_options,
            join_columns=self.show_join_columns,
            where_id=getattr(item, self.datamodel.get_pk_attr()),
        )
        item = await smart_run(query.execute, many=False)
        await smart_run(self.post_add, item, PARAM_BODY_QUERY(body=body, query=query))
        pk, data = self._convert_to_result(item)
        body = self.add_return_schema(id=pk, result=data)
        return body

    async def put_headless(
        self,
        id: str | int = SelfType().datamodel.id_schema,
        body: BaseModel = SelfType().edit_schema,
        query: QueryManager = SelfDepends().get_query_manager,
    ):
        """
        Updates an item in a headless mode.

        Args:
            id (str | int): The id of the item.
            body (BaseModel): The request body.
            query (QueryManager): The query manager object.

        Returns:
            add_return_schema: The add return schema.

        ### Note:
            If you are overriding this method, make sure to copy all the decorators too.
        """
        await smart_run(
            query.add_options, join_columns=self.show_join_columns, where_id=id
        )
        item: User | None = await smart_run(query.execute, many=False)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        body_json = await smart_run(
            self._process_body, query.db, body, self.edit_query_rel_fields
        )
        item.update(body_json)
        await smart_run(self.pre_update, item, PARAM_BODY_QUERY(body=body, query=query))
        user_update = UserUpdate()
        for key in body_json:
            item_val = getattr(item, key)
            setattr(user_update, key, item_val)
        item = await g.current_app.security.update_user(
            item, user_update, session=query.db
        )
        await smart_run(
            self.post_update, item, PARAM_BODY_QUERY(body=body, query=query)
        )
        pk, data = self._convert_to_result(item)
        body = self.edit_return_schema(id=pk, result=data)
        return body


class AuthApi(BaseApi):
    resource_name = "auth"

    def __init__(self):
        super().__init__()
        if g.config.get("AUTH_LOGIN_COOKIE", True):
            self.router.include_router(
                get_auth_router(
                    g.auth.cookie_backend,
                    g.auth.fastapi_users.get_user_manager,
                    g.auth.fastapi_users.authenticator,
                )
            )
        if g.config.get("AUTH_LOGIN_JWT"):
            self.router.include_router(
                get_auth_router(
                    g.auth.jwt_backend,
                    g.auth.fastapi_users.get_user_manager,
                    g.auth.fastapi_users.authenticator,
                ),
                prefix="/jwt",
            )
        if g.config.get("AUTH_USER_REGISTRATION"):
            self.router.include_router(
                g.auth.fastapi_users.get_register_router(UserRead, UserCreate),
            )
        if g.config.get("AUTH_USER_RESET_PASSWORD"):
            self.router.include_router(
                g.auth.fastapi_users.get_reset_password_router(),
            )
        if g.config.get("AUTH_USER_VERIFY"):
            self.router.include_router(
                g.auth.fastapi_users.get_verify_router(UserRead),
            )

        oauth_clients = g.config.get("OAUTH_CLIENTS") or g.config.get(
            "OAUTH_PROVIDERS", []
        )
        for client in oauth_clients:
            oauth_client = client["oauth_client"]
            associate_by_email = client.get("associate_by_email", False)
            on_after_register = client.get("on_after_register", None)

            self.router.include_router(
                get_oauth_router(
                    oauth_client=oauth_client,
                    backend=g.auth.cookie_backend,
                    get_user_manager=g.auth.fastapi_users.get_user_manager,
                    state_secret=g.auth.secret_key,
                    redirect_url=g.config.get("oauth_redirect_url"),
                    associate_by_email=associate_by_email,
                    on_after_register=on_after_register,
                ),
            )

    @expose(
        "/user",
        methods=["GET"],
        response_model=UserReadWithStringRoles,
        responses={
            status.HTTP_401_UNAUTHORIZED: {
                "description": "Missing token or inactive user.",
            }
        },
    )
    def get_user():
        if not g.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing token or inactive user.",
            )
        user_data = UserRead.model_validate(g.user)
        user_data.roles = [role.name for role in g.user.roles]
        return user_data

    @expose(
        "/user",
        methods=["PUT"],
        responses={
            status.HTTP_401_UNAUTHORIZED: {
                "description": "Missing token or inactive user.",
            }
        },
    )
    async def update_user(
        request: Request,
        user_update: UserUpdate,
        user_db: UserDatabase = Depends(get_user_db),
    ):
        if not g.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing token or inactive user.",
            )
        user_manager = next(g.auth.get_user_manager(user_db))
        await user_manager.update(user_update, g.user, safe=True, request=request)
        return GeneralResponse(detail="User updated successfully.")
