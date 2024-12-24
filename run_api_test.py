import os
import conftest

def run_tests():
    """Run both Playwright and API tests and generate reports."""
   # os.system("pytest test_api/test_bvt_doa.py -m api -vv --html=reports/BuildVerificationTest.html --self-contained-html")
    #conftest.pytest_html_report_title(report,title="This is my report name")
    os.system("pytest tests/api/bvt/ -vv --self-contained-html ")
    #os.system("pytest test_api/test_demo.py -vv --html=reports/BuildVerificationTest.html --self-contained-html --tracing on")
if __name__ == "__main__":
    run_tests()
