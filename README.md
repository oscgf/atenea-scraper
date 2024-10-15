# UC3M Job Offers Scraper 🚀

This project is a web scraper that fetches the latest job offers from the UC3M (Universidad Carlos III de Madrid) website. It checks for new job offers and sends an email notification when new offers appear or existing offers are updated.

## Features
- Scrapes job offers from UC3M's job offers page.
- Detects new job offers or changes in the offer's status.
- Sends an email notification with the details of new offers.
- Supports running via GitHub Actions for automation.

## Prerequisites

### Local Setup
- **Python 3.x**: Make sure you have Python 3.x installed on your local machine.
- **Gmail Account** (if using Gmail for notifications):
  - You will need to generate an **App Password** for your Gmail account. [Follow these instructions](https://support.google.com/mail/answer/185833) to generate an App Password.
  
### GitHub Setup
- **GitHub Account**: You'll need a GitHub account to use GitHub Actions.
- **GitHub Secrets**: Set up the necessary secrets in your GitHub repository to securely manage email credentials (more information below).

## Installation

### 1. Clone the Repository
First, clone this repository to your local machine:

```bash
git clone https://github.com/oscgf/atenea-scraper.git
cd atena-scraper
```

### 2. Install Dependencies
Install the necessary Python dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
For local development, create a .env file in the project root with the following content:

```bash
SENDER_EMAIL=your-email@gmail.com
PASSWORD=your-app-password
RECEIVER_EMAIL=recipient-email@gmail.com
```

- `SENDER_EMAIL`: The email address that will send the notifications.
- `PASSWORD`: Your Gmail App Password. [Instructions for setting up App Passwords](https://support.google.com/mail/answer/185833).
- `RECEIVER_EMAIL`: The email address that will receive job alerts.

### 4. Running the Scraper Locally
You can run the scraper manually by executing the Python script:

```bash
python your_script.py
```

## GitHub Actions Automation
This project is also configured to run automatically using GitHub Actions. The GitHub Actions workflow is located in `.github/workflows/scraper.yml`.

### 1. Setup GitHub Secrets
In order to send email notifications using GitHub Actions, you need to configure the following secrets in your GitHub repository:

1. Go to your **GitHub repository**.
2. Click on the **Settings** tab.
3. On the left sidebar, go to **Secrets and variables > Actions**.
4. Click **New repository secret** and add the following secrets:

 - `SENDER_EMAIL`: Your sender email address.
 - `PASSWORD`: Your email app password.
 - `RECEIVER_EMAIL`: The email address that will receive notifications.
 
If you want to commit and push automatically the changes when the job offers ara updated, ensure that `GITHUB_TOKEN` is enabled and has write permissions:

5. Navigate to **Settings > Actions > General**.
6. Scroll down to **Workflow permissions**.
7. Ensure **"Read and write permissions"** is selected for `GITHUB_TOKEN`.
8. Also, check **"Allow GitHub Actions to create and approve pull requests"** if you plan to use that in the future.

### 2. Running the Workflow Manually
To run the workflow manually (in case you don't want to wait for the scheduled time):

1. Go to the **Actions** tab in your GitHub repository.
2. Select the **Job Alert Email** workflow.
3. Click the **Run workflow** button on the right side to manually trigger the job.

### 3. Scheduled Workflow
The scraper is configured to run every day at 9:00 AM UTC. You can change this schedule by modifying the `cron` expression in `.github/workflows/scraper.yml`:

```bash
on:
  schedule:
    - cron: '0 9 * * *'  # Change this to your preferred schedule
```

## Troubleshooting

### Enabling Gmail App Passwords
If you are using a Gmail account to send email notifications, you will need to enable an App Password. This is a security measure by Google to allow third-party apps to send emails securely.

1. **Enable 2-Step Verification** for your Gmail account: [Google 2-Step Verification](https://myaccount.google.com/security-checkup).
2. **Generate an App Password**: Go to [App Passwords](https://myaccount.google.com/apppasswords), choose "Mail" as the app, and "Other" as the device. Copy the generated password and use it in your `.env` file or GitHub Secrets.

### Debugging Locally
If you encounter any issues while running the scraper locally, make sure:

- Your email credentials are correct in the `.env` file.
- You are not blocking SMTP connections (some networks may block ports).

You can also review logs in GitHub Actions for any issues with the automation process.

## Contributions
Feel free to contribute to this project or suggest new features!