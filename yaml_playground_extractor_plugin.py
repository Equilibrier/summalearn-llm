import yaml
import subprocess
import json

def validate_and_extract_params(entry):
    if 'extract_model' not in entry or 'output_pdf' not in entry:
        return "Lipsește extract_model sau output_pdf", None

    if 'output_pdf' not in entry:
        return "Lipsește output_pdf", None

    extract_model = entry['extract_model']
    params = {'output_pdf': entry['output_pdf']}

    if extract_model.lower() == 'from_html':
        if 'url' not in entry:
            return "Lipsește url pentru from_html", None
        params['url'] = entry['url']
        params['selectors'] = entry.get('selectors', "")  # default to empty list if not present

    elif extract_model.lower() == 'from_pdf':
        if 'source_pdf' not in entry:
            return "Lipsește source_pdf pentru from_pdf", None
        if 'start_page' not in entry or 'end_page' not in entry:
            return "Lipsește start_page sau end_page pentru from_pdf", None
        params['source_pdf'] = entry['source_pdf']
        params['start_page'] = entry['start_page']
        params['end_page'] = entry['end_page']

    elif extract_model.lower() == 'direct_text':
        if 'source_text' not in entry:
            return "Lipsește source_text pentru direct_text", None
        params['source_text'] = entry['source_text']

    else:
        return f"Model necunoscut: {extract_model}", None

    return None, params

def process_entry(entry, interactive=True):
    from lib_common import text_to_pdf
    import os

    error, params = validate_and_extract_params(entry)
    if error:
        print(f"Eroare: {error}")
        return False

    if os.path.exists(params["output_pdf"]):
        print(f"Entry {entry} already generated in a previous session...")
        if interactive:
            while (resp:=input("Skipping this step (y,n)?: ").strip().lower()) not in ["yes", "no", "y", "n"]: print("Wrong answer, try again...!")
            if resp.strip().lower() in ["yes", "y"]:
                return True
        else:
            return True

    # Convert the params to a JSON string to pass to the subprocess
    extract_model = entry['extract_model']

    try:
        if extract_model.lower() == "from_html":
            p = subprocess.Popen(["python3", "yaml_playground_html_reader.py", params["url"], params["output_pdf"], params["selectors"]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            outp, err = p.communicate()
            if int(p.returncode) != 0:
                print(f"Processing entry {entry} failed.\nstandard output was:\n\t{outp}\n\nerr output was:\n\t{err}\n\nExiting now...")
                return False
        elif extract_model.lower() == "from_pdf":
             p = subprocess.Popen(["python3", "nlp_playground_pdf_split.py", params["source_pdf"], params["output_pdf"], str(params["start_page"]), str(params["end_page"])], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
             outp, err = p.communicate()
             if int(p.returncode) != 0:
                print(f"Processing entry {entry} failed.\nstandard output was:\n\t{outp}\n\nerr output was:\n\t{err}\n\nExiting now...")
                return False
        elif extract_model.lower() == "direct_text":
            text_to_pdf(params["source_text"], params["output_pdf"], content_mode="simple_text", split_mode="simple")
            
        print(f"File {params['output_pdf']} was succesfully created !")
        return True
    except Exception as e:
        import traceback
        import sys
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        print(traceback.format_exc())
        print(f"Processing entry {entry} failed with exception in file {fname}, at line {line_number}: {str(e)}")
        return False

def main(yaml_filepath, interactive=True):
    with open(yaml_filepath, "r") as file:
        data = yaml.safe_load(file)
        for entry in data['entries']:
            if not process_entry(entry, interactive):
                print("Correct the issues and try again ! Exiting now...!")
                return False
    return True

if __name__ == "__main__":
    import sys
    if len(sys.argv) <= 1:
        print("ERROR one param expected, yaml file path")
        sys.exit(1)

    sys.exit(0 if main(sys.argv[1], interactive=False) else 1)
