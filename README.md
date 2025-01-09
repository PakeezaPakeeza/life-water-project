## Steps to Set Up the Project

### 1. Download the `trp` Library Zip File
- Clone or download the `.zip` file from the GitHub repository:
  - Repository URL: `<Your GitHub Repository URL>`
- Ensure you have the `textract-trp-layer.zip` file downloaded locally.

### 2. Upload the Layer to AWS Lambda
1. Go to **AWS Console → Lambda → Layers**.
2. Click **Create Layer** and upload the `textract-trp-layer.zip` file.
3. Select the runtime (e.g., Python 3.9) and note the Layer ARN.

### 3. Create an IAM Role for the Lambda Function
1. Go to **IAM Console → Roles → Create Role**.
2. Select **Lambda** as the trusted entity.
3. Attach the following policies:
   - **AmazonS3FullAccess** (or restrict access to the `ngo1` bucket).
   - **AmazonTextractFullAccess**.
   - **CloudWatchLogsFullAccess**.
4. Complete the role creation and note the Role ARN.

### 4. Create a Lambda Function
1. Go to **AWS Console → Lambda → Create Function**.
2. Choose **Author from scratch**:
   - Function name: `extract_Text_From_Images`
   - Runtime: Python 3.9
   - Execution role: Select the previously created role.
3. Upload your function code from the repository.

### 5. Add the Lambda Layer
1. In the **Lambda Console**, go to your function.
2. Select the **Layers** section → **Add a layer**.
3. Choose **Custom layer** → Select the uploaded `textract-trp-layer`.

### 6. Configure S3 Trigger
1. Go to the **S3 Console** → `ngo1` bucket.
2. Under **Properties → Event Notifications**, create a new event:
   - **Event Name**: `gptmade`
   - **Event Type**: **PUT**
   - **Prefix**: `input/`
   - **Suffix**: `.jpeg` (or modify as per your input files).
   - **Destination**: Select the Lambda function (`extract_Text_From_Images`).

### 7. Adjust Lambda Timeout
- If processing large images or documents, **increase the timeout** for the Lambda function:
  1. Go to **Lambda Console → Configuration → General Configuration**.
  2. Set **Timeout** to a higher value (e.g., 1 or 2 minutes).

---

## Testing the Setup

### Upload a Test Image:
- Upload a `.jpeg` file to the `input` folder of the `ngo1` S3 bucket.

### Check Lambda Execution:
- Navigate to the **CloudWatch Logs** associated with your Lambda function to verify the processing.

### Verify Output:
- Check the `output` folder in the `ngo1` bucket for the generated `.json` file containing the processed data.


