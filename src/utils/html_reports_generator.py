from typing import Dict, List
from datetime import datetime
from .test_summary import TestSummaryGenerator


class HTMLReportGenerator:
    @staticmethod
    def generate_full_report(results: Dict) -> str:
        """Generate complete HTML report with file-wise summary"""
        # Generate file-wise summary
        file_results = TestSummaryGenerator.group_tests_by_file(results.get('test_cases', []))
        file_summary_table = TestSummaryGenerator.generate_summary_table(file_results)

        return f"""
        <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h2>Test Execution Summary</h2>
                <p>Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

                <h3>Test Results by Features</h3>
                {file_summary_table}

                <h3>Failed Tests Details</h3>
                {HTMLReportGenerator.generate_failed_tests_table(results.get('test_cases', []))}
            </body>
        </html>
        """

    @staticmethod
    def generate_failed_tests_table(test_cases: List[Dict]) -> str:
        """Generate HTML table for failed tests"""
        failed_tests = [test for test in test_cases if test['outcome'] == 'failed']

        if not failed_tests:
            return "<p style='color: green;'>No failed tests! 🎉</p>"

        rows = []
        for test in failed_tests:
            # Extract file name and module name
            file_path = test['nodeid'].split('::')[0]
            file_name, module_name = TestSummaryGenerator.get_file_and_module_name(file_path)

            rows.append(f"""
                <tr>
                    <td style="padding: 8px;">{module_name}</td>
                    <td style="padding: 8px;">{file_name}</td>
                    <td style="padding: 8px;">{test['name']}</td>
                    <td style="padding: 8px;">{test['nodeid']}</td>
                    <td style="padding: 8px; color: red;">{test.get('error', 'No error message')}</td>
                </tr>
            """)

        return f"""
        <table border="1" style="border-collapse: collapse; width: 100%;">
            <tr style="background-color: #f2f2f2;">
                <th style="padding: 8px;">Module</th>
                <th style="padding: 8px;">File Name</th>
                <th style="padding: 8px;">Test Name</th>
                <th style="padding: 8px;">Test Path</th>
                <th style="padding: 8px;">Error</th>
            </tr>
            {''.join(rows)}
        </table>
        """