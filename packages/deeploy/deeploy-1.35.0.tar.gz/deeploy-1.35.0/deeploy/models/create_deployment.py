from typing import Dict, Optional

from pydantic import BaseModel

from deeploy.enums import ExplainerType, ModelType, TransformerType


class CreateDeployment(BaseModel):
    """Class that contains the options for creating a Deployment"""

    name: str
    """str: name of the Deployment"""
    description: Optional[str] = None
    """str, optional: the description of the Deployment"""
    repository_id: str
    """str: uuid of the Repository"""
    branch_name: str
    """str: the branch name of the Repository to deploy"""
    commit: str
    """str: the commit sha on the selected branch"""
    commit_message: Optional[str] = None
    """str, optional: the commit message of the selected commit"""
    contract_path: Optional[str] = None
    """str, optional: relative repository subpath that contains the Deeploy contract to deploy from"""
    deployment_backend: Optional[str] = None
    """str, optional: deployment backend where Deeploy will deploy to [KServe, AzureML, Sagemaker]"""
    region: Optional[str] = None
    """str, optional: the AWS region used for this Deployment, only available for SageMaker Deployments"""
    model_type: ModelType
    """int: enum value from ModelType class"""
    model_serverless: bool = False
    """bool, optional: whether to deploy the model in a serverless fashion. Defaults to False"""
    model_credentials_id: Optional[str] = None
    """str, optional: uuid of credentials generated in Deeploy to access private Blob storage or Docker repo"""
    model_instance_type: Optional[str] = None
    """str, optional: the preferred instance type for the model"""
    model_mem_request: Optional[int] = None
    """int, optional: RAM request of model pod, in Megabytes."""
    model_mem_limit: Optional[int] = None
    """int, optional: RAM limit of model pod, in Megabytes."""
    model_cpu_request: Optional[float] = None
    """float, optional: CPU request of model pod, in CPUs."""
    model_cpu_limit: Optional[float] = None
    """float, optional: CPU limit of model pod, in CPUs."""
    explainer_type: Optional[ExplainerType] = ExplainerType.NO_EXPLAINER
    """int, optional: enum value from ExplainerType class. Defaults to 0 (no explainer)"""
    explainer_serverless: bool = False
    """bool, optional: whether to deploy the model in a serverless fashion. Defaults to False"""
    explainer_credentials_id: Optional[str] = None
    """str, optional: Credential id of credential generated in Deeploy to access private Blob storage or Docker repo"""
    explainer_instance_type: Optional[str] = None
    """str, optional: The preferred instance type for the model pod."""
    explainer_mem_request: Optional[int] = None
    """int, optional: RAM request of model pod, in Megabytes."""
    explainer_mem_limit: Optional[int] = None
    """int, optional: RAM limit of model pod, in Megabytes."""
    explainer_cpu_request: Optional[float] = None
    """float, optional: CPU request of model pod, in CPUs."""
    explainer_cpu_limit: Optional[float] = None
    """float, optional: CPU limit of model pod, in CPUs."""
    transformer_type: Optional[TransformerType] = TransformerType.NO_TRANSFORMER
    """int, optional: enum value from TransformerType class. Defaults to 0 (no transformer)"""
    transformer_serverless: bool = False
    """bool, optional: whether to deploy the model in a serverless fashion. Defaults to False"""
    transformer_credentials_id: Optional[str] = None
    """str, optional: Credential id of credential generated in Deeploy to access private Blob storage or Docker repo"""
    transformer_instance_type: Optional[str] = None
    """str, optional: The preferred instance type for the model pod."""
    transformer_mem_request: Optional[int] = None
    """int, optional: RAM request of model pod, in Megabytes."""
    transformer_mem_limit: Optional[int] = None
    """int, optional: RAM limit of model pod, in Megabytes."""
    transformer_cpu_request: Optional[float] = None
    """float, optional: CPU request of model pod, in CPUs."""
    transformer_cpu_limit: Optional[float] = None
    """float, optional: CPU limit of model pod, in CPUs."""

    def to_request_body(self) -> Dict:
        return {
            "name": self.name,
            "description": self.description,
            "repositoryId": self.repository_id,
            "branchName": self.branch_name,
            "commit": self.commit,
            "commitMessage": self.commit_message,
            "contractPath": self.contract_path,
            "deploymentBackend": self.deployment_backend,
            "region": self.region,
            "modelType": self.model_type.value,
            "modelServerless": self.model_serverless,
            "modelCredentialsId": self.model_credentials_id,
            "modelInstanceType": self.model_instance_type,
            "modelMemRequest": self.model_mem_request,
            "modelMemLimit": self.model_mem_limit,
            "modelCpuRequest": self.model_cpu_request,
            "modelCpuLimit": self.model_cpu_limit,
            "explainerType": self.explainer_type.value,
            "explainerServerless": self.explainer_serverless,
            "explainerInstanceType": self.explainer_instance_type,
            "explainerCredentialsId": self.explainer_credentials_id,
            "explainerMemRequest": self.explainer_mem_request,
            "explainerMemLimit": self.explainer_mem_limit,
            "explainerCpuRequest": self.explainer_cpu_request,
            "explainerCpuLimit": self.explainer_cpu_limit,
            "transformerType": self.transformer_type.value,
            "transformerServerless": self.transformer_serverless,
            "transformerCredentialsId": self.transformer_credentials_id,
            "transformerInstanceType": self.transformer_instance_type,
            "transformerMemRequest": self.transformer_mem_request,
            "transformerMemLimit": self.transformer_mem_limit,
            "transformerCpuRequest": self.transformer_cpu_request,
            "transformerCpuLimit": self.transformer_cpu_limit,
        }


class CreateAzureMLDeployment(BaseModel):
    """Class that contains the options for creating an Azure Machine Learning deployment"""

    name: str
    """str: name of the Deployment"""
    description: Optional[str] = None
    """str, optional: the description of the Deployment"""
    repository_id: str
    """str: uuid of the Repository"""
    branch_name: str
    """str: the branch name of the Repository to deploy"""
    commit: str
    """str: the commit sha on the selected branch"""
    commit_message: Optional[str] = None
    """str, optional: the commit message of the selected commit"""
    contract_path: Optional[str] = None
    """str, optional: relative repository subpath that contains the Deeploy contract to deploy from"""
    model_type: ModelType
    """int: enum value from ModelType class"""
    explainer_type: Optional[ExplainerType] = ExplainerType.NO_EXPLAINER
    """int, optional: enum value from ExplainerType class. Defaults to 0 (no explainer)"""
    transformer_type: Optional[TransformerType] = TransformerType.NO_TRANSFORMER
    """int, optional: enum value from TransformerType class. Defaults to 0 (no transformer)"""
    model_instance_type: Optional[str] = None
    """str, optional: the preferred instance type for the model"""
    model_instance_count: Optional[int] = None
    """int, optional: the amount of compute instances used for your model deployment"""
    explainer_instance_type: Optional[str] = None
    """str, optional: The preferred instance type for the model pod."""
    explainer_instance_count: Optional[int] = None
    """int, optional: the amount of compute instances used for your explainer deployment"""

    def to_request_body(self) -> Dict:
        return {
            "name": self.name,
            "description": self.description,
            "repositoryId": self.repository_id,
            "branchName": self.branch_name,
            "commit": self.commit,
            "commitMessage": self.commit_message,
            "contractPath": self.contract_path,
            "modelType": self.model_type.value,
            "explainerType": self.explainer_type.value,
            "transformerType": self.transformer_type.value,
            "modelInstanceType": self.model_instance_type,
            "modelInstanceCount": self.model_instance_count,
            "explainerInstanceType": self.explainer_instance_type,
            "explainerInstanceCount": self.explainer_instance_count,
        }
