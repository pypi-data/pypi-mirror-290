# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = [
    'GetActionsRepositoryOidcSubjectClaimCustomizationTemplateResult',
    'AwaitableGetActionsRepositoryOidcSubjectClaimCustomizationTemplateResult',
    'get_actions_repository_oidc_subject_claim_customization_template',
    'get_actions_repository_oidc_subject_claim_customization_template_output',
]

@pulumi.output_type
class GetActionsRepositoryOidcSubjectClaimCustomizationTemplateResult:
    """
    A collection of values returned by getActionsRepositoryOidcSubjectClaimCustomizationTemplate.
    """
    def __init__(__self__, id=None, include_claim_keys=None, name=None, use_default=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if include_claim_keys and not isinstance(include_claim_keys, list):
            raise TypeError("Expected argument 'include_claim_keys' to be a list")
        pulumi.set(__self__, "include_claim_keys", include_claim_keys)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if use_default and not isinstance(use_default, bool):
            raise TypeError("Expected argument 'use_default' to be a bool")
        pulumi.set(__self__, "use_default", use_default)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="includeClaimKeys")
    def include_claim_keys(self) -> Sequence[str]:
        """
        The list of OpenID Connect claim keys.
        """
        return pulumi.get(self, "include_claim_keys")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="useDefault")
    def use_default(self) -> bool:
        """
        Whether the repository uses the default template.
        """
        return pulumi.get(self, "use_default")


class AwaitableGetActionsRepositoryOidcSubjectClaimCustomizationTemplateResult(GetActionsRepositoryOidcSubjectClaimCustomizationTemplateResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetActionsRepositoryOidcSubjectClaimCustomizationTemplateResult(
            id=self.id,
            include_claim_keys=self.include_claim_keys,
            name=self.name,
            use_default=self.use_default)


def get_actions_repository_oidc_subject_claim_customization_template(name: Optional[str] = None,
                                                                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetActionsRepositoryOidcSubjectClaimCustomizationTemplateResult:
    """
    Use this data source to retrieve the OpenID Connect subject claim customization template for a repository

    ## Example Usage

    ```python
    import pulumi
    import pulumi_github as github

    example = github.get_actions_repository_oidc_subject_claim_customization_template(name="example_repository")
    ```


    :param str name: Name of the repository to get the OpenID Connect subject claim customization template for.
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('github:index/getActionsRepositoryOidcSubjectClaimCustomizationTemplate:getActionsRepositoryOidcSubjectClaimCustomizationTemplate', __args__, opts=opts, typ=GetActionsRepositoryOidcSubjectClaimCustomizationTemplateResult).value

    return AwaitableGetActionsRepositoryOidcSubjectClaimCustomizationTemplateResult(
        id=pulumi.get(__ret__, 'id'),
        include_claim_keys=pulumi.get(__ret__, 'include_claim_keys'),
        name=pulumi.get(__ret__, 'name'),
        use_default=pulumi.get(__ret__, 'use_default'))


@_utilities.lift_output_func(get_actions_repository_oidc_subject_claim_customization_template)
def get_actions_repository_oidc_subject_claim_customization_template_output(name: Optional[pulumi.Input[str]] = None,
                                                                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetActionsRepositoryOidcSubjectClaimCustomizationTemplateResult]:
    """
    Use this data source to retrieve the OpenID Connect subject claim customization template for a repository

    ## Example Usage

    ```python
    import pulumi
    import pulumi_github as github

    example = github.get_actions_repository_oidc_subject_claim_customization_template(name="example_repository")
    ```


    :param str name: Name of the repository to get the OpenID Connect subject claim customization template for.
    """
    ...
