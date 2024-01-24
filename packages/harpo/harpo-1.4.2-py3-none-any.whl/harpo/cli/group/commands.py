import os

import click

from harpo.cli.user.commands import complete_user_name
from harpo.cli.util import complete_from_list, print_formatted, print_normal, with_harpo_context
from harpo.main import Harpo
from harpo.util import find_harpo_basedir


def complete_group_name(ctx, args, incomplete):
    """Complete group name

    NOTE: Context is not yet initialized
    and we have no access to default options values from here

    So just return empty list if we weren't successful
    in determining harpo base_dir
    """
    base_dir = ctx.parent.parent.params.get("base_dir") or find_harpo_basedir()
    if base_dir is not None and os.path.isdir(base_dir):
        harpo = Harpo(base_dir, gpg_home=None)
        return complete_from_list(incomplete, harpo.groups.list())
    else:
        return []


@click.group()
def group():
    """Manage groups"""
    pass


@group.command()
@click.argument("group_name")
@with_harpo_context
def create(harpo, common_parameters, group_name):
    harpo.group_create(group_name)


@group.command()
@click.argument("group_name", shell_complete=complete_group_name)
@with_harpo_context
def destroy(harpo, common_parameters, group_name):
    harpo.group_destroy(group_name)


@group.command()
@click.option("--members/--no-members", default=False)
@with_harpo_context
def list(harpo, common_parameters, members):
    groups = harpo.group_list(members=members)
    if members:
        print_formatted(groups, output_format=common_parameters["format"])
    else:
        print_normal(groups, tablefmt="plain")


@group.command(deprecated=True)
@click.argument("group_name", shell_complete=complete_group_name)
@click.argument("user_name", shell_complete=complete_user_name)
@with_harpo_context
def include_user(harpo, common_parameters, group_name, user_name):
    """Add user to group"""
    harpo.group_include_user(group_name, user_name)


@group.command(deprecated=True)
@click.argument("group_name", shell_complete=complete_group_name)
@click.argument("user_name", shell_complete=complete_user_name)
@with_harpo_context
def exclude_user(harpo, common_parameters, group_name, user_name):
    """Remove user from group"""
    harpo.group_exclude_user(group_name, user_name)


@group.group()
def members():
    """Manage group members"""
    pass


@members.command()
@click.argument("group_name", shell_complete=complete_group_name)
@click.argument("user_name", shell_complete=complete_user_name)
@with_harpo_context
def add(harpo, common_parameters, group_name, user_name):
    """Add user to group"""
    harpo.group_include_user(group_name, user_name)


@members.command()
@click.argument("group_name", shell_complete=complete_group_name)
@click.argument("user_name", shell_complete=complete_user_name)
@with_harpo_context
def remove(harpo, common_parameters, group_name, user_name):
    """Remove user from group"""
    harpo.group_exclude_user(group_name, user_name)


@members.command(name="list")
@click.argument("group_name", shell_complete=complete_group_name)
@with_harpo_context
def list_members(harpo, common_parameters, group_name):
    """List users in group"""
    print_normal(harpo.group_list_members(group_name), tablefmt="plain")
