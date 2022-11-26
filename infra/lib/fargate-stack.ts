import * as cdk from 'aws-cdk-lib';
import * as ecr from 'aws-cdk-lib/aws-ecr';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as ecs from 'aws-cdk-lib/aws-ecs';
import { Construct } from 'constructs';
import { Port } from 'aws-cdk-lib/aws-ec2';

interface ConsumerProps extends cdk.StackProps {
    ecrRepo: ecr.IRepository;
    infraVpc: ec2.IVpc
  }

// This is the root construct that contains the other constructs
export class FargateStack extends cdk.Stack {
  // This method is called when the new object is created. It takes the properties scope, id and KV props.
  constructor(scope: Construct, id: string, props: ConsumerProps) {
    // Calls the parent class constructor with the same properties
    super(scope, id, props);

    const cluster = new ecs.Cluster(this, 'strongFargateCluster', { 
        vpc: props.infraVpc,
        enableFargateCapacityProviders: true
      });

    const taskDefinition = new ecs.FargateTaskDefinition(this, 'StrongFargateTaskDef', {
      memoryLimitMiB: 512,
      cpu: 256,
    });

    const container = taskDefinition.addContainer("strong-visualizer", {
      // Use an image from from ECR private registry
      image: ecs.ContainerImage.fromEcrRepository(props.ecrRepo, "latest"),
    });

    container.addPortMappings({
      containerPort: 8050,
      hostPort: 8050
    });


    const fargate_sg = new ec2.SecurityGroup(this, 'fargateSG', {
      vpc: props.infraVpc,
      allowAllOutbound: true
    });

    fargate_sg.addIngressRule(
      ec2.Peer.anyIpv4(), 
      ec2.Port.tcp(8050), 
      'HTTP from anywhere');

    const service = new ecs.FargateService(this, 'StrongFargateService', {
      cluster, 
      taskDefinition, 
      assignPublicIp: true,
      securityGroups: [fargate_sg]
     });

  }
}
