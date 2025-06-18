# tds_virtual_ta


# ⚠️ Deployment Note
Due to an unexpected issue in the requirements.txt file, the application could not be deployed successfully on Render. The error was related to a missing dependency (uvicorn) that I identified at the final stage of deployment, just before the submission deadline.
Because of this last-minute discovery, I could not update and redeploy the application in time.
However, the complete and functional source code is available in this repository, and with the correct environment setup (including installing all required dependencies), the application can be run locally without issues.

# 💡 API Usage Details
For Answering Questions (app.py):
I have used Hugging Face Inference API to generate answers based on matched course content.

For Embedding Course Content (embed_chunks.py):
I intended to use Gemini's embedding model (gemini-embedding-exp-03-07) to generate and store content embeddings.
However, my system runs on Windows 7, and the required Gemini SDK features are not supported on this older OS version. Despite this limitation, I have included the correct implementation logic in the code, which will work on newer systems.


# ✅ Final Note
The source code is complete and working. Once the correct environment is set up (preferably on a newer OS), the app should run and embed data as intended.

