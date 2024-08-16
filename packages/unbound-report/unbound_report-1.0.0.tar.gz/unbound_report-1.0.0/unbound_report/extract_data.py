from robot.api import ExecutionResult, ResultVisitor
from datetime import datetime
from robot.result import For
from robot.model import Keyword

time_format = "%Y%m%d %H:%M:%S.%f"

class SuiteDataExtractor(ResultVisitor):
    def __init__(self):
        self.suite_stats = []
        self.test_stats = []
        self.test_duration_stats = []
        self.suite_data = []
        self.error_stats = {}
            
    def visit_statistics(self, stats):
        self.test_stats = {
            'total': stats.total.total,
            'passed': stats.total.passed,
            'failed': stats.total.failed,
            'skipped': stats.total.skipped
        }
        
    def visit_result(self, result):
        for suite in result.suite.suites:
            suite.visit(self)
        
        self.suite_stats = {
            'total': len(result.suite.suites),
            'passed': len([suite for suite in result.suite.suites if suite.passed]),
            'failed': len([suite for suite in result.suite.suites if suite.failed]),
            'skipped': len([suite for suite in result.suite.suites if suite.skipped])
        }
        
        result.statistics.visit(self)
        
    def end_result(self, result):
        return super().end_result(result)
    
    def visit_errors(self, errors):
        return super().visit_errors(errors)

        
    def collect_keywords(self, keyword):
        """Recursively collect keyword data, including nested keywords."""
        keyword_data = {
            'name': keyword.name,
            'status': keyword.status,
            'starttime': datetime.strptime(keyword.starttime, time_format).strftime("%d %b %Y, %H:%M:%S") if keyword.starttime else None,
            'endtime': datetime.strptime(keyword.endtime, time_format).strftime("%d %b %Y, %H:%M:%S") if keyword.endtime else None,
            'duration': keyword.elapsedtime/1000 if keyword.elapsedtime else 0,  
            'status_message': keyword.message if keyword.status == 'FAIL' else '',
            'args': keyword.args, 
            'doc': keyword.doc, 
            'messages': [msg.message for msg in keyword.messages],  
            'keywords': []  
        }
        
        
        for kw in keyword.body:
            if kw.type == 'KEYWORD':
                keyword_data['keywords'].append(self.collect_keywords(kw))
                
        return keyword_data


    def visit_suite(self, suite):
        
        suite_data = {
            'name': suite.name,
            'status': suite.status,
            'total': len(suite.tests),
            'passed': 0,
            'failed': 0,
            'skipped': 0,            
            'starttime': suite.starttime,
            'endtime': suite.endtime,
            'duration': suite.elapsedtime/1000,
            'setup': {},
            'teardown': {},
            'tests': []
        }
        
        if suite.setup:
            suite_data['setup'] = {
                'name': suite.setup.name,
                'status': suite.setup.status,
                'starttime': datetime.strptime(suite.setup.starttime, time_format).strftime("%d %b %Y, %H:%M:%S") if suite.setup.starttime else None,
                'endtime': datetime.strptime(suite.setup.endtime, time_format).strftime("%d %b %Y, %H:%M:%S") if suite.setup.endtime else None,
                'duration': suite.setup.elapsedtime/1000 if suite.setup.elapsedtime else 0, 
                'status_message': suite.setup.message if suite.setup.status == 'FAIL' else ''
            }
            
        if suite.teardown:
            suite_data['teardown'] = {
                'name': suite.teardown.name,
                'status': suite.teardown.status,
                'starttime': datetime.strptime(suite.teardown.starttime, time_format).strftime("%d %b %Y, %H:%M:%S") if suite.teardown.starttime else None,
                'endtime': datetime.strptime(suite.teardown.endtime, time_format).strftime("%d %b %Y, %H:%M:%S") if suite.teardown.endtime else None,
                'duration': suite.teardown.elapsedtime/1000 if suite.teardown.elapsedtime else 0,  
                'status_message': suite.teardown.message if suite.teardown.status == 'FAIL' else ''
            }
        
        count_passed = 0
        count_failed = 0
        count_skipped = 0
        
        for test in suite.tests:
            if test.status == 'PASS':
                count_passed += 1
            elif test.status == 'FAIL':
                count_failed += 1
            elif test.status == 'SKIP':
                count_skipped += 1
            
            keywords_data = []
            for keyword in test.body:
                if keyword.type == 'KEYWORD':
                    keywords_data.append(self.collect_keywords(keyword))
            
            data = {
                'id': test.id,
                'name': test.name,
                'status': test.status,
                'starttime':datetime.strptime(test.starttime, time_format).strftime("%d %b %Y, %H:%M:%S"),
                'endtime': datetime.strptime(test.starttime, time_format).strftime("%d %b %Y, %H:%M:%S"),
                'duration': test.elapsedtime/1000,
                'tags': test.tags,
                'status_message': test.message if test.status == 'FAIL' else None,
                'keywords': keywords_data
            }                
            suite_data['tests'].append(data)
            
            # Collect error statistics
            if test.status == 'FAIL':
                error_message = suite.name+': "'+test.message+'"'
                if not self.error_stats.get(error_message):
                    self.error_stats[error_message] = []
                self.error_stats[error_message].append(data)
            

        suite_data['passed'] = count_passed
        suite_data['failed'] = count_failed
        suite_data['skipped'] = count_skipped
        self.suite_data.append(suite_data)
        
    def get_suite_stats(self):
        return self.suite_stats
    
    def get_test_stats(self):
        return self.test_stats
    
    def get_test_duration_stats(self):
        return self.test_duration_stats

    def get_suite_data(self):
        return self.suite_data
    
    def get_error_stats(self):
        return self.error_stats