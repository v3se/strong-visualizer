import * as cdk from 'aws-cdk-lib';
import * as ecr from 'aws-cdk-lib/aws-ecr';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import { Construct } from 'constructs';

// This is the root construct that contains the other constructs
export class InfraStack extends cdk.Stack {
  // This method is called when the new object is created. It takes the properties scope, id and KV props.
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    // Calls the parent class constructor with the same properties
    super(scope, id, props);

    // Parameter for the ECR private registry name where the docker image is stored
    const repository_name = new cdk.CfnParameter(this, 'repositoryName', {
      type: "String",
      description: "The name of the ecr repo"});

    // Import the ECR repository based on the name  
    const repository = ecr.Repository.fromRepositoryName(this, 'ecrRepo', repository_name.valueAsString)

    const vpc = new ec2.Vpc(this, 'strongVisualizerVpc', {
      ipAddresses: ec2.IpAddresses.cidr('192.168.0.0/16'),
      natGateways: 0,
      vpcName: 'strongVisualizerVPC'
   })

    // Define a new variable which contains new ecr repository
    // Moved this out of the CDK since the container needs to be pushed to ECR before running this app
    // const repository = new ecr.Repository(this, 'strongVisualizerEcr');

    const cluster = new ecs.Cluster(this, 'StrongFargateCluster', { 
      vpc: vpc,
      enableFargateCapacityProviders: true
    });

    const fargateTaskDefinition = new ecs.FargateTaskDefinition(this, 'StrongFargateTaskDef', {
      memoryLimitMiB: 512,
      cpu: 256,
    });

    const c = fargateTaskDefinition.addContainer("test", {
      // Use an image from from ECR private registry
      image: ecs.ContainerImage.fromEcrRepository(repository, "latest"),
    });

    const service = new ecs.FargateService(this, 'StrongFargateService', { cluster, fargateTaskDefinition });
    
    // Create CFN output with the value of the ecr repository URI. We will use this in the CI/CD pipeline when pushing images
    // new cdk.CfnOutput(this, 'repositoryUri', {
    //   value: repository.repositoryUri,
    //   description: 'The URI  of Strong Visualizer ECR repository',
    //   exportName: 'strongRepositoryUri',
    // });

  }
}
