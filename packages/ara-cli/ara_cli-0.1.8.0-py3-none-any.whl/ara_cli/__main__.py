# PYTHON_ARGCOMPLETE_OK
import os
import sys
import argparse
import argcomplete
import json
from ara_cli.classifier import Classifier
from ara_cli.version import __version__
from ara_cli.commandline_completer import ArtefactCompleter, ParentCompleter
from ara_cli.output_suppressor import suppress_stdout


def check_validity(condition, error_message):
    if not condition:
        print(error_message)
        sys.exit(1)


def create_action(args):
    from ara_cli.artefact_creator import ArtefactCreator
    from ara_cli.classifier_validator import is_valid_classifier
    from ara_cli.filename_validator import is_valid_filename
    from ara_cli.template_manager import SpecificationBreakdownAspects

    check_validity(is_valid_classifier(args.classifier), "Invalid classifier provided. Please provide a valid classifier.")
    check_validity(is_valid_filename(args.parameter), "Invalid filename provided. Please provide a valid filename.")

    aspect = args.aspect if hasattr(args, "aspect") else None
    if args.parameter and args.classifier and aspect:
        sba = SpecificationBreakdownAspects()
        try:
            sba.create(args.parameter, args.classifier, aspect)
            return
        except ValueError as ve:
            print(f"Error: {ve}")
            sys.exit(1)

    parent_classifier = args.parent_classifier if hasattr(args, "parent_classifier") else None
    parent_name = args.parent_name if hasattr(args, "parent_name") else None
    if parent_classifier and parent_name:
        check_validity(is_valid_classifier(parent_classifier), "Invalid parent classifier provided. Please provide a valid classifier")
        check_validity(is_valid_filename(parent_name), "Invalid filename provided for parent. Please provide a valid filename.")

    template_path = os.path.join(os.path.dirname(__file__), 'templates')
    artefact_creator = ArtefactCreator()
    artefact_creator.run(args.parameter, args.classifier, template_path, parent_classifier, parent_name)


def delete_action(args):
    from ara_cli.artefact_deleter import ArtefactDeleter

    artefact_deleter = ArtefactDeleter()
    artefact_deleter.delete(args.parameter, args.classifier)


def rename_action(args):
    from ara_cli.artefact_renamer import ArtefactRenamer
    from ara_cli.classifier_validator import is_valid_classifier
    from ara_cli.filename_validator import is_valid_filename

    check_validity(is_valid_filename(args.parameter), "Invalid filename provided. Please provide a valid filename.")
    check_validity(is_valid_classifier(args.classifier), "Invalid classifier provided. Please provide a valid classifier.")
    check_validity(is_valid_filename(args.aspect), "Invalid new filename provided. Please provide a valid filename.")

    artefact_renamer = ArtefactRenamer()
    artefact_renamer.rename(args.parameter, args.aspect, args.classifier)


def list_action(args):
    from ara_cli.artefact_lister import ArtefactLister

    artefact_lister = ArtefactLister()
    if (args.tags):
        artefact_lister.list_files(tags=args.tags)
        return
    artefact_lister.list_files()


def get_tags_action(args):
    from ara_cli.tag_extractor import TagExtractor

    tag_extractor = TagExtractor()
    tags = tag_extractor.extract_tags()

    if args.json:
        output = json.dumps({"tags": tags})
        print(output)
        return

    output = "\n".join(f"- {tag}" for tag in tags)
    print(output)


def prompt_action(args):
    from ara_cli.prompt_handler import initialize_prompt_templates, load_selected_prompt_templates
    from ara_cli.prompt_handler import create_and_send_custom_prompt
    from ara_cli.prompt_extractor import extract_and_save_prompt_results
    from ara_cli.update_config_prompt import update_artefact_config_prompt_files
    from ara_cli.prompt_rag import search_and_add_relevant_files_to_prompt_givens
    from ara_cli.prompt_chat import initialize_prompt_chat_mode
    from ara_cli.classifier_validator import is_valid_classifier
    from ara_cli.filename_validator import is_valid_filename

    check_validity(is_valid_classifier(args.classifier), "Invalid classifier provided. Please provide a valid classifier.")
    check_validity(is_valid_filename(args.parameter), "Invalid filename provided. Please provide a valid filename.")

    classifier = args.classifier
    param = args.parameter
    init = args.steps

    if (init == 'init'):
        initialize_prompt_templates(classifier, param)
    if (init == 'init-rag'):
        initialize_prompt_templates(classifier, param)
        search_and_add_relevant_files_to_prompt_givens(classifier, param)
    if (init == 'load'):
        load_selected_prompt_templates(classifier, param)
    if (init == 'send'):
        create_and_send_custom_prompt(classifier, param)
    if (init == 'load-and-send'):
        load_selected_prompt_templates(classifier, param)
        create_and_send_custom_prompt(classifier, param)
    if (init == 'extract'):
        extract_and_save_prompt_results(classifier, param)
        print(f"automatic update after extract")
        update_artefact_config_prompt_files(classifier, param, automatic_update=True)
    if (init == 'chat'):
        chat_name = args.chat_name
        reset = args.reset
        output_mode = args.output_mode
        append_strings = args.append
        initialize_prompt_chat_mode(classifier, param, chat_name, reset=reset, output_mode=output_mode, append_strings=append_strings)
    if (init == 'update'):
        update_artefact_config_prompt_files(classifier, param, automatic_update=True)


def chat_action(args):
    from ara_cli.chat import Chat

    reset = args.reset
    output_mode = args.output_mode
    append_strings = args.append

    chat_name = "chat"
    if args.chat_name:
        chat_name = args.chat_name
    cwd = os.getcwd()
    chat_file_path = os.path.join(cwd, chat_name)
    with suppress_stdout(output_mode):
        chat = Chat(chat_file_path, reset=reset)

    if append_strings:
        chat.append_strings(append_strings)

    if output_mode:
        chat.start_non_interactive()
        return
    chat.start()


def template_action(args):
    from ara_cli.classifier import Classifier
    from ara_cli.template_manager import TemplatePathManager

    check_validity(Classifier.is_valid_classifier(args.classifier), "Invalid classifier provided. Please provide a valid classifier.")
    check_validity(Classifier.is_valid_classifier(args.classifier), "Invalid classifier provided. Please provide a valid classifier.")

    template_manager = TemplatePathManager()
    content = template_manager.get_template_content(args.classifier)

    print(content)


def handle_invalid_action(args):
    sys.exit("Invalid action provided. Type ara -h for help")


def create_parser(subparsers):
    create_parser = subparsers.add_parser("create", help="Create a classified artefact with data directory")
    create_parser.add_argument("classifier", choices=Classifier.ordered_classifiers(), help="Classifier that also serves as file extension for the artefact file to be created. Valid Classifiers are: businessgoal, capability, keyfeature, feature, epic, userstory, example, task")
    create_parser.add_argument("parameter", help="Artefact name that serves as filename").completer = ArtefactCompleter()

    option_parser = create_parser.add_subparsers(dest="option")

    contribution_parser = option_parser.add_parser("contributes-to")
    contribution_parser.add_argument("parent_classifier", choices=Classifier.ordered_classifiers(), help="Classifier of the parent")
    contribution_parser.add_argument("parent_name",  help="Name of a parent artefact").completer = ParentCompleter()

    aspect_parser = option_parser.add_parser("aspect")
    aspect_parser.add_argument("aspect", choices=["customer", "persona", "concept", "technology", "step"], help="Adds additional specification breakdown aspects in data directory.")


def delete_parser(subparsers):
    delete_parser = subparsers.add_parser("delete", help="Delete an artefact file including its data directory")
    delete_parser.add_argument("classifier", choices=Classifier.ordered_classifiers(), help="Classifier of the artefact to be deleted")
    delete_parser.add_argument("parameter", help="Filename of artefact").completer = ArtefactCompleter()


def rename_parser(subparsers):
    rename_parser = subparsers.add_parser("rename", help="Rename a classified artefact and its data directory")
    rename_parser.add_argument("classifier", choices=Classifier.ordered_classifiers(), help="Classifier of the artefact")
    rename_parser.add_argument("parameter", help="Filename of artefact").completer = ArtefactCompleter()
    rename_parser.add_argument("aspect", help="New artefact name and new data directory name")


def list_parser(subparsers):
    list_parser = subparsers.add_parser("list", help="List files with optional tags")
    list_parser.add_argument("tags", nargs="*", help="Tags for listing files")


def get_tags_parser(subparsers):
    tags_parser = subparsers.add_parser("get-tags", help="Show tags")
    tags_parser.add_argument("--json", "-j", help="Output tags as JSON", action=argparse.BooleanOptionalAction)


def add_chat_arguments(chat_parser):
    chat_parser.add_argument("chat_name", help="Optional name for a specific chat. Pass the .md file to continue an existing chat", nargs='?', default=None)

    chat_parser.add_argument("-r", "--reset", dest="reset", action=argparse.BooleanOptionalAction, help="Reset the chat file if it exists")
    chat_parser.set_defaults(reset=None)

    chat_parser.add_argument("--out", dest="output_mode", action="store_true", help="Output the contents of the chat file instead of entering interactive chat mode")

    chat_parser.add_argument("--append", nargs='*', default=None, help="Append strings to the chat file")


def prompt_parser(subparsers):
    prompt_parser = subparsers.add_parser("prompt", help="Base command for prompt interaction mode")

    steps = ['init', 'load', 'send', 'load-and-send', 'extract', 'update', 'chat', 'init-rag']
    steps_parser = prompt_parser.add_subparsers(dest='steps')
    for step in steps:
        step_parser = steps_parser.add_parser(step)
        step_parser.add_argument("classifier", choices=Classifier.ordered_classifiers(), help="Classifier of the artefact")
        step_parser.add_argument("parameter", help="Name of artefact data directory for prompt creation and interaction").completer = ArtefactCompleter()
        if step == 'chat':
            add_chat_arguments(step_parser)


def chat_parser(subparsers):
    chat_parser = subparsers.add_parser("chat", help="Command line chatbot. Chat control with SEND/s | RERUN/r | QUIT/q")
    add_chat_arguments(chat_parser)


def template_parser(subparsers):
    template_parser = subparsers.add_parser("template", help="Outputs a classified ara template in the terminal")
    template_parser.add_argument("classifier", choices=Classifier.ordered_classifiers(), help="Classifier of the artefact type")


def cli():
    parser = argparse.ArgumentParser(description="Ara tools for creating files and directories.")
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')

    subparsers = parser.add_subparsers(dest="action", help="Action to perform")
    create_parser(subparsers)
    delete_parser(subparsers)
    rename_parser(subparsers)
    list_parser(subparsers)
    get_tags_parser(subparsers)
    prompt_parser(subparsers)
    chat_parser(subparsers)
    template_parser(subparsers)

    action_mapping = {
        "create": create_action,
        "delete": delete_action,
        "rename": rename_action,
        "list": list_action,
        "get-tags": get_tags_action,
        "prompt": prompt_action,
        "chat": chat_action,
        "template": template_action
    }

    argcomplete.autocomplete(parser)

    args = parser.parse_args()
    if hasattr(args, 'action') and args.action:
        action = action_mapping.get(args.action, handle_invalid_action)
        action(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    cli()
