# https://docs.djangoproject.com/en/3.2/topics/db/models/#organizing-models-in-a-package

# Must be imported first as other models depend on it
from .base import (  # noqa
    BaseModel,
    Label,
    MasterModel,
    pulp_uuid,
)

from .access_policy import (  # noqa
    AccessPolicy,
    AutoAddObjPermsMixin,
    Group,
)

from .acs import AlternateContentSource, AlternateContentSourcePath  # noqa

from .content import (  # noqa
    Artifact,
    AsciiArmoredDetachedSigningService,
    Content,
    ContentManager,
    ContentArtifact,
    PulpTemporaryFile,
    RemoteArtifact,
    SigningService,
    UnsupportedDigestValidationError,
)

from .generic import GenericRelationModel  # noqa

from .exporter import (  # noqa
    Export,
    ExportedResource,
    Exporter,
    FilesystemExport,
    FilesystemExporter,
    PulpExport,
    PulpExporter,
)

from .importer import (  # noqa
    Import,
    Importer,
    PulpImport,
    PulpImporter,
)

from .publication import (  # noqa
    ContentGuard,
    Distribution,
    Publication,
    PublishedArtifact,
    PublishedMetadata,
    RBACContentGuard,
    ContentRedirectContentGuard,
)

from .repository import (  # noqa
    Remote,
    Repository,
    RepositoryContent,
    RepositoryVersion,
    RepositoryVersionContentDetails,
)

# This can lead to circular imports with a custom user model depending on this very module
# Moved to plugin/models/role.py to avoid the circular import.
# from .role import (  # noqa
#     GroupRole,
#     Role,
#     UserRole,
# )

from .status import ContentAppStatus  # noqa

from .task import (  # noqa
    CreatedResource,
    Task,
    TaskGroup,
    TaskSchedule,
    Worker,
)

from .telemetry import SystemID  # noqa

from .upload import (  # noqa
    Upload,
    UploadChunk,
)

# Moved here to avoid a circular import with Task
from .progress import GroupProgressReport, ProgressReport  # noqa
