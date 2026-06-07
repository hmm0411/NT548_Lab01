import subprocess
import boto3


TERRAFORM_DIR = "../terraform"


def run_cmd(command):
    result = subprocess.run(
        command,
        cwd=TERRAFORM_DIR,
        capture_output=True,
        text=True,
        shell=True
    )

    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError(f"Command failed: {command}")

    return result.stdout.strip()


def tf_output(name):
    return run_cmd(f"terraform output -raw {name}")


def check(condition, message):
    if condition:
        print(f"[PASS] {message}")
    else:
        print(f"[FAIL] {message}")
        raise AssertionError(message)

REGION = "us-east-1"

vpc_id = tf_output("vpc_id")
public_subnet_id = tf_output("public_subnet_id")
private_subnet_id = tf_output("private_subnet_id")
igw_id = tf_output("igw_id")
nat_gateway_id = tf_output("nat_gateway_id")
public_route_table_id = tf_output("public_route_table_id")
private_route_table_id = tf_output("private_route_table_id")
public_sg_id = tf_output("public_sg_id")
private_sg_id = tf_output("private_sg_id")
public_ec2_public_ip = tf_output("public_ec2_public_ip")
private_ec2_private_ip = tf_output("private_ec2_private_ip")

ec2 = boto3.client("ec2", region_name=REGION)


print("\n===== TEST 1: VPC =====")
vpc = ec2.describe_vpcs(VpcIds=[vpc_id])["Vpcs"][0]
check(vpc["State"] == "available", "VPC exists and is available")
check(vpc["CidrBlock"] != "", "VPC has CIDR block")


print("\n===== TEST 2: SUBNETS =====")
subnets = ec2.describe_subnets(
    SubnetIds=[public_subnet_id, private_subnet_id]
)["Subnets"]

public_subnet = next(s for s in subnets if s["SubnetId"] == public_subnet_id)
private_subnet = next(s for s in subnets if s["SubnetId"] == private_subnet_id)

check(public_subnet["VpcId"] == vpc_id, "Public subnet belongs to VPC")
check(private_subnet["VpcId"] == vpc_id, "Private subnet belongs to VPC")
check(public_subnet["MapPublicIpOnLaunch"] is True, "Public subnet maps public IP on launch")
check(private_subnet["MapPublicIpOnLaunch"] is False, "Private subnet does not map public IP on launch")


print("\n===== TEST 3: INTERNET GATEWAY =====")
igw = ec2.describe_internet_gateways(
    InternetGatewayIds=[igw_id]
)["InternetGateways"][0]

attachments = igw.get("Attachments", [])
check(len(attachments) > 0, "Internet Gateway has attachment")
check(
    any(a["VpcId"] == vpc_id and a["State"] == "available" for a in attachments),
    "Internet Gateway is attached to VPC"
)


print("\n===== TEST 4: NAT GATEWAY =====")
nat = ec2.describe_nat_gateways(
    NatGatewayIds=[nat_gateway_id]
)["NatGateways"][0]

check(nat["State"] == "available", "NAT Gateway is available")
check(nat["SubnetId"] == public_subnet_id, "NAT Gateway is placed in public subnet")


print("\n===== TEST 5: ROUTE TABLES =====")
public_rt = ec2.describe_route_tables(
    RouteTableIds=[public_route_table_id]
)["RouteTables"][0]

private_rt = ec2.describe_route_tables(
    RouteTableIds=[private_route_table_id]
)["RouteTables"][0]

public_has_igw_route = any(
    r.get("DestinationCidrBlock") == "0.0.0.0/0"
    and r.get("GatewayId") == igw_id
    for r in public_rt["Routes"]
)

private_has_nat_route = any(
    r.get("DestinationCidrBlock") == "0.0.0.0/0"
    and r.get("NatGatewayId") == nat_gateway_id
    for r in private_rt["Routes"]
)

public_assoc = any(
    a.get("SubnetId") == public_subnet_id
    for a in public_rt.get("Associations", [])
)

private_assoc = any(
    a.get("SubnetId") == private_subnet_id
    for a in private_rt.get("Associations", [])
)

check(public_has_igw_route, "Public route table routes 0.0.0.0/0 to Internet Gateway")
check(private_has_nat_route, "Private route table routes 0.0.0.0/0 to NAT Gateway")
check(public_assoc, "Public route table is associated with public subnet")
check(private_assoc, "Private route table is associated with private subnet")


print("\n===== TEST 6: SECURITY GROUPS =====")
sgs = ec2.describe_security_groups(
    GroupIds=[public_sg_id, private_sg_id]
)["SecurityGroups"]

public_sg = next(s for s in sgs if s["GroupId"] == public_sg_id)
private_sg = next(s for s in sgs if s["GroupId"] == private_sg_id)

public_ssh_rules = [
    p for p in public_sg["IpPermissions"]
    if p.get("IpProtocol") == "tcp"
    and p.get("FromPort") == 22
    and p.get("ToPort") == 22
    and len(p.get("IpRanges", [])) > 0
]

private_ssh_from_public_sg = [
    p for p in private_sg["IpPermissions"]
    if p.get("IpProtocol") == "tcp"
    and p.get("FromPort") == 22
    and p.get("ToPort") == 22
    and any(pair.get("GroupId") == public_sg_id for pair in p.get("UserIdGroupPairs", []))
]

check(len(public_ssh_rules) == 1, "Public EC2 SG allows SSH from specific IP")
check(len(private_ssh_from_public_sg) == 1, "Private EC2 SG allows SSH from Public EC2 SG only")


print("\n===== TEST 7: EC2 INSTANCES =====")
reservations = ec2.describe_instances(
    Filters=[
        {"Name": "vpc-id", "Values": [vpc_id]},
        {"Name": "instance-state-name", "Values": ["running"]}
    ]
)["Reservations"]

instances = []
for reservation in reservations:
    instances.extend(reservation["Instances"])

public_instances = [
    i for i in instances
    if i.get("PublicIpAddress") == public_ec2_public_ip
]

private_instances = [
    i for i in instances
    if i.get("PrivateIpAddress") == private_ec2_private_ip
]

check(len(public_instances) == 1, "Public EC2 is running")
check(len(private_instances) == 1, "Private EC2 is running")
check("PublicIpAddress" in public_instances[0], "Public EC2 has public IP")
check("PublicIpAddress" not in private_instances[0], "Private EC2 has no public IP")


print("\n===== ALL INFRASTRUCTURE TESTS PASSED! All components are correctly set up. =====")