# NT548 Lab01 - Terraform & CloudFormation AWS Infrastructure

## 1. Giới thiệu

**Lab 01 - Công nghệ DevOps và ứng dụng - NT548**.

Mục tiêu của bài lab là sử dụng **Terraform** và **AWS CloudFormation** để quản lý và triển khai tự động hạ tầng AWS theo mô hình public/private subnet.

Hạ tầng được triển khai gồm:

- VPC
- Public Subnet
- Private Subnet
- Internet Gateway
- NAT Gateway
- Public Route Table
- Private Route Table
- Public EC2 Instance
- Private EC2 Instance
- Security Groups
- CloudFormation Stack
- Test cases kiểm tra hạ tầng bằng Python

---

## 2. Kiến trúc triển khai

Mô hình triển khai:

```text
Internet
   |
Internet Gateway
   |
Public Route Table
   |
Public Subnet
   |---- Public EC2 / Bastion Host
   |---- NAT Gateway
              |
Private Route Table
              |
Private Subnet
   |---- Private EC2
```

Luồng hoạt động:

```text
Máy cá nhân -> SSH -> Public EC2
Máy cá nhân -> Public EC2 -> SSH -> Private EC2
Private EC2 -> NAT Gateway -> Internet Gateway -> Internet
```

Public EC2 có public IP và cho phép SSH từ IP cá nhân.  
Private EC2 không có public IP và chỉ cho phép SSH từ Public EC2 Security Group.

---

## 3. Cấu trúc thư mục

```text
NT548_Lab01/
├── .gitignore
├── README.md
├── cloudformation/
│   └── infrastructure.yaml
├── terraform/
│   ├── main.tf
│   ├── outputs.tf
│   ├── provider.tf
│   ├── terraform.tfvars.example
│   ├── variables.tf
│   └── modules/
│       ├── ec2/
│       │   ├── main.tf
│       │   ├── outputs.tf
│       │   └── variables.tf
│       ├── route_table/
│       │   ├── main.tf
│       │   ├── outputs.tf
│       │   └── variables.tf
│       ├── security_group/
│       │   ├── main.tf
│       │   ├── outputs.tf
│       │   └── variables.tf
│       ├── subnet/
│       │   ├── main.tf
│       │   ├── outputs.tf
│       │   └── variables.tf
│       └── vpc/
│           ├── main.tf
│           ├── outputs.tf
│           └── variables.tf
└── tests/
    └── test_infra.py
```

---

## 4. Yêu cầu cài đặt

Trước khi chạy mã nguồn, cần cài đặt:

### 4.1. AWS CLI

Kiểm tra:

```powershell
aws --version
```

Cấu hình AWS credentials:

```powershell
aws configure
```

Nhập các thông tin:

```text
AWS Access Key ID
AWS Secret Access Key
Default region name
Default output format
```

Kiểm tra tài khoản AWS hiện tại:

```powershell
aws sts get-caller-identity
```

---

### 4.2. Terraform

Kiểm tra:

```powershell
terraform -version
```

---

### 4.3. Python

Kiểm tra:

```powershell
python --version
```

Cài thư viện dùng cho test:

```powershell
pip install boto3
```

---

### 4.4. SSH Key

Tạo SSH key nếu chưa có:

```powershell
ssh-keygen -t rsa -b 4096 -f C:\Users\ADMIN\.ssh\nt548-lab01-key
```

Sau khi tạo, cần có hai file:

```text
C:\Users\ADMIN\.ssh\nt548-lab01-key
C:\Users\ADMIN\.ssh\nt548-lab01-key.pub
```

Trong đó:

- `nt548-lab01-key` là private key, dùng để SSH.
- `nt548-lab01-key.pub` là public key, được Terraform dùng để tạo AWS Key Pair.

---

## 5. Cấu hình Terraform

Vào thư mục Terraform:

```powershell
cd terraform
```

Tạo file biến từ file mẫu:

```powershell
copy terraform.tfvars.example terraform.tfvars
```

Mở file cấu hình:

```powershell
notepad terraform.tfvars
```

Nội dung mẫu:

```hcl
aws_region = "us-east-1"

project_name = "nt548-lab01"

vpc_cidr = "10.10.0.0/16"

public_subnet_cidr = "10.10.1.0/24"

private_subnet_cidr = "10.10.2.0/24"

my_ip = "YOUR_PUBLIC_IP/32"

public_key_path = "C:/Users/ADMIN/.ssh/nt548-lab01-key.pub"
```

Lấy IP public hiện tại:

```powershell
curl ifconfig.me
```

Hoặc:

```powershell
curl https://checkip.amazonaws.com
```

Ví dụ nếu IP là `171.250.164.182`, cấu hình:

```hcl
my_ip = "171.250.164.182/32"
```

---

## 6. Triển khai hạ tầng bằng Terraform

Trong thư mục `terraform`, chạy lần lượt:

```powershell
terraform init
```

```powershell
terraform fmt -recursive
```

```powershell
terraform validate
```

```powershell
terraform plan
```

```powershell
terraform apply
```

Khi Terraform hỏi xác nhận:

```text
Do you want to perform these actions?
```

Nhập:

```text
yes
```

Sau khi triển khai xong, xem output:

```powershell
terraform output
```

Một số output quan trọng:

```text
vpc_id
public_subnet_id
private_subnet_id
igw_id
nat_gateway_id
public_route_table_id
private_route_table_id
public_sg_id
private_sg_id
public_ec2_public_ip
public_ec2_private_ip
private_ec2_private_ip
```

Lấy riêng public IP của Public EC2:

```powershell
terraform output -raw public_ec2_public_ip
```

Lấy private IP của Private EC2:

```powershell
terraform output -raw private_ec2_private_ip
```

---

## 7. Kiểm thử hạ tầng bằng Python

Sau khi Terraform apply thành công, quay lại thư mục gốc project:

```powershell
cd ..
```

Vào thư mục test:

```powershell
cd tests
```

Cài thư viện nếu chưa có:

```powershell
pip install boto3
```

Chạy test:

```powershell
python test_infra.py
```

Kết quả mong đợi:

```text
===== TEST 1: VPC =====
[PASS] VPC exists and is available
[PASS] VPC has CIDR block

===== TEST 2: SUBNETS =====
[PASS] Public subnet belongs to VPC
[PASS] Private subnet belongs to VPC
[PASS] Public subnet maps public IP on launch
[PASS] Private subnet does not map public IP on launch

===== TEST 3: INTERNET GATEWAY =====
[PASS] Internet Gateway has attachment
[PASS] Internet Gateway is attached to VPC

===== TEST 4: NAT GATEWAY =====
[PASS] NAT Gateway is available
[PASS] NAT Gateway is placed in public subnet

===== TEST 5: ROUTE TABLES =====
[PASS] Public route table routes 0.0.0.0/0 to Internet Gateway
[PASS] Private route table routes 0.0.0.0/0 to NAT Gateway
[PASS] Public route table is associated with public subnet
[PASS] Private route table is associated with private subnet

===== TEST 6: SECURITY GROUPS =====
[PASS] Public EC2 SG allows SSH from specific IP
[PASS] Private EC2 SG allows SSH from Public EC2 SG only

===== TEST 7: EC2 INSTANCES =====
[PASS] Public EC2 is running
[PASS] Private EC2 is running
[PASS] Public EC2 has public IP
[PASS] Private EC2 has no public IP

===== ALL INFRASTRUCTURE TESTS PASSED =====
```

Các test này kiểm tra:

- VPC đã được tạo và available.
- Public/private subnet thuộc đúng VPC.
- Internet Gateway đã attach vào VPC.
- NAT Gateway ở trạng thái available.
- Route table định tuyến đúng.
- Security Group cấu hình đúng.
- Public EC2 và Private EC2 đang running.

---

## 8. SSH vào Public EC2

Lấy public IP:

```powershell
cd terraform
terraform output -raw public_ec2_public_ip
```

SSH vào Public EC2:

```powershell
ssh -i C:\Users\ADMIN\.ssh\nt548-lab01-key ec2-user@PUBLIC_EC2_PUBLIC_IP
```

Ví dụ:

```powershell
ssh -i C:\Users\ADMIN\.ssh\nt548-lab01-key ec2-user@32.197.189.0
```

Nếu thành công, terminal sẽ hiển thị:

```text
[ec2-user@ip-10-10-1-xxx ~]$
```

Điều này chứng minh Public EC2 có thể truy cập từ Internet thông qua SSH.

---

## 9. SSH vào Private EC2 thông qua Public EC2

Private EC2 không có public IP, vì vậy không thể SSH trực tiếp từ Internet.

Lấy private IP:

```powershell
terraform output -raw private_ec2_private_ip
```

SSH vào Private EC2 thông qua Public EC2 bằng ProxyJump:

```powershell
ssh -i C:\Users\ADMIN\.ssh\nt548-lab01-key `
  -o IdentitiesOnly=yes `
  -J ec2-user@PUBLIC_EC2_PUBLIC_IP `
  ec2-user@PRIVATE_EC2_PRIVATE_IP
```

Ví dụ:

```powershell
ssh -i C:\Users\ADMIN\.ssh\nt548-lab01-key `
  -o IdentitiesOnly=yes `
  -J ec2-user@32.197.189.0 `
  ec2-user@10.10.2.173
```

Nếu thành công:

```text
[ec2-user@ip-10-10-2-xxx ~]$
```

Điều này chứng minh Private EC2 chỉ có thể truy cập thông qua Public EC2/Bastion Host.

---

## 10. Kiểm tra Private EC2 truy cập Internet qua NAT Gateway

Sau khi SSH vào Private EC2, chạy:

```bash
curl https://checkip.amazonaws.com
```

Nếu lệnh trả về một địa chỉ IP public, nghĩa là Private EC2 đã truy cập Internet thành công thông qua NAT Gateway.

Có thể kiểm tra thêm:

```bash
sudo dnf update -y
```

Ý nghĩa:

- Private EC2 không có public IP.
- Private EC2 không bị truy cập trực tiếp từ Internet.
- Private EC2 vẫn có thể truy cập Internet outbound thông qua NAT Gateway.

---

## 11. Triển khai bằng CloudFormation

Ngoài Terraform, project có file CloudFormation:

```text
cloudformation/infrastructure.yaml
```

Từ thư mục gốc project, chạy:

```powershell
aws cloudformation create-stack `
  --stack-name nt548-lab01-cfn `
  --template-body file://cloudformation/infrastructure.yaml `
  --parameters `
    ParameterKey=ProjectName,ParameterValue=nt548-lab01-cfn `
    ParameterKey=MyIP,ParameterValue=YOUR_PUBLIC_IP/32 `
    ParameterKey=KeyName,ParameterValue=nt548-lab01-key `
  --region us-east-1
```

Chờ stack tạo xong:

```powershell
aws cloudformation wait stack-create-complete `
  --stack-name nt548-lab01-cfn `
  --region us-east-1
```

Xem thông tin stack:

```powershell
aws cloudformation describe-stacks `
  --stack-name nt548-lab01-cfn `
  --region us-east-1
```

Xem output:

```powershell
aws cloudformation describe-stacks `
  --stack-name nt548-lab01-cfn `
  --region us-east-1 `
  --query "Stacks[0].Outputs"
```

Nếu stack ở trạng thái `CREATE_COMPLETE`, CloudFormation đã triển khai hạ tầng thành công.

---

## 12. Xóa tài nguyên để tránh phát sinh chi phí

### 12.1. Xóa tài nguyên Terraform

Trong thư mục `terraform`, chạy:

```powershell
terraform destroy
```

Nhập:

```text
yes
```

### 12.2. Xóa CloudFormation Stack

```powershell
aws cloudformation delete-stack `
  --stack-name nt548-lab01-cfn `
  --region us-east-1
```

Kiểm tra stack đã xóa:

```powershell
aws cloudformation describe-stacks `
  --stack-name nt548-lab01-cfn `
  --region us-east-1
```

---
## 13. Kết luận

Project đã triển khai thành công hạ tầng AWS bằng Terraform và CloudFormation.

Terraform được tổ chức theo module, giúp dễ quản lý và tái sử dụng. CloudFormation template được xây dựng để triển khai hạ tầng tương đương. Bộ test Python kiểm tra được từng dịch vụ chính, bao gồm VPC, Subnet, Internet Gateway, NAT Gateway, Route Tables, Security Groups và EC2 instances.

Mô hình đảm bảo yêu cầu bảo mật:

- Public EC2 chỉ cho phép SSH từ IP người dùng.
- Private EC2 không có public IP.
- Private EC2 chỉ cho phép SSH từ Public EC2 Security Group.
- Private EC2 truy cập Internet outbound thông qua NAT Gateway.