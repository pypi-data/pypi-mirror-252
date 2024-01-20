import json
import os

os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
from pathlib import Path
import urllib.request

from nostr_dvm.interfaces.dvmtaskinterface import DVMTaskInterface, process_venv
from nostr_dvm.utils.admin_utils import AdminConfig
from nostr_dvm.utils.definitions import EventDefinitions
from nostr_dvm.utils.dvmconfig import DVMConfig, build_default_config
from nostr_dvm.utils.nip89_utils import NIP89Config, check_and_set_d_tag
from nostr_dvm.utils.output_utils import upload_media_to_hoster
from nostr_dvm.utils.nostr_utils import get_event_by_id, get_referenced_event_by_id

"""
This File contains a Module to generate Audio based on an input and a voice

Accepted Inputs: Text
Outputs: Generated Audiofile
"""


class TextToSpeech(DVMTaskInterface):
    KIND: int = EventDefinitions.KIND_NIP90_TEXT_TO_SPEECH
    TASK: str = "text-to-speech"
    FIX_COST: float = 50
    PER_UNIT_COST = 0.5
    dependencies = [("nostr-dvm", "nostr-dvm"),
                    ("TTS", "TTS==0.22.0")]

    def __init__(self, name, dvm_config: DVMConfig, nip89config: NIP89Config,
                 admin_config: AdminConfig = None, options=None):
        dvm_config.SCRIPT = os.path.abspath(__file__)
        super().__init__(name, dvm_config, nip89config, admin_config, options)

    def is_input_supported(self, tags, client=None, dvm_config=None):
        for tag in tags:
            if tag.as_vec()[0] == 'i':
                input_value = tag.as_vec()[1]
                input_type = tag.as_vec()[2]
                if input_type != "event" and input_type != "job" and input_type != "text":
                    return False
                if input_type == "text" and len(input_value) > 250:
                    return False
                if input_type == "event":
                    evt = get_event_by_id(tag.as_vec()[1], client=client, config=dvm_config)
                    if len(evt.content()) > 250:
                        return False
            elif tag.as_vec()[0] == 'param':
                param = tag.as_vec()[1]
                if param == "language":  # check for param type
                    if tag.as_vec()[2] != "en":  # todo add other available languages
                        return False

        return True

    def create_request_from_nostr_event(self, event, client=None, dvm_config=None):
        request_form = {"jobID": event.id().to_hex() + "_" + self.NAME.replace(" ", "")}
        prompt = "test"
        if self.options.get("input_file") and self.options.get("input_file") != "":
            input_file = self.options['input_file']
        else:
            if not Path.exists(Path('cache/input.wav')):
                input_file_url = "https://media.nostr.build/av/de104e3260be636533a56fd4468b905c1eb22b226143a997aa936b011122af8a.wav"
                urllib.request.urlretrieve(input_file_url, "cache/input.wav")
            input_file = "cache/input.wav"
        language = "en"

        for tag in event.tags():
            if tag.as_vec()[0] == 'i':
                input_type = tag.as_vec()[2]
                if input_type == "event":
                    evt = get_event_by_id(tag.as_vec()[1], client=client, config=dvm_config)
                    prompt = evt.content()
                elif input_type == "text":
                    prompt = tag.as_vec()[1]
                elif input_type == "job":
                    evt = get_referenced_event_by_id(event_id=tag.as_vec()[1], client=client,
                                                     kinds=[EventDefinitions.KIND_NIP90_RESULT_EXTRACT_TEXT,
                                                            EventDefinitions.KIND_NIP90_RESULT_SUMMARIZE_TEXT,
                                                            EventDefinitions.KIND_NIP90_RESULT_TRANSLATE_TEXT],
                                                     dvm_config=dvm_config)
                    prompt = evt.content()
                if input_type == "url":
                    input_file = tag.as_vec()[1]
            elif tag.as_vec()[0] == 'param':
                param = tag.as_vec()[1]
                if param == "language":  # check for param type
                    language = tag.as_vec()[2]

        options = {
            "prompt": prompt,
            "input_wav": input_file,
            "language": language
        }
        request_form['options'] = json.dumps(options)

        return request_form

    def process(self, request_form):
        import torch
        from TTS.api import TTS
        options = DVMTaskInterface.set_options(request_form)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        # else "mps" if torch.backends.mps.is_available() \

        print(TTS().list_models())
        try:
            # model = "tts_models/deu/fairseq/vits"
            # model = "tts_models/multilingual/multi-dataset/your_tts"
            model = "tts_models/multilingual/multi-dataset/xtts_v2"
            tts = TTS(model).to(device)

            tts.tts_to_file(
                text=options["prompt"],
                speaker_wav=options["input_wav"], language=options["language"], file_path="outputs/output.wav")
            result = upload_media_to_hoster("outputs/output.wav")
            print(result)
            return result
        except Exception as e:
            print("Error in Module: " + str(e))
            raise Exception(e)


# We build an example here that we can call by either calling this file directly from the main directory,
# or by adding it to our playground. You can call the example and adjust it to your needs or redefine it in the
# playground or elsewhere
def build_example(name, identifier, admin_config):
    dvm_config = build_default_config(identifier)
    admin_config.LUD16 = dvm_config.LN_ADDRESS

    # use an alternative local wav file you want to use for cloning
    options = {'input_file': ""}

    nip89info = {
        "name": name,
        "image": "https://image.nostr.build/c33ca6fc4cc038ca4adb46fdfdfda34951656f87ee364ef59095bae1495ce669.jpg",
        "about": "I Generate Speech from Text",
        "encryptionSupported": True,
        "cashuAccepted": True,
        "nip90Params": {
            "language": {
                "required": False,
                "values": []
            }
        }
    }

    nip89config = NIP89Config()
    nip89config.DTAG = check_and_set_d_tag(identifier, name, dvm_config.PRIVATE_KEY, nip89info["image"])
    nip89config.CONTENT = json.dumps(nip89info)

    return TextToSpeech(name=name, dvm_config=dvm_config, nip89config=nip89config, admin_config=admin_config,
                        options=options)


if __name__ == '__main__':
    process_venv(TextToSpeech)
