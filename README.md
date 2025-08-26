run_leebounds(df) defines a Python function that acts as a wrapper around Stata’s leebounds command. Instead of typing Stata code manually, you call this Python function and it automates the setup + call to Stata.

In an RCT with attrition (missing outcomes), treatment assignment is random, but who stays in the study (S=1) may depend on treatment. This creates selection bias, since treatment and control may have different follow-up rates 
(if treated participants are more likely to drop out, the observed mean outcome among treated isn’t representative of all treated.)

Lee Bounds - 
1. Compare attrition rates between treated vs control. (Suppose treated has higher attrition (more missing outcomes))

2. Trim the upper tail of outcomes in the group with lower attrition, so that the two groups have the same effective sample size. - This balances out the selection effect.

3. Compute treatment effect using trimmed samples. Trim the lower tail instead → gives the Lee upper bound.

