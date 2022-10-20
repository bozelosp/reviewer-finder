# reviewer-finder
---
# Milvus SDK Installation
## Dependencies
- Terraform
- Ansible (Linux only, use WSL on Windows)
- pymilvus
## Installation
- [Install Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)
- [Install Ansible](https://www.techrepublic.com/article/how-to-install-ansible-on-ubuntu-server-18-04/#:~:text=ready%20to%20install.-,Installing%20Ansible,-Next%2C%20install%20Ansible)
- Install pymilvus
  - Create new venv `python == 3.9.13`
  - *On Windows:* [Install Visual Studio Build Tools](https://www.microsoft.com/en-us/download/confirmation.aspx?id=48159)
  - *On Windows:* Using Visual Studio Build Tools install: *Windows 10 SDK, Windows Universl CRT SDK, MSVC v140 - VS 2015 C++ build tools, NuGet target and build tasks, .NET Framework 4.6 targeting pack, Visual Studio SDK Build Tools Core*
  - [Install pymilvus with pip3](https://pypi.org/project/pymilvus/) (If you think your python version will do and you have C++ build tools installed, try this step first)
---
# Milvus cluster deployment
## Terraform - Cloud infrastructure
- Navigate to terraform folder
- Configure Terraform Variables
  - Provide your credentials as `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables
  - Configure settings variables in `terraform.tfvars` to your liking (you can find description of variables in `variables.tf`)
- Run `terraform init` - download AWS API
- Run `terraform apply` - create AWS resources
- Write down Terraform output - `proxy_ips_private, proxy_ips_public, server_ips_public`
## Ansible - Application infrastructure
- Navigate to ansible folder
- Configure `inventory.ini`
  -  `ansible_host` = public ip's for next variables: `proxy, main-1, main-2`
  -  Provide private ip to all variables in `proxy containers` section
- Run `ansible-playbook ping.yml` - check if hosts are available
- Run `ansible-playbook deploy-docker.yml` - install docker on hosts
- Run `ansible-playbook deploy-milvus.yml` - download and start docker containers
## pymilvus - create collection, search, drop collection
- Navigate to python folder
- Configure `settings.json`
  - `proxy_ip` = `proxy_ips_public`
  - Leave the rest untouched, already configured for 10 million
- Activate venv created for pymilvus
- Run `rewrite-pkl.py` - process dicts with non normalized vectors
  - Reads `data/query_embeddings.pkl`, writes normalised vectors as list to `data/query_embeddings_list.pkl`
  - Reads `data/article_id_to_emb_dict_*.pkl`, writes `data/entries/article_vector_list_*_part_i.pkl`
- Run `connect-remote.py` - connect to Milvus proxy and show existing collections
- Run `create-collection.py` - create collection configured in `settings.json`. Takes ~ 120 minutes to upload 10 million vectors and 5 more hours to create index
- Run `load-collection.py` - load collection to RAM
- Run `query.py` - load vectors from `data/query_embeddings_list.pkl` and perform search.
## Making changes to Cluster
### Change instances types to reduce cost:
- Navigate to Terraform folder
  - Change `terraform.tfvars`
  - Run `terraform apply`
  - Run `terraform refresh`
  - Write down Terraform output - `proxy_ips_private, proxy_ips_public, server_ips_public`
- Navigate to Ancible folder
  - Configure `inventory.ini`
  - Run `ansible-playbook deploy-milvus.yml`
- Navigate to python folder
  - Configure `settings.json`
  - Run `load-collection.py`
### Adding data to collection
- Navigate to python folder
- Prepare data as nested list: `[[articles_id], [vectors]]` and store in `.pkl` file
- Configure variable `filenames` in `update-collection.py` to point at `.pkl` file
- Run `update-collection.py`
