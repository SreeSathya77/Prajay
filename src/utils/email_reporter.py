import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime
import os
from typing import List, Optional, Dict
from .logger import logger
from .html_reports_generator import HTMLReportGenerator
from .environment import is_running_in_docker


class EmailReporter:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.recipient_emails = os.getenv('RECIPIENT_EMAILS', '').split(',')

    def send_report(self, results: Dict, report_files: Optional[List[str]] = None) -> bool:
        """Send test results via email only when running in Docker"""
        if not is_running_in_docker():
            logger.info("Skipping email report - not running in Docker")
            return True

        try:
            if not all([self.smtp_username, self.smtp_password, self.sender_email, self.recipient_emails]):
                logger.warning("Email configuration incomplete - skipping email report")
                return False

            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = ', '.join(self.recipient_emails)

            # Create subject with pass/fail status and environment info
            status = "✅ PASSED" if results.get('failed', 0) == 0 else "❌ FAILED"
            msg['Subject'] = f"[DOCKER] QMaasTestLab Execution Report [{status}] - {datetime.now().strftime('%Y-%m-%d %H:%M')}"

            # Generate and add HTML report
            html_report = HTMLReportGenerator.generate_full_report(results)
            msg.attach(MIMEText(html_report, 'html'))

            # Attach report files
            if report_files:
                for file_path in report_files:
                    if os.path.exists(file_path):
                        with open(file_path, 'rb') as f:
                            part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
                            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                            msg.attach(part)

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)

            logger.info("Test report email sent successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to send test report email: {str(e)}", exc_info=e)
            return False