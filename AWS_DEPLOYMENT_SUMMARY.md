# AWS Deployment Summary

## What You Have

✅ **S3 Bucket**: `ashoka-ai1-s3` with folder `all_data/` in `us-east-1`  
✅ **DynamoDB Table**: `ashoka_contentint` in `us-east-1`
✅ **Application Code**: Ready for deployment

---

## What You Need

### 1. EC2 Instance - YES, YOU NEED THIS! ✓

**Why?** Your NiceGUI application needs a server to run 24/7. EC2 provides this.

**Recommended Configuration:**
- **Instance Type**: t3.medium (2 vCPU, 4 GB RAM)
- **OS**: Ubuntu 22.04 LTS
- **Storage**: 20 GB
- **Region**: us-east-1 (same as your S3 and RDS)
- **Cost**: ~$30/month (or ~$20/month with Reserved Instance)

### 2. DynamoDB Table

Your DynamoDB table:
- **Table name**: `ashoka_contentint`
- **Region**: `us-east-1`
- **Purpose**: Stores user data, content metadata, and application state

---

## Deployment Architecture

```
Internet
   ↓
[Route 53 / Domain] (optional)
   ↓
[EC2 Instance]
   ├── Nginx (Port 80/443) → Reverse Proxy
   ├── NiceGUI App (Port 8080) → Your Dashboard
   ├── Supervisor → Keeps app running
   └── Python Environment
Internet
   ↓
[Route 53 / Domain] (optional)
   ↓
[EC2 Instance]
   ├── Nginx (Port 80/443) → Reverse Proxy
   ├── NiceGUI App (Port 8080) → Your Dashboard
   ├── Supervisor → Keeps app running
   └── Python Environment
       ↓
       ├── → S3 Bucket (ashoka-ai1-s3/all_data/)
       └── → DynamoDB Table (ashoka_contentint)ployment guide
- ✅ `AWS_DEPLOYMENT_SUMMARY.md` - This file

### 2. Code Files
- ✅ `src/database/rds_connection.py` - RDS database connection module
- ✅ `.env.production.example` - Production environment template

### 3. Deployment Scripts
- ✅ `deployment_scripts/setup_ec2.sh` - EC2 initial setup
- ✅ `deployment_scripts/supervisor_ashoka.conf` - Process manager config
- ✅ `deployment_scripts/nginx_ashoka.conf` - Web server config
- ✅ `deployment_scripts/deploy.sh` - Automated deployment script

- ✅ `src/database/dynamodb_connection.py` - DynamoDB connection module
- ✅ `requirements.txt` - Added PostgreSQL and MySQL drivers

---

## Step-by-Step Deployment (30 Minutes)

### Phase 1: AWS Setup (10 min)

1. **Launch EC2 Instance**
   - Go to AWS Console → EC2 → Launch Instance
   - Choose Ubuntu 22.04, t3.medium
   - Configure security group (ports 22, 80, 443, 8080)
   - Download key pair (.pem file)

2. **Get RDS Details**
   - Go to AWS Console → RDS
   - Find your database endpoint
   - Note down username, password, database name

3. **Verify S3 Access**
   - Go to AWS Console → S3
   - Confirm bucket `ashoka-ai1-s3all_data` exists

### Phase 2: EC2 Setup (10 min)

```bash
# 1. SSH into EC2
ssh -i your-key.pem ubuntu@your-ec2-ip

# 2. Run setup script
   - Confirm bucket `ashoka-ai1-s3` with folder `all_data/` existseployment_scripts/setup_ec2.sh
chmod +x setup_ec2.sh
./setup_ec2.sh

# 3. Configure AWS
aws configure
# Enter: Access Key, Secret Key, us-east-1, json
```

### Phase 3: Deploy Application (10 min)

```bash
# 1. Upload code (from your local machine)
scp -i your-key.pem -r /path/to/ashoka ubuntu@your-ec2-ip:/opt/ashoka/

# 2. Setup Python (on EC2)
cd /opt/ashoka
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Configure environment
cp .env.production.example .env
nano .env  # Fill in your values

# 4. Test connections
python3 -c "from src.database.rds_connection import test_connection; test_connection()"

# 5. Create database tables
python3 -c "from src.database.rds_connection import create_tables; create_tables()"

# 6. Start application
sudo cp deployment_scripts/supervisor_ashoka.conf /etc/supervisor/conf.d/
sudo supervisorctl reread && sudo supervisorctl update
sudo supervisorctl start ashoka

# 7. Setup Nginx
sudo cp deployment_scripts/nginx_ashoka.conf /etc/nginx/sites-available/ashoka
sudo ln -s /etc/nginx/sites-available/ashoka /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl restart nginx
```

---

## Access Your Live Application

🎉 **After deployment, access at:**

- **With Nginx**: `http://your-ec2-public-ip`
- **Direct**: `http://your-ec2-public-ip:8080`
- **With Domain**: `http://your-domain.com` (after DNS setup)

**Default Credentials:**
- Admin: `admin / admin123`
- Demo: `demo / demo123`

⚠️ **IMPORTANT**: Change these passwords immediately after first login!

---

## Key Differences: Local vs AWS

| Aspect | Local Development | AWS Production |
|--------|------------------|----------------|
| Database | DuckDB (file-based) | RDS (PostgreSQL/MySQL) |
| Storage | Local `data/` folder | S3 bucket |
| Access | localhost:8080 | Public IP or domain |
| Uptime | Only when you run it | 24/7 |
| Scalability | Single machine | Can scale up/out |
| Cost | Free | ~$50-60/month |

---

## Monitoring Your Application

### View Logs
```bash
# Application logs
sudo tail -f /var/log/ashoka/app.log

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Supervisor status
sudo supervisorctl status
```

### Restart Application
```bash
sudo supervisorctl restart ashoka
```

### Update Application
```bash
cd /opt/ashoka
git pull  # if using git
source venv/bin/activate
pip install -r requirements.txt
sudo supervisorctl restart ashoka
```

---

## Security Checklist

After deployment, ensure:

- [ ] Changed default admin password
- [ ] SSH restricted to your IP only
- [ ] RDS not publicly accessible
- [ ] S3 bucket has proper IAM policies
- [ ] SSL certificate installed (HTTPS)
- [ ] Environment variables secured
- [ ] Regular backups configured
- [ ] CloudWatch monitoring enabled

---

## Cost Breakdown

**Monthly Costs (Approximate):**

| Service | Configuration | Cost |
|---------|--------------|------|
| EC2 | t3.medium | $30 |
| RDS | db.t3.micro | $15 |
| S3 | 100 GB storage | $2.30 |
| Data Transfer | ~50 GB | $5 |
| **Total** | | **~$52/month** |

**Cost Optimization Tips:**
1. Use Reserved Instances (save 40%)
2. Use Spot Instances for dev/test
3. Enable S3 lifecycle policies
4. Use CloudWatch to monitor usage
5. Stop EC2 when not needed (dev only)

---

## Troubleshooting

### Application Won't Start
```bash
# Check logs
sudo tail -100 /var/log/ashoka/app.log

# Check supervisor
sudo supervisorctl status ashoka

# Restart
sudo supervisorctl restart ashoka
```

### Can't Connect to RDS
```bash
# Test connection
psql -h your-rds-endpoint -U username -d ashoka_contentint

# Check security group allows EC2 IP
# Check RDS is in same VPC or publicly accessible
```

### S3 Access Denied
```bash
# Test S3
aws s3 ls s3://ashoka-ai1-s3all_data/

# Check IAM role attached to EC2
# Check S3 bucket policy
```

### Port 8080 Not Accessible
```bash
# Check if app is running
aws s3 ls s3://ashoka-ai1-s3/all_data/

# Check if port is listening
sudo netstat -tulpn | grep 8080

# Check security group allows port 8080
```

---

## Next Steps After Deployment

1. **Setup SSL Certificate**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

2. **Configure Custom Domain**
   - Point your domain to EC2 Elastic IP
   - Update Nginx config with your domain

3. **Setup Automated Backups**
   - Enable RDS automated backups
   - Create S3 lifecycle policies
   - Setup database backup scripts

4. **Enable Monitoring**
   - Setup CloudWatch alarms
   - Configure SNS notifications
   - Monitor costs with AWS Budgets

5. **Implement CI/CD**
   - Setup GitHub Actions
   - Automate deployments
   - Add automated testing

---

## Support Resources

- **Detailed Guide**: See `AWS_DEPLOYMENT.md`
- **Quick Start**: See `QUICK_START_AWS.md`
- **AWS Documentation**: https://docs.aws.amazon.com/
- **NiceGUI Docs**: https://nicegui.io/documentation

---

## Questions?

Common questions answered:

**Q: Do I really need EC2?**  
A: Yes! Your NiceGUI app needs a server running 24/7. EC2 provides this.

**Q: Can I use Lambda instead?**  
A: Not easily. NiceGUI is designed for long-running servers, not serverless.

**Q: Why not just use my local machine?**  
A: Your local machine isn't accessible from the internet and won't run 24/7.

**Q: Can I use a cheaper instance?**  
A: Yes, t3.small works but may be slower. t3.micro is too small.

**Q: How do I get a domain name?**  
A: Register via Route 53, GoDaddy, Namecheap, etc. Point to your EC2 IP.

**Q: Is this production-ready?**  
A: Yes, but add SSL, monitoring, and backups for full production readiness.

---

**Ready to deploy? Start with `QUICK_START_AWS.md`!** 🚀
