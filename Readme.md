# Repository Purpose

## Agent Creation for Onboarding

The goal is to create an agent that helps guide people during their onboarding process. To avoid building the agent from scratch, we will use [IBM's Prompt Lab](https://www.ibm.com/docs/en/watsonx/saas?topic=solutions-prompt-lab). This tool will allow us to create and train an agent with specific onboarding content. The idea  is to use [cloud.ibm.com](https://cloud.ibm.com) and the `granite-13b-chat-v2` model to create a prompt session, feed it with data, and enable it to respond to training and/or onboarding questions.

## Integration with External Applications

To integrate the prompt with external applications, the REST API of [cloud.ibm.com](https://cloud.ibm.com) will be used. Follow these steps:

1. **Create an API Key**:  
   Go to [IBM Cloud API Keys](https://cloud.ibm.com/iam/apikeys) to create an API key.

2. **Generate a JWT**:  
   After creating the API key, generate a JWT by following the instructions [here](https://cloud.ibm.com/docs/watson?topic=watson-iam#iam) to connect to the APIs.
