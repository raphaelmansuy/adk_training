# Tutorial 23 Quick Reference Card

**Print this or bookmark for quick access!**

---

## 🚀 Quick Start (Choose Your Path)

### 1. **I want to deploy NOW** ⚡
```bash
# 5 minutes to production
adk deploy cloud_run --project YOUR_PROJECT --region us-central1
```
👉 Then: Read [DEPLOYMENT_CHECKLIST.md](tutorial_implementation/tutorial23/DEPLOYMENT_CHECKLIST.md)

### 2. **I need compliance (FedRAMP)** 🔐
```bash
# Agent Engine for compliance
adk deploy agent_engine --project YOUR_PROJECT --region us-central1
```
👉 Then: Read [SECURITY_VERIFICATION.md](tutorial_implementation/tutorial23/SECURITY_VERIFICATION.md)

### 3. **I have Kubernetes** ⚙️
```bash
# Deploy to GKE
adk deploy gke
kubectl apply -f deployment.yaml
```
👉 Then: See MIGRATION_GUIDE.md for safe deployment

### 4. **I need custom authentication** 🔑
```bash
# Use Tutorial 23 patterns + Cloud Run
cd tutorial_implementation/tutorial23
make demo
```
👉 Then: Follow DEPLOYMENT_CHECKLIST.md

### 5. **I'm just learning** 📚
```bash
# Run locally first
adk api_server --port 8080
```
👉 Then: Read docs/tutorial/23_production_deployment.md

---

## 💰 Quick Cost Reference

| Platform | Cost/Month | Setup Time | Best For |
|----------|-----------|-----------|----------|
| **Local** | $0 | <1 min | Learning |
| **Cloud Run** | $40-50 | 5 min | ✅ Most production apps |
| **Agent Engine** | ~$527 | 10 min | Compliance (FedRAMP) |
| **GKE** | $200-500+ | 20+ min | Advanced control |

---

## 📋 Pre-Deployment Checklist

Before you deploy anywhere:

- [ ] Environment variables configured
- [ ] Secrets in Secret Manager (not in code!)
- [ ] API keys rotated
- [ ] Health endpoint working locally
- [ ] Logs configured
- [ ] Monitoring alerts setup

**Full checklist**: [DEPLOYMENT_CHECKLIST.md](tutorial_implementation/tutorial23/DEPLOYMENT_CHECKLIST.md)

---

## 🔐 Post-Deployment Verification

After you deploy:

1. **Test it works**
   ```bash
   curl $SERVICE_URL/health
   ```

2. **Verify it's secure**
   ```bash
   # See SECURITY_VERIFICATION.md for platform-specific checks
   ```

3. **Check logs**
   ```bash
   gcloud logging read "resource.service.name=agent" --limit 10
   ```

4. **Monitor metrics** (Cloud Logging dashboard)

---

## 🔄 Moving Between Platforms?

**Complete guide**: [MIGRATION_GUIDE.md](tutorial_implementation/tutorial23/MIGRATION_GUIDE.md)

**Common paths**:
- Local → Cloud Run (15 min)
- Cloud Run → Agent Engine (30 min)
- Cloud Run → GKE (60 min)
- GKE → Cloud Run (15 min)

---

## 💡 Common Questions Answered

**Q: Which platform should I choose?**  
A: Read the [decision framework](docs/tutorial/23_production_deployment.md#-decision-framework-choose-your-platform) in the main tutorial.

**Q: Is the built-in server secure?**  
A: Yes - security is handled by the platform (Cloud Run, Agent Engine, GKE). Read [SECURITY_RESEARCH_SUMMARY.md](SECURITY_RESEARCH_SUMMARY.md).

**Q: How much will it cost?**  
A: Typically $40-50/month for small-medium apps on Cloud Run. See [COST_BREAKDOWN.md](tutorial_implementation/tutorial23/COST_BREAKDOWN.md) for details.

**Q: Can I migrate later?**  
A: Yes! Your agent code stays the same. See [MIGRATION_GUIDE.md](tutorial_implementation/tutorial23/MIGRATION_GUIDE.md).

**Q: When do I need a custom server?**  
A: Only if you need custom authentication or very specific patterns. For most users: use Cloud Run + IAM.

---

## 📚 Document Navigator

| Document | Purpose | Reading Time |
|----------|---------|--------------|
| [Main Tutorial](docs/tutorial/23_production_deployment.md) | Overview of all platforms | 15-20 min |
| [Decision Framework](docs/tutorial/23_production_deployment.md#-decision-framework) | Choose your platform | 2 min |
| [SECURITY_VERIFICATION.md](tutorial_implementation/tutorial23/SECURITY_VERIFICATION.md) | Verify your deployment is secure | 10 min |
| [DEPLOYMENT_CHECKLIST.md](tutorial_implementation/tutorial23/DEPLOYMENT_CHECKLIST.md) | Step-by-step verification | 20 min |
| [MIGRATION_GUIDE.md](tutorial_implementation/tutorial23/MIGRATION_GUIDE.md) | Move between platforms | 30 min |
| [COST_BREAKDOWN.md](tutorial_implementation/tutorial23/COST_BREAKDOWN.md) | Budget planning | 15 min |

---

## 🧪 Test Your Setup

```bash
# Run all tests
cd tutorial_implementation/tutorial23
make test

# Run specific test
pytest tests/test_agent.py -v

# Check coverage
pytest tests/ --cov=production_agent
```

**Expected result**: 40/40 tests passing ✅

---

## 🆘 Troubleshooting

**Problem**: Can't access deployed service  
**Solution**: Check SECURITY_VERIFICATION.md → "Issue: Unauthenticated access allowed"

**Problem**: Deployed but no traffic showing up  
**Solution**: Check DEPLOYMENT_CHECKLIST.md → "Post-deployment verification"

**Problem**: Want to switch platforms  
**Solution**: See MIGRATION_GUIDE.md for your migration path

**Problem**: Worried about security  
**Solution**: Read SECURITY_RESEARCH_SUMMARY.md, then follow SECURITY_VERIFICATION.md

---

## 🔗 All Resources

### Getting Started
- 🎯 [Main Tutorial](docs/tutorial/23_production_deployment.md)
- 📖 [README](tutorial_implementation/tutorial23/README.md)

### Deployment & Verification
- ✅ [Deployment Checklist](tutorial_implementation/tutorial23/DEPLOYMENT_CHECKLIST.md)
- 🔐 [Security Verification](tutorial_implementation/tutorial23/SECURITY_VERIFICATION.md)

### Planning & Migration
- 💰 [Cost Breakdown](tutorial_implementation/tutorial23/COST_BREAKDOWN.md)
- 🔄 [Migration Guide](tutorial_implementation/tutorial23/MIGRATION_GUIDE.md)

### Security & Best Practices
- 📋 [Security Research Summary](SECURITY_RESEARCH_SUMMARY.md)
- 🔍 [Detailed Security Analysis](SECURITY_ANALYSIS_ALL_DEPLOYMENT_OPTIONS.md)
- 📖 [FastAPI Best Practices](tutorial_implementation/tutorial23/FASTAPI_BEST_PRACTICES.md)

### Implementation
- 💻 [Code](tutorial_implementation/tutorial23/)
- 🧪 [Tests](tutorial_implementation/tutorial23/tests/)

---

## ⏱️ Time Estimates

| Task | Time | Difficulty |
|------|------|------------|
| Read decision framework | 2 min | Easy |
| Deploy to Cloud Run | 5 min | Easy |
| Deploy to Agent Engine | 10 min | Easy |
| Deploy to GKE | 20+ min | Medium |
| Security verification | 10 min | Easy |
| Budget planning | 10 min | Easy |
| Platform migration | 15-60 min | Medium |

---

## ✅ Success Indicators

**You're ready for production when**:
- ✅ Deployment checklist is complete
- ✅ Health endpoint responding
- ✅ Logs appearing in Cloud Logging
- ✅ Security verification passed
- ✅ Monitoring/alerts configured
- ✅ Cost monitoring set up

---

**Need help?** Check the appropriate guide above or re-read the [main tutorial](docs/tutorial/23_production_deployment.md).

**Found an issue?** The tutorial is tested (40/40 tests passing) - if something doesn't work, check TROUBLESHOOTING section.

**Ready to deploy?** Pick your platform from the quick start above! 🚀
