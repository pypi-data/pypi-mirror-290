import copy
import json
import traceback
import uuid

from llmonpy.llm_client import GPT4omini, GEMINI_FLASH, FIREWORKS_MYTHOMAXL2_13B, FIREWORKS_LLAMA3_1_8B, \
    ANTHROPIC_HAIKU, MISTRAL_7B
from llmonpy.llmon_pypeline import LLMonPypeline
from llmonpy.llmonpy_prompt import LLMonPyPrompt, create_prompt_steps
from llmonpy.llmonpy_step import LLMonPyStepOutput, LLMONPY_OUTPUT_FORMAT_TEXT, TraceLogRecorderInterface, \
    STEP_TYPE_PYPELINE, make_model_list, ModelTemp
from llmonpy.system_startup import llmonpy_start, llmonpy_stop


class PassFailOutput(LLMonPyStepOutput):
    def __init__(self):
        pass

    def is_correct(self):
        raise NotImplementedError("PassFailOutput.is_correct() is not implemented")


class MatchPassFailOutput(PassFailOutput):
    def __init__(self, generated_answer, correct_answer):
        self.generated_answer = generated_answer
        self.correct_answer = correct_answer

    def is_correct(self):
        result = False
        if self.generated_answer is not None:
            result = self.generated_answer.lower() == self.correct_answer.lower()
        return result


class ColaPrompt(LLMonPyPrompt):
    prompt_text = """
    Given the following sentence, determine if it is grammatically correct or not. Write 'Yes' if it is grammatical, and 'No' if it is not:{{ sentence }}
    Do not include any other text in your response. Only respond with 'Yes' or 'No'.
    """
    system_prompt = "You are an expert at english grammar."
    output_format = LLMONPY_OUTPUT_FORMAT_TEXT

    def __init__(self, id, sentence, correct_answer):
        super().__init__()
        self.id = id
        self.sentence = sentence
        self.correct_answer = correct_answer

    def output_from_string(self, string):
        result = self.LLMonPyOutput(self.id, string, self.correct_answer)
        return result

    class LLMonPyOutput(LLMonPyStepOutput):
        def __init__(self, id, generated_answer, correct_answer):
            self.id = id
            self.generated_answer = generated_answer if generated_answer is None else generated_answer.strip()
            self.correct_answer = correct_answer

        def is_correct(self):
            result = self.generated_answer == self.correct_answer
            print("generated_answer:" + self.generated_answer + " correct_answer:" + self.correct_answer + " is_correct:" + str(result))
            return result

        def to_dict(self):
            result = copy.copy(vars(self))
            return result


class ParallelStep(LLMonPypeline):
    class LLMonPyOutput(LLMonPyStepOutput):
        def __init__(self, response_list: [ColaPrompt.LLMonPyOutput]):
            self.response_list = response_list

        def to_dict(self):
            result = {"response_list": [response.to_dict() for response in self.response_list]}
            return result

    def __init__(self, prompt, model_info_list):
        self.prompt = prompt
        self.model_info_list = model_info_list

    def get_step_type(self) -> str:
        return STEP_TYPE_PYPELINE

    def get_input_dict(self, recorder: TraceLogRecorderInterface):
        model_info_list = [model_info.to_dict() for model_info in self.model_info_list]
        result = {"prompt_template": self.prompt.get_prompt_text(),
                  "prompt_input_dict": self.prompt.to_dict(),
                  "model_list": model_info_list}
        return result

    def execute_step(self, recorder: TraceLogRecorderInterface):
        step_list = create_prompt_steps(recorder, self.prompt, self.model_info_list)
        self.run_parallel_steps(step_list)
        response_list = [step.get_step_output() for step in step_list]
        return self.LLMonPyOutput(response_list)


class ColaTest:
    def __init__(self, instance_dict):
        self.id = instance_dict["id"]
        self.sentence = instance_dict["instance"]
        self.answer = instance_dict["annotations"]["grammaticality"]["majority_human"]

    @staticmethod
    def read_from_file(file_path):
        cola_test_list = []
        with open(file_path, "r") as file:
            cola_file_dict = json.load(file)
            instance_list = cola_file_dict["instances"]
            for instance_dict in instance_list:
                cola_test = ColaTest(instance_dict)
                cola_test_list.append(cola_test)
        return cola_test_list


if __name__ == "__main__":
    llmonpy_start()
    try:
        cola_test_list = ColaTest.read_from_file("data/cola.json")
        first_cola_test = cola_test_list[0]
        cola_prompt = ColaPrompt(first_cola_test.id, first_cola_test.sentence, first_cola_test.answer)
        model_info_list = make_model_list(ModelTemp([ANTHROPIC_HAIKU, GPT4omini, GEMINI_FLASH],[0.0]))
        step = ParallelStep(cola_prompt, model_info_list).create_step(None)
        #make wrapper of ParallStep that sums responses to get final output, Make output PassFailOutput, then make equivalent to CompareOutputStep
        step.record_step()
        result = step.get_step_output()
        response_list = result.response_list
        for response in response_list:
            print("id:" + str(response.id) + " is correct:" + str(response.is_correct()))
    except Exception as e:
        stack_trace = traceback.format_exc()
        print(stack_trace)
        print("Error:", str(e))
    finally:
        llmonpy_stop()
        exit(0)
