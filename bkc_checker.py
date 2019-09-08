import json
import subprocess
import sys
import logging
logging.basicConfig(format='%(message)s', level=logging.INFO)
try:
    filename = sys.argv[1]
except IndexError:
    print("bkc_checker.py <software.bkc.json>")
    sys.exit()

f = open(filename, "r")
data = json.load(f)
f.close()
logging.debug(data)

logging.info("bkc_checker : Best Known Configuration Checker")
logging.info("==============================================")
logging.info("Software : {}".format(data['software']))
logging.info("Meta information :")
for each in data['meta']:
    logging.info("\t {}".format(each))
logging.info("")
checker_output = {}

for key in data['checker'].keys():
    logging.info("-------------")
    logging.info("| checking for {}".format(key))
    logging.info("-------------")
    checker_output[key] = False
    output = {}
    try:
        # run cmdline to check output
        output = subprocess.run(
            data['checker'][key]['cmdline'], capture_output=True)
        output_stdout = output.stdout.decode('utf-8').rstrip()
        expected_stdout = data['checker'][key]['expected_stdout']

        # compare cmdline with expected output
        if expected_stdout.startswith('<SEARCH>'):
            processed = expected_stdout.replace('<SEARCH>', '')
            if output_stdout.find(processed) != -1:
                logging.info("{} seems ok".format(key))
                logging.info("")
                checker_output[key] = True
            else:
                logging.info("Cant find expected string in output.")
                logging.info("expected  : {}".format(processed))
                logging.info("output    : {}".format(output_stdout))
        else:
            print("not supported 'expected_stdout'")
            sys.exit()
    except FileNotFoundError:
        logging.info("command \"{}\" failed with FILE NOT FOUND error.".format(
            data['checker'][key]['cmdline']))
    if checker_output[key] == False:
        logging.info("")
        logging.info("# Common fix for {} :".format(key))
        for issue in data['checker'][key]['common_issue']:
            logging.info("{}".format(issue))
        logging.info("")

logging.info("Final Result :")
logging.info("==============")
for each in checker_output.keys():
    if checker_output[each] == True:
        logging.info("[ {} ] {}".format(u'\u2713', each))
    else:
        logging.info("[   ] {} ".format(each))
