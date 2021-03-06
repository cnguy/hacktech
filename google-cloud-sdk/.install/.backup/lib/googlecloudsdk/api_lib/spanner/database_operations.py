# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Spanner database operations API helper."""

from apitools.base.py import list_pager
from googlecloudsdk.api_lib.util import apis
from googlecloudsdk.api_lib.util import waiter
from googlecloudsdk.core import resources


def Await(operation, message):
  """Wait for the specified operation."""
  client = apis.GetClientInstance('spanner', 'v1')
  poller = EmbeddedResponsePoller(
      client.projects_instances_databases_operations)
  ref = resources.REGISTRY.ParseRelativeName(
      operation.name,
      collection='spanner.projects.instances.databases.operations')
  return waiter.WaitFor(poller, ref, message)


def Cancel(instance, database, operation):
  """Cancel the specified operation."""
  client = apis.GetClientInstance('spanner', 'v1')
  msgs = apis.GetMessagesModule('spanner', 'v1')
  ref = resources.REGISTRY.Parse(
      operation,
      params={'instancesId': instance, 'databasesId': database},
      collection='spanner.projects.instances.databases.operations')
  req = msgs.SpannerProjectsInstancesDatabasesOperationsCancelRequest(
      name=ref.RelativeName())
  return client.projects_instances_databases_operations.Cancel(req)


def Get(instance, database, operation):
  """Get the specified operation."""
  client = apis.GetClientInstance('spanner', 'v1')
  msgs = apis.GetMessagesModule('spanner', 'v1')
  ref = resources.REGISTRY.Parse(
      operation,
      params={'instancesId': instance, 'databasesId': database},
      collection='spanner.projects.instances.databases.operations')
  req = msgs.SpannerProjectsInstancesDatabasesOperationsGetRequest(
      name=ref.RelativeName())
  return client.projects_instances_databases_operations.Get(req)


def List(instance, database):
  """List operations on the database."""
  client = apis.GetClientInstance('spanner', 'v1')
  msgs = apis.GetMessagesModule('spanner', 'v1')
  ref = resources.REGISTRY.Parse(
      database,
      params={'instancesId': instance},
      collection='spanner.projects.instances.databases')
  req = msgs.SpannerProjectsInstancesDatabasesOperationsListRequest(
      name=ref.RelativeName()+'/operations')
  return list_pager.YieldFromList(
      client.projects_instances_databases_operations,
      req,
      field='operations',
      batch_size_attribute='pageSize')


class EmbeddedResponsePoller(waiter.CloudOperationPoller):
  """As CloudOperationPoller for polling, but uses the Operation.response."""

  def __init__(self, operation_service):
    self.operation_service = operation_service

  def GetResult(self, operation):
    return operation.response
