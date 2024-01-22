import subprocess
import os
    

languages=[
        "English-Spanish",
        "Inglés-Español"
    ];


def get_word_by_index(sentence, index):
    words = sentence.split('-')

    if 0 <= index < len(words):
        return words[index]
    else:
        return ""


def close_process(process_name):
    try:
        subprocess.run(["taskkill", "/f", "/im", process_name], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        print("Community website https://github.com/voicetranslator")
    except subprocess.CalledProcessError as e:
        print("Community website https://github.com/voicetranslator")



def voice_translator(x1,x2):

    app_name="streamtranslator.exe"

    base_path = os.path.dirname(
            os.path.abspath(__file__)
        )
    app = os.path.join(base_path, app_name)
    
    close_process(app_name)
    
    input_dict={"en-US":0,"es-ES":1}
    output_dict={"en-US":0,"es-ES":1}

    if x1 in input_dict:
        input_lang=str(input_dict[x1])
    else:
        print("Error: Please try with en-US or es-ES")
        return 0

    if x2 in output_dict:
        output_lang=str(output_dict[x2])
    else:
        print("Error: Please try with en-US or es-ES")
        return 0

    print(get_word_by_index(languages[output_dict[x2]],input_dict[x1])+" - "+languages[output_dict[x2]].split("-")[output_dict[x2]])
        
    startup_info = subprocess.STARTUPINFO()
    startup_info.dwFlags = subprocess.STARTF_USESHOWWINDOW 
    startup_info.wShowWindow = subprocess.SW_HIDE
    process = subprocess.Popen(
        [
            app,
            input_lang,
            output_lang,
            "hash"
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        startupinfo=startup_info,
        text=True,
        encoding='utf-8'
    )

    message_to_cpp = "finish_python_app"
    process.stdin.write(message_to_cpp)
    process.stdin.flush()
    flac_data, stderr = process.communicate()
    process.terminate()


    try:
        subprocess.run(["taskkill", "/f", "/im", app_name], check=True, creationflags=subprocess.CREATE_NO_WINDOW)
        print("Starting...")
    except subprocess.CalledProcessError as e:
        print("Starting...")
        

    
    process = subprocess.Popen(
        [
            app,
            input_lang,
            output_lang,
            "provided_by_voicetranslator_github_io"
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        startupinfo=startup_info,
        text=True,
        encoding='utf-8'
    )

    off=0
    try:
        while True:
            line = process.stdout.readline()
                
            if not line:
                break

            print(line)
            if "Library error:\n"==line:
                off=1


    finally:
        if off!=1:
            message_to_cpp = "finish_python_app"
            process.stdin.write(message_to_cpp)
            process.stdin.flush()
            flac_data, stderr = process.communicate()
            process.terminate()
            
    

    return 1



