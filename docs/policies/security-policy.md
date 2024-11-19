# Security Policy

!!! note

    Accessing most of the links below require being on the Caktus Group networks.

At Caktus we strive to adhere to community security best practices. We recognize the importance of the confidential information shared with us by clients regularly and give it the respect and care needed when storing and transferring confidential information.

Caktus is committed to protecting its employees, clients, and the company from illegal or damaging actions by individuals, either knowingly or unknowingly. Effective security is a team effort involving the participation and support of every Caktus employee and affiliate who deals with information and/or information systems.

## Acceptance and Training

1. This policy applies to employees, contractors, consultants, interns, and other workers at Caktus.
1. This policy applies to all equipment that is owned or leased by Caktus and all equipment owned or leased by contractors and consultants used while performing work for Caktus.
1. It is the responsibility of the individual to know these guidelines, and to conduct their activities accordingly.
1. Employees, contractors, consultants, and interns must complete training assigned in KnowBe4 (https://training.knowbe4.com/ui/dashboard/)
1. High Security Projects
    1. Employees and Contractors must read and accept the Security Policy in the KnowBe4 console (https://training.knowbe4.com/ui/training/policies) acknowledging understanding of this policy.
    1. Employees and Contractors may need to undergo client-specific security trainings.

## Security Incident Response
1. General ongoing security related concerns and immediate security incidents should be shared via email with [security@caktusgroup.com](mailto:security@caktusgroup.com) as soon as they have been identified. These may include security incidents and concerns on Caktus maintained projects, software applications and libraries used at Caktus, third party services we utilize, and the Caktus office space.
2. Project Security Incidents
    1. In case of a security incident on a Caktus project, the Lead Developer is responsible for leading the security [Incident Response](http://caktus.github.io/caktus-security/topics/incidents.html) with input from Tech Support, third parties, and other relevant Caktii.
    2. A [Security Incident Response document](https://docs.google.com/document/d/1L6YiDJzujNSM4AcvlA7ShUutxhGMzq7ZI6Y0OUvB_y0/edit) will be created and shared with the client via the Project Manager within 48 hours of the incident and once the initial assessment has been made.
    3. This document will document all compromises, what data may have been compromised, what steps were taken, and are ongoing to remedy the situation.

## Physical Facilities Security
1. Access Control and Security System
    1. Caktus’ office space is secured by both an Access Control and Security System.
    1. Access to the property requires a valid key card at all times. Only Caktus employees, contractors who regularly work on-site, and janitorial services are provided key cards.
    1. The Security System is armed at night between 10p-6a and is triggered by glass break, motion, and door contacts throughout the office.
1. Keys
    1. All full-time employees are given keys to a locked cabinet for storing workstations and shared electronics. The cabinet must always remain locked. If utilized, you must re-lock it immediately after each use.
    1. File cabinets are secured by key and accessible only by the Operations Team.
    1. The server closet is secured by key and only Tech Support, Operations Team, and Marketing Team are provided access.
1. Visitors
    1. Clients and other visitors to the secured second floor work area who are meeting on premises are to be accompanied by a Caktus employee at all times.
    1. Visitors to [local events](https://sites.google.com/caktusgroup.com/employees/marketing/caktus-tech-space) are only allowed access to the Caktus Tech Space on the 1st floor. There is no private information stored on this floor. There are access controlled locks between the first floor and second floor at all times.

### Clean Workstation
1. Employees are required to ensure that all sensitive/confidential information in hardcopy or electronic form is secure in their work area at the end of the day and when they are expected to be gone for an extended period.
1. Any sensitive/confidential information must be removed from workspace and locked in a cabinet when the desk is unoccupied and at the end of the work day. 
1. Passwords may not be left on sticky notes posted on or under a computer, nor may they be left written down in an accessible location. 
1. Printouts containing sensitive/confidential information should be immediately removed from the printer. 
1. Upon disposal of sensitive/confidential documents, they should be shredded using the shredder at the reception desk in the main work area.
1. Whiteboards containing sensitive/confidential information should be erased once the meeting or work session in which they were created in finished.

### Network and WiFi
1. The Caktus office network is behind a firewall.
1. WiFi access is partitioned into Caktus and Guest networks.
    1. Credentials to access the primary Caktus network are only provided to employees and on-site contractors.
    1. The Caktus-Guest network is password protected and is partitioned safely from the primary Caktus network.

## Workstations
1. Caktus workstations (laptops) are intended for use exclusively on work-related projects in order to limit the chance of infection of the computer with malware. However, you may work on personal development projects that use Caktus-related technologies (e.g. Django projects) on your Caktus workstation. This applies to professional development activities like attending a conference.
1. It is understood that in the course of completing one’s day-to-day job, especially as a software developer, it is important to have administrative access to control your own workstation to download and run software from the Internet. Please use common sense and evaluate each third-party piece of software carefully before installing it.
1. Security
    1. Workstations must be screen-locked when workspace is unoccupied.
    1. Workstations must be kept in a secure, locked cabinet when not in the presence of their user. 
    1. Encryption will always be enabled for confidential data in transit through SSH and HTTPS connections.
    1. All workstations are provisioned with the following defaults and services (and they should not be changed):
        1. Disabled SSH password authentication
        1. Latest supported Operating Systems and automatic security updates
        1. All workstations have their data secured at rest using GPG encrypted files, and LUKS & FileVault whole disk encryption.
        1. Tech Support SSH remote access
    1. Workstations assigned to High Security Projects are provisioned with the following defaults and services (and they should not be changed):
        1. Firewall
        1. Antivirus software
        1. fail2ban
1. Maintenance and Backups
    1. Regular maintenance of workstations is performed, including regular security updates using automated tools.
    1. Backups and Logs
        1. Backups are stored on a secure and updated FreeNAS computer stored in a locked server closet.
        1. Logs are stored centrally for each computer including security related daemon logs & login details.
        1. All backups and logs are stored for a minimum of 12 months.
### Personal Computers & Phones
1. It is required that employees restrict access to Caktus’ computing infrastructure from their personal workstations and communication devices. Accessing client-owned services from a personal device is prohibited unless otherwise approved by the Security Team.
1. For convenience, you may access Caktus services from personal devices, but please restrict access to the minimum set of services required to perform your duties.
    1. You are required to enable the following security precautions on your mobile device:
        1. Configure a lock screen with a 5 minute timeout on your devices
        1. Enable “Encrypt Device” on Android devices
        1. Keep OS up to date with the latest security updates available
    1. We recommend you enable the following security precautions on your mobile device:
        1. Android: [Find my Phone](https://www.google.com/android/find)
        1. iPhone: [Find my iPhone](https://support.apple.com/en-us/HT205362) (so you can use [https://www.icloud.com/#find](https://www.icloud.com/find))
1. For services not on your personal mobile device, like your laptop, only access Caktus services via a separate incognito browser session.
1. All others services should only be accessed using your Caktus workstation.
### Shared Office Technology
1. Conference rooms are equipped with workstations for presentations and conference calls. Guest accounts are available, but are restricted and all information from the session is deleted on logout.
1. All shared office technology is either protected by a password (conference room computer) or locked when not in use.
1. It is common for Caktus employees to use shared tablets, phones, and computers for communicating with clients, running meetings, and performing quality assurance testing. While using these shared computers please follow the following best practices:
    1. Use your own authentication credentials rather than a shared login when possible
    1. Only access the sites needed to do your work
    1. Lock the screen of the computer when it is not in use
## Confidential Information
1. You may access, use or share confidential information only to the extent it is authorized and necessary to fulfill your assigned job duties.
1. Storage
    1. Confidential information stored on electronic and computing devices whether owned or leased by Caktus, the employee or a third party, remains the sole property of Caktus or its clients.
    1. Confidential information should only ever be stored or transferred via workstations, client servers, Dropbox, Google Docs, email, and paper.
        1. High Security Projects: Only workstations and client servers.
    1. USB flash drives, SD cards, and portable hard drives should only be used for temporary storage (less than a day) and should be securely wiped once the transfer is completed.
1. Deletion
    1. When finished with client projects, all confidential information should be deleted and destroyed.
    1. All Caktus maintained storage that is retired from use will be securely wiped and all paper documents should be shredded when they are no longer needed.
## Accounts, Authentication & Secrets
1. Authentication and Accounts
    1. If it is possible to authenticate via your Caktus Google account, using 2-factor authentication, or via stored SSH keys, these methods are always preferred to simple password authentication.
    1. **Multi-factor authentication** is recommended for all services that support it and is required for specific services at Caktus. The required services and their rollout schedule can be found on Caktus Security: [MFA/2FA Rollout Schedule](https://docs.google.com/spreadsheets/d/1R9lzkv5BeZDch5bdlgb5GyxRNZpcoC7CJ9F7sJXF8o8/edit#gid=0).
        1. Caktus believes the best MFA is the one you use. Hardware authentication devices, such as Yubikeys, are available and can be provided to Caktus employees upon request.
        1. It may be preferable for some accounts, such as your Google Account, to enable several MFA options, so it’s still possible to log into accounts without using your hardware key.
        1. If a service offers multiple MFA options, we recommend choosing either a Yubikey or Authenticator app rather than SMS.
    1. When possible, accounts should be created for each individual person who uses a system, rather than using shared authentication credentials.
1. Passwords
    1. Passwords used for Caktus-related accounts should be generated programmatically (1password, pwgen, etc.) by tools that create random passwords and should be at least eight characters long. Here’s an example using the command line tool: pwgen --secure --symbols --numerals 12
    1. Passwords should be stored in Caktus’ Enterprise 1password account. If this isn’t possible, then Keepass or written on paper is acceptable. If they are written down on paper, the password should be kept in a secure location and should not be kept with other authentication information such as what the password is for or a user name.
    1. Passwords should only be communicated via secure channels of communication (1Password) or in person, and with other authentication information (e.g. user name) sent via a second means of secure communication.
    1. Passwords should never be stored or transmitted in plain text.
1. Personal account and data restrictions
    1. Accessing Caktus data from personal accounts is prohibited. Data and account privileges should never be shared with personal accounts. For example, never share Caktus Google Drive data with your personal Google account.
    1. Using your Caktus email address with accounts intended for personal use is prohibited. Accounts associated with Caktus email addresses should only be used for Caktus-related work.
    1. Web access to personal accounts (e.g. Gmail) is only allowed from a separate browser profile to help mitigate accidental cross-pollination of data.
    1. Storing Caktus and personal data within the same 3rd party account (e.g. Dropbox) is prohibited, except for open source repositories, package managers, and CI tools.
    1. You may use personal accounts to facilitate auxiliary business processes, such as booking a reimbursable flight on Delta, so long as the account will never have access to client or Caktus IP.
### Sharing secrets with Caktus
Whenever possible, we try to avoid communicating passwords (or other secrets) directly. Some ways to avoid it:

* Grant access to us via our existing accounts. For example, give our Github accounts access to your repositories on Github, or share Google Drive documents with our Google accounts (our xxx@caktusgroup.com addresses).
* Create new accounts under our email addresses, then let us set our own passwords, possibly using the usual “reset password” mechanism.

Both of these methods preserve security by not sharing a password at all.

But sometimes it’s unavoidable that you need to send us information that needs to be kept secret. Here are our preferred ways of doing that, in order:

1. Share with us through a secure system like 1Password (our preference), PassPack, or anything similar to those. If you don't have an account yet, you can share a secret with us via LastPass as follows:
    1. Navigate to [https://lastpass.com/create_account.php](https://lastpass.com/create_account.php) and create a new account
    1. Once you're logged in, create a new "Secure Note" via the button in the bottom right corner
    1. Copy and paste your secret into the note (this is generally easier than attaching the file, which requires a "binary extension" on some computers)
    1. Under "Advanced Settings," check the box titled "Require Password Reprompt"
    1. Give the note a name and save it
    1. Click on the share/people icon on the new note
    1. Share it with the email address of the individual at Caktus you are corresponding with
    1. You may be prompted to verify your own email address, if you haven't yet
1. Share with us using the site [https://onetimesecret.com](https://onetimesecret.com/) (for passwords or other secrets) or[ https://send.firefox.com](https://www.mozilla.org/en-US/) (for files). It works like this:
    1. Go to the site, type anything you want in a text field (e.g. password, secret key, whatever) or upload a file, and save it. A link will be displayed on the next page that you can email to us. We immediately click on the link when we get it, and the secret (or file) will be shown to us and immediately deleted from the site. Since it’s deleted as soon as we read it, nobody else can read it, even if they somehow get access to the email message with the link. Or if someone does that and beats us to it, when we try to read it we’ll find that it’s already deleted, know that something bad has happened, and let you know to immediately change the password.
    1. It’s still a good idea to put in just the password or secret, and not enough other information for someone who got hold of what you put on the site to know what that password is for.
If you don’t want to use any of these mechanisms, talk to us and we’ll work out something.

## Server Maintenance
1. Regular maintenance of supported servers will be performed including regular security updates using automated tools.
1. Encryption
    1. Encryption will always be enabled for confidential data in transit through SSH and HTTPS connections.
    1. Servers as required have their data secured at rest using GPG encrypted files, and LUKS whole disk encryption.
1. Backups and Logs
    1. Backups are stored on a secure and updated FreeNAS computer stored in a locked server closet.
    1. Logs are stored centrally for each computer including security related daemon logs & login details.
    1. All backups and logs are stored for a minimum of 12 months.
## Web Application Security
The Caktus [Security Policies and Best Practices](http://caktus.github.io/caktus-security/) should be followed on all software development projects developed by Caktus.

## Special Procedures
### Protected Health Information (PHI)
From time to time Caktus may take on projects that are required to be HIPAA compliant in that they involve Personal Health Information (PHI). In these instances there are a number of project specific best practices that must be adhered to in order to comply with the letter and intent of the HIPAA regulations and maintain patient data in the strictest confidence. The overall goals of these best practices are to not access any PHI unless doing so is unavoidable for one's job function and if access PHI is unavoidable, transferring, storing, and accessing it in a secure way.

**Project Specific Risk Analysis** 

First, a project specific risk analysis should be created in consultation with the HIPAA compliance officer, project System Administrator, and project Development Lead. This document should document all possible natural, environmental, and human threats to the security of PHI and how they will be addressed. Furthermore, if it is decided not to address a possible PHI threat, then justification must be provided. This Risk Analysis should be updated annually for ongoing projects or whenever there is a significant change to the project scope or management of PHI.

**Authorization** 

A list of Caktus workers and Caktus directed third parties on the project with access to PHI will be maintained by the Project Manager. All changes in the list must be approved in writing by the HIPAA compliance officer. This will include adding new team members as well as removing team members as soon as their job responsibilities no longer require access to PHI. Included in this notification should be the specific reasons and details of the person’s access to PHI. The HIPAA compliance officer will review the employee’s file for significant lapses in respect for client’s confidentiality before approving their access to any PHI.

**Sanctions** 

If project team members are found to be out of compliance with HIPAA compliant PHI procedures, they will be immediately removed from the project using the termination procedure and the incident will be reported to Human Resources for further evaluation.

**Training** 

All team members on projects related to PHI must complete a training module if they have not completed a training in the last year. If someone currently with access to PHI has not completed training within the last year, they must also complete a training module. The completion of trainings should be shared with the HIPAA compliance officer for their record keeping.

**Communication & Storage** 

PHI should only be communicated over a network via SSH and HTTPS connections. Email, Dropbox, Google Apps, and chat should never be used to communicate PHI. PHI should not be transmitted via or stored on portable physical media (CDROM, DVD, portable hard drive, USB jump drive, SD card, etc.) due to the possibility of loss and the details of cleaning or disposing of the media after use. The only media that should hold PHI are encrypted workstation hard drives, backup storage, and media controlled by approved third party hosting providers.

Shared and personal devices should never be used to access systems containing PHI. If mobile devices are needed for application testing, they should be exclusive to the project and their storage wiped clean once they are no longer needed for the project.

All paper project notes and communications relating to the system used in the development process should be kept locked up when not in use and shredded once they are no longer needed.

Business Associates Agreements with Subcontractors

All subcontractors with access to PHI including independent contractors, hosting providers, and communications providers must sign BAA agreements with Caktus prior to having access to any PHI.

Special Development Practices

The following best practices are specific to projects handling PHI in addition to the standard [Security Policies and Best Practices](http://caktus.github.io/caktus-security/).

1. Automatic logoff
1. Unique user IDs
1. Password recovery procedures
1. Audit controls
1. Isolation of clearinghouse functionality
1. Do not email production errors
    1. Forms contain PHI -> Requests contain -> Email contains PHI
    1. Log errors and send email notifications of errors
1. “Personal Identifying Information,” as defined by the North Carolina Identity Theft Protection Act of 2005. This includes employer tax ID numbers, drivers' license numbers, passport numbers, SSNs, state identification card numbers, credit/debit card numbers, banking account numbers, PIN codes, digital signatures, biometric data, fingerprints, passwords, and any other numbers or info that can be used to access a person's financial resources. 
1. “Protected Health Information” as defined by HIPAA 
1. Student “education records,” as defined by the Family Educational Rights and Privacy Act (FERPA) 
1. “Customer record information,” as defined by the Gramm Leach Bliley Act (GLBA) 
1. “Card holder data,” as defined by the Payment Card Industry (PCI) Data Security Standard 
1. Confidential “personnel information,” as defined by the State Personnel Act Information that is deemed to be confidential in accordance with the North Carolina Public Records Act 
## Security Team
### Purpose
Security can take many forms: from PCI compliance, server firewalls, and encryption to security patches and incident response guidelines. Best practices and procedures can guide development to build secure web applications. The Caktus Security Team creates team best practices and procedures, facilitates knowledge sharing, and helps with responding to security incidents. We strive to:

* Proactively research and implement improvements to further Caktus’ security procedures
* Maintain the Caktus Security Policy and best practices
* Monitor for security exploits, review severity, and inform teams
* Recommend solutions to team-raised security questions
* Guide teams through security incident reports and responses
### Process
* Triage backlog into 2 lanes:
    * Immediate Support
    * Ongoing Initiatives
* Weekly 10-minute standups
    * Determine if any newly added issues should be prioritized
    * Check-in on WIP issues (always limit to 4)
### Policy Maintenance and Compliance
1. Maintenance and Compliance
    1. The Security Team maintains the policies and procedures related to day to day security and incident responses at Caktus. They are also responsible for the implementation of the policies at Caktus and compliance with relevant regulations.
    1. Caktus will verify compliance to this policy through various methods, including but not limited to, internal and external audits and feedback to the Security Team.
1. Risk Analysis
    1. Quarterly, a cross functional team including representatives from Human Resources, Systems Administration, Software Development, and Operations will meet to review the current policies and procedures and their implementation.
    1. Annually the [HealthIT.gov risk assessment tool](https://www.healthit.gov/topic/privacy-security-and-hipaa/security-risk-assessment-tool) will be used to create a new risk assessment document.
    1. The systems administration team is determined to be notified about new security threats by following the security lists and Common Vulnerabilities and Exposures (CVE) announcements related to the specific software stack employed by projects at Caktus.
