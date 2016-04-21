Supported Browsers and Devices
##############################

There are hundreds of browsers that have been released over the course of the Web’s lifetime. There are thousands of distinct versions between all of these different browsers. We will not be testing every project across thousands of individual test browsers, so we need to narrow down the selection to a concise set of browser versions that represent the largest possible swath of the target user base.

Keep in mind that depending on the project the target user base will be made of people from different demographics, from different areas, with distinct technological patterns. The best set of browser versions to test may differ between projects based on the understanding of this user base.

The rule of thumb is: the latest two versions of Major Browsers. There are some special cases related to mobile browsers.

Major Browsers
==============

We consider the following vendors to produce “Major Browsers” for the purposes of determining a default set of support browsers.

- Google (Chrome)
- Mozilla (Firefox)
- Microsoft (Internet Explorer, Edge)
- Apple (Safari, Mobile Safari)

Grading System
==============

We will rate browsers and devices by a simple grading system. This helps to
categorize the approach to support for each browser. As any release ages, its
grade will be reduced.

=====   ========================================================================================
Grade   Level of Support Offered
=====   ========================================================================================
A       Supported by default in all new projects.
B       Supported by default, but allowed to present degraded experiences based on unsupported features.
C       Not supported by default. If required in a project, additional time must be estimated. Support may be degraded.
D       Not supported by default. Will strongly discourage support at client request.
=====   ========================================================================================

Current Grade Chart
===================

Browsers
--------

=========   ===================     ===========     =====
Vendor      Browser                 Version(s)      Grade
=========   ===================     ===========     =====
Google      Chrome                  50              **A**
Google      Chrome                  49              **A**
Mozilla     Firefox                 45              **A**
Mozilla     Firefox                 44              **A**
Apple       Safari                  9               **A**
Apple       Safari                  8               B
Apple       Safari                  7               C
Apple       Safari Mobile           9               **A**
Apple       Safari Mobile           8               B
Google      Chrome for Android      49              B
Google      Android Browser         4.2-4.3         C
Google      Android Browser         2.3-4.1         C
Microsoft   Edge                    14              **A**
Microsoft   Edge                    13              B
Microsoft   Edge                    12              B
Microsoft   Internet Explorer       11              **A**
Microsoft   Internet Explorer       10              C
Microsoft   Internet Explorer       9               C
Microsoft   Internet Explorer       8 and below     D
=========   ===================     ===========     =====

Update Policy
=============

This policy and the gradings should be reviewed at least quarterly by QA or development, or when
beginning a new project and commiting to the support levels defined by this document.
