import sys
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterable,
    Iterator,
    List,
    Mapping,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from django import forms
from django.contrib.admin.filters import FieldListFilter, ListFilter
from django.contrib.admin.models import LogEntry
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.views.main import ChangeList
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.contenttypes.models import ContentType
from django.core.checks.messages import CheckMessage
from django.core.paginator import Paginator
from django.db.models.base import Model
from django.db.models.fields import Field
from django.db.models.fields.related import ForeignKey, ManyToManyField, RelatedField
from django.db.models.options import Options
from django.db.models.query import QuerySet
from django.forms.fields import Field as FormField
from django.forms.fields import TypedChoiceField
from django.forms.forms import BaseForm
from django.forms.formsets import BaseFormSet
from django.forms.models import BaseInlineFormSet, ModelChoiceField, ModelMultipleChoiceField
from django.forms.widgets import Media
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.response import _TemplateForResponseT
from django.urls.resolvers import URLPattern
from django.utils.datastructures import _ListOrTuple
from django.utils.safestring import SafeString

if sys.version_info < (3, 8):
    from typing_extensions import Literal, TypedDict
else:
    from typing import Literal, TypedDict

IS_POPUP_VAR: str
TO_FIELD_VAR: str
HORIZONTAL: Literal[1] = ...
VERTICAL: Literal[2] = ...

_Direction = Union[Literal[1], Literal[2]]

def get_content_type_for_model(obj: Union[Type[Model], Model]) -> ContentType: ...
def get_ul_class(radio_style: int) -> str: ...

class IncorrectLookupParameters(Exception): ...

FORMFIELD_FOR_DBFIELD_DEFAULTS: Any
csrf_protect_m: Any

_FieldGroups = Sequence[Union[str, Sequence[str]]]

class _OptionalFieldOpts(TypedDict, total=False):
    classes: Sequence[str]
    description: str

class _FieldOpts(_OptionalFieldOpts, total=True):
    fields: _FieldGroups

# Workaround for mypy issue, a Sequence type should be preferred here.
# https://github.com/python/mypy/issues/8921
# _FieldsetSpec = Sequence[Tuple[Optional[str], _FieldOpts]]
_FieldsetSpec = _ListOrTuple[Tuple[Optional[str], _FieldOpts]]
_ListFilterT = Union[
    Type[ListFilter],
    Field,
    str,
    Tuple[Union[Field, str], Type[FieldListFilter]],
    List[Union[Field, str, Type[FieldListFilter]]],
]

# Generic type specifically for models, for use in BaseModelAdmin and subclasses
# https://github.com/typeddjango/django-stubs/issues/482
_ModelT = TypeVar("_ModelT", bound=Model)

class BaseModelAdmin(Generic[_ModelT]):
    autocomplete_fields: Sequence[str] = ...
    raw_id_fields: Sequence[str] = ...
    fields: Optional[_FieldGroups] = ...
    exclude: Optional[Sequence[str]] = ...
    fieldsets: Optional[_FieldsetSpec] = ...
    form: Type[forms.ModelForm[_ModelT]] = ...
    filter_vertical: Sequence[str] = ...
    filter_horizontal: Sequence[str] = ...
    radio_fields: Mapping[str, _Direction] = ...
    prepopulated_fields: Dict[str, Sequence[str]] = ...
    formfield_overrides: Mapping[Type[Field], Mapping[str, Any]] = ...
    readonly_fields: Sequence[str] = ...
    ordering: Optional[Sequence[str]] = ...
    sortable_by: Optional[_ListOrTuple[str]] = ...
    view_on_site: Union[bool, Callable[[_ModelT], str]] = ...
    show_full_result_count: bool = ...
    checks_class: Any = ...
    model: Type[_ModelT]
    opts: Options[_ModelT]
    admin_site: AdminSite
    def __init__(self) -> None: ...
    def check(self, **kwargs: Any) -> List[CheckMessage]: ...
    def formfield_for_dbfield(self, db_field: Field, request: HttpRequest, **kwargs: Any) -> Optional[FormField]: ...
    def formfield_for_choice_field(self, db_field: Field, request: HttpRequest, **kwargs: Any) -> TypedChoiceField: ...
    def get_field_queryset(
        self, db: Optional[str], db_field: RelatedField, request: HttpRequest
    ) -> Optional[QuerySet]: ...
    def formfield_for_foreignkey(
        self, db_field: ForeignKey, request: HttpRequest, **kwargs: Any
    ) -> ModelChoiceField: ...
    def formfield_for_manytomany(
        self, db_field: ManyToManyField, request: HttpRequest, **kwargs: Any
    ) -> Optional[ModelMultipleChoiceField]: ...
    def get_autocomplete_fields(self, request: HttpRequest) -> Sequence[str]: ...
    def get_view_on_site_url(self, obj: Optional[_ModelT] = ...) -> Optional[str]: ...
    def get_empty_value_display(self) -> SafeString: ...
    def get_exclude(self, request: HttpRequest, obj: Optional[_ModelT] = ...) -> Optional[Sequence[str]]: ...
    def get_fields(self, request: HttpRequest, obj: Optional[_ModelT] = ...) -> _FieldGroups: ...
    def get_fieldsets(self, request: HttpRequest, obj: Optional[_ModelT] = ...) -> _FieldsetSpec: ...
    def get_inlines(self, request: HttpRequest, obj: Optional[_ModelT]) -> List[Type[InlineModelAdmin]]: ...
    def get_ordering(self, request: HttpRequest) -> Sequence[str]: ...
    def get_readonly_fields(self, request: HttpRequest, obj: Optional[_ModelT] = ...) -> Sequence[str]: ...
    def get_prepopulated_fields(
        self, request: HttpRequest, obj: Optional[_ModelT] = ...
    ) -> Dict[str, Sequence[str]]: ...
    def get_queryset(self, request: HttpRequest) -> QuerySet[_ModelT]: ...
    def get_sortable_by(self, request: HttpRequest) -> Sequence[str]: ...
    def lookup_allowed(self, lookup: str, value: str) -> bool: ...
    def to_field_allowed(self, request: HttpRequest, to_field: str) -> bool: ...
    def has_add_permission(self, request: HttpRequest) -> bool: ...
    def has_change_permission(self, request: HttpRequest, obj: Optional[_ModelT] = ...) -> bool: ...
    def has_delete_permission(self, request: HttpRequest, obj: Optional[_ModelT] = ...) -> bool: ...
    def has_view_permission(self, request: HttpRequest, obj: Optional[_ModelT] = ...) -> bool: ...
    def has_view_or_change_permission(self, request: HttpRequest, obj: Optional[_ModelT] = ...) -> bool: ...
    def has_module_permission(self, request: HttpRequest) -> bool: ...

_DisplayT = _ListOrTuple[Union[str, Callable[[_ModelT], str]]]

class ModelAdmin(BaseModelAdmin[_ModelT]):
    list_display: _DisplayT = ...
    list_display_links: _DisplayT = ...
    list_filter: _ListOrTuple[_ListFilterT] = ...
    list_select_related: Union[bool, Sequence[str]] = ...
    list_per_page: int = ...
    list_max_show_all: int = ...
    list_editable: Sequence[str] = ...
    search_fields: Sequence[str] = ...
    date_hierarchy: Optional[str] = ...
    save_as: bool = ...
    save_as_continue: bool = ...
    save_on_top: bool = ...
    paginator: Type = ...
    preserve_filters: bool = ...
    inlines: Sequence[Type[InlineModelAdmin]] = ...
    add_form_template: Optional[_TemplateForResponseT] = ...
    change_form_template: Optional[_TemplateForResponseT] = ...
    change_list_template: Optional[_TemplateForResponseT] = ...
    delete_confirmation_template: Optional[_TemplateForResponseT] = ...
    delete_selected_confirmation_template: Optional[_TemplateForResponseT] = ...
    object_history_template: Optional[_TemplateForResponseT] = ...
    popup_response_template: Optional[_TemplateForResponseT] = ...
    actions: Optional[Sequence[Union[Callable[[ModelAdmin, HttpRequest, QuerySet], None], str]]] = ...
    action_form: Any = ...
    actions_on_top: bool = ...
    actions_on_bottom: bool = ...
    actions_selection_counter: bool = ...
    model: Type[_ModelT] = ...
    opts: Options[_ModelT] = ...
    admin_site: AdminSite = ...
    def __init__(self, model: Type[_ModelT], admin_site: AdminSite) -> None: ...
    def get_inline_instances(self, request: HttpRequest, obj: Optional[_ModelT] = ...) -> List[InlineModelAdmin]: ...
    def get_urls(self) -> List[URLPattern]: ...
    @property
    def urls(self) -> List[URLPattern]: ...
    @property
    def media(self) -> Media: ...
    def get_model_perms(self, request: HttpRequest) -> Dict[str, bool]: ...
    def get_form(
        self, request: Any, obj: Optional[_ModelT] = ..., change: bool = ..., **kwargs: Any
    ) -> Type[forms.ModelForm[_ModelT]]: ...
    def get_changelist(self, request: HttpRequest, **kwargs: Any) -> Type[ChangeList]: ...
    def get_changelist_instance(self, request: HttpRequest) -> ChangeList: ...
    def get_object(
        self, request: HttpRequest, object_id: str, from_field: Optional[str] = ...
    ) -> Optional[_ModelT]: ...
    def get_changelist_form(self, request: Any, **kwargs: Any): ...
    def get_changelist_formset(self, request: Any, **kwargs: Any): ...
    def get_formsets_with_inlines(self, request: HttpRequest, obj: Optional[_ModelT] = ...) -> Iterator[Any]: ...
    def get_paginator(
        self,
        request: HttpRequest,
        queryset: QuerySet,
        per_page: int,
        orphans: int = ...,
        allow_empty_first_page: bool = ...,
    ) -> Paginator: ...
    def log_addition(self, request: HttpRequest, object: _ModelT, message: Any) -> LogEntry: ...
    def log_change(self, request: HttpRequest, object: _ModelT, message: Any) -> LogEntry: ...
    def log_deletion(self, request: HttpRequest, object: _ModelT, object_repr: str) -> LogEntry: ...
    def action_checkbox(self, obj: _ModelT) -> SafeString: ...
    def get_actions(self, request: HttpRequest) -> Dict[str, Optional[Tuple[Callable[..., str], str, str]]]: ...
    def get_action_choices(
        self, request: HttpRequest, default_choices: List[Tuple[str, str]] = ...
    ) -> List[Tuple[str, str]]: ...
    def get_action(self, action: Union[Callable, str]) -> Optional[Tuple[Callable[..., str], str, str]]: ...
    def get_list_display(self, request: HttpRequest) -> _DisplayT: ...
    def get_list_display_links(self, request: HttpRequest, list_display: _DisplayT) -> _DisplayT: ...
    def get_list_filter(self, request: HttpRequest) -> Sequence[_ListFilterT]: ...
    def get_list_select_related(self, request: HttpRequest) -> Union[bool, Sequence[str]]: ...
    def get_search_fields(self, request: HttpRequest) -> Sequence[str]: ...
    def get_search_results(
        self, request: HttpRequest, queryset: QuerySet, search_term: str
    ) -> Tuple[QuerySet[_ModelT], bool]: ...
    def get_preserved_filters(self, request: HttpRequest) -> str: ...
    def _get_edited_object_pks(self, request: HttpRequest, prefix: str) -> List[str]: ...
    def _get_list_editable_queryset(self, request: HttpRequest, prefix: str) -> QuerySet[_ModelT]: ...
    def construct_change_message(
        self, request: HttpRequest, form: AdminPasswordChangeForm, formsets: Iterable[BaseFormSet], add: bool = ...
    ) -> List[Dict[str, Dict[str, List[str]]]]: ...
    def message_user(
        self,
        request: HttpRequest,
        message: str,
        level: Union[int, str] = ...,
        extra_tags: str = ...,
        fail_silently: bool = ...,
    ) -> None: ...
    def save_form(self, request: Any, form: Any, change: Any): ...
    def save_model(self, request: Any, obj: _ModelT, form: Any, change: Any) -> None: ...
    def delete_model(self, request: HttpRequest, obj: _ModelT) -> None: ...
    def delete_queryset(self, request: HttpRequest, queryset: QuerySet) -> None: ...
    def save_formset(self, request: Any, form: Any, formset: Any, change: Any) -> None: ...
    def save_related(self, request: Any, form: Any, formsets: Any, change: Any) -> None: ...
    def render_change_form(
        self,
        request: Any,
        context: Any,
        add: bool = ...,
        change: bool = ...,
        form_url: str = ...,
        obj: Optional[_ModelT] = ...,
    ): ...
    def response_add(
        self, request: HttpRequest, obj: _ModelT, post_url_continue: Optional[str] = ...
    ) -> HttpResponse: ...
    def response_change(self, request: HttpRequest, obj: _ModelT) -> HttpResponse: ...
    def response_post_save_add(self, request: HttpRequest, obj: _ModelT) -> HttpResponseRedirect: ...
    def response_post_save_change(self, request: HttpRequest, obj: _ModelT) -> HttpResponseRedirect: ...
    # Probably FileResponse cannot come from ModelAdmin views
    def response_action(self, request: HttpRequest, queryset: QuerySet) -> Optional[HttpResponse]: ...
    def response_delete(self, request: HttpRequest, obj_display: str, obj_id: int) -> HttpResponse: ...
    def render_delete_form(self, request: Any, context: Any): ...
    def get_inline_formsets(
        self, request: HttpRequest, formsets: List[Any], inline_instances: List[Any], obj: Optional[_ModelT] = ...
    ) -> List[Any]: ...
    def get_changeform_initial_data(self, request: HttpRequest) -> Dict[str, Union[str, List[str]]]: ...
    def changeform_view(
        self,
        request: HttpRequest,
        object_id: Optional[str] = ...,
        form_url: str = ...,
        extra_context: Optional[Dict[str, Any]] = ...,
    ) -> HttpResponse: ...
    def add_view(
        self, request: HttpRequest, form_url: str = ..., extra_context: Optional[Dict[str, Any]] = ...
    ) -> HttpResponse: ...
    def change_view(
        self, request: HttpRequest, object_id: str, form_url: str = ..., extra_context: Optional[Dict[str, Any]] = ...
    ) -> HttpResponse: ...
    def changelist_view(self, request: HttpRequest, extra_context: Optional[Dict[str, Any]] = ...) -> HttpResponse: ...
    def get_deleted_objects(
        self, objs: Union[Sequence[_ModelT], QuerySet[_ModelT]], request: HttpRequest
    ) -> Tuple[List[Model], Dict[str, int], Set[str], List[str]]: ...
    def delete_view(
        self, request: HttpRequest, object_id: str, extra_context: Optional[Dict[str, Any]] = ...
    ) -> HttpResponse: ...
    def history_view(
        self, request: HttpRequest, object_id: str, extra_context: Optional[Dict[str, Any]] = ...
    ) -> HttpResponse: ...

_ChildModelT = TypeVar("_ChildModelT", bound=Model)
_ParentModelT = TypeVar("_ParentModelT", bound=Model)

class InlineModelAdmin(Generic[_ChildModelT, _ParentModelT], BaseModelAdmin[_ChildModelT]):
    model: Type[_ChildModelT] = ...
    fk_name: Optional[str] = ...
    formset: Type[BaseInlineFormSet[_ChildModelT, _ParentModelT, forms.ModelForm[_ChildModelT]]] = ...
    extra: int = ...
    min_num: Optional[int] = ...
    max_num: Optional[int] = ...
    template: str = ...
    verbose_name: Optional[str] = ...
    verbose_name_plural: Optional[str] = ...
    can_delete: bool = ...
    show_change_link: bool = ...
    classes: Optional[Sequence[str]] = ...
    admin_site: AdminSite = ...
    parent_model: Type[_ParentModelT] = ...
    opts: Options[_ChildModelT] = ...
    has_registered_model: bool = ...
    def __init__(self, parent_model: Type[_ParentModelT], admin_site: AdminSite) -> None: ...
    @property
    def media(self) -> Media: ...
    def get_extra(self, request: HttpRequest, obj: Optional[_ParentModelT] = ..., **kwargs: Any) -> int: ...
    def get_min_num(self, request: HttpRequest, obj: Optional[_ParentModelT] = ..., **kwargs: Any) -> Optional[int]: ...
    def get_max_num(self, request: HttpRequest, obj: Optional[_ParentModelT] = ..., **kwargs: Any) -> Optional[int]: ...
    def get_formset(
        self, request: HttpRequest, obj: Optional[_ParentModelT] = ..., **kwargs: Any
    ) -> Type[BaseInlineFormSet[_ChildModelT, _ParentModelT, forms.ModelForm[_ChildModelT]]]: ...
    def get_queryset(self, request: HttpRequest) -> QuerySet[_ChildModelT]: ...
    def has_add_permission(self, request: HttpRequest, obj: Optional[_ParentModelT]) -> bool: ...  # type: ignore
    def has_change_permission(self, request: HttpRequest, obj: Optional[_ParentModelT] = ...) -> bool: ...  # type: ignore
    def has_delete_permission(self, request: HttpRequest, obj: Optional[_ParentModelT] = ...) -> bool: ...  # type: ignore
    def has_view_permission(self, request: HttpRequest, obj: Optional[_ParentModelT] = ...) -> bool: ...  # type: ignore

class StackedInline(InlineModelAdmin[_ChildModelT, _ParentModelT]):
    template: str = ...

class TabularInline(InlineModelAdmin[_ChildModelT, _ParentModelT]):
    template: str = ...
