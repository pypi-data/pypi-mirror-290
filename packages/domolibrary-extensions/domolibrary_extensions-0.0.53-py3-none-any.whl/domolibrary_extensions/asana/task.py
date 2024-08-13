# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/asana/02_task.ipynb.

# %% ../../nbs/asana/02_task.ipynb 2
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

import datetime as dt

from mdutils.mdutils import MdUtils

from nbdev.showdoc import patch_to

import domolibrary_extensions.utils.utils as deut
import domolibrary_extensions.utils.convert as decv
import domolibrary_extensions.client as gd
import domolibrary_extensions.asana.auth as deaa
import domolibrary_extensions.asana.user as au
import domolibrary_extensions.asana.project as ap

# %% auto 0
__all__ = ['AsanaSection', 'AsanaMembership', 'AsanaStory', 'AsanaCustomField', 'AsanaTask']

# %% ../../nbs/asana/02_task.ipynb 4
@dataclass
class AsanaSection:
    id: str
    name: str
    resource_type: str
    auth: deaa.AsanaAuth = field(repr=False)

    @classmethod
    def _from_json(cls, data: dict, auth=auth) -> "AsanaSection":
        return cls(
            id=data.get("gid"),
            name=data.get("name"),
            resource_type=data.get("resource_type"),
            auth=auth,
        )


@dataclass
class AsanaMembership:
    """relates a section to a project"""

    project: ap.AsanaProject
    section: AsanaSection
    auth: deaa.AsanaAuth = field(repr=False)

    @classmethod
    def _from_json(cls, data: dict, auth: deaa.AsanaAuth) -> "AsanaMembership":
        project = (
            ap.AsanaProject._from_json(data["project"], auth=auth)
            if data.get("project")
            else None
        )
        section = (
            AsanaSection._from_json(data["section"], auth=auth)
            if data.get("section")
            else None
        )
        return cls(project=project, section=section, auth=auth)

    def to_text(self):
        return f"{self.project.name} -> {self.section.name}"


@dataclass
class AsanaStory:
    id: str
    created_at: dt.datetime
    created_by: au.AsanaUser
    text: str
    type: str
    resource_subtype: str

    auth: deaa.AsanaAuth = field(repr=False)

    @classmethod
    def _from_json(cls, data: dict, auth: deaa.AsanaAuth) -> AsanaStory:
        created_by = (
            au.AsanaUser._from_json(data["created_by"], auth=auth)
            if data.get("created_by")
            else None
        )

        return cls(
            id=data.get("gid"),
            created_at=deut.convert_str_to_date(data.get("created_at")),
            created_by=created_by,
            text=data.get("text"),
            type=data.get("type"),
            resource_subtype=data.get("resource_subtype"),
            auth=auth,
        )

    def to_text(self):
        return f"{self.created_at.date()} - {self.created_by.name} - {self.text}"

    def to_json(self):

        res = {
            **self.__dict__,
            "created_at": decv.convert_datetime_to_str(self.created_at),
            "created_by": self.created_by.name,
        }
        del res["auth"]
        return res

# %% ../../nbs/asana/02_task.ipynb 6
@dataclass
class AsanaCustomField:
    id: str
    name: str
    description: str = None
    display_value: str = None
    type: str = None

    @classmethod
    def _from_json(cls, obj):
        return cls(
            id=obj["gid"],
            name=obj["name"],
            description=obj["description"],
            display_value=obj["display_value"],
            type=obj["type"],
        )


@dataclass
class AsanaTask:
    id: str
    name: str
    workspace_id: str

    auth: deaa.AsanaAuth = field(repr=False)
    assignee: au.AsanaUser = None

    assignee_status: str = None

    is_completed: bool = None

    created_at: dt.datetime = None
    completed_on: dt.datetime = None
    due_on: dt.datetime = None
    modified_at: dt.datetime = None

    memberships: List[dict] = None

    notes: str = None

    parent: Optional[dict] = None
    permalink_url: str = None
    projects: List[ap.AsanaProject] = None
    stories: List[AsanaStory] = None

    tags: List[dict] = None
    custom_fields: List[AsanaCustomField] = None

    @classmethod
    def _from_json(cls, obj: dict, auth: deaa.AsanaAuth) -> AsanaTask:
        assignee = (
            au.AsanaUser._from_json(obj.get("assignee"), auth=auth)
            if obj.get("assignee")
            else None
        )

        projects = [
            ap.AsanaProject._from_json(project, auth=auth)
            for project in obj.get("projects", [])
        ]

        memberships = [
            AsanaMembership._from_json(member_obj, auth=auth)
            for member_obj in obj.get("memberships", [])
        ]

        custom_fields = [
            AsanaCustomField._from_json(cfield)
            for cfield in obj.get("custom_fields", [])
            if cfield.get("display_value")
        ]

        return cls(
            id=obj.get("gid"),
            name=obj.get("name"),
            auth=auth,
            workspace_id=obj.get("workspace", {}).get("gid"),
            assignee=assignee,
            is_completed=obj.get("completed"),
            assignee_status=obj.get("assignee_status"),
            completed_on=deut.convert_str_to_date(obj.get("completed_at")),
            created_at=deut.convert_str_to_date(obj.get("created_at")),
            due_on=deut.convert_str_to_date(obj.get("due_on")),
            modified_at=deut.convert_str_to_date(obj.get("modified_at")),
            memberships=memberships,
            notes=obj.get("notes"),
            parent=obj.get("parent"),
            permalink_url=obj.get("permalink_url"),
            tags=obj.get("tags", []),
            projects=projects,
            custom_fields=custom_fields,
        )

# %% ../../nbs/asana/02_task.ipynb 8
@patch_to(AsanaTask, cls_method=True)
async def get_by_id(
    cls, auth, task_id, debug_api: bool = False, return_raw: bool = False
):
    url = f"{auth.base_url}/tasks/{task_id}"

    res = await gd.get_data(
        auth=auth,
        method="GET",
        url=url,
        debug_api=debug_api,
    )

    if not res.is_success:
        raise gd.BaseError(res=res)

    if return_raw:
        return res

    return cls._from_json(res.response["data"], auth=auth)

# %% ../../nbs/asana/02_task.ipynb 11
@patch_to(AsanaTask)
async def get_stories(
    self,
    debug_api: bool = False,
    return_raw: bool = False,
    is_only_comments: bool = False,  # stories include any changes to the task, comments are a subtype of stories
):
    auth = self.auth

    url = f"{auth.base_url}/tasks/{self.id}/stories"

    res = await gd.get_data(
        auth=self.auth,
        method="GET",
        url=url,
        debug_api=debug_api,
        # params = {"opt_fields" : "email"}
    )

    if not res.is_success:
        raise gd.BaseError(res=res)

    if return_raw:
        return res

    self.stories = [
        AsanaStory._from_json(story_obj, auth=auth)
        for story_obj in res.response["data"]
    ]

    if is_only_comments:
        self.stories = [
            story for story in self.stories if "comment" in story.resource_subtype
        ]

    return self.stories

# %% ../../nbs/asana/02_task.ipynb 14
def handle_render_user(mdFile, key, value):
    mdFile.new_line(f"{key} - {value.name}")


def handle_render_datetime(mdFile, key, value):
    mdFile.new_line(f"{key} - {value.date()}")


render_factory_values = {
    "AsanaUser": handle_render_user,
    "datetime": handle_render_datetime,
}


def handle_render_membership(mdFile, key, value):
    mdFile.new_header(level=1, title=key)
    [mdFile.new_line(asana_class.to_text()) for asana_class in value]


def handle_render_stories(mdFile, key, value):
    mdFile.new_header(level=1, title=key)
    [
        mdFile.new_line(asana_class.to_text())
        for asana_class in value
        if "comment" in asana_class.resource_subtype
    ]


def handle_render_default(mdFile, key, value):
    mdFile.new_line(f"{key} - {value}")


render_factory_keys = {
    "memberships": handle_render_membership,
    "stories": handle_render_stories,
    "default": handle_render_default,
}


def render_field(key: str, value: str, mdFile):
    if key in ["name", "projects"] or not value:
        return

    render_fn = (
        render_factory_values.get(value.__class__.__name__)
        or render_factory_keys.get(key)
        or render_factory_keys.get("default")
    )

    render_fn(mdFile=mdFile, key=key, value=value)


@patch_to(AsanaTask)
def to_md(self, output_folder="markdown", output_file=None):
    deut.upsert_folder(output_folder)

    mdFile = MdUtils(
        file_name=f"{output_folder}/{output_file or self.id}",
        title=output_file or self.name,
    )

    [
        render_field(key, getattr(self, key), mdFile)
        for key in self.__dict__.keys()
        if key not in ["auth", "workspace_id"]
    ]
    mdFile.create_md_file()

    return f"done exporting {mdFile.file_name}"
    # mdFile.new_table(columns=3, rows=6, text=list_of_strings, text_align='center')
