"""
Type annotations for ivs service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_ivs.client import IVSClient

    session = Session()
    client: IVSClient = session.client("ivs")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import ChannelLatencyModeType, ChannelTypeType, TranscodePresetType
from .paginator import (
    ListChannelsPaginator,
    ListPlaybackKeyPairsPaginator,
    ListRecordingConfigurationsPaginator,
    ListStreamKeysPaginator,
    ListStreamsPaginator,
)
from .type_defs import (
    BatchGetChannelResponseTypeDef,
    BatchGetStreamKeyResponseTypeDef,
    BatchStartViewerSessionRevocationResponseTypeDef,
    BatchStartViewerSessionRevocationViewerSessionTypeDef,
    CreateChannelResponseTypeDef,
    CreatePlaybackRestrictionPolicyResponseTypeDef,
    CreateRecordingConfigurationResponseTypeDef,
    CreateStreamKeyResponseTypeDef,
    DestinationConfigurationTypeDef,
    EmptyResponseMetadataTypeDef,
    GetChannelResponseTypeDef,
    GetPlaybackKeyPairResponseTypeDef,
    GetPlaybackRestrictionPolicyResponseTypeDef,
    GetRecordingConfigurationResponseTypeDef,
    GetStreamKeyResponseTypeDef,
    GetStreamResponseTypeDef,
    GetStreamSessionResponseTypeDef,
    ImportPlaybackKeyPairResponseTypeDef,
    ListChannelsResponseTypeDef,
    ListPlaybackKeyPairsResponseTypeDef,
    ListPlaybackRestrictionPoliciesResponseTypeDef,
    ListRecordingConfigurationsResponseTypeDef,
    ListStreamKeysResponseTypeDef,
    ListStreamSessionsResponseTypeDef,
    ListStreamsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    RenditionConfigurationUnionTypeDef,
    StreamFiltersTypeDef,
    ThumbnailConfigurationUnionTypeDef,
    UpdateChannelResponseTypeDef,
    UpdatePlaybackRestrictionPolicyResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("IVSClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ChannelNotBroadcasting: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    PendingVerification: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    StreamUnavailable: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class IVSClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IVSClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#exceptions)
        """

    def batch_get_channel(self, *, arns: Sequence[str]) -> BatchGetChannelResponseTypeDef:
        """
        Performs  GetChannel on multiple ARNs simultaneously.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.batch_get_channel)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#batch_get_channel)
        """

    def batch_get_stream_key(self, *, arns: Sequence[str]) -> BatchGetStreamKeyResponseTypeDef:
        """
        Performs  GetStreamKey on multiple ARNs simultaneously.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.batch_get_stream_key)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#batch_get_stream_key)
        """

    def batch_start_viewer_session_revocation(
        self, *, viewerSessions: Sequence[BatchStartViewerSessionRevocationViewerSessionTypeDef]
    ) -> BatchStartViewerSessionRevocationResponseTypeDef:
        """
        Performs  StartViewerSessionRevocation on multiple channel ARN and viewer ID
        pairs
        simultaneously.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.batch_start_viewer_session_revocation)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#batch_start_viewer_session_revocation)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#can_paginate)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#close)
        """

    def create_channel(
        self,
        *,
        name: str = ...,
        latencyMode: ChannelLatencyModeType = ...,
        type: ChannelTypeType = ...,
        authorized: bool = ...,
        recordingConfigurationArn: str = ...,
        tags: Mapping[str, str] = ...,
        insecureIngest: bool = ...,
        preset: TranscodePresetType = ...,
        playbackRestrictionPolicyArn: str = ...,
    ) -> CreateChannelResponseTypeDef:
        """
        Creates a new channel and an associated stream key to start streaming.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.create_channel)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#create_channel)
        """

    def create_playback_restriction_policy(
        self,
        *,
        allowedCountries: Sequence[str] = ...,
        allowedOrigins: Sequence[str] = ...,
        enableStrictOriginEnforcement: bool = ...,
        name: str = ...,
        tags: Mapping[str, str] = ...,
    ) -> CreatePlaybackRestrictionPolicyResponseTypeDef:
        """
        Creates a new playback restriction policy, for constraining playback by
        countries and/or
        origins.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.create_playback_restriction_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#create_playback_restriction_policy)
        """

    def create_recording_configuration(
        self,
        *,
        destinationConfiguration: DestinationConfigurationTypeDef,
        name: str = ...,
        tags: Mapping[str, str] = ...,
        thumbnailConfiguration: ThumbnailConfigurationUnionTypeDef = ...,
        recordingReconnectWindowSeconds: int = ...,
        renditionConfiguration: RenditionConfigurationUnionTypeDef = ...,
    ) -> CreateRecordingConfigurationResponseTypeDef:
        """
        Creates a new recording configuration, used to enable recording to Amazon S3.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.create_recording_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#create_recording_configuration)
        """

    def create_stream_key(
        self, *, channelArn: str, tags: Mapping[str, str] = ...
    ) -> CreateStreamKeyResponseTypeDef:
        """
        Creates a stream key, used to initiate a stream, for the specified channel ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.create_stream_key)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#create_stream_key)
        """

    def delete_channel(self, *, arn: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified channel and its associated stream keys.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.delete_channel)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#delete_channel)
        """

    def delete_playback_key_pair(self, *, arn: str) -> Dict[str, Any]:
        """
        Deletes a specified authorization key pair.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.delete_playback_key_pair)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#delete_playback_key_pair)
        """

    def delete_playback_restriction_policy(self, *, arn: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified playback restriction policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.delete_playback_restriction_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#delete_playback_restriction_policy)
        """

    def delete_recording_configuration(self, *, arn: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the recording configuration for the specified ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.delete_recording_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#delete_recording_configuration)
        """

    def delete_stream_key(self, *, arn: str) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the stream key for the specified ARN, so it can no longer be used to
        stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.delete_stream_key)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#delete_stream_key)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#generate_presigned_url)
        """

    def get_channel(self, *, arn: str) -> GetChannelResponseTypeDef:
        """
        Gets the channel configuration for the specified channel ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.get_channel)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#get_channel)
        """

    def get_playback_key_pair(self, *, arn: str) -> GetPlaybackKeyPairResponseTypeDef:
        """
        Gets a specified playback authorization key pair and returns the `arn` and
        `fingerprint`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.get_playback_key_pair)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#get_playback_key_pair)
        """

    def get_playback_restriction_policy(
        self, *, arn: str
    ) -> GetPlaybackRestrictionPolicyResponseTypeDef:
        """
        Gets the specified playback restriction policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.get_playback_restriction_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#get_playback_restriction_policy)
        """

    def get_recording_configuration(self, *, arn: str) -> GetRecordingConfigurationResponseTypeDef:
        """
        Gets the recording configuration for the specified ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.get_recording_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#get_recording_configuration)
        """

    def get_stream(self, *, channelArn: str) -> GetStreamResponseTypeDef:
        """
        Gets information about the active (live) stream on a specified channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.get_stream)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#get_stream)
        """

    def get_stream_key(self, *, arn: str) -> GetStreamKeyResponseTypeDef:
        """
        Gets stream-key information for a specified ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.get_stream_key)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#get_stream_key)
        """

    def get_stream_session(
        self, *, channelArn: str, streamId: str = ...
    ) -> GetStreamSessionResponseTypeDef:
        """
        Gets metadata on a specified stream.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.get_stream_session)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#get_stream_session)
        """

    def import_playback_key_pair(
        self, *, publicKeyMaterial: str, name: str = ..., tags: Mapping[str, str] = ...
    ) -> ImportPlaybackKeyPairResponseTypeDef:
        """
        Imports the public portion of a new key pair and returns its `arn` and
        `fingerprint`.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.import_playback_key_pair)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#import_playback_key_pair)
        """

    def list_channels(
        self,
        *,
        filterByName: str = ...,
        filterByRecordingConfigurationArn: str = ...,
        filterByPlaybackRestrictionPolicyArn: str = ...,
        nextToken: str = ...,
        maxResults: int = ...,
    ) -> ListChannelsResponseTypeDef:
        """
        Gets summary information about all channels in your account, in the Amazon Web
        Services region where the API request is
        processed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.list_channels)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#list_channels)
        """

    def list_playback_key_pairs(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListPlaybackKeyPairsResponseTypeDef:
        """
        Gets summary information about playback key pairs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.list_playback_key_pairs)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#list_playback_key_pairs)
        """

    def list_playback_restriction_policies(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListPlaybackRestrictionPoliciesResponseTypeDef:
        """
        Gets summary information about playback restriction policies.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.list_playback_restriction_policies)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#list_playback_restriction_policies)
        """

    def list_recording_configurations(
        self, *, nextToken: str = ..., maxResults: int = ...
    ) -> ListRecordingConfigurationsResponseTypeDef:
        """
        Gets summary information about all recording configurations in your account, in
        the Amazon Web Services region where the API request is
        processed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.list_recording_configurations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#list_recording_configurations)
        """

    def list_stream_keys(
        self, *, channelArn: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListStreamKeysResponseTypeDef:
        """
        Gets summary information about stream keys for the specified channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.list_stream_keys)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#list_stream_keys)
        """

    def list_stream_sessions(
        self, *, channelArn: str, nextToken: str = ..., maxResults: int = ...
    ) -> ListStreamSessionsResponseTypeDef:
        """
        Gets a summary of current and previous streams for a specified channel in your
        account, in the AWS region where the API request is
        processed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.list_stream_sessions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#list_stream_sessions)
        """

    def list_streams(
        self, *, filterBy: StreamFiltersTypeDef = ..., nextToken: str = ..., maxResults: int = ...
    ) -> ListStreamsResponseTypeDef:
        """
        Gets summary information about live streams in your account, in the Amazon Web
        Services region where the API request is
        processed.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.list_streams)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#list_streams)
        """

    def list_tags_for_resource(self, *, resourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        Gets information about Amazon Web Services tags for the specified ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#list_tags_for_resource)
        """

    def put_metadata(self, *, channelArn: str, metadata: str) -> EmptyResponseMetadataTypeDef:
        """
        Inserts metadata into the active stream of the specified channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.put_metadata)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#put_metadata)
        """

    def start_viewer_session_revocation(
        self, *, channelArn: str, viewerId: str, viewerSessionVersionsLessThanOrEqualTo: int = ...
    ) -> Dict[str, Any]:
        """
        Starts the process of revoking the viewer session associated with a specified
        channel ARN and viewer
        ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.start_viewer_session_revocation)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#start_viewer_session_revocation)
        """

    def stop_stream(self, *, channelArn: str) -> Dict[str, Any]:
        """
        Disconnects the incoming RTMPS stream for the specified channel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.stop_stream)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#stop_stream)
        """

    def tag_resource(self, *, resourceArn: str, tags: Mapping[str, str]) -> Dict[str, Any]:
        """
        Adds or updates tags for the Amazon Web Services resource with the specified
        ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#tag_resource)
        """

    def untag_resource(self, *, resourceArn: str, tagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        Removes tags from the resource with the specified ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#untag_resource)
        """

    def update_channel(
        self,
        *,
        arn: str,
        name: str = ...,
        latencyMode: ChannelLatencyModeType = ...,
        type: ChannelTypeType = ...,
        authorized: bool = ...,
        recordingConfigurationArn: str = ...,
        insecureIngest: bool = ...,
        preset: TranscodePresetType = ...,
        playbackRestrictionPolicyArn: str = ...,
    ) -> UpdateChannelResponseTypeDef:
        """
        Updates a channel's configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.update_channel)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#update_channel)
        """

    def update_playback_restriction_policy(
        self,
        *,
        arn: str,
        allowedCountries: Sequence[str] = ...,
        allowedOrigins: Sequence[str] = ...,
        enableStrictOriginEnforcement: bool = ...,
        name: str = ...,
    ) -> UpdatePlaybackRestrictionPolicyResponseTypeDef:
        """
        Updates a specified playback restriction policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.update_playback_restriction_policy)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#update_playback_restriction_policy)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_channels"]) -> ListChannelsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_playback_key_pairs"]
    ) -> ListPlaybackKeyPairsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_recording_configurations"]
    ) -> ListRecordingConfigurationsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_stream_keys"]) -> ListStreamKeysPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_streams"]) -> ListStreamsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs.html#IVS.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_ivs/client/#get_paginator)
        """
