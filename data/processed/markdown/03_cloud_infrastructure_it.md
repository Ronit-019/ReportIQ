
<!-- PDF_PAGE: 1 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

# **NEXORA TECHNOLOGIES PVT. LTD.** 

# **Cloud, Infrastructure, IT & Enterprise Technology Handbook** 

**Document ID:** NXR-TECH-003 **Version:** 1.0 **Effective Date:** 01 April 2026 **Review Date:** 31 March 2027 **Document Owner:** Cloud & Infrastructure **Approved By:** Vikram Rao, Chief Technology Officer **Information Classification:** Internal 

# **1. Purpose, Scope & Operating Model** 

## **a. Purpose** 

This handbook establishes the standards and operating practices used by Nexora Technologies for cloud platforms, infrastructure, enterprise technology and internal IT services. 

It defines how Nexora provisions, operates, secures, monitors and supports technology infrastructure used by employees, engineering teams, business functions and customer-facing workloads. 

The handbook covers: 

- Cloud platforms 

- Infrastructure engineering 

- Platform engineering 

- Networking 

- Compute 

- Storage 

- Databases 

- Identity infrastructure 

- Corporate IT 

- Employee devices 

- SaaS applications 

- Service Desk 

- IT asset management 

- Monitoring 

- Observability 

- Backup 

- Recovery 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 1 / 43 



<!-- PDF_PAGE: 2 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

- Capacity management 

- Infrastructure security 

- Cloud cost management 

- Infrastructure lifecycle 

It applies to company-managed infrastructure and approved third-party technology environments. 

## **b. Operating Principles** 

Nexora infrastructure is operated according to the following principles: 

### **I. Standardize where practical** 

Common platforms, configurations and operational processes should be reused wherever they meet business requirements. 

### **II. Automate infrastructure** 

Infrastructure provisioning and repeatable operational activities should use automation where practical. 

### **III. Secure by default** 

Infrastructure should use appropriate identity, network, encryption and monitoring controls before production use. 

### **IV. Minimize unnecessary access** 

Infrastructure access follows least-privilege principles. 

### **V. Monitor what matters** 

Critical systems must have sufficient observability to detect failures and abnormal behavior. 

### **VI. Design for recovery** 

Important workloads must have appropriate backup and recovery capabilities. 

### **VII. Manage cost deliberately** 

Cloud and technology consumption must be visible, monitored and aligned with business value. 

# **2. Infrastructure Organization** 

## **a. Infrastructure Functions** 

The Cloud & Infrastructure organization contains several specialized capabilities. 

|**Function**|**Primary Responsibility**|
|---|---|
|Cloud Engineering|Cloud architecture and services|
|Platform Engineering|Internal developer platforms|



NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 2 / 43 



<!-- PDF_PAGE: 3 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

|**Function**|**Primary Responsibility**|
|---|---|
|Site Reliability Engineering|Reliability and production operations|
|Network Engineering|Corporate and cloud networking|
|Database Engineering|Database platforms|
|Infrastructure Security|Infrastructure security controls|
|Corporate IT|Employee technology|
|IT Service Management|Service Desk and IT processes|
|IT Asset Management|Hardware and software assets|
|Cloud FinOps|Cloud cost governance|



## **b. Geographic Operations** 

Infrastructure support operates across Nexora's principal locations: 

- Bengaluru 

- Pune 

- Hyderabad 

- London 

Critical infrastructure support is organized around shared enterprise platforms rather than individual offices. 

## **c. Infrastructure Ownership** 

Every production infrastructure component should have an identifiable owner. 

Ownership should include: 

- Technical team 

- Service owner 

- Business owner where appropriate 

- Environment 

- Support path 

- Escalation path 

Unowned infrastructure is considered an operational risk. 

# **3. Enterprise Technology Architecture** 

## **a. Technology Layers** 

Nexora's technology environment can be represented in six major layers. 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 3 / 43 



<!-- PDF_PAGE: 4 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 



<!-- Start of picture text -->
Business Applications<br>        ↓<br>Application Platforms<br>        ↓<br>Data & Integration<br>        ↓<br>Cloud & Compute<br>        ↓<br>Network & Identity<br>        ↓<br>Physical / Endpoint Infrastructure<br><!-- End of picture text -->

Each layer may be operated by different technical teams. 

# **b. Enterprise Technology Platforms** 

Major internal platforms include: 

|**Platform**|**Primary Purpose**|
|---|---|
|Nexora PeopleHub|Human resources|
|Nexora ServiceDesk|IT service management|
|Nexora Workspace|Collaboration|
|Nexora Identity|Identity and access|
|Nexora KnowledgeHub|Internal knowledge|
|Nexora Insight|Enterprise analytics|
|Nexora Flow|Workflow automation|
|Nexora Sentinel|Security monitoring|
|Nexora Assist|Enterprise AI|



# **c. Standard Cloud Provider** 

Nexora's primary enterprise cloud platform for cloud-native workloads is **Google Cloud Platform (GCP)** . 

Other cloud platforms may be used when: 

   - Required by a customer 

   - Required by an acquired technology 

   - Required by a specific technical workload 

   - Required for geographic or regulatory reasons 

- Multi-cloud usage must have an identified business or technical rationale. 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 4 / 43 



<!-- PDF_PAGE: 5 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

# **4. Cloud Account & Project Structure** 

## **a. Cloud Organization** 

Cloud resources are organized using controlled organizational structures. 

A typical hierarchy is: 

```
Nexora Cloud Organization
        │
        ├── Production
        │     ├── Customer Workloads
        │     ├── Enterprise Platforms
        │     └── Shared Services
        │
        ├── Non-Production
        │     ├── Development
        │     ├── Testing
        │     └── Staging
        │
        └── Security & Governance
```

## **b. Project Naming** 

Cloud projects should use consistent naming. 

Example: 

```
NXR-DATA-PROD-01
NXR-DATA-STG-01
NXR-PLATFORM-PROD-01
NXR-SECURITY-PROD-01
NXR-DEVTOOLS-NONPROD-01
```

## **c. Resource Ownership** 

Each production cloud project should identify: 

- Business owner 

- Technical owner 

- Environment 

- Cost center 

- Data classification 

- Support team 

## **d. Project Creation** 

New production projects require approval from the relevant platform owner. 

Projects should not be created solely for convenience when an existing approved project can satisfy the requirement. 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 5 / 43 



<!-- PDF_PAGE: 6 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

# **5. Cloud Environment Standards** 

## **a. Environment Model** 

Nexora uses separate environments for different lifecycle stages. 

|**Environment**|**Purpose**|
|---|---|
|Development|Engineering development|
|Test|Automated and functional testing|
|Staging|Production-like validation|
|Production|Live business workloads|



Some teams may combine development and test environments for low-risk applications. 

## **b. Production Isolation** 

Production environments must be logically separated from development environments. 

Production credentials must not be reused in non-production environments. 

## **c. Production Data** 

Production data must not be copied into development environments without an approved data-handling process. 

Where test data is required, teams should use: 

- Synthetic data 

- Masked data 

- Anonymized data 

- Approved test datasets 

# **6. Compute Infrastructure** 

## **a. Compute Options** 

Nexora may use: 

- Virtual machines 

- Containers 

- Managed container platforms 

- Serverless compute 

- Batch processing 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 6 / 43 



<!-- PDF_PAGE: 7 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

- Specialized compute 

Technology selection depends on: 

- Workload 

- Scale 

- Operational requirements 

- Cost 

- Security 

- Team capability 

## **b. Virtual Machines** 

Virtual machines should use approved operating-system images. 

Production VM configurations should be documented. 

## **c. Containers** 

Containerized workloads should: 

- Use approved base images 

- Be vulnerability scanned 

- Avoid running with unnecessary privileges 

- Avoid embedded credentials 

- Define resource requirements 

- Use versioned images 

## **d. Resource Allocation** 

Production services should define: 

- CPU requirements 

- Memory requirements 

- Storage requirements 

- Scaling limits 

Teams should avoid unlimited resource allocation. 

# **7. Kubernetes & Container Platforms** 

## **a. Container Orchestration** 

Nexora may use managed Kubernetes or equivalent approved container platforms for workloads requiring orchestration. Typical use cases include: 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 7 / 43 



<!-- PDF_PAGE: 8 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

- Microservices 

- APIs 

- Background workers 

- Data services 

- Internal platforms 

## **b. Cluster Standards** 

Production clusters should have: 

- Centralized authentication 

- Network controls 

- Resource limits 

- Logging 

- Monitoring 

- Vulnerability scanning 

- Backup strategy where applicable 

## **c. Namespace Management** 

Namespaces should be separated by: 

- Environment 

- Application 

- Business function 

Teams should avoid placing unrelated production workloads in a single uncontrolled namespace. 

## **d. Resource Limits** 

Production workloads should define CPU and memory requests and limits where supported. 

A service repeatedly exceeding **80% of its allocated memory** should be reviewed for optimization or capacity adjustment. 

# **8. Networking** 

## **a. Network Architecture** 

Nexora network architecture separates: 

- Corporate networks 

- Cloud networks 

- Production workloads 

- Non-production workloads 

- Security services 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 8 / 43 



<!-- PDF_PAGE: 9 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

### External integrations 

## **b. Virtual Networks** 

Production cloud workloads should use approved virtual network configurations. 

Network segmentation should reflect workload sensitivity. 

## **c. Subnets** 

Subnets may be separated by: 

- Environment 

- Application tier 

- Region 

- Security boundary 

## **d. Firewall Rules** 

Firewall rules should follow least privilege. 

Rules should specify: 

- Source 

- Destination 

- Port 

- Protocol 

- Purpose 

- Owner 

Broad rules such as unrestricted access from the public internet should be avoided unless explicitly required and approved. 

## **e. Network Changes** 

Material firewall and routing changes must use approved change-management procedures. 

# **9. Internet Connectivity** 

## **a. Public Endpoints** 

Public-facing services must be reviewed for: 

- Authentication 

- TLS 

- Firewall controls 

- Rate limiting 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 9 / 43 



<!-- PDF_PAGE: 10 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

- Logging 

- Monitoring 

- DDoS protection where applicable 

## **b. TLS** 

External services should use current approved TLS configurations. 

Expired or invalid certificates must be remediated promptly. 

## **c. DNS** 

Corporate and production DNS zones must be administered through approved services. 

DNS changes affecting production services require appropriate authorization. 

# **10. Identity & Access Management** 

## **a. Identity Principles** 

Access follows: 

- Least privilege 

- Need to know 

- Role-based access 

- Strong authentication 

- Periodic review 

## **b. Nexora Identity** 

Nexora Identity is the central enterprise identity platform. 

It supports: 

- Employee authentication 

- Multi-factor authentication 

- Role assignment 

- Application access 

- Access lifecycle 

- Privileged access controls 

## **c. Multi-Factor Authentication** 

MFA is mandatory for: 

- Corporate accounts 

- Cloud consoles 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 10 / 43 



<!-- PDF_PAGE: 11 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

Privileged access 

- Security platforms 

- Sensitive business systems 

## **d. Privileged Access** 

Privileged access should be: 

- Limited 

- Approved 

- Logged 

- Reviewed 

Permanent administrative access should be minimized. 

## **e. Access Reviews** 

Critical application and infrastructure access should normally be reviewed at least **quarterly** . 

Privileged access should receive enhanced review. 

# **11. Joiner, Mover & Leaver Technology Access** 

## **a. Joiners** 

When an employee joins, Corporate IT provisions: 

- Identity 

- Email 

- Collaboration tools 

- Required applications 

- Device 

- Role-specific access 

Standard equipment should be ready by the employee's first working day. 

## **b. Movers** 

When an employee changes role: 

- Existing access should be reviewed 

- New access should be approved 

- Unnecessary access should be removed 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 11 / 43 



<!-- PDF_PAGE: 12 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

## **c. Leavers** 

When employment ends: 

- Corporate identity is disabled 

- Sessions are revoked where supported 

- Device access is removed 

- SaaS access is revoked 

- Privileged access is removed 

Critical access should be disabled promptly according to the approved separation process. 

# **12. Corporate IT** 

## **a. Corporate IT Responsibilities** 

Corporate IT supports: 

- Employee devices 

- Corporate applications 

- Collaboration 

- Connectivity 

- Printing where applicable 

- Endpoint security 

- Software provisioning 

- IT support 

## **b. Standard Employee Equipment** 

Standard equipment may include: 

- Business laptop 

- Docking station 

- Monitor 

- Keyboard and mouse 

- Headset 

Equipment depends on job role. 

Engineering, design and data-intensive roles may receive higher-performance configurations. 

## **c. Device Standards** 

Company-managed devices should have: 

- Disk encryption 

- Endpoint security 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 12 / 43 



<!-- PDF_PAGE: 13 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

- Screen lock 

- Automatic updates 

- Central management 

- Approved software 

## **d. Device Replacement** 

Standard corporate laptops should generally be reviewed for replacement after approximately **36 months** , subject to condition, performance and business requirements. 

# **13. IT Asset Management** 

## **a. Asset Inventory** 

Corporate IT maintains an inventory of managed assets. 

Assets may include: 

- Laptops 

- Desktops 

- Monitors 

- Mobile devices 

- Network equipment 

- Servers 

- Software licenses 

## **b. Asset Identification** 

Assets should have unique identifiers. 

Example: 

```
NXR-LAP-042817
NXR-MON-018274
NXR-MOB-006391
```

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 13 / 43 



<!-- PDF_PAGE: 14 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

## **c. Asset Lifecycle** 



<!-- Start of picture text -->
Procurement<br>   ↓<br>Receipt<br>   ↓<br>Assignment<br>   ↓<br>Maintenance<br>   ↓<br>Reassignment<br>   ↓<br>Return<br>   ↓<br>Secure Disposal<br><!-- End of picture text -->

## **d. Lost Equipment** 

Lost or stolen company equipment must be reported immediately. 

Corporate IT and Security may remotely lock or wipe managed devices where supported. 

# **14. IT Service Desk** 

## **a. ServiceDesk** 

Nexora ServiceDesk is the central system for employee IT requests and incidents. 

Employees should create tickets for: 

- Device problems 

- Application problems 

- Access requests 

- Network problems 

- Software installation 

- Hardware replacement 

## **b. Ticket Priority** 

|**Priority**|**Typical Impact**|
|---|---|
|P1|Critical enterprise impact|
|P2|Significant business impact|
|P3|Individual or limited impact|
|P4|General request / low urgency|



NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 14 / 43 



<!-- PDF_PAGE: 15 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

## **c. Reference Response Targets** 

|**Priority**|**Initial Response**|**Target Resolution**|
|---|---|---|
|P1|15 minutes|4 hours|
|P2|30 minutes|8 hours|
|P3|4 business hours|2 business days|
|P4|1 business day|5 business days|



These are standard internal targets and may vary by service. 

## **d. Escalation** 

Tickets should be escalated when: 

- The SLA is at risk 

- Multiple employees are affected 

- Security is suspected 

- A critical business function is unavailable 

# **15. Enterprise SaaS Applications** 

## **a. SaaS Management** 

Enterprise SaaS applications must have: 

- Business owner 

- Technical owner 

- Contract owner 

- Security assessment where applicable 

- Cost center 

- Access model 

## **b. Application Procurement** 

Employees must not independently purchase enterprise SaaS using company funds without following procurement procedures. 

## **c. SaaS Access** 

Access should be provisioned according to role. 

Inactive accounts should be reviewed and removed. 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 15 / 43 



<!-- PDF_PAGE: 16 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

## **d. Application Review** 

Critical SaaS platforms should be reviewed periodically for: 

- Security 

- Cost 

- Usage 

- Vendor performance 

- Business value 

# **16. Storage** 

## **a. Storage Types** 

Nexora may use: 

- Object storage 

- Block storage 

- File storage 

- Database storage 

- Archive storage 

## **b. Data Classification** 

Storage controls should reflect data classification. 

Restricted information requires stronger controls than Public information. 

## **c. Object Storage** 

Object storage buckets should not be publicly accessible unless there is an approved business requirement. 

## **d. Lifecycle Management** 

Storage lifecycle rules should move or delete data according to: 

- Business requirements 

- Retention policy 

- Cost considerations 

- Legal requirements 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 16 / 43 



<!-- PDF_PAGE: 17 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

# **17. Database Infrastructure** 

## **a. Managed Databases** 

Where practical, production systems should use managed database services. 

Benefits include: 

- Automated backups 

- Monitoring 

- Patch management 

- Availability features 

- Operational automation 

## **b. Database Availability** 

Critical databases should have appropriate: 

- Replication 

- Backup 

- Monitoring 

- Recovery procedures 

## **c. Database Access** 

Database access must use approved identity mechanisms. 

Direct production database access should be restricted. 

## **d. Database Performance** 

Database teams monitor: 

- Query latency 

- CPU 

- Memory 

- Storage 

- Connections 

- Replication health 

Sustained resource utilization above **80%** should trigger capacity review for critical production databases. 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 17 / 43 



<!-- PDF_PAGE: 18 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

# **18. Backup Management** 

## **a. Backup Principles** 

Important systems must have appropriate backups. 

Backup design should consider: 

- Recovery requirements 

- Data criticality 

- Retention 

- Cost 

- Geographic resilience 

## **b. Backup Frequency** 

Typical backup schedules may include: 

|**Workload**|**Reference Frequency**|
|---|---|
|Critical database|Continuous / frequent|
|Standard production database|Daily + transaction recovery where supported|
|File services|Daily|
|Configuration|Daily or version-controlled|
|Low-criticality systems|Weekly or according to requirements|



## **c. Backup Verification** 

Backups are not considered reliable merely because they completed successfully. 

Critical backups should be restored and tested periodically. 

## **d. Backup Retention** 

Typical retention may include: 

- Daily backups: 30 days 

- Monthly backups: 12 months 

- Annual archival: according to business/legal requirements 

Actual retention depends on system requirements. 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 18 / 43 



<!-- PDF_PAGE: 19 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

# **19. Disaster Recovery** 

## **a. Recovery Objectives** 

Systems may have defined: 

- Recovery Time Objective (RTO) 

Recovery Point Objective (RPO) 

Example classifications: 

|**Criticality**|**Reference RTO**|**Reference RPO**|
|---|---|---|
|Critical|4 hours|1 hour|
|High|8 hours|4 hours|
|Standard|24 hours|24 hours|
|Low|72 hours|48 hours|



Actual customer contracts or business continuity requirements may establish stricter objectives. 

## **b. Recovery Testing** 

Critical systems should participate in recovery testing at least **annually** . 

High-criticality systems may require more frequent testing. 

## **c. Recovery Documentation** 

Recovery documentation should identify: 

- System owner 

- Dependencies 

- Recovery sequence 

- Required credentials Infrastructure 

- Validation steps 

- Escalation contacts 

# **20. Monitoring & Observability** 

## **a. Infrastructure Monitoring** 

Infrastructure monitoring should cover: 

### CPU 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 19 / 43 



<!-- PDF_PAGE: 20 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

- Memory 

- Disk 

- Network 

- Availability 

- Error rates 

- Service health 

# **b. Application Monitoring** 

Application teams should monitor: 

- Requests 

- Latency 

- Errors 

- Dependency failures 

- Business transactions 

# **c. Alerts** 

Alerts should be: 

- Actionable 

- Assigned to an owner 

- Prioritized 

- Documented 

Teams should avoid alerts that consistently produce no action. 

# **d. Alert Thresholds** 

Example thresholds: 

|**Metric**|**Warning**|**Critical**|
|---|---|---|
|CPU|70%|85%|
|Memory|75%|90%|
|Disk|70%|85%|
|Error rate|2%|5%|
|API p95 latency|700 ms|1,500 ms|



Actual thresholds may differ according to workload characteristics. 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 20 / 43 



<!-- PDF_PAGE: 21 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

# **21. Infrastructure Incident Management** 

## **a. Incident Classification** 

Infrastructure incidents may include: 

- Cloud outage 

- Network outage 

- Database failure 

- Storage failure 

- Authentication failure 

- Capacity exhaustion 

- Configuration error 

- Security event 

## **b. Severity** 

|**Severity**|**Example**|
|---|---|
|Sev 1|Critical enterprise/customer outage|
|Sev 2|Significant service degradation|
|Sev 3|Limited impact|
|Sev 4|Minor issue|



## **c. Incident Process** 

```
Detection
   ↓
Triage
   ↓
Severity Assignment
   ↓
Mitigation
   ↓
Recovery
   ↓
Validation
   ↓
Root Cause Analysis
   ↓
Corrective Action
```

## **d. Incident Communication** 

For significant incidents, the incident lead should establish: 

Incident channel 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 21 / 43 



<!-- PDF_PAGE: 22 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

- Technical owner 

- Communications owner 

- Status cadence 

- Escalation path 

# **22. Cloud Cost Management** 

## **a. Cost Ownership** 

Every production cloud project must have: 

- Cost center 

- Business owner 

- Technical owner 

## **b. Cost Monitoring** 

Cloud costs should be reviewed at least monthly. 

Large or rapidly increasing costs should be investigated. 

## **c. Cost Categories** 

Typical cloud costs include: 

- Compute 

- Storage 

- Database 

- Networking 

- Data processing 

- Security 

- Monitoring 

- AI/ML services 

## **d. Budget Alerts** 

Cloud budgets should have alert thresholds. 

A reference configuration is: 

|**Threshold**|**Action**|
|---|---|
|50%|Monitoring|
|75%|Owner notification|
|90%|Finance + technical owner review|



NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 22 / 43 



<!-- PDF_PAGE: 23 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

|**Threshold**|**Action**|
|---|---|
|100%|Budget investigation|



## **e. Cost Optimization** 

Teams should consider: 

- Right-sizing Autoscaling Reserved capacity Storage lifecycle policies Idle resource removal Query optimization 

# **23. Infrastructure as Code** 

## **a. Standard** 

Production infrastructure should be managed through version-controlled infrastructure-as-code where practical. 

## **b. Benefits** 

Infrastructure-as-code provides: 

- Repeatability 

- Traceability 

- Reviewability 

- Automation 

- Faster recovery 

## **c. Change Process** 

Infrastructure changes should follow: 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 23 / 43 



<!-- PDF_PAGE: 24 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

```
Code Change
   ↓
Review
   ↓
Validation
   ↓
Plan / Preview
   ↓
Approval
   ↓
Apply
   ↓
Verification
```

## **d. State Management** 

Infrastructure state must be protected from unauthorized access and accidental deletion. 

# **24. Configuration Management** 

## **a. Configuration** 

Configuration should be separated from application code. 

Examples: 

- Environment variables 

- Feature flags Service endpoints Resource limits 

- Runtime settings 

## **b. Sensitive Configuration** 

Sensitive configuration must use approved secret-management systems. 

## **c. Configuration Changes** 

Material configuration changes affecting production should be traceable. 

# **25. Patch Management** 

## **a. Operating System Patches** 

Production operating systems should receive security updates according to vulnerability severity and operational risk. 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 24 / 43 



<!-- PDF_PAGE: 25 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

## **b. Reference Targets** 

|**Severity**<br>**Reference Target**|
|---|
|Critical<br>7 days|
|High<br>14 days|
|Medium<br>30 days|
|Low<br>90 days|



Emergency security patches may require accelerated deployment. 

## **c. Patch Exceptions** 

Exceptions must document: 

- Vulnerability 

- Affected system 

- Reason for delay 

- Compensating control 

- Owner 

- Target remediation date 

# **26. Capacity Management** 

## **a. Capacity Planning** 

Teams should monitor: 

- CPU 

- Memory 

- Storage 

- Network 

- Database connections 

- Queue depth 

- API traffic 

## **b. Capacity Threshold** 

A production service consistently operating above **80% of designed capacity** should be reviewed. 

## **c. Growth Planning** 

Teams should consider expected growth over: 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 25 / 43 



<!-- PDF_PAGE: 26 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

- 30 days 

- 90 days 

- 12 months 

Critical infrastructure should not rely on emergency scaling as its normal capacity strategy. 

# **27. Platform Engineering** 

## **a. Internal Platforms** 

Platform Engineering provides reusable capabilities to product teams. 

Examples include: 

- CI/CD templates 

- Container platforms 

- Logging 

- Monitoring 

- Identity integration 

- Infrastructure modules 

- Developer environments 

## **b. Platform Standards** 

Internal platforms should prioritize: 

- Self-service 

- Security 

- Reliability 

- Documentation 

- Consistency 

## **c. Platform Service Levels** 

Critical platform services should define: 

- Availability target 

- Support model 

- Escalation 

- Maintenance windows 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 26 / 43 



<!-- PDF_PAGE: 27 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

# **28. Enterprise Integration** 

## **a. Integration Principles** 

Enterprise integrations should define: 

- System owner 

- Data owner 

- Authentication 

- Data exchanged 

- Frequency 

- Failure handling 

- Monitoring 

## **b. Integration Types** 

Nexora may use: 

- REST APIs 

- Events 

- Message queues 

- Batch files 

- Managed integrations 

## **c. Integration Failures** 

Integration systems should handle: 

- Timeout 

- Retry 

- Duplicate messages 

- Invalid data 

- Authentication failure 

- Provider outage 

# **29. Employee Connectivity** 

## **a. Office Networks** 

Corporate offices provide managed connectivity for: 

- Employee devices 

- Approved corporate services 

- Conference systems 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 27 / 43 



<!-- PDF_PAGE: 28 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

Printers 

Guest access 

## **b. Guest Networks** 

Guest networks should be logically separated from corporate systems. 

## **c. VPN / Secure Remote Access** 

Remote access to internal systems must use approved secure-access mechanisms. 

## **d. Network Performance** 

Corporate IT should monitor: 

- Availability 

- Internet bandwidth 

- Latency 

- Packet loss 

- Access-point health 

# **30. Collaboration Technology** 

## **a. Collaboration Services** 

Nexora Workspace supports: 

- Email 

- Calendar 

- Document collaboration 

- Team communication 

- Meetings 

## **b. Access** 

Access should be provisioned based on employment status and role. 

## **c. Data Protection** 

Sensitive company information must only be shared through approved collaboration services. 

## **d. External Sharing** 

External sharing should be controlled according to information classification. 

Restricted information should not be externally shared without authorization. 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 28 / 43 



<!-- PDF_PAGE: 29 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

# **31. Endpoint Security** 

## **a. Endpoint Controls** 

Company-managed endpoints should use: 

- Disk encryption 

- Endpoint detection and response 

- Central management 

- Automatic security updates 

- Screen locking 

- Application controls 

## **b. Security Baseline** 

A standard endpoint should: 

- Lock after inactivity 

- Require authentication 

- Use supported operating systems 

- Run approved security software 

## **c. Personal Devices** 

Personal devices may only access corporate resources where specifically permitted. 

Access may be restricted based on security and data classification requirements. 

# **32. Software Licensing** 

## **a. License Management** 

Corporate IT maintains visibility of important software licenses. 

## **b. Procurement** 

Software requiring payment must follow procurement procedures. 

## **c. License Compliance** 

Employees must not: 

- Install unauthorized commercial software 

Share license keys 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 29 / 43 



<!-- PDF_PAGE: 30 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

Circumvent license controls 

Use pirated software 

## **d. License Optimization** 

Unused licenses should be reclaimed where practical. 

Enterprise software utilization should be reviewed periodically. 

# **33. Technology Procurement** 

## **a. Procurement Process** 

Technology procurement normally follows: 

```
Business Requirement
       ↓
Technical Assessment
       ↓
Security Review
       ↓
Budget Confirmation
       ↓
Vendor Evaluation
       ↓
Commercial Negotiation
       ↓
Approval
       ↓
Purchase
       ↓
Implementation
```

## **b. Vendor Evaluation** 

Technology vendors may be evaluated on: 

- Security 

- Reliability 

- Price 

- Support 

- Scalability 

- Integration 

- Contract terms 

## **c. High-Risk Vendors** 

Vendors handling Restricted data or critical infrastructure may require enhanced security and legal review. 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 30 / 43 



<!-- PDF_PAGE: 31 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

# **34. Maintenance Windows** 

## **a. Standard Maintenance** 

Maintenance should be planned to minimize business disruption. 

## **b. Maintenance Communication** 

Planned maintenance should communicate: 

- Date 

- Time 

- Expected impact 

- Duration 

- Services affected 

- Contact 

## **c. Emergency Maintenance** 

Emergency maintenance may be performed when required to protect: 

- Availability 

- Security 

- Data integrity 

- Customer impact 

Emergency changes must be documented retrospectively. 

# **35. Service Availability** 

## **a. Availability Targets** 

Reference targets for enterprise services include: 

|**Service Class**|**Target**|
|---|---|
|Critical|≥99.95%|
|High|≥99.9%|
|Standard|≥99.5%|
|Low|≥99.0%|



Customer contracts may specify different targets. 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 31 / 43 



<!-- PDF_PAGE: 32 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

## **b. Availability Calculation** 

Availability may be calculated as: 

```
Availability =
(Total Scheduled Time - Downtime)
÷
Total Scheduled Time
× 100
```

For a 30-day month: 

```
Total time = 720 hours
99.9% availability = approximately 43.2 minutes maximum downtime
```

Actual contractual calculations may exclude approved maintenance and defined exclusions. 

# **36. Service Ownership & Operational Readiness** 

Before a new production service is launched, the service should have: 

- Owner 

- Technical team 

- Support path 

- Monitoring 

- Alerting 

- Documentation 

- Deployment process 

- Backup where applicable 

- Recovery plan 

- Security assessment 

A service without operational ownership should not normally enter production. 

# **37. Infrastructure Change Management** 

## **a. Standard Changes** 

Standard, repeatable changes may follow pre-approved procedures. 

Examples: 

- Routine patching 

- Approved certificate renewal 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 32 / 43 



<!-- PDF_PAGE: 33 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

- Standard user provisioning 

## **b. Normal Changes** 

Normal infrastructure changes require: 

- Description 

- Risk 

- Implementation plan 

- Validation 

- Rollback 

- Approval 

## **c. Emergency Changes** 

Emergency changes are permitted when necessary to prevent or resolve significant incidents. 

Emergency changes must be reviewed afterward. 

# **38. Cloud Security Controls** 

Cloud environments should use: 

- Centralized identity 

- MFA 

- Role-based access 

- Network segmentation 

- Logging 

- Monitoring 

- Encryption 

- Vulnerability scanning 

- Security alerts 

Public cloud resources must not be exposed unintentionally. 

## **a. Public Resource Review** 

Public-facing storage, databases and management interfaces should receive additional review. 

## **b. Encryption** 

Sensitive information should use approved encryption mechanisms both: 

- At rest 

- In transit 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 33 / 43 



<!-- PDF_PAGE: 34 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

# **39. Infrastructure Documentation** 

Each critical infrastructure service should maintain documentation covering: 

- Architecture 

- Ownership Dependencies 

- Configuration Monitoring Backup Recovery Deployment 

- Escalation 

Documentation should be reviewed when major architecture changes occur. 

# **40. Infrastructure Operating Metrics** 

Cloud and IT leadership may review: 

|**Metric**|**Reference Target**|
|---|---|
|Critical service availability|≥99.95%|
|High service availability|≥99.9%|
|Critical incident response|≤15 minutes|
|P1 ServiceDesk response|≤15 minutes|
|Standard CI pipeline|≤15 minutes|
|Critical vulnerability remediation|≤7 days|
|Critical access review|Quarterly|
|Critical backup recovery test|At least annually|
|Standard laptop replacement review|~36 months|
|Cloud cost review|Monthly|
|Critical service ownership|100%|



# **41. Example Cloud Architecture** 

A typical Nexora production workload may use: 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 34 / 43 



<!-- PDF_PAGE: 35 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 



<!-- Start of picture text -->
                         Internet<br>                            |<br>                     Cloud Load Balancer<br>                            |<br>                       API Gateway<br>                            |<br>                 +----------+----------+<br>                 |                     |<br>          Application Service     Authentication<br>                 |<br>        +--------+--------+<br>        |                 |<br>   Cache Layer        Message Queue<br>        |                 |<br>        +--------+--------+<br>                 |<br>             PostgreSQL<br>                 |<br>          Data Warehouse<br>                 |<br>          Nexora Insight<br><!-- End of picture text -->

Supporting capabilities include: 

Centralized logging 

- Monitoring 

- Security monitoring 

- Secret management 

- CI/CD 

- Backup 

# **42. Example Production Environment** 

**Environment:** NXR-DATA-PROD-01 

**Business Function:** Data & AI 

**Primary Region:** Approved GCP region 

## **Workloads:** 

Data ingestion 

- Transformation 

- Analytics APIs 

- Scheduled processing 

## **Controls:** 

MFA 

Role-based access 

- Centralized logging 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 35 / 43 



<!-- PDF_PAGE: 36 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

- Monitoring 

- Backup 

- Security scanning 

## **Ownership:** 

- Technical Owner: Data Platform Engineering 

- Infrastructure Owner: Cloud & Infrastructure 

- Security Owner: Security Engineering 

- Business Owner: Data & AI 

# **43. Example IT Service Request** 

**Request ID:** IT-2026-08421 

**Employee:** NXR-EMP-02641 

**Request:** Additional development monitor 

**Reason:** Approved development workstation requirement 

**Priority:** P4 

**Approval:** Engineering Manager 

**Asset:** NXR-MON-018274 

**Status:** Fulfilled 

Corporate IT records the assignment in the asset inventory. 

# **44. Example Infrastructure Incident** 

**Incident ID:** INC-2026-0317 

**Severity:** Sev 2 

**Service:** Customer Analytics API 

**Detection:** Automated monitoring 

**Start:** 14 July 2026, 14:08 IST 

**Initial symptom:** API error rate increased from 0.4% to 7.2%. 

## **Initial action:** 

1. Incident declared 

2. Application team engaged 

3. Infrastructure metrics reviewed 

4. Database connection pool investigated 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 36 / 43 



<!-- PDF_PAGE: 37 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

5. Traffic reduced 

6. Service stabilized 

**Recovery:** 14:31 IST 

**Total impact:** 23 minutes 

## **Follow-up:** 

- Root-cause analysis 

- Connection-pool adjustment 

- Capacity review 

- Alert improvement 

# **45. Cloud Financial Management Example** 

**Cloud Project:** NXR-DATA-PROD-01 

|**Cost Category**|**Monthly Example**|
|---|---|
|Compute|₹1,850,000|
|Database|₹620,000|
|Storage|₹180,000|
|Data Processing|₹740,000|
|Networking|₹310,000|
|Monitoring/Security|₹210,000|
|**Total**|**₹3,910,000**|



If monthly spending exceeds the approved budget by more than **10%** , the technical owner and Finance should review the variance. 

Cost optimization opportunities may include: 

- Instance right-sizing 

- Storage lifecycle policies 

- Query optimization 

- Idle-resource removal 

- Reserved capacity 

# **46. Infrastructure Capacity Example** 

A production API currently handles: 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 37 / 43 



<!-- PDF_PAGE: 38 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

- 1,800 requests/second average 

- 3,200 requests/second peak 

- 68% average CPU 

- 76% average memory 

- 420 ms p95 latency 

The team expects traffic to increase by approximately **35% over the next six months** . 

The team should evaluate: 

- Horizontal scaling 

- Database capacity 

- Cache capacity 

- Network throughput 

- Cost impact 

Capacity planning should occur before the expected growth reaches existing limits. 

# **47. Cross-Functional Responsibilities** 

Infrastructure operations frequently intersect with other Nexora functions. 

|**Activity**|**Infrastructure**|**Other Function**|
|---|---|---|
|Cloud architecture|Cloud|Engineering|
|Access management|Infrastructure|Security|
|Employee device|IT|People Operations|
|Software purchase|IT|Procurement|
|Cloud budget|Infrastructure|Finance|
|Customer environment|Infrastructure|Delivery|
|Data platform|Infrastructure|Data & AI|
|AI infrastructure|Infrastructure|AI Engineering|
|Incident response|Infrastructure|Security / Engineering|
|Disaster recovery|Infrastructure|Corporate Operations|



The responsible owner must be identified for each production service. 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 38 / 43 



<!-- PDF_PAGE: 39 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

# **48. Infrastructure Governance** 

## **a. Architecture Governance** 

Major infrastructure architecture decisions may require Technology Architecture Council review. 

## **b. Security Governance** 

Infrastructure handling sensitive information must comply with Security requirements. 

## **c. Financial Governance** 

Cloud spending must remain within approved budgets unless an approved variance exists. 

## **d. Operational Governance** 

Critical infrastructure should participate in: 

- Monitoring reviews 

- Capacity reviews 

- Backup testing 

- Recovery exercises 

- Incident reviews 

# **49. Infrastructure Exceptions** 

Exceptions to this handbook must be documented. 

An exception should include: 

- Requirement 

- Reason 

- Risk 

- Compensating control 

- Owner 

- Approval 

- Expiry date 

Temporary exceptions should include a remediation plan. 

Security, legal and regulatory requirements cannot be bypassed through an ordinary infrastructure exception. 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 39 / 43 



<!-- PDF_PAGE: 40 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

# **50. Quick Reference** 

|**Topic**|**Standard**|
|---|---|
|Primary cloud platform|Google Cloud Platform|
|Standard environments|Development, Test, Staging, Production|
|MFA|Required for corporate and privileged access|
|Critical access review|Quarterly|
|Standard laptop replacement review|~36 months|
|P1 IT response|15 minutes|
|P1 target resolution|4 hours|
|P2 IT response|30 minutes|
|Standard production logs|30 days|
|Security-relevant logs|90 days|
|Critical vulnerability target|7 days|
|High vulnerability target|14 days|
|Medium vulnerability target|30 days|
|Critical service availability|≥99.95%|
|High service availability|≥99.9%|
|Standard service availability|≥99.5%|
|Critical recovery test|At least annually|
|Cloud cost review|Monthly|
|Capacity review threshold|~80% sustained utilization|
|Secret rotation target|90 days|



# **Appendix A — Standard Cloud Project Naming** 

```
NXR-<FUNCTION>-<ENVIRONMENT>-<NUMBER>
```

Examples: 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 40 / 43 



<!-- PDF_PAGE: 41 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

```
NXR-DATA-PROD-01
NXR-DATA-STG-01
NXR-APP-PROD-02
NXR-SEC-PROD-01
NXR-PLATFORM-NONPROD-01
```

# **Appendix B — Standard Infrastructure Tags** 

Production cloud resources should use appropriate metadata. 

Recommended fields include: 

```
company = nexora
environment = production
business_unit = data-ai
application = analytics-platform
owner = data-platform
cost_center = CC-4207
classification = confidential
managed_by = cloud-infrastructure
```

# **Appendix C — Service Readiness Checklist** 

## **Before Production** 

- [ ] Owner assigned 

- [ ] Business owner assigned 

- [ ] Environment created 

- [ ] Identity configured 

- [ ] Network controls configured 

- [ ] Secrets configured 

- [ ] Monitoring enabled 

- [ ] Logging enabled 

- [ ] Backup configured 

- [ ] Recovery requirements defined 

- [ ] Security review completed 

- [ ] Cost center assigned 

- [ ] Deployment documented 

- [ ] Support path defined 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 41 / 43 



<!-- PDF_PAGE: 42 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

## **After Production** 

- [ ] Health validated 

- [ ] Monitoring alerts tested 

- [ ] Backup verified 

- [ ] Access reviewed 

- [ ] Cost monitored 

- [ ] Documentation published 

# **Appendix D — Backup and Recovery Matrix** 

|**System Class**|**Backup**|**Recovery Test**|**Reference RTO**|**Reference RPO**|
|---|---|---|---|---|
|Critical|Continuous / frequent|Annual or more|4 hours|1 hour|
|High|Daily|Annual|8 hours|4 hours|
|Standard|Daily|Periodic|24 hours|24 hours|
|Low|Weekly|As required|72 hours|48 hours|



# **Appendix E — IT ServiceDesk Priority Matrix** 

|**Priority**|**Example**|**Response**|**Resolution Target**|
|---|---|---|---|
|P1|Enterprise-wide outage|15 min|4 hours|
|P2|Major team impact|30 min|8 hours|
|P3|Individual business impact|4 hours|2 business days|
|P4|Standard request|1 business day|5 business days|



# **Appendix F — Related Documents** 

- **NXR-CORP-001** — Company, People & Corporate Governance Handbook **NXR-TECH-002** — Product, Engineering & Software Development Handbook **NXR-ENG-STD-003** — Production Change Management 

- **NXR-SEC-POL-001** — Information Security Policy 

- **NXR-SEC-STD-002** — Information Classification Standard 

- **NXR-SEC-IRP-003** — Security Incident Response Plan 

- **NXR-DATA-STD-001** — Data Governance Standard 

- **NXR-AI-POL-001** — Responsible AI & Generative AI Policy 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 42 / 43 



<!-- PDF_PAGE: 43 -->

INTERNAL USE ONLY 

**NEXORA TECHNOLOGIES** 

**NXR-OPS-STD-001** — Business Continuity Standard 

**NXR-FIN-POL-001** — Financial Controls 

**NXR-LEG-POL-001** — Contract & Legal Review 

# **Document Approval** 

**Document Owner:** Cloud & Infrastructure **Executive Sponsor:** Vikram Rao, Chief Technology Officer **Effective Date:** 01 April 2026 **Review Date:** 31 March 2027 **Classification:** Internal 

## **End of Document** 

NEXORA TECHNOLOGIES 

Controlled Electronic Document 

PAGE 43 / 43 

