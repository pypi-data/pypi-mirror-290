import os
import argparse
from unbound_report import __version__
from unbound_report.extract_data import SuiteDataExtractor
from robot.api import ExecutionResult
from jinja2 import Environment, FileSystemLoader

def render_keywords(keyword):
    symbol = ""
    if keyword['status'] == 'PASS':
        symbol = """
        <div
            class="w-6 h-6 rounded-full bg-green-500 flex items-center justify-center text-white">
            <i class="fas fa-check"></i>
        </div>
        """
    elif keyword['status'] == 'FAIL':
        symbol = """<div
            class="w-6 h-6 rounded-full bg-red-500 flex items-center justify-center text-white">
            <i class="fa-solid fa-xmark"></i>
        </div>
        """
    elif keyword['status'] == 'SKIP':
        symbol = """<div
            class="w-6 h-6 rounded-full bg-yellow-500 flex items-center justify-center text-white">
            <i class="fa-solid fa-forward"></i>
        </div>
        """
    else:
        symbol = """<div
            class="w-6 h-6 rounded-full bg-blue-500 flex items-center justify-center text-white">
            <i class="fas fa-check"></i>
        </div>
        """
        
    html = f"""

        <div class="flex flex-col">
            <div class="accordion-header flex">
                <div class="w-8 h-8">
                    {symbol}
                </div>
                <div>
                    <span>{keyword['name']}</span>
                    {''.join(f'<span class="italic">{a}</span>' for a in keyword['args'])}
                    <span class="inline-flex items-center rounded-md bg-gray-50 px-2 py-1 text-xs font-medium text-gray-600 ring-1 ring-inset ring-gray-500/10">{keyword['duration']} s</span>
                </div>
                <div class="ml-2">
                    <svg class="w-6 h-6 text-gray-500 accordion-icon" fill="none" stroke="currentColor"
                        viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M19 9l-7 7-7-7"></path>
                    </svg>
                </div>
            </div>
            <div class="accordion-content ml-6">
                <div class="flex items-start my-1">
                    {''.join(f'<div class="text-white bg-yellow-300 rounded py-1/2 px-1 mr-2">Doc</div>{keyword["doc"]}<br>' if keyword['doc'] else '')}
                </div>
                <div class="flex items-start my-1">
                    {''.join(f'<div class="text-white bg-yellow-300 rounded py-1/2 px-1 mr-2">Message</div>{m}<br>' for m in keyword['messages'])}
                </div>
                {f'<div class="flex my-1"><div class="text-white bg-red-500 rounded py-1/2 px-1 mr-2">Error</div>{keyword["status_message"]}<br></div>' 
                if keyword['status_message'] != '' else ''
                }
                
                {''.join([render_keywords(kw) for kw in keyword['keywords']])}
            </div>
        </div>
        
    """
    return html

def generate_report(output_file, log_file, save_path):

    # Extract data
    result = ExecutionResult(f'{output_file}')
    extractor = SuiteDataExtractor()
    result.visit(extractor)
    suite_stats = extractor.get_suite_stats()
    test_stats = extractor.get_test_stats()
    error_stats = extractor.get_error_stats()
    test_duration_stats = extractor.get_test_duration_stats()
    suite_data = extractor.get_suite_data()
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')))
    env.globals.update(render_keywords=render_keywords) 
    template = env.get_template('report.html')
    html_report = template.render(suite_stats=suite_stats,
                                test_stats=test_stats, 
                                test_duration_stats=test_duration_stats,
                                suite_data=suite_data,
                                error_stats=error_stats,
                                log_file=log_file)

    # Write the report to an HTML file
    with open(f'{save_path}', 'w') as f:
        f.write(html_report)

    full_path = os.path.abspath(f'{save_path}')
    print(f"Your report has been generated successfully and is saved at {full_path}")

def main():
        
    parser = argparse.ArgumentParser(description="Process Robot Framework output.xml and save the result.")
    parser.add_argument("-v", "--version", action='version', version='unbound report '+__version__, help="Version")
    parser.add_argument("-o", "--output", required=False, help="Path to the input output.xml file")
    parser.add_argument("-l", "--log", required=False, help="Path to the input log.html file")
    parser.add_argument("-s", "--save-path", required=False, help="Path to save the processed file")

    args = parser.parse_args()
    
    output_file = args.output
    log_file = args.log
    save_path = args.save_path

    if not output_file:
        output_file = './output.xml'
        
    if not log_file:
        log_file = './log.html'
        
    if not save_path:
        save_path = './unbound-report.html'
        
    if save_path:
        basename = os.path.basename(save_path)
        if '.html' not in basename:
            save_path += '/unbound-report.html'

    generate_report(output_file=output_file, log_file=log_file, save_path=save_path)
    

if __name__ == '__main__':
    main()