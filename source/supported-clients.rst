Supported Browsers
##############################

There are hundreds of browsers that have been released over the course of the Web’s lifetime. There are thousands of distinct versions between all of these different browsers. We will not be testing every project across thousands of individual test browsers, so we need to narrow down the selection to a concise set of browser versions that represent the largest possible swath of the target user base.

Keep in mind that depending on the project the target user base will be made of people from different demographics, from different areas, with distinct technological patterns. The best set of browser versions to test may differ between projects based on the understanding of this user base.

Caktus takes a progressive enhancement approach to HTML development. This means we will provide the best visual rendering to users with modern browsers. Old browsers that lack support for specific features will gracefully degrade, maintaining necessary functionality while losing the compatibility to adapt new cosmetic features only supported in newer versions.
 
Caktus conducts quality assurance to verify that the website performs and functions according to the agreed upon project specifications. This step includes time to correct bugs and issues discovered by the quality assurance (QA) process.
 
Unless otherwise specified, Caktus will test on the following browsers to ensure that the website functions and renders correctly. The following browsers / platforms will be supported (current version and previous version at the time of launch):

- Chrome 
- Firefox
- Internet Explorer (11 only)
- Edge 
- Safari
- iOS Safari


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

=========   ===================     ===========              =====
Vendor      Browser                 Version(s)               Grade
=========   ===================     ===========              =====
Google      Chrome                  Most Recent              **A**
Google      Chrome                  Latest Previous          **A**
Mozilla     Firefox                 Most Recent              **A**
Mozilla     Firefox                 Latest Previous          **A**
Apple       Safari                  Most Recent              **A**
Apple       Safari                  Latest Previous            B
Apple       Safari Mobile           Most Recent              **A**
Apple       Safari Mobile           Latest Previous            B
Google      Chrome for Android      Most Recent              **A**
Microsoft   Edge                    Most Recent              **A**
Microsoft   Edge                    Latest Previous            B
Microsoft   Internet Explorer       Most Recent              **A**
=========   ===================     ===========              =====
