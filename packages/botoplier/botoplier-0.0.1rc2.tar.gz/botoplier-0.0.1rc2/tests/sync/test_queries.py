import pytest
from botoplier.sync.sessions import make_sessions
from botoplier.sync.smart_query import smart_query
from moto import mock_aws


@mock_aws
def test_basic_ec2():
    """No elements: empty response."""
    sessions = make_sessions({"testA": "1234567"}, ["eu-west-3"], {"testA": "myroles/test"})
    result = smart_query("ec2", "describe_instances", session=sessions["eu-west-3-testA"])
    assert result is not None
    assert len(result) == 0


@mock_aws
def test_basic_ecr():
    sessions = make_sessions({"testA": "1234567"}, ["eu-west-3"], {"testA": "myroles/test"})
    session = sessions["eu-west-3-testA"]
    ecr_client = session.client("ecr")
    ecr_client.create_repository(repositoryName="test_repo_1")
    ecr_client.create_repository(repositoryName="test_repo_2")
    result = smart_query("ecr", "describe_repositories", session=sessions["eu-west-3-testA"], subtree="repositories")
    repository_names = {e["repositoryName"] for e in result}
    assert len(result) == 2
    assert "test_repo_1" in repository_names
    assert "test_repo_2" in repository_names


@mock_aws
def test_basic_ecr_specific_subtree():
    sessions = make_sessions({"testA": "1234567"}, ["eu-west-3"], {"testA": "myroles/test"})
    session = sessions["eu-west-3-testA"]
    ecr_client = session.client("ecr")
    ecr_client.create_repository(repositoryName="test_repo_1")
    ecr_client.create_repository(repositoryName="test_repo_2")
    result = smart_query("ecr", "describe_repositories", session=sessions["eu-west-3-testA"], subtree="repositoryName")

    assert len(result) == 2
    assert "test_repo_1" in result
    assert "test_repo_2" in result


@mock_aws
def test_basic_ecr_specific_subtree_single_fail():
    sessions = make_sessions({"testA": "1234567"}, ["eu-west-3"], {"testA": "myroles/test"})
    session = sessions["eu-west-3-testA"]
    ecr_client = session.client("ecr")
    ecr_client.create_repository(repositoryName="test_repo_1")
    ecr_client.create_repository(repositoryName="test_repo_2")
    with pytest.raises(RuntimeError, match="The single option is set but result has 2 records."):
        smart_query("ecr", "describe_repositories", session=sessions["eu-west-3-testA"], subtree="repositoryName", single=True)


@mock_aws
def test_basic_ecr_no_subtree():
    sessions = make_sessions({"testA": "1234567"}, ["eu-west-3"], {"testA": "myroles/test"})
    session = sessions["eu-west-3-testA"]
    ecr_client = session.client("ecr")
    ecr_client.create_repository(repositoryName="test_repo_1")
    ecr_client.create_repository(repositoryName="test_repo_2")
    # with pytest.raises(RuntimeError, match="Cannot determine the way to unnest data" ):
    result = smart_query("ecr", "describe_repositories", session=sessions["eu-west-3-testA"])
    repository_names = {e["repositoryName"] for e in result}
    assert len(result) == 2
    assert "test_repo_1" in repository_names
    assert "test_repo_2" in repository_names


@mock_aws
def test_list_public_amis():
    """Many elements: we test pagination."""
    sessions = make_sessions({"testA": "1234567"}, ["eu-west-3"], {"testA": "myroles/test"})
    result = smart_query("ec2", "describe_images", session=sessions["eu-west-3-testA"], Filters=[{"Name": "is-public", "Values": ["true"]}], PageSize=10)
    assert len(result) > 10


@mock_aws
def test_describe_no_paginate():
    sessions = make_sessions({"testA": "1234567"}, ["eu-west-3"], {"testA": "myroles/test"})
    session = sessions["eu-west-3-testA"]
    ecr_client = session.client("ecr")
    ecr_client.create_repository(repositoryName="test_repo_1")
    # XXX Should infer it's single
    result = smart_query("ecr", "describe_registry", session=session, single=True)
    assert not isinstance(result, list)
    assert "registryId" in result
