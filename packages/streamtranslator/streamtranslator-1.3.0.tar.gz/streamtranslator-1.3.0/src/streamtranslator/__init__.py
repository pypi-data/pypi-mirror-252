version="1.3.0"
try:
    import streamtranslator._streamtranslator as sp
    print("Community website https://github.com/voicetranslator\nstreamtranslator "+version+"\n\nExample:\nimport streamtranslator\ndesktop_audio=streamtranslator.Translate('en-US','es-ES')\ndesktop_audio.start()\n\n")

except ImportError:
    print("Could not import the module")
    raise

class Translate:
    def __init__(self,input_lang=None, output_lang=None):
        self.input_lang=input_lang
        self.output_lang=output_lang
        self.validate_arguments()

    def validate_arguments(self):
        if self.input_lang is None or self.output_lang is None:
            print("Error: Please select 2 of the follow languages:\nen-US,es-ES\nExample:\nimport streamtranslator\ndesktop_audio=streamtranslator.Translate('en-US','es-ES')\ndesktop_audio.start()")
            
    def start(self):
        if self.input_lang is not None and self.output_lang is not None:
            sp.voice_translator(self.input_lang,self.output_lang)
        
