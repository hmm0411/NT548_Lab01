module "vpc" {
  source = "./modules/vpc"

  vpc_cidr     = var.vpc_cidr
  project_name = var.project_name
}

module "subnet" {
  source = "./modules/subnet"

  vpc_id              = module.vpc.vpc_id
  public_subnet_cidr  = var.public_subnet_cidr
  private_subnet_cidr = var.private_subnet_cidr
  project_name        = var.project_name
}

module "route_table" {
  source = "./modules/route_table"

  vpc_id            = module.vpc.vpc_id
  public_subnet_id  = module.subnet.public_subnet_id
  private_subnet_id = module.subnet.private_subnet_id
  igw_id            = module.subnet.igw_id
  nat_gateway_id    = module.subnet.nat_gateway_id
  project_name      = var.project_name
}

module "security_group" {
  source = "./modules/security_group"

  vpc_id       = module.vpc.vpc_id
  my_ip        = var.my_ip
  project_name = var.project_name
}

module "ec2" {
  source = "./modules/ec2"

  project_name      = var.project_name
  public_subnet_id  = module.subnet.public_subnet_id
  private_subnet_id = module.subnet.private_subnet_id
  public_sg_id      = module.security_group.public_sg_id
  private_sg_id     = module.security_group.private_sg_id
  public_key_path   = var.public_key_path
}