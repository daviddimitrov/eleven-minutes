import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as s3 from 'aws-cdk-lib/aws-s3';

export class ElevenMinutesStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    new s3.Bucket(this, 'MyFirstBucket', {
      versioned: true, // Aktiviert Versionierung
      removalPolicy: cdk.RemovalPolicy.DESTROY, // Löscht den Bucket beim Stack-Delete
    });
  }
}
