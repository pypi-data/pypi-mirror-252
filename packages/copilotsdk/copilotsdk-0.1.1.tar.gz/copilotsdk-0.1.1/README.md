# Webex Troubleshooting Copilot

This repository contains the Copilot SDK for Webex Troubleshooting Copilot. Copilot is an AI programming assistant that helps developers with troubleshooting and solutions

## Brief Introduction

Webex Troubleshooting Copilot is a powerful tool that assists developers in troubleshooting their Webex applications. 

## Disclaimers
- This SDK is intended for Cisco internal use only, you should uninstall it if you are not Cisco employees
- The API is opt to change in near future without any precaution or notification

## Example of Using Copilot SDK

To use the Copilot SDK in your project, follow these steps:

1. Install the Copilot SDK package:
```
pip install copilotsdk
```

2. Import the Copilot module into your code:
```python
    import asyncio
    import copilotsdk
```

3. Initialize the Copilot instnace:
```python
    async def _test_start(): 
        copilot = WebexCopilot("<<host-address>>")
        await copilot.start()
        await asyncio.wait_for(copilot.ready, timeout=100)

    asyncio.run(_test_start())
```

4. Fast Anomaly Check:
```python
    report = await copilot.generate_anomaly_report("<<link>>")
```
The paramerter can local file (current_log.txt or last_run_current_log.txt) or a link to control hub or jira.

5. Deep Anomaly Analysis
With the fast check result, you can continue to call generate_anomaly_deep_analysis_report for failure details:

```python
    report = await copilot.generate_anomaly_deep_analysis_report("7159edd516f0b33981d7be140cd114628b902f5866c806fcf3be79f10ac9de47","join meeting","callid-e80f6b25-519f-4ad6-a4ba-6aa4ccff34ff.txt")
```

6. Do text classification