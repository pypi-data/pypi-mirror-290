import random
import subprocess
from IPython.core.magic import Magics, magics_class, line_magic
from IPython import get_ipython

# try:
from .plt_manage import is_image_exist, hide_images
from .global_variable_check import check_global_variable_content, variable_content, get_err_vars
from .local_variable_check import check_local_variable_content, extract_modules
from .structure_check import check_structure
from .globals import set_global_var_dict, set_global_method_dict
from .method_utils import extract_names_and_body
from .general_check import check, check_syntax, add_missing_global_variables
from .file_loader import *
from .feedback_msg import display_feedback
from .format import code_format
from .compare import variables_content_compare
# except ImportError:
#     pass
#     from general_check import check, check_syntax
#     from global_variable_check import check_global_variable_content, variable_content
#     from local_variable_check import check_local_variable_content
#     from structure_check import check_structure
#     from globals import set_global_var_dict, set_global_method_dict
#     from method_utils import extract_names_and_body
#     from plt_manage import is_image_exist, hide_image_output

CONFIG = {
    'check_structure': False,
    'modules': ""
}


@magics_class
class MyMagics(Magics):
    def __init__(self, shell):
        super().__init__(shell)
        self.solutions = {}
        self.modules = ""

    @line_magic
    def load(self, line):
        """Load a Python script and extract variables."""
        script_name = line.strip()

        if not script_name:
            print("Please provide a script name.")
            return

        ext = script_name.split('.')[-1]
        if ext == 'py':
            solutions = get_variables_from_pyscript(script_name)
            if not solutions:
                print(f"Could not load any variables from {script_name}.")
            else:
                try:
                    self.solutions = solutions['solution']
                except KeyError:
                    print("The variable 'solution' is not defined")
                    return
                print(f"Successfully loaded solutions from: {script_name}")
        elif ext == 'csv':
            try:
                solutions = get_variables_from_csv(script_name)
            except Exception:
                print("Please check the format of the answer")
                return
            self.solutions = solutions
            print(f"Successfully loaded solutions from: {script_name}")

        else:
            print("Please check the file types")
            return

    @line_magic
    def check(self, line):

        response = get_response()
        task_name = line.strip()
        check_list, answer = self.solutions[task_name]
        if self.modules == "":
            self.modules = CONFIG['modules']
        evaluation_function(response, answer, check_list, self.modules)

    @line_magic
    def load_module(self, line):
        ip = get_ipython()
        cell_lines = ip.user_ns['_ih'][-1].strip().splitlines()
        cell_lines.pop()
        self.modules = "\n".join(cell_lines)
        print("Successfully loaded required modules")


def load_ipython_extension(ipython):
    ipython.register_magics(MyMagics)
    print("Successfully loaded the extension")


def evaluation_function(response, answer, check_list, modules):
    if isinstance(check_list, str):
        check_list = [var.strip() for var in check_list.split(',')]
    is_defined = True
    if len(check_list) == 0:
        is_defined = False

    # reduce unnecessary codes
    response = code_format(response)
    answer = code_format(answer)

    # the missing module and previous global variables should be imported manually:
    response = f"{modules}\n{add_missing_global_variables(response, 'Response')}\n{response}"
    answer = f"{modules}\n{add_missing_global_variables(answer, 'Answer')}\n{answer}"

    has_ans_image = is_image_exist(code_str=answer)
    has_res_image = is_image_exist(code_str=response)

    tmp = answer
    if has_ans_image:
        # hide image output
        answer = hide_images(answer, modules)
        response = hide_images(response, modules)

    general_feedback = check(response)
    is_correct_answer, msg = check_syntax(answer)
    if not is_correct_answer:
        print("SyntaxError: Please contact your teacher to give correct answer!")
        return
    if general_feedback != "General check passed!":
        display_feedback(False)
        print(general_feedback)
        return

    if CONFIG['check_structure']:
        if not check_structure(response, answer):
            display_feedback(False)
            print("The methods or classes are not correctly defined.")
            return

    if has_ans_image:
        if not has_res_image:
            display_feedback(False)
            print("The answer has graphs but seems like you did not have plotting methods included")
            return
        else:
            print("We detect the plot method, "
                  "please check the difference below (Notice that we have no method to check your plot) : ")
            ipython = get_ipython()
            ipython.run_cell(tmp)
    else:

        if has_res_image:
            print("You have additional plots but the answer does not have")

    del tmp
    del has_ans_image
    del has_res_image

    if msg:
        if not check_answer_with_output(response, msg):
            # if check_list != 0, it means that output is not the importance
            if len(check_list) == 0:
                error_feedback = "The output is different to given answer: \n"
                display_feedback(False)
                print(error_feedback)
                return
        else:
            display_feedback(True)
            save_globals(response, answer)
            return
    else:
        if check_each_letter(response, answer):
            display_feedback(True)
            save_globals(response, answer)
            return

    if is_defined:

        is_correct, feedback, remaining_check_list, response = check_global_variable_content(response, answer,
                                                                                             check_list)
        if not is_correct:
            display_feedback(False)
            print(feedback)
            _, res_var_dict = extract_modules(variable_content(response))
            _, ans_var_dict = extract_modules(variable_content(answer))
            variable_list = get_err_vars()
            print(variables_content_compare(variable_list, res_var_dict, ans_var_dict))
            return
        else:
            if len(remaining_check_list) == 0:
                display_feedback(True)
                save_globals(response, answer)
                return

        is_correct, feedback = check_local_variable_content(response, answer, remaining_check_list)
        if is_correct:
            if feedback != "NotDefined":
                display_feedback(True)
                save_globals(response, answer)
                return
        else:
            display_feedback(False)
            print(feedback)
            return

    print("The AI feedback functionality will be implemented after permission and security check")


def config(check_structure: bool = False):
    CONFIG['check_structure'] = check_structure


def check_answer_with_output(response, output_msg):
    """
    The function is called iff the answer is unique. i.e. aList = [1,2,3,4,5] is the unique answer
    Notice that styles (at least they can pass general check) are NOT sensitive
    """
    try:
        res_result = subprocess.run(['python', '-c', response], capture_output=True, text=True)
        if res_result.returncode != 0:
            res_feedback = f"Error: {res_result.stderr.strip()}"
        else:
            res_feedback = res_result.stdout.strip()
    except Exception as e:
        res_feedback = f"Exception occurred: {str(e)}"
    return check_each_letter(res_feedback, output_msg)


def check_each_letter(response, answer):
    """
    The function is called iff the answer and the response are unique. i.e. aList = [1,2,3,4,5] is the unique answer and response
    Notice that styles (at least they can pass general check) are NOT sensitive
    """
    return answer.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "") == response.replace(
        " ", "").replace("\t", "").replace("\n", "").replace("\r", "")


def load_module(modules):
    CONFIG['modules'] = modules
    print("Successfully loaded required modules")


def get_response():
    ip = get_ipython()

    cell_lines = ip.user_ns['_ih'][-1].strip().splitlines()
    cell_lines.pop()
    response_lines = cell_lines
    idx = -2
    while True:
        cell_lines = ip.user_ns['_ih'][idx].strip().splitlines()
        if "get_ipython()" in cell_lines[-1]:
            return ('\n'.join(response_lines)).strip()
        else:
            response_lines = cell_lines + response_lines
            idx -= 1


def save_globals(response, answer):
    _, res_var_dict = extract_modules(variable_content(response))
    _, ans_var_dict = extract_modules(variable_content(answer))
    set_global_var_dict(res_var_dict, ans_var_dict)
    set_global_method_dict(extract_names_and_body(response), extract_names_and_body(answer))
