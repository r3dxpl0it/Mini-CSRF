### curly-robot
A Minimal CSRF Scanner Customized for Cross-Site-Request-Forgery it Spiders the target website to find all pages , forms , parameter values. Generates random token strings and sets parameter values accordingly. Submits each form with the crafted tokens and Finds out if the tokens are sufficiently protected.
and at the end Generates custom proof of concepts after each successful request and subsequent discovery. it is maily used for POST CSRF Vulnerabilities. The Idea and Credit Belong to the Project "https://github.com/theInfectedDrake/XSRFProbe" and this code is a Minimal-LAMBADA of the XSRFProbe with Multiple Custom changes. 

### Versions 
There Will be 3 Versions Here : 
 - The Original Converted XSRFProbe (curly.py)
 - Optimized XSRFProbe (robot.py)
 - The XFrameWork CSRF Plugin (Which is Based on XSRFProbe) (curly-robot.py)
