# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from . import outputs
from ._inputs import *

__all__ = ['OrganizationRulesetArgs', 'OrganizationRuleset']

@pulumi.input_type
class OrganizationRulesetArgs:
    def __init__(__self__, *,
                 enforcement: pulumi.Input[str],
                 rules: pulumi.Input['OrganizationRulesetRulesArgs'],
                 target: pulumi.Input[str],
                 bypass_actors: Optional[pulumi.Input[Sequence[pulumi.Input['OrganizationRulesetBypassActorArgs']]]] = None,
                 conditions: Optional[pulumi.Input['OrganizationRulesetConditionsArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a OrganizationRuleset resource.
        :param pulumi.Input[str] enforcement: (String) Possible values for Enforcement are `disabled`, `active`, `evaluate`. Note: `evaluate` is currently only supported for owners of type `organization`.
        :param pulumi.Input['OrganizationRulesetRulesArgs'] rules: (Block List, Min: 1, Max: 1) Rules within the ruleset. (see below for nested schema)
        :param pulumi.Input[str] target: (String) Possible values are `branch` and `tag`.
        :param pulumi.Input[Sequence[pulumi.Input['OrganizationRulesetBypassActorArgs']]] bypass_actors: (Block List) The actors that can bypass the rules in this ruleset. (see below for nested schema)
        :param pulumi.Input['OrganizationRulesetConditionsArgs'] conditions: (Block List, Max: 1) Parameters for an organization ruleset condition. `ref_name` is required alongside one of `repository_name` or `repository_id`. (see below for nested schema)
        :param pulumi.Input[str] name: (String) The name of the ruleset.
        """
        pulumi.set(__self__, "enforcement", enforcement)
        pulumi.set(__self__, "rules", rules)
        pulumi.set(__self__, "target", target)
        if bypass_actors is not None:
            pulumi.set(__self__, "bypass_actors", bypass_actors)
        if conditions is not None:
            pulumi.set(__self__, "conditions", conditions)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter
    def enforcement(self) -> pulumi.Input[str]:
        """
        (String) Possible values for Enforcement are `disabled`, `active`, `evaluate`. Note: `evaluate` is currently only supported for owners of type `organization`.
        """
        return pulumi.get(self, "enforcement")

    @enforcement.setter
    def enforcement(self, value: pulumi.Input[str]):
        pulumi.set(self, "enforcement", value)

    @property
    @pulumi.getter
    def rules(self) -> pulumi.Input['OrganizationRulesetRulesArgs']:
        """
        (Block List, Min: 1, Max: 1) Rules within the ruleset. (see below for nested schema)
        """
        return pulumi.get(self, "rules")

    @rules.setter
    def rules(self, value: pulumi.Input['OrganizationRulesetRulesArgs']):
        pulumi.set(self, "rules", value)

    @property
    @pulumi.getter
    def target(self) -> pulumi.Input[str]:
        """
        (String) Possible values are `branch` and `tag`.
        """
        return pulumi.get(self, "target")

    @target.setter
    def target(self, value: pulumi.Input[str]):
        pulumi.set(self, "target", value)

    @property
    @pulumi.getter(name="bypassActors")
    def bypass_actors(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['OrganizationRulesetBypassActorArgs']]]]:
        """
        (Block List) The actors that can bypass the rules in this ruleset. (see below for nested schema)
        """
        return pulumi.get(self, "bypass_actors")

    @bypass_actors.setter
    def bypass_actors(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['OrganizationRulesetBypassActorArgs']]]]):
        pulumi.set(self, "bypass_actors", value)

    @property
    @pulumi.getter
    def conditions(self) -> Optional[pulumi.Input['OrganizationRulesetConditionsArgs']]:
        """
        (Block List, Max: 1) Parameters for an organization ruleset condition. `ref_name` is required alongside one of `repository_name` or `repository_id`. (see below for nested schema)
        """
        return pulumi.get(self, "conditions")

    @conditions.setter
    def conditions(self, value: Optional[pulumi.Input['OrganizationRulesetConditionsArgs']]):
        pulumi.set(self, "conditions", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        (String) The name of the ruleset.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _OrganizationRulesetState:
    def __init__(__self__, *,
                 bypass_actors: Optional[pulumi.Input[Sequence[pulumi.Input['OrganizationRulesetBypassActorArgs']]]] = None,
                 conditions: Optional[pulumi.Input['OrganizationRulesetConditionsArgs']] = None,
                 enforcement: Optional[pulumi.Input[str]] = None,
                 etag: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 node_id: Optional[pulumi.Input[str]] = None,
                 rules: Optional[pulumi.Input['OrganizationRulesetRulesArgs']] = None,
                 ruleset_id: Optional[pulumi.Input[int]] = None,
                 target: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering OrganizationRuleset resources.
        :param pulumi.Input[Sequence[pulumi.Input['OrganizationRulesetBypassActorArgs']]] bypass_actors: (Block List) The actors that can bypass the rules in this ruleset. (see below for nested schema)
        :param pulumi.Input['OrganizationRulesetConditionsArgs'] conditions: (Block List, Max: 1) Parameters for an organization ruleset condition. `ref_name` is required alongside one of `repository_name` or `repository_id`. (see below for nested schema)
        :param pulumi.Input[str] enforcement: (String) Possible values for Enforcement are `disabled`, `active`, `evaluate`. Note: `evaluate` is currently only supported for owners of type `organization`.
        :param pulumi.Input[str] etag: (String)
        :param pulumi.Input[str] name: (String) The name of the ruleset.
        :param pulumi.Input[str] node_id: (String) GraphQL global node id for use with v4 API.
        :param pulumi.Input['OrganizationRulesetRulesArgs'] rules: (Block List, Min: 1, Max: 1) Rules within the ruleset. (see below for nested schema)
        :param pulumi.Input[int] ruleset_id: (Number) GitHub ID for the ruleset.
        :param pulumi.Input[str] target: (String) Possible values are `branch` and `tag`.
        """
        if bypass_actors is not None:
            pulumi.set(__self__, "bypass_actors", bypass_actors)
        if conditions is not None:
            pulumi.set(__self__, "conditions", conditions)
        if enforcement is not None:
            pulumi.set(__self__, "enforcement", enforcement)
        if etag is not None:
            pulumi.set(__self__, "etag", etag)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if node_id is not None:
            pulumi.set(__self__, "node_id", node_id)
        if rules is not None:
            pulumi.set(__self__, "rules", rules)
        if ruleset_id is not None:
            pulumi.set(__self__, "ruleset_id", ruleset_id)
        if target is not None:
            pulumi.set(__self__, "target", target)

    @property
    @pulumi.getter(name="bypassActors")
    def bypass_actors(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['OrganizationRulesetBypassActorArgs']]]]:
        """
        (Block List) The actors that can bypass the rules in this ruleset. (see below for nested schema)
        """
        return pulumi.get(self, "bypass_actors")

    @bypass_actors.setter
    def bypass_actors(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['OrganizationRulesetBypassActorArgs']]]]):
        pulumi.set(self, "bypass_actors", value)

    @property
    @pulumi.getter
    def conditions(self) -> Optional[pulumi.Input['OrganizationRulesetConditionsArgs']]:
        """
        (Block List, Max: 1) Parameters for an organization ruleset condition. `ref_name` is required alongside one of `repository_name` or `repository_id`. (see below for nested schema)
        """
        return pulumi.get(self, "conditions")

    @conditions.setter
    def conditions(self, value: Optional[pulumi.Input['OrganizationRulesetConditionsArgs']]):
        pulumi.set(self, "conditions", value)

    @property
    @pulumi.getter
    def enforcement(self) -> Optional[pulumi.Input[str]]:
        """
        (String) Possible values for Enforcement are `disabled`, `active`, `evaluate`. Note: `evaluate` is currently only supported for owners of type `organization`.
        """
        return pulumi.get(self, "enforcement")

    @enforcement.setter
    def enforcement(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "enforcement", value)

    @property
    @pulumi.getter
    def etag(self) -> Optional[pulumi.Input[str]]:
        """
        (String)
        """
        return pulumi.get(self, "etag")

    @etag.setter
    def etag(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "etag", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        (String) The name of the ruleset.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="nodeId")
    def node_id(self) -> Optional[pulumi.Input[str]]:
        """
        (String) GraphQL global node id for use with v4 API.
        """
        return pulumi.get(self, "node_id")

    @node_id.setter
    def node_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "node_id", value)

    @property
    @pulumi.getter
    def rules(self) -> Optional[pulumi.Input['OrganizationRulesetRulesArgs']]:
        """
        (Block List, Min: 1, Max: 1) Rules within the ruleset. (see below for nested schema)
        """
        return pulumi.get(self, "rules")

    @rules.setter
    def rules(self, value: Optional[pulumi.Input['OrganizationRulesetRulesArgs']]):
        pulumi.set(self, "rules", value)

    @property
    @pulumi.getter(name="rulesetId")
    def ruleset_id(self) -> Optional[pulumi.Input[int]]:
        """
        (Number) GitHub ID for the ruleset.
        """
        return pulumi.get(self, "ruleset_id")

    @ruleset_id.setter
    def ruleset_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "ruleset_id", value)

    @property
    @pulumi.getter
    def target(self) -> Optional[pulumi.Input[str]]:
        """
        (String) Possible values are `branch` and `tag`.
        """
        return pulumi.get(self, "target")

    @target.setter
    def target(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target", value)


class OrganizationRuleset(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bypass_actors: Optional[pulumi.Input[Sequence[pulumi.Input[Union['OrganizationRulesetBypassActorArgs', 'OrganizationRulesetBypassActorArgsDict']]]]] = None,
                 conditions: Optional[pulumi.Input[Union['OrganizationRulesetConditionsArgs', 'OrganizationRulesetConditionsArgsDict']]] = None,
                 enforcement: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 rules: Optional[pulumi.Input[Union['OrganizationRulesetRulesArgs', 'OrganizationRulesetRulesArgsDict']]] = None,
                 target: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Creates a GitHub organization ruleset.

        This resource allows you to create and manage rulesets on the organization level. When applied, a new ruleset will be created. When destroyed, that ruleset will be removed.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_github as github

        example = github.OrganizationRuleset("example",
            name="example",
            target="branch",
            enforcement="active",
            conditions={
                "ref_name": {
                    "includes": ["~ALL"],
                    "excludes": [],
                },
            },
            bypass_actors=[{
                "actor_id": 13473,
                "actor_type": "Integration",
                "bypass_mode": "always",
            }],
            rules={
                "creation": True,
                "update": True,
                "deletion": True,
                "required_linear_history": True,
                "required_signatures": True,
                "branch_name_pattern": {
                    "name": "example",
                    "negate": False,
                    "operator": "starts_with",
                    "pattern": "ex",
                },
            })
        ```

        ## Import

        GitHub Organization Rulesets can be imported using the GitHub ruleset ID e.g.

        ```sh
        $ pulumi import github:index/organizationRuleset:OrganizationRuleset example 12345`
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[Union['OrganizationRulesetBypassActorArgs', 'OrganizationRulesetBypassActorArgsDict']]]] bypass_actors: (Block List) The actors that can bypass the rules in this ruleset. (see below for nested schema)
        :param pulumi.Input[Union['OrganizationRulesetConditionsArgs', 'OrganizationRulesetConditionsArgsDict']] conditions: (Block List, Max: 1) Parameters for an organization ruleset condition. `ref_name` is required alongside one of `repository_name` or `repository_id`. (see below for nested schema)
        :param pulumi.Input[str] enforcement: (String) Possible values for Enforcement are `disabled`, `active`, `evaluate`. Note: `evaluate` is currently only supported for owners of type `organization`.
        :param pulumi.Input[str] name: (String) The name of the ruleset.
        :param pulumi.Input[Union['OrganizationRulesetRulesArgs', 'OrganizationRulesetRulesArgsDict']] rules: (Block List, Min: 1, Max: 1) Rules within the ruleset. (see below for nested schema)
        :param pulumi.Input[str] target: (String) Possible values are `branch` and `tag`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: OrganizationRulesetArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates a GitHub organization ruleset.

        This resource allows you to create and manage rulesets on the organization level. When applied, a new ruleset will be created. When destroyed, that ruleset will be removed.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_github as github

        example = github.OrganizationRuleset("example",
            name="example",
            target="branch",
            enforcement="active",
            conditions={
                "ref_name": {
                    "includes": ["~ALL"],
                    "excludes": [],
                },
            },
            bypass_actors=[{
                "actor_id": 13473,
                "actor_type": "Integration",
                "bypass_mode": "always",
            }],
            rules={
                "creation": True,
                "update": True,
                "deletion": True,
                "required_linear_history": True,
                "required_signatures": True,
                "branch_name_pattern": {
                    "name": "example",
                    "negate": False,
                    "operator": "starts_with",
                    "pattern": "ex",
                },
            })
        ```

        ## Import

        GitHub Organization Rulesets can be imported using the GitHub ruleset ID e.g.

        ```sh
        $ pulumi import github:index/organizationRuleset:OrganizationRuleset example 12345`
        ```

        :param str resource_name: The name of the resource.
        :param OrganizationRulesetArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(OrganizationRulesetArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bypass_actors: Optional[pulumi.Input[Sequence[pulumi.Input[Union['OrganizationRulesetBypassActorArgs', 'OrganizationRulesetBypassActorArgsDict']]]]] = None,
                 conditions: Optional[pulumi.Input[Union['OrganizationRulesetConditionsArgs', 'OrganizationRulesetConditionsArgsDict']]] = None,
                 enforcement: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 rules: Optional[pulumi.Input[Union['OrganizationRulesetRulesArgs', 'OrganizationRulesetRulesArgsDict']]] = None,
                 target: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = OrganizationRulesetArgs.__new__(OrganizationRulesetArgs)

            __props__.__dict__["bypass_actors"] = bypass_actors
            __props__.__dict__["conditions"] = conditions
            if enforcement is None and not opts.urn:
                raise TypeError("Missing required property 'enforcement'")
            __props__.__dict__["enforcement"] = enforcement
            __props__.__dict__["name"] = name
            if rules is None and not opts.urn:
                raise TypeError("Missing required property 'rules'")
            __props__.__dict__["rules"] = rules
            if target is None and not opts.urn:
                raise TypeError("Missing required property 'target'")
            __props__.__dict__["target"] = target
            __props__.__dict__["etag"] = None
            __props__.__dict__["node_id"] = None
            __props__.__dict__["ruleset_id"] = None
        super(OrganizationRuleset, __self__).__init__(
            'github:index/organizationRuleset:OrganizationRuleset',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            bypass_actors: Optional[pulumi.Input[Sequence[pulumi.Input[Union['OrganizationRulesetBypassActorArgs', 'OrganizationRulesetBypassActorArgsDict']]]]] = None,
            conditions: Optional[pulumi.Input[Union['OrganizationRulesetConditionsArgs', 'OrganizationRulesetConditionsArgsDict']]] = None,
            enforcement: Optional[pulumi.Input[str]] = None,
            etag: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            node_id: Optional[pulumi.Input[str]] = None,
            rules: Optional[pulumi.Input[Union['OrganizationRulesetRulesArgs', 'OrganizationRulesetRulesArgsDict']]] = None,
            ruleset_id: Optional[pulumi.Input[int]] = None,
            target: Optional[pulumi.Input[str]] = None) -> 'OrganizationRuleset':
        """
        Get an existing OrganizationRuleset resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[Union['OrganizationRulesetBypassActorArgs', 'OrganizationRulesetBypassActorArgsDict']]]] bypass_actors: (Block List) The actors that can bypass the rules in this ruleset. (see below for nested schema)
        :param pulumi.Input[Union['OrganizationRulesetConditionsArgs', 'OrganizationRulesetConditionsArgsDict']] conditions: (Block List, Max: 1) Parameters for an organization ruleset condition. `ref_name` is required alongside one of `repository_name` or `repository_id`. (see below for nested schema)
        :param pulumi.Input[str] enforcement: (String) Possible values for Enforcement are `disabled`, `active`, `evaluate`. Note: `evaluate` is currently only supported for owners of type `organization`.
        :param pulumi.Input[str] etag: (String)
        :param pulumi.Input[str] name: (String) The name of the ruleset.
        :param pulumi.Input[str] node_id: (String) GraphQL global node id for use with v4 API.
        :param pulumi.Input[Union['OrganizationRulesetRulesArgs', 'OrganizationRulesetRulesArgsDict']] rules: (Block List, Min: 1, Max: 1) Rules within the ruleset. (see below for nested schema)
        :param pulumi.Input[int] ruleset_id: (Number) GitHub ID for the ruleset.
        :param pulumi.Input[str] target: (String) Possible values are `branch` and `tag`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _OrganizationRulesetState.__new__(_OrganizationRulesetState)

        __props__.__dict__["bypass_actors"] = bypass_actors
        __props__.__dict__["conditions"] = conditions
        __props__.__dict__["enforcement"] = enforcement
        __props__.__dict__["etag"] = etag
        __props__.__dict__["name"] = name
        __props__.__dict__["node_id"] = node_id
        __props__.__dict__["rules"] = rules
        __props__.__dict__["ruleset_id"] = ruleset_id
        __props__.__dict__["target"] = target
        return OrganizationRuleset(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="bypassActors")
    def bypass_actors(self) -> pulumi.Output[Optional[Sequence['outputs.OrganizationRulesetBypassActor']]]:
        """
        (Block List) The actors that can bypass the rules in this ruleset. (see below for nested schema)
        """
        return pulumi.get(self, "bypass_actors")

    @property
    @pulumi.getter
    def conditions(self) -> pulumi.Output[Optional['outputs.OrganizationRulesetConditions']]:
        """
        (Block List, Max: 1) Parameters for an organization ruleset condition. `ref_name` is required alongside one of `repository_name` or `repository_id`. (see below for nested schema)
        """
        return pulumi.get(self, "conditions")

    @property
    @pulumi.getter
    def enforcement(self) -> pulumi.Output[str]:
        """
        (String) Possible values for Enforcement are `disabled`, `active`, `evaluate`. Note: `evaluate` is currently only supported for owners of type `organization`.
        """
        return pulumi.get(self, "enforcement")

    @property
    @pulumi.getter
    def etag(self) -> pulumi.Output[str]:
        """
        (String)
        """
        return pulumi.get(self, "etag")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        (String) The name of the ruleset.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="nodeId")
    def node_id(self) -> pulumi.Output[str]:
        """
        (String) GraphQL global node id for use with v4 API.
        """
        return pulumi.get(self, "node_id")

    @property
    @pulumi.getter
    def rules(self) -> pulumi.Output['outputs.OrganizationRulesetRules']:
        """
        (Block List, Min: 1, Max: 1) Rules within the ruleset. (see below for nested schema)
        """
        return pulumi.get(self, "rules")

    @property
    @pulumi.getter(name="rulesetId")
    def ruleset_id(self) -> pulumi.Output[int]:
        """
        (Number) GitHub ID for the ruleset.
        """
        return pulumi.get(self, "ruleset_id")

    @property
    @pulumi.getter
    def target(self) -> pulumi.Output[str]:
        """
        (String) Possible values are `branch` and `tag`.
        """
        return pulumi.get(self, "target")

