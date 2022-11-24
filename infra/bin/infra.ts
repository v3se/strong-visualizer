#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { InfraStack } from '../lib/infra-stack';
import { FargateStack } from '../lib/fargate-stack';

const app = new cdk.App();
const infrastack = new InfraStack(app, 'InfraStack', {});
// Import a ecr repository object to Fargate stack from InfraStack
// Example: https://docs.aws.amazon.com/cdk/api/v1/docs/aws-s3-readme.html#sharing-buckets-between-stacks
new FargateStack(app, 'FargateStack', { ecrRepo: infrastack.ecrRepository, infraVpc: infrastack.infraVpc });