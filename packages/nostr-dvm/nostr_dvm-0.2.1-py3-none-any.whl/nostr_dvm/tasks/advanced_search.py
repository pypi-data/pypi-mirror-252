import json
import os
from datetime import timedelta
from nostr_sdk import Client, Timestamp, PublicKey, Tag, Keys, Options, SecretKey, ClientSigner

from nostr_dvm.interfaces.dvmtaskinterface import DVMTaskInterface, process_venv
from nostr_dvm.utils.admin_utils import AdminConfig
from nostr_dvm.utils.definitions import EventDefinitions
from nostr_dvm.utils.dvmconfig import DVMConfig, build_default_config
from nostr_dvm.utils.nip89_utils import NIP89Config, check_and_set_d_tag
from nostr_dvm.utils.output_utils import post_process_list_to_events

"""
This File contains a Module to search for notes
Accepted Inputs: a search query
Outputs: A list of events 
Params:  None
"""


class AdvancedSearch(DVMTaskInterface):
    KIND: int = EventDefinitions.KIND_NIP90_CONTENT_SEARCH
    TASK: str = "search-content"
    FIX_COST: float = 0
    dvm_config: DVMConfig
    dependencies = [("nostr-dvm", "nostr-dvm")]

    def __init__(self, name, dvm_config: DVMConfig, nip89config: NIP89Config,
                 admin_config: AdminConfig = None, options=None):
        dvm_config.SCRIPT = os.path.abspath(__file__)
        super().__init__(name, dvm_config, nip89config, admin_config, options)

    def is_input_supported(self, tags, client=None, dvm_config=None):
        for tag in tags:
            if tag.as_vec()[0] == 'i':
                input_value = tag.as_vec()[1]
                input_type = tag.as_vec()[2]
                if input_type != "text":
                    return False
        return True

    def create_request_from_nostr_event(self, event, client=None, dvm_config=None):
        self.dvm_config = dvm_config
        print(self.dvm_config.PRIVATE_KEY)

        request_form = {"jobID": event.id().to_hex()}

        # default values
        user = ""
        users = []
        since_days = 800  # days ago
        until_days = 0  # days ago
        search = ""
        max_results = 20

        for tag in event.tags():
            if tag.as_vec()[0] == 'i':
                input_type = tag.as_vec()[2]
                if input_type == "text":
                    search = tag.as_vec()[1]
            elif tag.as_vec()[0] == 'param':
                param = tag.as_vec()[1]
                if param == "user":  # check for param type
                    user = tag.as_vec()[2]
                elif param == "users":  # check for param type
                    users = json.loads(tag.as_vec()[2])
                elif param == "since":  # check for param type
                    since_days = int(tag.as_vec()[2])
                elif param == "until":  # check for param type
                    until_days = int(tag.as_vec()[2])
                elif param == "max_results":  # check for param type
                    max_results = int(tag.as_vec()[2])

        options = {
            "search": search,
            "user": user,
            "users": users,
            "since": since_days,
            "until": until_days,
            "max_results": max_results
        }
        request_form['options'] = json.dumps(options)
        return request_form

    def process(self, request_form):
        from nostr_sdk import Filter
        options = DVMTaskInterface.set_options(request_form)

        opts = (Options().wait_for_send(False).send_timeout(timedelta(seconds=self.dvm_config.RELAY_TIMEOUT)))
        sk = SecretKey.from_hex(self.dvm_config.PRIVATE_KEY)
        keys = Keys.from_sk_str(sk.to_hex())
        signer = ClientSigner.keys(keys)
        cli = Client.with_opts(signer, opts)

        cli.add_relay("wss://relay.nostr.band")
        cli.connect()

        search_since_seconds = int(options["since"]) * 24 * 60 * 60
        dif = Timestamp.now().as_secs() - search_since_seconds
        search_since = Timestamp.from_secs(dif)

        search_until_seconds = int(options["until"]) * 24 * 60 * 60
        dif = Timestamp.now().as_secs() - search_until_seconds
        search_until = Timestamp.from_secs(dif)
        userkeys = []
        for user in options["users"]:
            user = user[1]
            user = str(user).lstrip("@")
            if str(user).startswith('npub'):
                userkey = PublicKey.from_bech32(user)
            elif str(user).startswith("nostr:npub"):
                userkey = PublicKey.from_nostr_uri(user)
            else:
                userkey = PublicKey.from_hex(user)

            userkeys.append(userkey)

        if not options["users"] and options["user"] == "":
            notes_filter = Filter().kind(1).search(options["search"]).since(search_since).until(search_until).limit(
                options["max_results"])
        elif options["search"] == "":
            if options["users"]:
                notes_filter = Filter().kind(1).authors(userkeys).since(search_since).until(
                    search_until).limit(options["max_results"])
            else:
                notes_filter = Filter().kind(1).authors([PublicKey.from_hex(options["user"])]).since(search_since).until(
                    search_until).limit(options["max_results"])
        else:
            if options["users"]:
                notes_filter = Filter().kind(1).authors(userkeys).search(options["search"]).since(
                    search_since).until(search_until).limit(options["max_results"])
            else:
                notes_filter = Filter().kind(1).authors([PublicKey.from_hex(options["user"])]).search(options["search"]).since(
                    search_since).until(search_until).limit(options["max_results"])


        events = cli.get_events_of([notes_filter], timedelta(seconds=5))

        result_list = []
        if len(events) > 0:

            for event in events:
                e_tag = Tag.parse(["e", event.id().to_hex()])
                print(e_tag.as_vec())
                result_list.append(e_tag.as_vec())

        return json.dumps(result_list)

    def post_process(self, result, event):
        """Overwrite the interface function to return a social client readable format, if requested"""
        for tag in event.tags():
            if tag.as_vec()[0] == 'output':
                format = tag.as_vec()[1]
                if format == "text/plain":  # check for output type
                    result = post_process_list_to_events(result)

        # if not text/plain, don't post-process
        return result


# We build an example here that we can call by either calling this file directly from the main directory,
# or by adding it to our playground. You can call the example and adjust it to your needs or redefine it in the
# playground or elsewhere
def build_example(name, identifier, admin_config):
    dvm_config = build_default_config(identifier)
    admin_config.LUD16 = dvm_config.LN_ADDRESS
    # Add NIP89
    nip89info = {
        "name": name,
        "image": "https://image.nostr.build/c33ca6fc4cc038ca4adb46fdfdfda34951656f87ee364ef59095bae1495ce669.jpg",
        "about": "I search notes",
        "encryptionSupported": True,
        "cashuAccepted": True,
        "nip90Params": {
            "user": {
                "required": False,
                "values": [],
                "description": "Do the task for another user"
            },
            "since": {
                "required": False,
                "values": [],
                "description": "The number of days in the past from now the search should include"
            },
            "until": {
                "required": False,
                "values": [],
                "description": "The number of days in the past from now the search should include up to"
            },
            "max_results": {
                "required": False,
                "values": [],
                "description": "The number of maximum results to return (default currently 20)"
            }
        }
    }

    nip89config = NIP89Config()
    nip89config.DTAG = check_and_set_d_tag(identifier, name, dvm_config.PRIVATE_KEY, nip89info["image"])
    nip89config.CONTENT = json.dumps(nip89info)

    return AdvancedSearch(name=name, dvm_config=dvm_config, nip89config=nip89config,
                          admin_config=admin_config)


if __name__ == '__main__':
    process_venv(AdvancedSearch)
