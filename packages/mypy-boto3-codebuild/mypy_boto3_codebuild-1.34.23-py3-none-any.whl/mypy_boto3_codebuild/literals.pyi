"""
Type annotations for codebuild service literal definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codebuild/literals/)

Usage::

    ```python
    from mypy_boto3_codebuild.literals import ArtifactNamespaceType

    data: ArtifactNamespaceType = "BUILD_ID"
    ```
"""

import sys

if sys.version_info >= (3, 12):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "ArtifactNamespaceType",
    "ArtifactPackagingType",
    "ArtifactsTypeType",
    "AuthTypeType",
    "BatchReportModeTypeType",
    "BucketOwnerAccessType",
    "BuildBatchPhaseTypeType",
    "BuildPhaseTypeType",
    "CacheModeType",
    "CacheTypeType",
    "ComputeTypeType",
    "CredentialProviderTypeType",
    "DescribeCodeCoveragesPaginatorName",
    "DescribeTestCasesPaginatorName",
    "EnvironmentTypeType",
    "EnvironmentVariableTypeType",
    "FileSystemTypeType",
    "FleetContextCodeType",
    "FleetScalingMetricTypeType",
    "FleetScalingTypeType",
    "FleetSortByTypeType",
    "FleetStatusCodeType",
    "ImagePullCredentialsTypeType",
    "LanguageTypeType",
    "ListBuildBatchesForProjectPaginatorName",
    "ListBuildBatchesPaginatorName",
    "ListBuildsForProjectPaginatorName",
    "ListBuildsPaginatorName",
    "ListProjectsPaginatorName",
    "ListReportGroupsPaginatorName",
    "ListReportsForReportGroupPaginatorName",
    "ListReportsPaginatorName",
    "ListSharedProjectsPaginatorName",
    "ListSharedReportGroupsPaginatorName",
    "LogsConfigStatusTypeType",
    "PlatformTypeType",
    "ProjectSortByTypeType",
    "ProjectVisibilityTypeType",
    "ReportCodeCoverageSortByTypeType",
    "ReportExportConfigTypeType",
    "ReportGroupSortByTypeType",
    "ReportGroupStatusTypeType",
    "ReportGroupTrendFieldTypeType",
    "ReportPackagingTypeType",
    "ReportStatusTypeType",
    "ReportTypeType",
    "RetryBuildBatchTypeType",
    "ServerTypeType",
    "SharedResourceSortByTypeType",
    "SortOrderTypeType",
    "SourceAuthTypeType",
    "SourceTypeType",
    "StatusTypeType",
    "WebhookBuildTypeType",
    "WebhookFilterTypeType",
    "CodeBuildServiceName",
    "ServiceName",
    "ResourceServiceName",
    "PaginatorName",
    "RegionName",
)

ArtifactNamespaceType = Literal["BUILD_ID", "NONE"]
ArtifactPackagingType = Literal["NONE", "ZIP"]
ArtifactsTypeType = Literal["CODEPIPELINE", "NO_ARTIFACTS", "S3"]
AuthTypeType = Literal["BASIC_AUTH", "OAUTH", "PERSONAL_ACCESS_TOKEN"]
BatchReportModeTypeType = Literal["REPORT_AGGREGATED_BATCH", "REPORT_INDIVIDUAL_BUILDS"]
BucketOwnerAccessType = Literal["FULL", "NONE", "READ_ONLY"]
BuildBatchPhaseTypeType = Literal[
    "COMBINE_ARTIFACTS",
    "DOWNLOAD_BATCHSPEC",
    "FAILED",
    "IN_PROGRESS",
    "STOPPED",
    "SUBMITTED",
    "SUCCEEDED",
]
BuildPhaseTypeType = Literal[
    "BUILD",
    "COMPLETED",
    "DOWNLOAD_SOURCE",
    "FINALIZING",
    "INSTALL",
    "POST_BUILD",
    "PRE_BUILD",
    "PROVISIONING",
    "QUEUED",
    "SUBMITTED",
    "UPLOAD_ARTIFACTS",
]
CacheModeType = Literal["LOCAL_CUSTOM_CACHE", "LOCAL_DOCKER_LAYER_CACHE", "LOCAL_SOURCE_CACHE"]
CacheTypeType = Literal["LOCAL", "NO_CACHE", "S3"]
ComputeTypeType = Literal[
    "BUILD_GENERAL1_2XLARGE",
    "BUILD_GENERAL1_LARGE",
    "BUILD_GENERAL1_MEDIUM",
    "BUILD_GENERAL1_SMALL",
    "BUILD_GENERAL1_XLARGE",
    "BUILD_LAMBDA_10GB",
    "BUILD_LAMBDA_1GB",
    "BUILD_LAMBDA_2GB",
    "BUILD_LAMBDA_4GB",
    "BUILD_LAMBDA_8GB",
]
CredentialProviderTypeType = Literal["SECRETS_MANAGER"]
DescribeCodeCoveragesPaginatorName = Literal["describe_code_coverages"]
DescribeTestCasesPaginatorName = Literal["describe_test_cases"]
EnvironmentTypeType = Literal[
    "ARM_CONTAINER",
    "ARM_LAMBDA_CONTAINER",
    "LINUX_CONTAINER",
    "LINUX_GPU_CONTAINER",
    "LINUX_LAMBDA_CONTAINER",
    "WINDOWS_CONTAINER",
    "WINDOWS_SERVER_2019_CONTAINER",
]
EnvironmentVariableTypeType = Literal["PARAMETER_STORE", "PLAINTEXT", "SECRETS_MANAGER"]
FileSystemTypeType = Literal["EFS"]
FleetContextCodeType = Literal["CREATE_FAILED", "UPDATE_FAILED"]
FleetScalingMetricTypeType = Literal["FLEET_UTILIZATION_RATE"]
FleetScalingTypeType = Literal["TARGET_TRACKING_SCALING"]
FleetSortByTypeType = Literal["CREATED_TIME", "LAST_MODIFIED_TIME", "NAME"]
FleetStatusCodeType = Literal[
    "ACTIVE",
    "CREATE_FAILED",
    "CREATING",
    "DELETING",
    "ROTATING",
    "UPDATE_ROLLBACK_FAILED",
    "UPDATING",
]
ImagePullCredentialsTypeType = Literal["CODEBUILD", "SERVICE_ROLE"]
LanguageTypeType = Literal[
    "ANDROID", "BASE", "DOCKER", "DOTNET", "GOLANG", "JAVA", "NODE_JS", "PHP", "PYTHON", "RUBY"
]
ListBuildBatchesForProjectPaginatorName = Literal["list_build_batches_for_project"]
ListBuildBatchesPaginatorName = Literal["list_build_batches"]
ListBuildsForProjectPaginatorName = Literal["list_builds_for_project"]
ListBuildsPaginatorName = Literal["list_builds"]
ListProjectsPaginatorName = Literal["list_projects"]
ListReportGroupsPaginatorName = Literal["list_report_groups"]
ListReportsForReportGroupPaginatorName = Literal["list_reports_for_report_group"]
ListReportsPaginatorName = Literal["list_reports"]
ListSharedProjectsPaginatorName = Literal["list_shared_projects"]
ListSharedReportGroupsPaginatorName = Literal["list_shared_report_groups"]
LogsConfigStatusTypeType = Literal["DISABLED", "ENABLED"]
PlatformTypeType = Literal["AMAZON_LINUX", "DEBIAN", "UBUNTU", "WINDOWS_SERVER"]
ProjectSortByTypeType = Literal["CREATED_TIME", "LAST_MODIFIED_TIME", "NAME"]
ProjectVisibilityTypeType = Literal["PRIVATE", "PUBLIC_READ"]
ReportCodeCoverageSortByTypeType = Literal["FILE_PATH", "LINE_COVERAGE_PERCENTAGE"]
ReportExportConfigTypeType = Literal["NO_EXPORT", "S3"]
ReportGroupSortByTypeType = Literal["CREATED_TIME", "LAST_MODIFIED_TIME", "NAME"]
ReportGroupStatusTypeType = Literal["ACTIVE", "DELETING"]
ReportGroupTrendFieldTypeType = Literal[
    "BRANCHES_COVERED",
    "BRANCHES_MISSED",
    "BRANCH_COVERAGE",
    "DURATION",
    "LINES_COVERED",
    "LINES_MISSED",
    "LINE_COVERAGE",
    "PASS_RATE",
    "TOTAL",
]
ReportPackagingTypeType = Literal["NONE", "ZIP"]
ReportStatusTypeType = Literal["DELETING", "FAILED", "GENERATING", "INCOMPLETE", "SUCCEEDED"]
ReportTypeType = Literal["CODE_COVERAGE", "TEST"]
RetryBuildBatchTypeType = Literal["RETRY_ALL_BUILDS", "RETRY_FAILED_BUILDS"]
ServerTypeType = Literal["BITBUCKET", "GITHUB", "GITHUB_ENTERPRISE"]
SharedResourceSortByTypeType = Literal["ARN", "MODIFIED_TIME"]
SortOrderTypeType = Literal["ASCENDING", "DESCENDING"]
SourceAuthTypeType = Literal["OAUTH"]
SourceTypeType = Literal[
    "BITBUCKET", "CODECOMMIT", "CODEPIPELINE", "GITHUB", "GITHUB_ENTERPRISE", "NO_SOURCE", "S3"
]
StatusTypeType = Literal["FAILED", "FAULT", "IN_PROGRESS", "STOPPED", "SUCCEEDED", "TIMED_OUT"]
WebhookBuildTypeType = Literal["BUILD", "BUILD_BATCH"]
WebhookFilterTypeType = Literal[
    "ACTOR_ACCOUNT_ID", "BASE_REF", "COMMIT_MESSAGE", "EVENT", "FILE_PATH", "HEAD_REF"
]
CodeBuildServiceName = Literal["codebuild"]
ServiceName = Literal[
    "accessanalyzer",
    "account",
    "acm",
    "acm-pca",
    "alexaforbusiness",
    "amp",
    "amplify",
    "amplifybackend",
    "amplifyuibuilder",
    "apigateway",
    "apigatewaymanagementapi",
    "apigatewayv2",
    "appconfig",
    "appconfigdata",
    "appfabric",
    "appflow",
    "appintegrations",
    "application-autoscaling",
    "application-insights",
    "applicationcostprofiler",
    "appmesh",
    "apprunner",
    "appstream",
    "appsync",
    "arc-zonal-shift",
    "athena",
    "auditmanager",
    "autoscaling",
    "autoscaling-plans",
    "b2bi",
    "backup",
    "backup-gateway",
    "backupstorage",
    "batch",
    "bcm-data-exports",
    "bedrock",
    "bedrock-agent",
    "bedrock-agent-runtime",
    "bedrock-runtime",
    "billingconductor",
    "braket",
    "budgets",
    "ce",
    "chime",
    "chime-sdk-identity",
    "chime-sdk-media-pipelines",
    "chime-sdk-meetings",
    "chime-sdk-messaging",
    "chime-sdk-voice",
    "cleanrooms",
    "cleanroomsml",
    "cloud9",
    "cloudcontrol",
    "clouddirectory",
    "cloudformation",
    "cloudfront",
    "cloudfront-keyvaluestore",
    "cloudhsm",
    "cloudhsmv2",
    "cloudsearch",
    "cloudsearchdomain",
    "cloudtrail",
    "cloudtrail-data",
    "cloudwatch",
    "codeartifact",
    "codebuild",
    "codecatalyst",
    "codecommit",
    "codedeploy",
    "codeguru-reviewer",
    "codeguru-security",
    "codeguruprofiler",
    "codepipeline",
    "codestar",
    "codestar-connections",
    "codestar-notifications",
    "cognito-identity",
    "cognito-idp",
    "cognito-sync",
    "comprehend",
    "comprehendmedical",
    "compute-optimizer",
    "config",
    "connect",
    "connect-contact-lens",
    "connectcampaigns",
    "connectcases",
    "connectparticipant",
    "controltower",
    "cost-optimization-hub",
    "cur",
    "customer-profiles",
    "databrew",
    "dataexchange",
    "datapipeline",
    "datasync",
    "datazone",
    "dax",
    "detective",
    "devicefarm",
    "devops-guru",
    "directconnect",
    "discovery",
    "dlm",
    "dms",
    "docdb",
    "docdb-elastic",
    "drs",
    "ds",
    "dynamodb",
    "dynamodbstreams",
    "ebs",
    "ec2",
    "ec2-instance-connect",
    "ecr",
    "ecr-public",
    "ecs",
    "efs",
    "eks",
    "eks-auth",
    "elastic-inference",
    "elasticache",
    "elasticbeanstalk",
    "elastictranscoder",
    "elb",
    "elbv2",
    "emr",
    "emr-containers",
    "emr-serverless",
    "entityresolution",
    "es",
    "events",
    "evidently",
    "finspace",
    "finspace-data",
    "firehose",
    "fis",
    "fms",
    "forecast",
    "forecastquery",
    "frauddetector",
    "freetier",
    "fsx",
    "gamelift",
    "glacier",
    "globalaccelerator",
    "glue",
    "grafana",
    "greengrass",
    "greengrassv2",
    "groundstation",
    "guardduty",
    "health",
    "healthlake",
    "honeycode",
    "iam",
    "identitystore",
    "imagebuilder",
    "importexport",
    "inspector",
    "inspector-scan",
    "inspector2",
    "internetmonitor",
    "iot",
    "iot-data",
    "iot-jobs-data",
    "iot-roborunner",
    "iot1click-devices",
    "iot1click-projects",
    "iotanalytics",
    "iotdeviceadvisor",
    "iotevents",
    "iotevents-data",
    "iotfleethub",
    "iotfleetwise",
    "iotsecuretunneling",
    "iotsitewise",
    "iotthingsgraph",
    "iottwinmaker",
    "iotwireless",
    "ivs",
    "ivs-realtime",
    "ivschat",
    "kafka",
    "kafkaconnect",
    "kendra",
    "kendra-ranking",
    "keyspaces",
    "kinesis",
    "kinesis-video-archived-media",
    "kinesis-video-media",
    "kinesis-video-signaling",
    "kinesis-video-webrtc-storage",
    "kinesisanalytics",
    "kinesisanalyticsv2",
    "kinesisvideo",
    "kms",
    "lakeformation",
    "lambda",
    "launch-wizard",
    "lex-models",
    "lex-runtime",
    "lexv2-models",
    "lexv2-runtime",
    "license-manager",
    "license-manager-linux-subscriptions",
    "license-manager-user-subscriptions",
    "lightsail",
    "location",
    "logs",
    "lookoutequipment",
    "lookoutmetrics",
    "lookoutvision",
    "m2",
    "machinelearning",
    "macie2",
    "managedblockchain",
    "managedblockchain-query",
    "marketplace-agreement",
    "marketplace-catalog",
    "marketplace-deployment",
    "marketplace-entitlement",
    "marketplacecommerceanalytics",
    "mediaconnect",
    "mediaconvert",
    "medialive",
    "mediapackage",
    "mediapackage-vod",
    "mediapackagev2",
    "mediastore",
    "mediastore-data",
    "mediatailor",
    "medical-imaging",
    "memorydb",
    "meteringmarketplace",
    "mgh",
    "mgn",
    "migration-hub-refactor-spaces",
    "migrationhub-config",
    "migrationhuborchestrator",
    "migrationhubstrategy",
    "mobile",
    "mq",
    "mturk",
    "mwaa",
    "neptune",
    "neptune-graph",
    "neptunedata",
    "network-firewall",
    "networkmanager",
    "networkmonitor",
    "nimble",
    "oam",
    "omics",
    "opensearch",
    "opensearchserverless",
    "opsworks",
    "opsworkscm",
    "organizations",
    "osis",
    "outposts",
    "panorama",
    "payment-cryptography",
    "payment-cryptography-data",
    "pca-connector-ad",
    "personalize",
    "personalize-events",
    "personalize-runtime",
    "pi",
    "pinpoint",
    "pinpoint-email",
    "pinpoint-sms-voice",
    "pinpoint-sms-voice-v2",
    "pipes",
    "polly",
    "pricing",
    "privatenetworks",
    "proton",
    "qbusiness",
    "qconnect",
    "qldb",
    "qldb-session",
    "quicksight",
    "ram",
    "rbin",
    "rds",
    "rds-data",
    "redshift",
    "redshift-data",
    "redshift-serverless",
    "rekognition",
    "repostspace",
    "resiliencehub",
    "resource-explorer-2",
    "resource-groups",
    "resourcegroupstaggingapi",
    "robomaker",
    "rolesanywhere",
    "route53",
    "route53-recovery-cluster",
    "route53-recovery-control-config",
    "route53-recovery-readiness",
    "route53domains",
    "route53resolver",
    "rum",
    "s3",
    "s3control",
    "s3outposts",
    "sagemaker",
    "sagemaker-a2i-runtime",
    "sagemaker-edge",
    "sagemaker-featurestore-runtime",
    "sagemaker-geospatial",
    "sagemaker-metrics",
    "sagemaker-runtime",
    "savingsplans",
    "scheduler",
    "schemas",
    "sdb",
    "secretsmanager",
    "securityhub",
    "securitylake",
    "serverlessrepo",
    "service-quotas",
    "servicecatalog",
    "servicecatalog-appregistry",
    "servicediscovery",
    "ses",
    "sesv2",
    "shield",
    "signer",
    "simspaceweaver",
    "sms",
    "sms-voice",
    "snow-device-management",
    "snowball",
    "sns",
    "sqs",
    "ssm",
    "ssm-contacts",
    "ssm-incidents",
    "ssm-sap",
    "sso",
    "sso-admin",
    "sso-oidc",
    "stepfunctions",
    "storagegateway",
    "sts",
    "supplychain",
    "support",
    "support-app",
    "swf",
    "synthetics",
    "textract",
    "timestream-query",
    "timestream-write",
    "tnb",
    "transcribe",
    "transfer",
    "translate",
    "trustedadvisor",
    "verifiedpermissions",
    "voice-id",
    "vpc-lattice",
    "waf",
    "waf-regional",
    "wafv2",
    "wellarchitected",
    "wisdom",
    "workdocs",
    "worklink",
    "workmail",
    "workmailmessageflow",
    "workspaces",
    "workspaces-thin-client",
    "workspaces-web",
    "xray",
]
ResourceServiceName = Literal[
    "cloudformation",
    "cloudwatch",
    "dynamodb",
    "ec2",
    "glacier",
    "iam",
    "opsworks",
    "s3",
    "sns",
    "sqs",
]
PaginatorName = Literal[
    "describe_code_coverages",
    "describe_test_cases",
    "list_build_batches",
    "list_build_batches_for_project",
    "list_builds",
    "list_builds_for_project",
    "list_projects",
    "list_report_groups",
    "list_reports",
    "list_reports_for_report_group",
    "list_shared_projects",
    "list_shared_report_groups",
]
RegionName = Literal[
    "af-south-1",
    "ap-east-1",
    "ap-northeast-1",
    "ap-northeast-2",
    "ap-northeast-3",
    "ap-south-1",
    "ap-south-2",
    "ap-southeast-1",
    "ap-southeast-2",
    "ap-southeast-3",
    "ap-southeast-4",
    "ca-central-1",
    "eu-central-1",
    "eu-central-2",
    "eu-north-1",
    "eu-south-1",
    "eu-south-2",
    "eu-west-1",
    "eu-west-2",
    "eu-west-3",
    "il-central-1",
    "me-central-1",
    "me-south-1",
    "sa-east-1",
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2",
]
