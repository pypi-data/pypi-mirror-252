"""Helper class to reference the AIConfigRuntime state
"""
from threading import Event
from typing import Any, Dict, Literal

from aiconfig import AIConfigRuntime, ModelParserRegistry
from aiconfig.registry import update_model_parser_registry_with_config_runtime
from aiconfig_extension_hugging_face import (
    HuggingFaceAutomaticSpeechRecognitionTransformer,
    HuggingFaceImage2TextTransformer,
    HuggingFaceText2ImageDiffusor,
    HuggingFaceText2SpeechTransformer,
    HuggingFaceTextGenerationTransformer,
    HuggingFaceTextSummarizationTransformer,
    HuggingFaceTextTranslationTransformer,
)

from .utils import EXCLUDE_OPTIONS

# TODO (rossdanlm): Use os.path to get better relative path to file
DEFAULT_FILE_PATH: Literal = "./my_config.aiconfig.json"
DEFAULT_AICONFIG_SETTINGS: Dict[str, Any] = {
    "name": "Gradio Workbook AIConfig",
    "description": "This is the AIConfig that is used for the current Gradio workbook",
}


class AIConfigManager:
    """
    Manages the AIConfigRuntime state so that we can
    reference it from other classes without worrying about it being stale
    This also ensures that there are no circular dependencies for classes
    that need to reference the AIConfigRuntime

    Also will contain utility methods if needed
    """

    config: AIConfigRuntime
    thread_events: dict[str, Event]

    def __init__(self, filepath: str):
        self._clear_default_model_parsers()
        self._register_model_parsers()
        self.config = self.create_or_load_aiconfig(filepath)
        self.thread_events = {}

    def _clear_default_model_parsers(self):
        """
        By default, there are a ton of non-hf models/parsers registered in the
        ModelParserRegistry. We want to clear these out so that we can register
        only the hf ones to start
        """
        ModelParserRegistry.clear_registry()

    def _register_model_parsers(self):
        """
        Register the model parsers to use for the AIConfig.
        By default, we register the main HuggingFace parsers.

        TODO: Support user-provider parser registration
        """
        automatic_speech_recognition = (
            HuggingFaceAutomaticSpeechRecognitionTransformer()
        )
        AIConfigRuntime.register_model_parser(
            automatic_speech_recognition, automatic_speech_recognition.id()
        )

        image_to_text = HuggingFaceImage2TextTransformer()
        AIConfigRuntime.register_model_parser(image_to_text, image_to_text.id())

        text_to_image = HuggingFaceText2ImageDiffusor()
        AIConfigRuntime.register_model_parser(text_to_image, text_to_image.id())

        text_to_speech = HuggingFaceText2SpeechTransformer()
        AIConfigRuntime.register_model_parser(text_to_speech, text_to_speech.id())

        text_generation = HuggingFaceTextGenerationTransformer()
        AIConfigRuntime.register_model_parser(text_generation, text_generation.id())

        text_summarization = HuggingFaceTextSummarizationTransformer()
        AIConfigRuntime.register_model_parser(
            text_summarization, text_summarization.id()
        )

        text_translation = HuggingFaceTextTranslationTransformer()
        AIConfigRuntime.register_model_parser(text_translation, text_translation.id())

    def get_config(self) -> AIConfigRuntime:
        """Self-explanatory"""
        return self.config

    def get_config_json(self) -> str:
        """Helper function to return the config in json str format"""
        return self.get_config().model_dump(exclude=EXCLUDE_OPTIONS)

    def set_config(self, config: AIConfigRuntime):
        """Self-explanatory"""
        self.config = config

    def create_or_load_aiconfig(self, filepath: str) -> AIConfigRuntime:
        """Create or load an AIConfigRuntime from a filepath"""
        already_tried_default_filepath = False
        if not filepath:
            print(
                f"Warning, no filepath was provided so using default path '{DEFAULT_FILE_PATH}' instead"
            )
            filepath = DEFAULT_FILE_PATH
            already_tried_default_filepath = True

        try:
            config = AIConfigRuntime.load(filepath)
        # TODO (rossdanlm): Test this also with malformed json format to see which error it produces and catch for that
        except FileNotFoundError:
            try:
                if not already_tried_default_filepath:
                    print(
                        f"Warning, filepath '{filepath}' not found, trying default filepath '{DEFAULT_FILE_PATH}' instead..."
                    )
                    filepath = DEFAULT_FILE_PATH
                    config = AIConfigRuntime.load(filepath)
                else:
                    raise FileNotFoundError()
            except FileNotFoundError:
                print(
                    f"Warning, filepath '{filepath}' not found, creating new AIConfig. If needed, this AIConfig will be saved to '{DEFAULT_FILE_PATH}'"
                )
                filepath = DEFAULT_FILE_PATH
                config = AIConfigRuntime.create(**DEFAULT_AICONFIG_SETTINGS)
        config.file_path = filepath
        update_model_parser_registry_with_config_runtime(config)
        return config

    def get_models(self) -> list[str]:
        """Helper function to get the models from the ModelParserRegistry"""
        return ModelParserRegistry.parser_ids()
