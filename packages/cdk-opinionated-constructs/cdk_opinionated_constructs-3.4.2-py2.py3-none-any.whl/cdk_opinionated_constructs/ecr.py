"""Opinionated CDK construct for AWS ECR repository with enabled security."""


import aws_cdk as cdk
import aws_cdk.aws_ecr as ecr

from constructs import Construct


class ECR(Construct):
    """Create ECR resource with tag immutability, lifecycle rule and removal
    policy."""

    def __init__(self, scope: Construct, id: str):  # noqa: A002
        super().__init__(scope, id)

    def repository(
            self, repository_name: str, empty_on_delete: bool, **kwargs  # noqa: FBT001
    ) -> ecr.Repository | ecr.IRepository:
        """
        Creates an ECR repository with the given name.

        Parameters:
        - repository_name (str): The name for the ECR repository.
        - empty_on_delete (bool): Whether to empty the repository instead of deleting on destroy.
        - max_image_age (int, optional): The maximum age in days for images before they are cleaned up.
        - max_image_count (int, optional): The maximum number of images to retain in the repository.

        Returns:
        - ecr.Repository | ecr.IRepository: The created ECR repository resource.

        The repository will have image scanning on push enabled, immutable tagging, 
        and a lifecycle rule configured based on the max_image_age and max_image_count
        parameters if provided.
        """

        max_image_age = None
        max_image_count = None

        if kwargs.get("max_image_age"):
            max_image_age = cdk.Duration.days(kwargs.get("max_image_age"))

        if kwargs.get("max_image_count"):
            max_image_age = max_image_count

        return ecr.Repository(
            self,
            id=repository_name,
            empty_on_delete=empty_on_delete,
            image_scan_on_push=True,
            image_tag_mutability=ecr.TagMutability.IMMUTABLE,
            lifecycle_rules=[
                ecr.LifecycleRule(
                    max_image_count=max_image_count,
                    max_image_age=max_image_age,
                )
            ],
            repository_name=repository_name,
        )
