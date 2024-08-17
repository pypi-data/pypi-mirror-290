"""
Type annotations for fsx service client.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/)

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_fsx.client import FSxClient

    session = Session()
    client: FSxClient = session.client("fsx")
    ```
"""

import sys
from typing import Any, Dict, Mapping, Sequence, Type, overload

from botocore.client import BaseClient, ClientMeta

from .literals import (
    DataRepositoryTaskTypeType,
    FileSystemTypeType,
    OpenZFSCopyStrategyType,
    RestoreOpenZFSVolumeOptionType,
    StorageTypeType,
    StorageVirtualMachineRootVolumeSecurityStyleType,
    UpdateOpenZFSVolumeOptionType,
    VolumeTypeType,
)
from .paginator import (
    DescribeBackupsPaginator,
    DescribeFileSystemsPaginator,
    DescribeStorageVirtualMachinesPaginator,
    DescribeVolumesPaginator,
    ListTagsForResourcePaginator,
)
from .type_defs import (
    AssociateFileSystemAliasesResponseTypeDef,
    CancelDataRepositoryTaskResponseTypeDef,
    CompletionReportTypeDef,
    CopyBackupResponseTypeDef,
    CopySnapshotAndUpdateVolumeResponseTypeDef,
    CreateBackupResponseTypeDef,
    CreateDataRepositoryAssociationResponseTypeDef,
    CreateDataRepositoryTaskResponseTypeDef,
    CreateFileCacheLustreConfigurationTypeDef,
    CreateFileCacheResponseTypeDef,
    CreateFileSystemFromBackupResponseTypeDef,
    CreateFileSystemLustreConfigurationTypeDef,
    CreateFileSystemOntapConfigurationTypeDef,
    CreateFileSystemOpenZFSConfigurationTypeDef,
    CreateFileSystemResponseTypeDef,
    CreateFileSystemWindowsConfigurationTypeDef,
    CreateOntapVolumeConfigurationTypeDef,
    CreateOpenZFSVolumeConfigurationTypeDef,
    CreateSnapshotResponseTypeDef,
    CreateStorageVirtualMachineResponseTypeDef,
    CreateSvmActiveDirectoryConfigurationTypeDef,
    CreateVolumeFromBackupResponseTypeDef,
    CreateVolumeResponseTypeDef,
    DataRepositoryTaskFilterTypeDef,
    DeleteBackupResponseTypeDef,
    DeleteDataRepositoryAssociationResponseTypeDef,
    DeleteFileCacheResponseTypeDef,
    DeleteFileSystemLustreConfigurationTypeDef,
    DeleteFileSystemOpenZFSConfigurationTypeDef,
    DeleteFileSystemResponseTypeDef,
    DeleteFileSystemWindowsConfigurationTypeDef,
    DeleteSnapshotResponseTypeDef,
    DeleteStorageVirtualMachineResponseTypeDef,
    DeleteVolumeOntapConfigurationTypeDef,
    DeleteVolumeOpenZFSConfigurationTypeDef,
    DeleteVolumeResponseTypeDef,
    DescribeBackupsResponseTypeDef,
    DescribeDataRepositoryAssociationsResponseTypeDef,
    DescribeDataRepositoryTasksResponseTypeDef,
    DescribeFileCachesResponseTypeDef,
    DescribeFileSystemAliasesResponseTypeDef,
    DescribeFileSystemsResponseTypeDef,
    DescribeSharedVpcConfigurationResponseTypeDef,
    DescribeSnapshotsResponseTypeDef,
    DescribeStorageVirtualMachinesResponseTypeDef,
    DescribeVolumesResponseTypeDef,
    DisassociateFileSystemAliasesResponseTypeDef,
    FileCacheDataRepositoryAssociationTypeDef,
    FilterTypeDef,
    ListTagsForResourceResponseTypeDef,
    ReleaseConfigurationTypeDef,
    ReleaseFileSystemNfsV3LocksResponseTypeDef,
    RestoreVolumeFromSnapshotResponseTypeDef,
    S3DataRepositoryConfigurationUnionTypeDef,
    SnapshotFilterTypeDef,
    StartMisconfiguredStateRecoveryResponseTypeDef,
    StorageVirtualMachineFilterTypeDef,
    TagTypeDef,
    UpdateDataRepositoryAssociationResponseTypeDef,
    UpdateFileCacheLustreConfigurationTypeDef,
    UpdateFileCacheResponseTypeDef,
    UpdateFileSystemLustreConfigurationTypeDef,
    UpdateFileSystemOntapConfigurationTypeDef,
    UpdateFileSystemOpenZFSConfigurationTypeDef,
    UpdateFileSystemResponseTypeDef,
    UpdateFileSystemWindowsConfigurationTypeDef,
    UpdateOntapVolumeConfigurationTypeDef,
    UpdateOpenZFSVolumeConfigurationTypeDef,
    UpdateSharedVpcConfigurationResponseTypeDef,
    UpdateSnapshotResponseTypeDef,
    UpdateStorageVirtualMachineResponseTypeDef,
    UpdateSvmActiveDirectoryConfigurationTypeDef,
    UpdateVolumeResponseTypeDef,
    VolumeFilterTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = ("FSxClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ActiveDirectoryError: Type[BotocoreClientError]
    BackupBeingCopied: Type[BotocoreClientError]
    BackupInProgress: Type[BotocoreClientError]
    BackupNotFound: Type[BotocoreClientError]
    BackupRestoring: Type[BotocoreClientError]
    BadRequest: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DataRepositoryAssociationNotFound: Type[BotocoreClientError]
    DataRepositoryTaskEnded: Type[BotocoreClientError]
    DataRepositoryTaskExecuting: Type[BotocoreClientError]
    DataRepositoryTaskNotFound: Type[BotocoreClientError]
    FileCacheNotFound: Type[BotocoreClientError]
    FileSystemNotFound: Type[BotocoreClientError]
    IncompatibleParameterError: Type[BotocoreClientError]
    IncompatibleRegionForMultiAZ: Type[BotocoreClientError]
    InternalServerError: Type[BotocoreClientError]
    InvalidDataRepositoryType: Type[BotocoreClientError]
    InvalidDestinationKmsKey: Type[BotocoreClientError]
    InvalidExportPath: Type[BotocoreClientError]
    InvalidImportPath: Type[BotocoreClientError]
    InvalidNetworkSettings: Type[BotocoreClientError]
    InvalidPerUnitStorageThroughput: Type[BotocoreClientError]
    InvalidRegion: Type[BotocoreClientError]
    InvalidSourceKmsKey: Type[BotocoreClientError]
    MissingFileCacheConfiguration: Type[BotocoreClientError]
    MissingFileSystemConfiguration: Type[BotocoreClientError]
    MissingVolumeConfiguration: Type[BotocoreClientError]
    NotServiceResourceError: Type[BotocoreClientError]
    ResourceDoesNotSupportTagging: Type[BotocoreClientError]
    ResourceNotFound: Type[BotocoreClientError]
    ServiceLimitExceeded: Type[BotocoreClientError]
    SnapshotNotFound: Type[BotocoreClientError]
    SourceBackupUnavailable: Type[BotocoreClientError]
    StorageVirtualMachineNotFound: Type[BotocoreClientError]
    UnsupportedOperation: Type[BotocoreClientError]
    VolumeNotFound: Type[BotocoreClientError]

class FSxClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        FSxClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.exceptions)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#exceptions)
        """

    def associate_file_system_aliases(
        self, *, FileSystemId: str, Aliases: Sequence[str], ClientRequestToken: str = ...
    ) -> AssociateFileSystemAliasesResponseTypeDef:
        """
        Use this action to associate one or more Domain Name Server (DNS) aliases with
        an existing Amazon FSx for Windows File Server file
        system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.associate_file_system_aliases)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#associate_file_system_aliases)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.can_paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#can_paginate)
        """

    def cancel_data_repository_task(
        self, *, TaskId: str
    ) -> CancelDataRepositoryTaskResponseTypeDef:
        """
        Cancels an existing Amazon FSx for Lustre data repository task if that task is
        in either the `PENDING` or `EXECUTING`
        state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.cancel_data_repository_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#cancel_data_repository_task)
        """

    def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.close)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#close)
        """

    def copy_backup(
        self,
        *,
        SourceBackupId: str,
        ClientRequestToken: str = ...,
        SourceRegion: str = ...,
        KmsKeyId: str = ...,
        CopyTags: bool = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CopyBackupResponseTypeDef:
        """
        Copies an existing backup within the same Amazon Web Services account to
        another Amazon Web Services Region (cross-Region copy) or within the same
        Amazon Web Services Region (in-Region
        copy).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.copy_backup)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#copy_backup)
        """

    def copy_snapshot_and_update_volume(
        self,
        *,
        VolumeId: str,
        SourceSnapshotARN: str,
        ClientRequestToken: str = ...,
        CopyStrategy: OpenZFSCopyStrategyType = ...,
        Options: Sequence[UpdateOpenZFSVolumeOptionType] = ...,
    ) -> CopySnapshotAndUpdateVolumeResponseTypeDef:
        """
        Updates an existing volume by using a snapshot from another Amazon FSx for
        OpenZFS file
        system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.copy_snapshot_and_update_volume)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#copy_snapshot_and_update_volume)
        """

    def create_backup(
        self,
        *,
        FileSystemId: str = ...,
        ClientRequestToken: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
        VolumeId: str = ...,
    ) -> CreateBackupResponseTypeDef:
        """
        Creates a backup of an existing Amazon FSx for Windows File Server file system,
        Amazon FSx for Lustre file system, Amazon FSx for NetApp ONTAP volume, or
        Amazon FSx for OpenZFS file
        system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.create_backup)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#create_backup)
        """

    def create_data_repository_association(
        self,
        *,
        FileSystemId: str,
        DataRepositoryPath: str,
        FileSystemPath: str = ...,
        BatchImportMetaDataOnCreate: bool = ...,
        ImportedFileChunkSize: int = ...,
        S3: S3DataRepositoryConfigurationUnionTypeDef = ...,
        ClientRequestToken: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateDataRepositoryAssociationResponseTypeDef:
        """
        Creates an Amazon FSx for Lustre data repository association (DRA).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.create_data_repository_association)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#create_data_repository_association)
        """

    def create_data_repository_task(
        self,
        *,
        Type: DataRepositoryTaskTypeType,
        FileSystemId: str,
        Report: CompletionReportTypeDef,
        Paths: Sequence[str] = ...,
        ClientRequestToken: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
        CapacityToRelease: int = ...,
        ReleaseConfiguration: ReleaseConfigurationTypeDef = ...,
    ) -> CreateDataRepositoryTaskResponseTypeDef:
        """
        Creates an Amazon FSx for Lustre data repository task.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.create_data_repository_task)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#create_data_repository_task)
        """

    def create_file_cache(
        self,
        *,
        FileCacheType: Literal["LUSTRE"],
        FileCacheTypeVersion: str,
        StorageCapacity: int,
        SubnetIds: Sequence[str],
        ClientRequestToken: str = ...,
        SecurityGroupIds: Sequence[str] = ...,
        Tags: Sequence[TagTypeDef] = ...,
        CopyTagsToDataRepositoryAssociations: bool = ...,
        KmsKeyId: str = ...,
        LustreConfiguration: CreateFileCacheLustreConfigurationTypeDef = ...,
        DataRepositoryAssociations: Sequence[FileCacheDataRepositoryAssociationTypeDef] = ...,
    ) -> CreateFileCacheResponseTypeDef:
        """
        Creates a new Amazon File Cache resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.create_file_cache)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#create_file_cache)
        """

    def create_file_system(
        self,
        *,
        FileSystemType: FileSystemTypeType,
        StorageCapacity: int,
        SubnetIds: Sequence[str],
        ClientRequestToken: str = ...,
        StorageType: StorageTypeType = ...,
        SecurityGroupIds: Sequence[str] = ...,
        Tags: Sequence[TagTypeDef] = ...,
        KmsKeyId: str = ...,
        WindowsConfiguration: CreateFileSystemWindowsConfigurationTypeDef = ...,
        LustreConfiguration: CreateFileSystemLustreConfigurationTypeDef = ...,
        OntapConfiguration: CreateFileSystemOntapConfigurationTypeDef = ...,
        FileSystemTypeVersion: str = ...,
        OpenZFSConfiguration: CreateFileSystemOpenZFSConfigurationTypeDef = ...,
    ) -> CreateFileSystemResponseTypeDef:
        """
        Creates a new, empty Amazon FSx file system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.create_file_system)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#create_file_system)
        """

    def create_file_system_from_backup(
        self,
        *,
        BackupId: str,
        SubnetIds: Sequence[str],
        ClientRequestToken: str = ...,
        SecurityGroupIds: Sequence[str] = ...,
        Tags: Sequence[TagTypeDef] = ...,
        WindowsConfiguration: CreateFileSystemWindowsConfigurationTypeDef = ...,
        LustreConfiguration: CreateFileSystemLustreConfigurationTypeDef = ...,
        StorageType: StorageTypeType = ...,
        KmsKeyId: str = ...,
        FileSystemTypeVersion: str = ...,
        OpenZFSConfiguration: CreateFileSystemOpenZFSConfigurationTypeDef = ...,
        StorageCapacity: int = ...,
    ) -> CreateFileSystemFromBackupResponseTypeDef:
        """
        Creates a new Amazon FSx for Lustre, Amazon FSx for Windows File Server, or
        Amazon FSx for OpenZFS file system from an existing Amazon FSx
        backup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.create_file_system_from_backup)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#create_file_system_from_backup)
        """

    def create_snapshot(
        self,
        *,
        Name: str,
        VolumeId: str,
        ClientRequestToken: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateSnapshotResponseTypeDef:
        """
        Creates a snapshot of an existing Amazon FSx for OpenZFS volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.create_snapshot)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#create_snapshot)
        """

    def create_storage_virtual_machine(
        self,
        *,
        FileSystemId: str,
        Name: str,
        ActiveDirectoryConfiguration: CreateSvmActiveDirectoryConfigurationTypeDef = ...,
        ClientRequestToken: str = ...,
        SvmAdminPassword: str = ...,
        Tags: Sequence[TagTypeDef] = ...,
        RootVolumeSecurityStyle: StorageVirtualMachineRootVolumeSecurityStyleType = ...,
    ) -> CreateStorageVirtualMachineResponseTypeDef:
        """
        Creates a storage virtual machine (SVM) for an Amazon FSx for ONTAP file system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.create_storage_virtual_machine)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#create_storage_virtual_machine)
        """

    def create_volume(
        self,
        *,
        VolumeType: VolumeTypeType,
        Name: str,
        ClientRequestToken: str = ...,
        OntapConfiguration: CreateOntapVolumeConfigurationTypeDef = ...,
        Tags: Sequence[TagTypeDef] = ...,
        OpenZFSConfiguration: CreateOpenZFSVolumeConfigurationTypeDef = ...,
    ) -> CreateVolumeResponseTypeDef:
        """
        Creates an FSx for ONTAP or Amazon FSx for OpenZFS storage volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.create_volume)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#create_volume)
        """

    def create_volume_from_backup(
        self,
        *,
        BackupId: str,
        Name: str,
        ClientRequestToken: str = ...,
        OntapConfiguration: CreateOntapVolumeConfigurationTypeDef = ...,
        Tags: Sequence[TagTypeDef] = ...,
    ) -> CreateVolumeFromBackupResponseTypeDef:
        """
        Creates a new Amazon FSx for NetApp ONTAP volume from an existing Amazon FSx
        volume
        backup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.create_volume_from_backup)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#create_volume_from_backup)
        """

    def delete_backup(
        self, *, BackupId: str, ClientRequestToken: str = ...
    ) -> DeleteBackupResponseTypeDef:
        """
        Deletes an Amazon FSx backup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.delete_backup)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#delete_backup)
        """

    def delete_data_repository_association(
        self,
        *,
        AssociationId: str,
        ClientRequestToken: str = ...,
        DeleteDataInFileSystem: bool = ...,
    ) -> DeleteDataRepositoryAssociationResponseTypeDef:
        """
        Deletes a data repository association on an Amazon FSx for Lustre file system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.delete_data_repository_association)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#delete_data_repository_association)
        """

    def delete_file_cache(
        self, *, FileCacheId: str, ClientRequestToken: str = ...
    ) -> DeleteFileCacheResponseTypeDef:
        """
        Deletes an Amazon File Cache resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.delete_file_cache)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#delete_file_cache)
        """

    def delete_file_system(
        self,
        *,
        FileSystemId: str,
        ClientRequestToken: str = ...,
        WindowsConfiguration: DeleteFileSystemWindowsConfigurationTypeDef = ...,
        LustreConfiguration: DeleteFileSystemLustreConfigurationTypeDef = ...,
        OpenZFSConfiguration: DeleteFileSystemOpenZFSConfigurationTypeDef = ...,
    ) -> DeleteFileSystemResponseTypeDef:
        """
        Deletes a file system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.delete_file_system)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#delete_file_system)
        """

    def delete_snapshot(
        self, *, SnapshotId: str, ClientRequestToken: str = ...
    ) -> DeleteSnapshotResponseTypeDef:
        """
        Deletes an Amazon FSx for OpenZFS snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.delete_snapshot)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#delete_snapshot)
        """

    def delete_storage_virtual_machine(
        self, *, StorageVirtualMachineId: str, ClientRequestToken: str = ...
    ) -> DeleteStorageVirtualMachineResponseTypeDef:
        """
        Deletes an existing Amazon FSx for ONTAP storage virtual machine (SVM).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.delete_storage_virtual_machine)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#delete_storage_virtual_machine)
        """

    def delete_volume(
        self,
        *,
        VolumeId: str,
        ClientRequestToken: str = ...,
        OntapConfiguration: DeleteVolumeOntapConfigurationTypeDef = ...,
        OpenZFSConfiguration: DeleteVolumeOpenZFSConfigurationTypeDef = ...,
    ) -> DeleteVolumeResponseTypeDef:
        """
        Deletes an Amazon FSx for NetApp ONTAP or Amazon FSx for OpenZFS volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.delete_volume)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#delete_volume)
        """

    def describe_backups(
        self,
        *,
        BackupIds: Sequence[str] = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> DescribeBackupsResponseTypeDef:
        """
        Returns the description of a specific Amazon FSx backup, if a `BackupIds` value
        is provided for that
        backup.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.describe_backups)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#describe_backups)
        """

    def describe_data_repository_associations(
        self,
        *,
        AssociationIds: Sequence[str] = ...,
        Filters: Sequence[FilterTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> DescribeDataRepositoryAssociationsResponseTypeDef:
        """
        Returns the description of specific Amazon FSx for Lustre or Amazon File Cache
        data repository associations, if one or more `AssociationIds` values are
        provided in the request, or if filters are used in the
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.describe_data_repository_associations)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#describe_data_repository_associations)
        """

    def describe_data_repository_tasks(
        self,
        *,
        TaskIds: Sequence[str] = ...,
        Filters: Sequence[DataRepositoryTaskFilterTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> DescribeDataRepositoryTasksResponseTypeDef:
        """
        Returns the description of specific Amazon FSx for Lustre or Amazon File Cache
        data repository tasks, if one or more `TaskIds` values are provided in the
        request, or if filters are used in the
        request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.describe_data_repository_tasks)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#describe_data_repository_tasks)
        """

    def describe_file_caches(
        self, *, FileCacheIds: Sequence[str] = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeFileCachesResponseTypeDef:
        """
        Returns the description of a specific Amazon File Cache resource, if a
        `FileCacheIds` value is provided for that
        cache.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.describe_file_caches)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#describe_file_caches)
        """

    def describe_file_system_aliases(
        self,
        *,
        FileSystemId: str,
        ClientRequestToken: str = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> DescribeFileSystemAliasesResponseTypeDef:
        """
        Returns the DNS aliases that are associated with the specified Amazon FSx for
        Windows File Server file
        system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.describe_file_system_aliases)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#describe_file_system_aliases)
        """

    def describe_file_systems(
        self, *, FileSystemIds: Sequence[str] = ..., MaxResults: int = ..., NextToken: str = ...
    ) -> DescribeFileSystemsResponseTypeDef:
        """
        Returns the description of specific Amazon FSx file systems, if a
        `FileSystemIds` value is provided for that file
        system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.describe_file_systems)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#describe_file_systems)
        """

    def describe_shared_vpc_configuration(self) -> DescribeSharedVpcConfigurationResponseTypeDef:
        """
        Indicates whether participant accounts in your organization can create Amazon
        FSx for NetApp ONTAP Multi-AZ file systems in subnets that are shared by a
        virtual private cloud (VPC)
        owner.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.describe_shared_vpc_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#describe_shared_vpc_configuration)
        """

    def describe_snapshots(
        self,
        *,
        SnapshotIds: Sequence[str] = ...,
        Filters: Sequence[SnapshotFilterTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
        IncludeShared: bool = ...,
    ) -> DescribeSnapshotsResponseTypeDef:
        """
        Returns the description of specific Amazon FSx for OpenZFS snapshots, if a
        `SnapshotIds` value is
        provided.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.describe_snapshots)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#describe_snapshots)
        """

    def describe_storage_virtual_machines(
        self,
        *,
        StorageVirtualMachineIds: Sequence[str] = ...,
        Filters: Sequence[StorageVirtualMachineFilterTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> DescribeStorageVirtualMachinesResponseTypeDef:
        """
        Describes one or more Amazon FSx for NetApp ONTAP storage virtual machines
        (SVMs).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.describe_storage_virtual_machines)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#describe_storage_virtual_machines)
        """

    def describe_volumes(
        self,
        *,
        VolumeIds: Sequence[str] = ...,
        Filters: Sequence[VolumeFilterTypeDef] = ...,
        MaxResults: int = ...,
        NextToken: str = ...,
    ) -> DescribeVolumesResponseTypeDef:
        """
        Describes one or more Amazon FSx for NetApp ONTAP or Amazon FSx for OpenZFS
        volumes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.describe_volumes)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#describe_volumes)
        """

    def disassociate_file_system_aliases(
        self, *, FileSystemId: str, Aliases: Sequence[str], ClientRequestToken: str = ...
    ) -> DisassociateFileSystemAliasesResponseTypeDef:
        """
        Use this action to disassociate, or remove, one or more Domain Name Service
        (DNS) aliases from an Amazon FSx for Windows File Server file
        system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.disassociate_file_system_aliases)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#disassociate_file_system_aliases)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.generate_presigned_url)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#generate_presigned_url)
        """

    def list_tags_for_resource(
        self, *, ResourceARN: str, MaxResults: int = ..., NextToken: str = ...
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists tags for Amazon FSx resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.list_tags_for_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#list_tags_for_resource)
        """

    def release_file_system_nfs_v3_locks(
        self, *, FileSystemId: str, ClientRequestToken: str = ...
    ) -> ReleaseFileSystemNfsV3LocksResponseTypeDef:
        """
        Releases the file system lock from an Amazon FSx for OpenZFS file system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.release_file_system_nfs_v3_locks)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#release_file_system_nfs_v3_locks)
        """

    def restore_volume_from_snapshot(
        self,
        *,
        VolumeId: str,
        SnapshotId: str,
        ClientRequestToken: str = ...,
        Options: Sequence[RestoreOpenZFSVolumeOptionType] = ...,
    ) -> RestoreVolumeFromSnapshotResponseTypeDef:
        """
        Returns an Amazon FSx for OpenZFS volume to the state saved by the specified
        snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.restore_volume_from_snapshot)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#restore_volume_from_snapshot)
        """

    def start_misconfigured_state_recovery(
        self, *, FileSystemId: str, ClientRequestToken: str = ...
    ) -> StartMisconfiguredStateRecoveryResponseTypeDef:
        """
        After performing steps to repair the Active Directory configuration of an FSx
        for Windows File Server file system, use this action to initiate the process of
        Amazon FSx attempting to reconnect to the file
        system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.start_misconfigured_state_recovery)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#start_misconfigured_state_recovery)
        """

    def tag_resource(self, *, ResourceARN: str, Tags: Sequence[TagTypeDef]) -> Dict[str, Any]:
        """
        Tags an Amazon FSx resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.tag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#tag_resource)
        """

    def untag_resource(self, *, ResourceARN: str, TagKeys: Sequence[str]) -> Dict[str, Any]:
        """
        This action removes a tag from an Amazon FSx resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.untag_resource)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#untag_resource)
        """

    def update_data_repository_association(
        self,
        *,
        AssociationId: str,
        ClientRequestToken: str = ...,
        ImportedFileChunkSize: int = ...,
        S3: S3DataRepositoryConfigurationUnionTypeDef = ...,
    ) -> UpdateDataRepositoryAssociationResponseTypeDef:
        """
        Updates the configuration of an existing data repository association on an
        Amazon FSx for Lustre file
        system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.update_data_repository_association)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#update_data_repository_association)
        """

    def update_file_cache(
        self,
        *,
        FileCacheId: str,
        ClientRequestToken: str = ...,
        LustreConfiguration: UpdateFileCacheLustreConfigurationTypeDef = ...,
    ) -> UpdateFileCacheResponseTypeDef:
        """
        Updates the configuration of an existing Amazon File Cache resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.update_file_cache)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#update_file_cache)
        """

    def update_file_system(
        self,
        *,
        FileSystemId: str,
        ClientRequestToken: str = ...,
        StorageCapacity: int = ...,
        WindowsConfiguration: UpdateFileSystemWindowsConfigurationTypeDef = ...,
        LustreConfiguration: UpdateFileSystemLustreConfigurationTypeDef = ...,
        OntapConfiguration: UpdateFileSystemOntapConfigurationTypeDef = ...,
        OpenZFSConfiguration: UpdateFileSystemOpenZFSConfigurationTypeDef = ...,
        StorageType: StorageTypeType = ...,
    ) -> UpdateFileSystemResponseTypeDef:
        """
        Use this operation to update the configuration of an existing Amazon FSx file
        system.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.update_file_system)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#update_file_system)
        """

    def update_shared_vpc_configuration(
        self,
        *,
        EnableFsxRouteTableUpdatesFromParticipantAccounts: str = ...,
        ClientRequestToken: str = ...,
    ) -> UpdateSharedVpcConfigurationResponseTypeDef:
        """
        Configures whether participant accounts in your organization can create Amazon
        FSx for NetApp ONTAP Multi-AZ file systems in subnets that are shared by a
        virtual private cloud (VPC)
        owner.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.update_shared_vpc_configuration)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#update_shared_vpc_configuration)
        """

    def update_snapshot(
        self, *, Name: str, SnapshotId: str, ClientRequestToken: str = ...
    ) -> UpdateSnapshotResponseTypeDef:
        """
        Updates the name of an Amazon FSx for OpenZFS snapshot.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.update_snapshot)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#update_snapshot)
        """

    def update_storage_virtual_machine(
        self,
        *,
        StorageVirtualMachineId: str,
        ActiveDirectoryConfiguration: UpdateSvmActiveDirectoryConfigurationTypeDef = ...,
        ClientRequestToken: str = ...,
        SvmAdminPassword: str = ...,
    ) -> UpdateStorageVirtualMachineResponseTypeDef:
        """
        Updates an FSx for ONTAP storage virtual machine (SVM).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.update_storage_virtual_machine)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#update_storage_virtual_machine)
        """

    def update_volume(
        self,
        *,
        VolumeId: str,
        ClientRequestToken: str = ...,
        OntapConfiguration: UpdateOntapVolumeConfigurationTypeDef = ...,
        Name: str = ...,
        OpenZFSConfiguration: UpdateOpenZFSVolumeConfigurationTypeDef = ...,
    ) -> UpdateVolumeResponseTypeDef:
        """
        Updates the configuration of an Amazon FSx for NetApp ONTAP or Amazon FSx for
        OpenZFS
        volume.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.update_volume)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#update_volume)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_backups"]
    ) -> DescribeBackupsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_file_systems"]
    ) -> DescribeFileSystemsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_storage_virtual_machines"]
    ) -> DescribeStorageVirtualMachinesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_volumes"]
    ) -> DescribeVolumesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx.html#FSx.Client.get_paginator)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/client/#get_paginator)
        """
