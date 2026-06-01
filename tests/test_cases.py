import boto3
import paramiko
import subprocess

# ---------- Config ----------
region = "us-east-1"
vpc_id = "<VPC_ID>"
public_subnet_id = "<PUBLIC_SUBNET_ID>"
private_subnet_id = "<PRIVATE_SUBNET_ID>"
public_sg_id = "<PUBLIC_SG_ID>"
private_sg_id = "<PRIVATE_SG_ID>"
public_ec2_ip = "<PUBLIC_EC2_PUBLIC_IP>"
private_ec2_ip = "<PRIVATE_EC2_PRIVATE_IP>"
key_file = "/path/to/key.pem"
username = "ec2-user"
my_ip = "<YOUR_PUBLIC_IP>/32"
# ----------------------------

ec2 = boto3.client("ec2", region_name=region)

def print_header(title):
    print("\n" + "="*10 + f" {title} " + "="*10)

# ---------- VPC Test ----------
print_header("VPC Test")
vpcs = ec2.describe_vpcs(VpcIds=[vpc_id])
print("VPC exists:", len(vpcs['Vpcs']) == 1)

# ---------- Subnet Test ----------
print_header("Subnets Test")
subnets = ec2.describe_subnets(SubnetIds=[public_subnet_id, private_subnet_id])
for s in subnets['Subnets']:
    print(f"Subnet {s['SubnetId']} CIDR:", s['CidrBlock'], "MapPublicIP:", s.get("MapPublicIpOnLaunch", False))

# ---------- Internet Gateway Test ----------
print_header("IGW Test")
igws = ec2.describe_internet_gateways(Filters=[{"Name":"attachment.vpc-id","Values":[vpc_id]}])
print("IGW attached:", len(igws['InternetGateways']) > 0)

# ---------- NAT Gateway Test ----------
print_header("NAT Gateway Test")
nat_gateways = ec2.describe_nat_gateways(Filters=[{"Name":"vpc-id","Values":[vpc_id]}])
nat_available = any(n['State']=='available' for n in nat_gateways['NatGateways'])
print("NAT Gateway available:", nat_available)

# ---------- Route Table Test ----------
print_header("Route Tables Test")
route_tables = ec2.describe_route_tables(Filters=[{"Name":"vpc-id","Values":[vpc_id]}])
for rt in route_tables['RouteTables']:
    print("Route Table:", rt['RouteTableId'])
    for r in rt['Routes']:
        print("  Route:", r.get('DestinationCidrBlock'), "via", r.get('GatewayId') or r.get('NatGatewayId'))

# ---------- Security Groups Test ----------
print_header("Security Groups Test")
sgs = ec2.describe_security_groups(GroupIds=[public_sg_id, private_sg_id])
for sg in sgs['SecurityGroups']:
    print(f"SG {sg['GroupName']} Ingress:")
    for rule in sg['IpPermissions']:
        print(rule)

# ---------- SSH Test to Public EC2 ----------
print_header("SSH Public EC2 Test")
def ssh_test(host_ip):
    key = paramiko.RSAKey.from_private_key_file(key_file)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host_ip, username=username, pkey=key, timeout=10)
        stdin, stdout, stderr = ssh.exec_command("echo 'SSH OK'")
        print(stdout.read().decode())
        ssh.close()
        return True
    except Exception as e:
        print("SSH Failed:", e)
        return False

ssh_test(public_ec2_ip)

# ---------- SSH Test to Private EC2 via Public EC2 ----------
print_header("SSH Private EC2 via Bastion Test")
def ssh_private_via_bastion(private_ip):
    key = paramiko.RSAKey.from_private_key_file(key_file)
    bastion = paramiko.SSHClient()
    bastion.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    bastion.connect(public_ec2_ip, username=username, pkey=key)

    transport = bastion.get_transport()
    dest_addr = (private_ip, 22)
    local_addr = ("127.0.0.1", 0)
    channel = transport.open_channel("direct-tcpip", dest_addr, local_addr)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(private_ip, username=username, pkey=key, sock=channel)

    stdin, stdout, stderr = client.exec_command("echo 'SSH OK via Bastion'")
    print(stdout.read().decode())
    client.close()
    bastion.close()

ssh_private_via_bastion(private_ec2_ip)

# ---------- Internet Connectivity Test ----------
print_header("Internet Connectivity Test")
def ping_test(ip):
    result = subprocess.run(["ping", "-c", "2", ip], capture_output=True)
    print(f"Ping {ip}: Success" if result.returncode==0 else f"Ping {ip}: Failed")

ping_test(public_ec2_ip)
ping_test(private_ec2_ip)