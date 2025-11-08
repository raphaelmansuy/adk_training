# IT Security Policy

## Purpose

This policy establishes guidelines for information security, data protection, and
secure computing practices within our organization.

## Scope

This policy applies to all employees, contractors, vendors, and any individual with
access to company information systems or data.

---

## 1. Information Classification

### Classification Levels

All company information must be classified into one of the following categories:

**Public**: Information that can be freely shared externally without risk
- Marketing materials
- Public website content
- Published documents

**Internal**: Information that should only be accessed by employees
- Internal communications
- General policies
- Non-sensitive business documents

**Confidential**: Sensitive information requiring restricted access
- Financial data
- Employee personal information
- Strategic plans
- Client information

**Restricted**: Highly sensitive information with limited access
- Passwords and authentication credentials
- Encryption keys
- Legal documents
- Trade secrets

---

## 2. Access Control

### Authentication Requirements

- All system access requires unique username and password
- Default passwords must be changed immediately upon first login
- Multi-factor authentication (MFA) is required for:
  - Remote access
  - Administrative accounts
  - Email systems
  - Cloud services

### Password Policy

- Minimum 12 characters
- Must contain uppercase, lowercase, numbers, and special characters
- Must not contain username or dictionary words
- Must be changed every 90 days
- Previous 5 passwords cannot be reused
- Accounts will be locked after 5 failed login attempts
- Never share passwords with anyone, including IT staff

### Access Provisioning

- All system access must be requested through the IT helpdesk
- Manager approval is required for all access requests
- Access must follow the principle of least privilege
- Access reviews will be conducted quarterly
- Terminated employees' access will be revoked immediately

---

## 3. Data Protection

### Data Backup

- Critical data must be backed up daily
- Backup integrity will be tested monthly
- Backup recovery procedures must be documented
- Off-site backup copies must be maintained

### Encryption

- Sensitive data must be encrypted both in transit and at rest
- File-level encryption is required for:
  - Documents containing confidential information
  - Employee data
  - Financial records
  - Client data

- Encryption protocols:
  - TLS 1.2 or higher for data in transit
  - AES-256 for data at rest

### Data Retention and Disposal

- Data must be retained according to legal and business requirements
- Data must be securely destroyed when no longer needed
- Destruction methods must render data unrecoverable
- Certificates of destruction must be maintained

---

## 4. Endpoint Security

### Workstation Requirements

All company workstations must have:

- Current operating system with latest security updates
- Antivirus and anti-malware software
- Firewall enabled and properly configured
- Hard drive encryption enabled
- Regular security patches applied within 30 days of release
- BIOS/UEFI password protection

### Mobile Device Security

- Mobile devices accessing company data must have:
  - Screen lock enabled
  - Device encryption enabled
  - Mobile device management (MDM) software installed
  - Automatic lock after 15 minutes of inactivity
  - Lost device reporting procedures in place

### USB and Removable Media

- Removable media is prohibited unless specifically approved
- Approved removable media must be encrypted
- Personal devices may not be connected to company networks

---

## 5. Network Security

### Wireless Networks

- Only authorized wireless networks may be used
- WPA2 or WPA3 encryption is required for all wireless networks
- Public WiFi networks should not be used for company work
- VPN must be used when connecting from public networks

### Firewall Requirements

- All network traffic must pass through company firewall
- Unnecessary ports must be closed
- Inbound traffic must be restricted to necessary services only
- Firewall rules must be reviewed quarterly

### VPN Requirements

- VPN must be used for all remote access
- VPN clients must have current certificates
- VPN logs must be maintained for at least 90 days
- VPN access is restricted to approved users and devices

---

## 6. Software and Systems

### Approved Software Only

- Only company-approved software may be installed on workstations
- Personal software, freeware, and open-source software must be approved by IT
- Unauthorized software must be removed immediately
- Software licensing must be tracked and documented

### Security Updates

- Security patches must be applied within 30 days of release
- Critical security patches must be applied within 7 days
- Patch management will be centrally coordinated by IT
- Testing of patches will occur on non-production systems first

### Vulnerability Management

- Annual vulnerability assessments will be conducted
- Critical vulnerabilities must be remediated within 7 days
- High-risk vulnerabilities must be remediated within 30 days
- Scan results and remediation efforts will be documented

---

## 7. Third-Party and Vendor Management

### Vendor Requirements

All vendors with access to company systems or data must:

- Sign a security agreement
- Provide evidence of security practices
- Comply with this security policy
- Undergo security assessments as required
- Maintain liability insurance

### Contractor Responsibilities

Contractors must:

- Sign an NDA before accessing any company information
- Comply with all policies in this document
- Use only company-provided equipment
- Return all equipment and data upon termination
- Not disclose company information to third parties

---

## 8. Incident Response

### Reporting Security Incidents

All security incidents, suspicious activity, or policy violations must be reported
immediately to IT Security at security@company.com or ext. 5555.

### Incident Classification

- **Critical**: Confirmed data breach, ransomware, large-scale attack
- **High**: Unauthorized access, malware infection, policy violation
- **Medium**: Failed login attempts, misconfiguration, phishing attempt
- **Low**: Informational, policy questions, minor issues

### Response Procedures

1. Immediately disconnect affected systems from network
2. Preserve evidence (logs, screenshots, memory)
3. Notify IT Security team
4. Do not attempt to repair or restore without authorization
5. Cooperate fully with investigation
6. Follow investigation team's instructions

### Breach Notification

If a data breach occurs:

- Affected individuals will be notified within 48 hours
- Regulatory agencies will be notified as required by law
- A detailed breach report will be prepared
- Remediation steps will be implemented

---

## 9. Acceptable Use

### Permitted Uses

Company resources are provided for business purposes. Limited personal use is permitted if it:

- Does not interfere with job duties
- Does not violate this policy or laws
- Does not consume significant resources
- Is not offensive or harassing in nature

### Prohibited Uses

Employees may not use company resources to:

- Access or distribute inappropriate or illegal material
- Conduct personal business or generate income
- Harass, threaten, or discriminate against anyone
- Access personal social media during work hours
- Play games or access entertainment sites
- Conduct activities that violate laws

### Monitoring and Privacy

Employees should have no expectation of privacy when using company systems.
The company may monitor:

- Email messages and attachments
- Web browsing activity
- File access and transfers
- USB device connections
- Application usage
- Network traffic

---

## 10. Security Awareness

### Training Requirements

- All employees must complete security training within 30 days of hire
- Annual security refresher training is mandatory
- Department-specific training may be required
- Training completion will be tracked

### Phishing Awareness

- Do not click links from unknown senders
- Do not download unexpected attachments
- Verify sender email addresses carefully
- Report suspicious emails to IT Security
- Be especially cautious with emails requesting passwords or sensitive data

---

## 11. Remote Work Security

Remote workers must:

- Use VPN for all network access
- Use personal devices only if approved by IT
- Maintain physical security of company equipment
- Use secure WiFi networks (not public WiFi)
- Lock computers when away from desk
- Not discuss confidential information in public
- Report lost or stolen devices immediately

---

## 12. Enforcement

### Violations

Violations of this security policy may result in:

- Disciplinary action up to and including termination
- Legal action for theft or fraud
- Financial penalties
- Loss of system access privileges
- Criminal charges for serious violations

### Reporting Violations

To report suspected policy violations, contact:

- Your manager
- Human Resources
- IT Security: security@company.com
- Anonymous hotline: 1-800-REPORT-POLICY

---

## 13. Policy Review

This policy will be reviewed annually and updated as needed to reflect:

- Changes in technology
- New security threats
- Organizational changes
- Regulatory requirements
- Industry best practices

---

**Last Updated**: November 2025  
**Next Review**: November 2026

This policy is not a contract. The company reserves the right to modify this
policy at any time. All employees will be notified of significant changes.

For questions, contact: IT Security Department  
Email: security@company.com
